import fnmatch
import os
import shutil
from lib.processFile import processFile

numBins = 100

# 
#  call processFile on every *.json file in in recordings/
#  write the new, processed file to an identical path in processed/
#

# find all .json files in recordings/ dir
jsonFiles = []
for root, dirnames, filenames in os.walk('recordings'):
  for filename in fnmatch.filter(filenames, '*.json'):
    jsonFiles.append(os.path.join(root, filename))

# remove everything in processed/ currently
shutil.rmtree('processed')

# save all of these files in a directory with the same structure, 
# but who's top-level dir is processed/
for path in jsonFiles:
  parentDirectory = os.path.abspath(os.path.join(path, os.pardir))
  # recursively create directory 
  try:
    writePath = parentDirectory.replace('recordings', 'processed')
    os.makedirs(writePath)
  except:
    print '..', 
  with open(path.replace('recordings', 'processed'), 'wb') as newFile:
    # process the file and write it in the new directory
    newFile.write(processFile(path, numBins))
