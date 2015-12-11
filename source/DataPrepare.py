__author__ = 'Aman'



def parseFile(fileAddress):
    fileData = open(fileAddress)
    listRows = []
    for line in fileData:
        row = line.split(',')
        if(row[15] == '+\n'):
            row[15] = '+'
        else:
            row[15] = '-'
        row = cleanRow(row)
        listRows.append(row)

    return listRows

def parseQueryFile(fileAddress):
    fileData = open(fileAddress)
    listRows = []
    for line in fileData:
        row = line.split(',')
        row = cleanRow(row)
        listRows.append(row)

    return listRows


def cleanRow(row):

    floatValuesInd = [1,2,7,10,13,14]
    for i in floatValuesInd:
        if row[i] != '?':
            row[i] = float(row[i])

    return row


parseFile("data.txt")