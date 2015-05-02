import json
import logBin
import brainlib

# takes a path to a json object
# returns a string
def processFile(path, numBins):
  f = open(path, 'r')
  processedData = processData(json.loads(f.read()), numBins)
  return json.dumps(processedData)

def processData(dictionary, numBins):
  rawValues = dictionary[u'raw_values']
  # power spec of the raw values
  pspec = brainlib.pSpectrum(rawValues)
  dictionary[u'pspec'] = json.dumps(pspec.tolist())
  return dictionary
