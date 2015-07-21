import os.path
import json
import brainlib

# number of readings per task
READINGS_IN_TRIAL = 20
# number of trials per task
NUM_TRIALS_PER_TASK = 3
# the number of power spectra we compress into 1 feature vector
# each power spectrum represents a half second
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

def allVectors (subject, electrodePos, task):
	featureVectors = []
	for trial in range(NUM_TRIALS_PER_TASK):
		featureVectors.extend(
			featureVectorsFromTrial(subject, electrodePos, task, trial, POWER_SPECTRUM_RESOLUTION))
	return featureVectors
