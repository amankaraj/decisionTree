__author__ = 'Aman'

import EntropyCalculate
import ParseData

class DecisionTree:

    dictIntervalContVar = None
    def __init__(self, attributeName, listSubtrees,finalValue = -1,edgeVal = None):
        self.attributeName = attributeName
        self.listSubtrees = listSubtrees
        self.finalValue = finalValue
        self.edgeVal = edgeVal

    def setEdgeVal(self,edgeVal):
        self.edgeVal = edgeVal

def main():

    listDiscreteAttribute = []
    for i in range(0,14):
         listDiscreteAttribute.append(i)

    listContAttribute = [1,2,7,10,13,14]
    dictIntervalContVar = {}

    listRows = ParseData.parseFile("data.txt")
    for indexCont in listContAttribute:
        tuple = updateContVariables(listRows, indexCont)
        dictIntervalContVar[indexCont] = tuple[0]
        listRows = tuple[1]

    root = buildTree(listRows,listDiscreteAttribute,15)
    #printRoot(root,0)
    root.dictIntervalContVar = dictIntervalContVar
    return root


def printRoot(root,level):

    if root.edgeVal != None:
                print "  EdgeVal:", root.edgeVal
    if root.finalValue != -1:
        print root.finalValue
        return

    print "AttributeName:  ",root.attributeName,"  Level:",level


    for attVal in root.listSubtrees:
        printRoot(attVal,level+1)
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
            if (isfinal['+'] > isfinal['-']):
                return DecisionTree(None,None,'+',edgeValue)
            else:
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







