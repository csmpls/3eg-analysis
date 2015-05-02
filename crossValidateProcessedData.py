import os.path
import json

from sklearn import svm
from sklearn import cross_validation
import numpy as np


# all of our data - mostly for reference
subjects = ['nick', 'john']
electrodePositions = ['erb', 'erh', 'normal']
tasks = ['auditory', 'baseline', 'color count', 'eye move', 'eye open move', 'eye open static', 'imagine rotating a cube', 'imagined auditory', 'motor imagery', 'pass', 'videoclip']


#
# config
#
# number of readings per task
readingNum = 20
# number of trials per task
trialNum = 3
# the feature vector we're interested in from the output data
featureVectorKey = u'pspec'
# the directory where our readings are kept
readingDir = 'processed'




# a generator of arrays
# each array is a feature vector to feed to our svm
def loadAllFeatureVectors(subject, electrodePos, task):
	for reading in range(readingNum):
		for trial in range(trialNum):
			try:
				yield loadFeatureVector(subject, electrodePos, task, trial, reading)
			except:
				print 'cant find', subject, electrodePos, task, trial, reading

def loadFeatureVector(subject, electrodePos, task, trial, reading):
	readingPath = os.path.join(readingDir, subject, electrodePos, task, str(trial), str(reading) + '.json')
	with open (readingPath, 'r') as f:
		return json.load(f)[featureVectorKey]



# takes an array of generators,
# each one representing a feature vector
# and produces X and y vectors
# X is list a vectors, y is a list if (int) labels for those vectors
# X and y need to be the same length.
def vecotrsAndLabels(arrayOfGenerators):
	X = []
	y = []
	currentLabel = 0
	for generator in arrayOfGenerators:
		for vector in generator:
			# NB: feature vectors are serialized as strings sometimes
			# we map them to floats
			X.append(eval(vector))
			y.append(currentLabel)
		currentLabel+=1

	return X, y



#
# example
#
vectors1 = loadAllFeatureVectors('nick', 'erb', 'baseline')
vectors2 = loadAllFeatureVectors('nick', 'erb', 'color count')

X, y = vecotrsAndLabels([vectors1, vectors2])

clf = svm.LinearSVC()
scores = cross_validation.cross_val_score(clf, np.array(X), y, cv=7)
print scores.mean()





