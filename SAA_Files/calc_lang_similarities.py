#!/bin/python
import itertools, numpy

def normalizeVector(vec):
    norm = numpy.linalg.norm(vec)
    return [v / norm for v in vec]

def getVector(line):
    features = []
    tokens = line.split()[1:]
    for token in tokens:
        features.append(float(token.split(":")[-1]))
    return normalizeVector(features)

def getAverageVec(vecs):
    numVecs = len(vecs)
    avg = []
    for i in range(len(vecs[0])):
        featSum = 0.0
        for vec in vecs:
            featSum += vec[i]
        avg.append(featSum / numVecs)
    return avg


def getMeanNormalizedVectors(featuresLines, langLabels, labelDict):
    vecMap = {}
    for i in range(len(featuresLines)):
        lang = labelDict[int(langLabels[i])]
        if lang not in vecMap:
            vecMap[lang] = []
        vecMap[lang].append(getVector(featuresLines[i]))

    for lang in vecMap:
        avgVec = getAverageVec(vecMap[lang])
        vecMap[lang] = normalizeVector(avgVec)

    return vecMap

def getGenderLines(featuresLines, langLabels, genderLabels):
	maleLines = [[], []]
	femaleLines = [[], []]
	for i in range(len(featuresLines)):
		if 'm' in genderLabels[i]:
			maleLines[0].append(featuresLines[i])
			maleLines[1].append(langLabels[i])
		else:
			femaleLines[0].append(featuresLines[i])
			femaleLines[1].append(langLabels[i])
	return maleLines, femaleLines

def cosineSim(vec1, vec2):
    # Note: assume length normalized
    return numpy.dot(vec1, vec2)

def writeSim(tup, outFile):
	outFile.write(tup[0] + " " + tup[1] + " " + str(tup[2]) + "\n")

def calc_gender_sims(featureLines, langLabels, labelDict, outFilename):	
	meanVectorsMap = getMeanNormalizedVectors(featureLines, langLabels, labelDict)
	langs = list(meanVectorsMap.keys())
	pairs = list(itertools.combinations(langs, 2))

	outFile = open(outFilename, 'w')
	pairSims = []
	for pair in pairs:
		pairSims.append((pair[0], pair[1], cosineSim(meanVectorsMap[pair[0]], meanVectorsMap[pair[1]])))
	
	sortedSims = sorted(pairSims, key=lambda tup: tup[2], reverse=True)
	for tup in sortedSims:
		writeSim(tup, outFile)
	
	outFile.close()

def calc_sims(extDir, labelDict):
	featureLines = open(extDir + "features.lsvm", 'r').readlines()
	langLabels = open(extDir + "language_labels.txt", 'r').readlines()
	genderLabels = open(extDir + "gender_labels.txt", 'r').readlines()
	
	maleLines, femaleLines = getGenderLines(featureLines, langLabels, genderLabels)
	calc_gender_sims(maleLines[0], maleLines[1], labelDict, extDir + "male-sims.txt")
	calc_gender_sims(femaleLines[0], femaleLines[1], labelDict, extDir + "female-sims.txt")


if __name__ == "__main__":
    labelDict = {
        0: 'arabic',
        1: 'cantonese',
        2: 'dutch',
        3: 'french',
        4: 'german',
        5: 'italian',
        6: 'japanese',
        7: 'korean',
        8: 'macedonian',
        9: 'mandarin',
        10: 'polish',
        11: 'portuguese',
        12: 'russian',
        13: 'spanish',
        14: 'turkish'
    }
    calc_sims("extracted/", labelDict)
