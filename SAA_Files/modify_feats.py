#!/bin/python

startRows = [1,13,25,37,49,61,73,85,97,109,121,133,145,181,193,373]
columnsToKeep = [2,3,6,7,8,10,11,12]

def getFeaturesToKeep():
    featuresToKeep = []
    for row in startRows:
        featuresToKeep.extend([row + i - 1 for i in columnsToKeep])
    return featuresToKeep

def modifyFeats(featsFilename, outFilename):
    featuresToKeep = getFeaturesToKeep()
    featsFile = open(featsFilename, 'r')
    lines = featsFile.readlines()
    newlines = []

    for line in lines:
        tokens = line.split()
        newTokens = [tokens[0]]
        for i in featuresToKeep:
            newTokens.append(tokens[i])
        newlines.append(" ".join(newTokens) + "\n")

    featsFile.close()

    outfile = open(outFilename, 'w')
    for line in newlines:
        outfile.write(line)
    outfile.close()


if __name__ == "__main__":
    featsFile = "extracted/rawFeats.lsvm"
    outFeatsFile = "extracted/features.lsvm"
    modifyFeats(featsFile, outFeatsFile)