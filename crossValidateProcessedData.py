import os.path
import json

from sklearn import svm
from sklearn import cross_validation
import numpy as np
import itertools

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
	for trial in range(trialNum):
		for reading in range(readingNum):
			try:
				yield loadFeatureVector(subject, electrodePos, task, trial, reading)
			except:
				pass
				# print 'cant find', subject, electrodePos, task, trial, reading

def loadFeatureVector(subject, electrodePos, task, trial, reading):
	readingPath = os.path.join(readingDir, subject, electrodePos, task, str(trial), str(reading) + '.json')
	with open (readingPath, 'r') as f:
		return json.load(f)[featureVectorKey]



# takes an array of generators,
# each one representing a feature vector
# and produces X and y vectors
# X is list a vectors, y is a list if (int) labels for those vectors
# X and y need to be the same length.
def vectorsAndLabels(arrayOfGenerators):
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

# train + 7-fold cv an svm on set of features + labels
def crossValidate(X,y):
	clf = svm.LinearSVC()
	scores = cross_validation.cross_val_score(clf, np.array(X), y, cv=7)
	return scores.mean()




#
# example
#
taskpairs = itertools.combinations(tasks,2)
for taskpair in taskpairs:
	vectors1 = loadAllFeatureVectors('john', 'erh', taskpair[0])
	vectors2 = loadAllFeatureVectors('john', 'erh', taskpair[1])

	X, y = vectorsAndLabels([vectors1, vectors2])

	try:
		print crossValidate(X,y), ",", taskpair[0], ",", taskpair[1]
	except:
		print 'some problem - probably cant find task:', taskpair[0], taskpair[1]





