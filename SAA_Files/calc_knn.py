#!/bin/python
import itertools, numpy, Queue

def normalizeVector(vec):
    norm = numpy.linalg.norm(vec)
    return [v / norm for v in vec]

def getNormalizedVector(line):
    features = []
    tokens = line.split()[1:]
    for token in tokens:
        features.append(float(token.split(":")[-1]))
    return normalizeVector(features)

def getNormalizedVectorTuples(featureLines, langLabels, genderLabels, labelDict):
    vecTuples = []
    for i in range(len(featureLines)):
        vec = getNormalizedVector(featureLines[i])
        lang = labelDict[int(langLabels[i])]
        gender = genderLabels[i].strip()
        vecTuples.append((i, vec, lang, gender))
    return vecTuples

def cosineSim(vec1, vec2):
    # Note: assume length normalized
    return numpy.dot(vec1, vec2)

def writeSim(pair, meanVectorsMap, outFile):
    sim = cosineSim(meanVectorsMap[pair[0]], meanVectorsMap[pair[1]])
    outFile.write(pair[0] + " " + pair[1] + " " + str(sim) + "\n")

def getDescriptorString(vecTuple, sim):
    if not sim:
        return "" + str(vecTuple[0]) + ": " + vecTuple[3] + "-" + vecTuple[2]
    else:
        return "[" + str(vecTuple[0]) + ": " + vecTuple[3] + "-" + vecTuple[2] + " (" + str(sim) + ")]"

def outputKNN(sim, otherTuple, outFile):
    outFile.write(getDescriptorString(otherTuple, sim) + "\t")

def getMostFreqLang(langs):
    counts = [(lang, langs.count(lang)) for lang in set(langs)]
    sortedLangs = sorted(counts, key=lambda tup: tup[1], reverse=True)
    if len(sortedLangs) < 2:
        return sortedLangs[0], None
    else:
	   return sortedLangs[0], sortedLangs[1]

def trialResult(targetLang, langs, name, cutoff=None):
    mostFreqTup, secondMostFreqTup = getMostFreqLang(langs)
    if cutoff is not None and not mostFreqTup[1] >= cutoff:
        return name + "decline"
    elif secondMostFreqTup is not None and not mostFreqTup[1] > secondMostFreqTup[1]:
        return name + "decline"
    elif mostFreqTup[0] == targetLang:
        return name + "success"
    else:
        return name + "fail"

def updateStats(knnStats, targetLang, knn3Langs, knn5Langs, knn10Langs):
	incKey3 = trialResult(targetLang, knn3Langs, "knn3-", 2)
	incKey5 = trialResult(targetLang, knn5Langs, "knn5-", 3)
	incKey10 = trialResult(targetLang, knn10Langs, "knn10-", 4)
	knnStats[incKey3] = knnStats[incKey3] + 1
	knnStats[incKey5] = knnStats[incKey5] + 1
	knnStats[incKey10] = knnStats[incKey10] + 1

def writeKNN(vecTuple, vecTuples, outFile, k, knnStats):
    pq = Queue.PriorityQueue()
    outFile.write(getDescriptorString(vecTuple, None) + ":\t")

    for tup in vecTuples:
        if tup != vecTuple:
            sim = cosineSim(vecTuple[1], tup[1])
            pq.put((-1.0 * sim, tup))
	
	knn3Langs = []
	knn5Langs = []
	knn10Langs = []
    for i in range(k):
		nextNeighbor = pq.get()
		if i <= 3:
			knn3Langs.append(nextNeighbor[1][2])
		if i <= 5:
			knn5Langs.append(nextNeighbor[1][2])
		
		knn10Langs.append(nextNeighbor[1][2])
		outputKNN(-1.0 * nextNeighbor[0], nextNeighbor[1], outFile)
	
    updateStats(knnStats, vecTuple[2], knn3Langs, knn5Langs, knn10Langs)
    outFile.write("\n")

def writeStats(knnStats, outfile):
	outfile.write("3NN: success {}, decline {}, fail {}\n".format(str(knnStats["knn3-success"]), str(knnStats["knn3-decline"]), str(knnStats["knn3-fail"])))
	outfile.write("5NN: success {}, decline {}, fail {}\n".format(str(knnStats["knn5-success"]), str(knnStats["knn5-decline"]), str(knnStats["knn5-fail"])))
	outfile.write("10NN: success {}, decline {}, fail {}\n".format(str(knnStats["knn10-success"]), str(knnStats["knn10-decline"]), str(knnStats["knn10-fail"])))


def calc_knn(extDir, labelDict, k):
	featureLines = open(extDir + "features.lsvm", 'r').readlines()
	langLabels = open(extDir + "language_labels.txt", 'r').readlines()
	genderLabels = open(extDir + "gender_labels.txt", 'r').readlines()

	vecTuples = getNormalizedVectorTuples(featureLines, langLabels, genderLabels, labelDict)
	outFile = open(extDir + "knn" + str(k) + ".txt", 'w')
	knnStats = {}
	statsFields = ["knn3-success", "knn3-decline", "knn3-fail", "knn5-success", "knn5-decline", "knn5-fail", "knn10-success", "knn10-decline", "knn10-fail"]
	for field in statsFields:
		knnStats[field] = 0
	for vecTuple in vecTuples:
		print "Calcing knn for #{}".format(str(vecTuple[0]))
		writeKNN(vecTuple, vecTuples, outFile, k, knnStats)
	outFile.close()

	statsFile = open(extDir + "knn-stats.txt", 'w')
	writeStats(knnStats, statsFile)
	statsFile.close()


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
    calc_knn("extracted/", labelDict, 10)
