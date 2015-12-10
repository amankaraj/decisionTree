__author__ = 'Aman'

import DecisionTree
import ParseData

tree = DecisionTree.main()

def cleanRow(row):
    row = ParseData.cleanRow(row)

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

def findValue(listRows):

    listResults = []
    for row in listRows:
        row = cleanRow(row)
        listResults.append(calculateProb(row,tree))

    return listResults

def calculateProb(row,root):
    if root == None or root.finalValue != -1:
        return root.finalValue

    val = row[int(root.attributeName)]
    for subT in root.listSubtrees:
        if subT.edgeVal == val:
            return calculateProb(row,subT)



def testTree():
    listRows = ParseData.parseFile("testing.txt")
    listResults = findValue(listRows)

    countCorrect = 0.0
    for i in range(0,len(listRows)):
        row = listRows[i]
        if(row[15] == listResults[i]):
            countCorrect = countCorrect + 1

    return countCorrect*100/float(len(listRows))


print testTree()