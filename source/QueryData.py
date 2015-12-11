__author__ = 'Aman'

import DataPrepare
import DataSpecific
import DecisionTree

'''
tree is the root of DecisionTree obtained by training the data in data file
'''
tree = DecisionTree.trainData()
'''
Updating the attribute list with values obtained from converting continuous variables.
'''
DataSpecific.attribute_list.update(tree.dictIntervalContVar)

'''
Convert continuous variables from the query/test data to discrete variables using the intervals used in decision tree.
'''
def cleanRow(row):
    row = DataPrepare.cleanRow(row)

    dictContVar = tree.dictIntervalContVar

    for entry in dictContVar.keys():
        listIntervals = dictContVar[entry]
        for  i in range(0,len(listIntervals)-1):
            if row[entry] == '?':
                break
            if  row[entry] > listIntervals[i] and row[entry] <= listIntervals[i+1]:
                row[entry] = i
                break

    return row


'''
Function would compute the result for a set of rows.
'''
def findValue(listRows):

    listResults = []
    for row in listRows:
        row = cleanRow(row)
        listResults.append(queryRow(row))

    return listResults

'''
Recursive function to traverse the Tree and find the final value for a given row.
'''
def calculateProb(row,root):
    if root == None or root.finalValue != -1:
        return root.finalValue

    val = row[int(root.attributeName)]
    for subT in root.listSubtrees:
        if subT.edgeVal == val:
            return calculateProb(row,subT)


'''
Method to pick the rows from testing data file and calculate the final values.
It would use the final value to compute the accuracy of model
'''
def testTree():
    listRows = DataPrepare.parseFile(DataSpecific.testingDFile)
    listResults = findValue(listRows)

    countCorrect = 0.0
    for i in range(0,len(listRows)):
        row = listRows[i]
        if(row[15] == listResults[i]):
            countCorrect = countCorrect + 1

    return countCorrect*100/float(len(listRows))

'''
For each of the missing values, we would create multiple rows with all possible values, we would do this for each of such attribute.
Once we have all set of new rows, we will calculate the value for each of them and would return the majority, breaking ties arbit.
'''
import Queue
import copy

'''
Method to handle missing data in the query/testing rows.
For each missing value, we would convert the data into a number of rows, one for each possible value of missing attribute.
'''
def missingValueUpdate(row):

    indexMissing = []
    for i in range(0,len(row)):
        if row[i] == '?':
            indexMissing.append(i)

    rowQueue = Queue.Queue()
    rowQueue.put(row)


    for misInd in indexMissing:
        sizeQueue = rowQueue.qsize()
        for i in range(0,sizeQueue):
            currRow = rowQueue.get()
            for j in DataSpecific.attribute_list[misInd]:
                newRow = copy.deepcopy(currRow)
                newRow[misInd] = j
                rowQueue.put(newRow)

    listRows = []
    while(rowQueue.empty() is False):
        row = rowQueue.get()
        listRows.append(row)

    return listRows




'''
Query for a particular row.
This would perform:
Cleaning
Update missing value
calculate probability
'''
def queryRow(row):
    row = cleanRow(row)
    listRows = missingValueUpdate(row)

    count = 0
    for row in listRows:
        result = calculateProb(row,tree)
        if(result == '+'):
            count = count + 1


    if (count/float(len(listRows)) >= 0.5):
        return '+'
    else:
        return '-'





def query():
    listRows = DataPrepare.parseQueryFile(DataSpecific.queryDFile)
    dictValues = {}

    for row in listRows:
        print "Row: ",row, " Result:", queryRow(row)
