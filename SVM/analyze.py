import os.path
import json

import numpy as np
from sklearn import svm
from sklearn import cross_validation
import itertools

from lib import brainlib

# all of our data - mostly for reference
subjects = ['nick', 'john']
electrodePositions = ['erb', 'erh', 'normal']
tasks = ['auditory', 'baseline', 'color count', 'eye move', 'eye open move', 'eye open static', 'imagine rotating a cube', 'imagined auditory', 'motor imagery', 'pass', 'videoclip']


#
# config
#

# number of readings per task
READINGS_IN_TRIAL = 20
# number of trials per task
NUM_TRIALS_PER_TASK = 3
# the number of power spectra we compress into 1 feature vector
# NB: READINGS IN TRIAL % POWER SPECTRUM RESOLUTION == 0
POWER_SPECTRUM_RESOLUTION = 5
# the key from the processed data json we're using
KEY_IN_PROCESSED_DATA = u'pspec'
# the directory where our readings are kept
PROCESSED_DATA_DIR = 'processed'
# the number of values in power spectra in our dataset
POWER_SPECTRUM_SIZE = 128
# the number of values we want in our feature vectors
FEATURE_VECTOR_SIZE = 300




#
#
#  helper utils for loading vectors

# load 1 power spectrum from disk
# this will call a db eventually, but just loads from disk for now
def getPowerSpectrum (subject, electrodePos, task, trial, reading):
	readingPath = os.path.join(PROCESSED_DATA_DIR, subject, electrodePos, task, str(trial), str(reading) + '.json')
	with open (readingPath, 'r') as f:
		# turn this string into an array of floats
		return eval(json.load(f)[KEY_IN_PROCESSED_DATA])

# generates a list of powerspectra from each reading (a numerical index 0-mREADINGS_IN_TRIAL) in listOfReadings
def powerSpectra (subject, electrodePosition, task, trial, listOfReadings):
	for reading in listOfReadings:
		# read file
		yield getPowerSpectrum(subject, electrodePosition, task, trial, reading) 


def relevantReadings (index, resolution):
	return range(index, index+resolution)
		
# generator for assembling task vectors of size `resolution`, where `resolution` is a number of consecutive readings within a single trial
# retruns an array of veraged powerspectra
def featureVectorsFromTrial (subject, electrodePosition, task, trial, resolution):

	# for each resolution-sized segment of the trial
	for i in range(READINGS_IN_TRIAL/resolution):

		pspecs = []
		gen = powerSpectra(subject, electrodePosition, task, trial,relevantReadings(i, resolution))
		for spectrum in gen:
			pspecs.append(spectrum)


		avgPSpec = brainlib.avgPercentileUp(
				pspecs	
				, brainlib.getXOutput(POWER_SPECTRUM_SIZE, FEATURE_VECTOR_SIZE)
				, 3)
		yield avgPSpec

# a generator of arrays
# each array is a feature vector to feed to our svm
def loadAllFeatureVectors(subject, electrodePos, task):
	featureVectors = []

	for trial in range(NUM_TRIALS_PER_TASK):
		featureVectors.extend(
			featureVectorsFromTrial(subject, electrodePos, task, trial, POWER_SPECTRUM_RESOLUTION))

	return featureVectors







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
			X.append(vector)
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

def generateResults ():
	for taskpair in itertools.combinations(tasks,2):

		try:
			vectors1 = loadAllFeatureVectors('john', 'erh', taskpair[0])
			vectors2 = loadAllFeatureVectors('john', 'erh', taskpair[1])

			X, y = vectorsAndLabels([vectors1, vectors2])

			yield crossValidate(X,y), taskpair[0], taskpair[1]

		except:
			print 'some problem - probably cant find task:', taskpair[0], taskpair[1]

results = [result for result in generateResults()]

for topFiveGesture in sorted(results)[-5:][::-1]:
	print topFiveGesture, '\r'