import json
import numpy as np
import numpy.fft as fft
import logBin

# takes a path to a json object
# returns a string
def processFile(path, numBins):
  f = open(path, 'r')
  processedData = processData(json.loads(f.read()), numBins)
  return json.dumps(processedData)

def processData(dictionary, numBins):
  # fft the raw values (1024 in length)
  fftOfRawValues = fft.fft(dictionary[u'raw_values'], 1024)
  # log bin it (100 bins)
  #print logBin.percentile(fftOfRawValues, numBins)
  dictionary[u'binned_vector'] = str(logBin.percentile(fftOfRawValues, numBins))
  return dictionary
