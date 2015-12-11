__author__ = 'Aman'

import EntropyCalculate
import DataPrepare
import DataSpecific

'''
This class would store the Decision Tree.
AttributeName: Name of the attribute which is used to split the subtree.
ListSubtrees: List of subtrees. There would be one subtree for each of the value of attributes.
FinalValue: This would be not set(-1) until we have found the leaf of the tree, which is final classification.

DictIntervalContVar: This is a class variable and is used to store the intervals for the continuous variables.
'''
class DecisionTree:

    dictIntervalContVar = None
    def __init__(self, attributeName, listSubtrees,finalValue = -1,edgeVal = None):
        self.attributeName = attributeName
        self.listSubtrees = listSubtrees
        self.finalValue = finalValue
        self.edgeVal = edgeVal

    def setEdgeVal(self,edgeVal):
        self.edgeVal = edgeVal

'''
The trainData function is the main function that would create the decision tree based on provided training data.
In the former section of the function, we convert continuous variable to  discrete.
In the later section of the function, we create the decision tree.
'''
def trainData():

    listDiscreteAttribute = []
    for i in range(0,14):
         listDiscreteAttribute.append(i)

    listContAttribute = [1,2,7,10,13,14]
    dictIntervalContVar = {}

    listRows = DataPrepare.parseFile(DataSpecific.trainDFile)
    for indexCont in listContAttribute:
        tuple = updateContVariables(listRows, indexCont)
        dictIntervalContVar[indexCont] = tuple[0]
        listRows = tuple[1]

    root = buildTree(listRows,listDiscreteAttribute,15)
    #printRoot(root,0)
    root.dictIntervalContVar = dictIntervalContVar
    return root


'''
Convert the continueous variable to discrete values, divide the group into #totalCount/5 intervals.
Assign values to each interval.
'''
def updateContVariables(listRows, indexContAtr):

    listVal = []
    for i in listRows:
        listVal.append(i[indexContAtr])

    listIntervals = findInterval(listVal,5)

    for i in listRows:
        for intr in range(0,len(listIntervals)-1):
            if i[indexContAtr] == '?':
                break
            if  float(i[indexContAtr]) > float(listIntervals[intr]) and float(i[indexContAtr]) <= float(listIntervals[intr+1]):
                i[indexContAtr] = intr
                break

    return (listIntervals,listRows)


'''
This function would find the intervals which should be appropriate for each of the attributes.
The base for these intervals depends on the frequency for each of the values.
We decided to partition based on frequency to keep the tree balanced.
'''
def findInterval(listValues, countInterval):
    countInterval = countInterval - 1
    listValues = filter(lambda a: a != '?', listValues)
    listValues.sort()
    multiple = len(listValues)/countInterval
    listIntervals = [float("-inf")]

    for i in range(0,countInterval):
        listIntervals.append(listValues[i*multiple])

    listIntervals.append(float("inf"))

    return listIntervals

'''
The BuildTree function: Recursive function to create and return the complete decision tree.
DataRows: The list of rows we need to consider for the root of the variable depending on Entropy.

If the there are no more Data rows left: return +
If all the classification of Data Rows results in + or -, return that value.
If we are exhausted with all the attributes and are still ambiguous on the data. Return Majority

Overfitting: When the + and - or vice versa are in the ratio of 1:0.2, consider one as noise and return majority.

If none of the above holds and we still need to classify data.
Find the attribute with Max Entropy gain
Split rows based on this attribute and recursively call BuildTree on each nodes.
'''
def buildTree(dataRows, listAttribute, evalColumn,edgeValue=None):

        if len(dataRows) == 0:
            return DecisionTree(None,None,'+',edgeValue)

        isfinal = {}
        for row in dataRows:
            if row[evalColumn] not in isfinal:
                isfinal[row[evalColumn]] = []
            isfinal[row[evalColumn]].append(row)

        if len(isfinal) == 1:
            return DecisionTree(None,None,isfinal.keys()[0],edgeValue)

        if len(listAttribute) == 0:
            if (len(isfinal['+']) > len(isfinal['-'])):
                return DecisionTree(None,None,'+',edgeValue)
            else:
                return DecisionTree(None,None,'-',edgeValue)

        if (0.2*len(isfinal['+']) > len(isfinal['-'])):
                return DecisionTree(None,None,'+',edgeValue)
        elif(0.2*len(isfinal['-']) > len(isfinal['+'])):
                return DecisionTree(None,None,'-',edgeValue)

        chosenAttr = EntropyCalculate.maxInformationGain(dataRows,listAttribute,evalColumn)

        rowsSplit = {}
        for row in dataRows:
            if row[chosenAttr] not in rowsSplit:
                rowsSplit[row[chosenAttr]] = []
            rowsSplit[row[chosenAttr]].append(row)

        listSubTrees = []
        import copy
        newListAttribute = copy.deepcopy(listAttribute)
        newListAttribute.remove(chosenAttr)

        for attrVal in rowsSplit:
            listSubTrees.append(buildTree(rowsSplit[attrVal],newListAttribute,evalColumn,attrVal))

        nameAttr = `chosenAttr`
        root = DecisionTree(nameAttr,listSubTrees,-1,edgeValue)

        return root


'''
Function to do a basic representation of decision tree.
'''
def printRoot(root,level):

    if root.edgeVal != None:
                print "  EdgeVal:", root.edgeVal
    if root.finalValue != -1:
        print root.finalValue
        return

    print "AttributeName:  ",root.attributeName,"  Level:",level


    for attVal in root.listSubtrees:
        printRoot(attVal,level+1)



