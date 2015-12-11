__author__ = 'Aman'
'''
Contain helper functions for the Build Tree method to calculate entropy.
'''

import math

'''
Calculate the count of positives in the total set of rows.
Calculate entropy based on that data.
'''
def calculateEntropy(dataRows, indexPos):

    countPos = 0
    for row in dataRows:
        if row[indexPos] == '+':
            countPos = countPos + 1

    lengthDataRow = float(len(dataRows))
    if countPos == 0 or countPos == lengthDataRow:
        return 0


    entropy = -1*((countPos/lengthDataRow)*(math.log(countPos/lengthDataRow,2)) +
                  ((lengthDataRow - countPos)/lengthDataRow)*(math.log((lengthDataRow - countPos)/lengthDataRow,2)))

    return entropy

'''
Function to calculate the Information Gain:
Data Rows: The list of rows we need to consider for Information Gain
ChkAtrPos: The index of attribute which we are considering for calculation of the current information gain
evalPos: The index of the evaluation position. Classsifier.
'''
def informationGain(dataRows, chkAtrPos, evalPos):

    countDictionary = {}
    successCountDict = {}

    for row in dataRows:
        if row[chkAtrPos] == '?':
            continue
        if row[chkAtrPos] not in countDictionary:
            countDictionary[row[chkAtrPos]] = 0
        countDictionary[row[chkAtrPos]] += 1
        if row[chkAtrPos] not in successCountDict:
                successCountDict[row[chkAtrPos]] = 0
        if row[evalPos] == '+':
            successCountDict[row[chkAtrPos]] += 1

    entropy = calculateEntropy(dataRows,evalPos)
    for i in countDictionary:
        if not (successCountDict[i] == countDictionary[i] or successCountDict[i] == 0):
            successRatio = successCountDict[i]/float(countDictionary[i])
            failRatio = (countDictionary[i] - successCountDict[i])/float(countDictionary[i])
            entropy = entropy - -1*(countDictionary[i]/float(len(dataRows)))*(successRatio*math.log(successRatio,2) + failRatio*math.log(failRatio,2))

    return entropy

import DataPrepare
'''
Function to calculate the attribute with the maximum information gain.
DataRows: List of data rows
listValidAttr: List of valid attributes that can be considered as root for this subtree.
EvalCol: Final Classifier columnn
'''
def maxInformationGain(dataRows, listValidAttr, evalColumn):


    maxInfoGain = -1
    maxAttr = 15
    for i in listValidAttr:
        localInfoGain = informationGain(dataRows,i,evalColumn)
        print "localInfo gain: i:",i," ",localInfoGain
        if localInfoGain > maxInfoGain:
            maxAttr = i
            maxInfoGain = localInfoGain


    return maxAttr


