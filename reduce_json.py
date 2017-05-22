'''
This script reads a json file and writes a tabfile for a manual control
'''
from SentenceInfoGetter import SentenceInfoGetter
from JsonLoader import JSONLoader
from JSON2tab import JSON2tab
from flaggedWorkers import BadWorkers
import time
from SentenceInfoGetter_withFlaggedFilter import SentenceInfoGetter as SIG
import sys
# Path to the folder where the results are located
PATH = '/home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/'
JSONFILE = 'CZ_json.zip'
OUTFILENAME = 'CZ_out_filtertest.json'



badworkers = BadWorkers()
badworkers.update_from_workerfile('/home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/cz-workset987586.csv')
badworkers.read_from_files('untrusted.txt', 'flagged.txt')


# Name of the file with the results (may be a json or a zip)
if len(sys.argv) >=3:
    filename = sys.argv[1]#'
    OUTFILENAME = sys.argv[2] #'CZ_out_filtertest.json'
else:
    filename = JSONFILE

# Get the location of the file
totfilename = PATH + filename

# Make a jsonloaderobject and read the jsons
jsonloader = JSONLoader()
dingen = jsonloader.read_json2list(totfilename, returntype='json')  # <-- sorry for the bad variable name

# Initialize list of jsons
clean_jsons = []


thetime = str(time.time())

sucesses = 0 # <-- counts nr of successful parses
for ding in dingen:   # <-- sorry for the bad naming

    single_json = ding

    # Initialise the sentence info getter
    #x = SentenceInfoGetter(single_json)
    x = SIG(single_json, badworkers, thetime)

    x.extract_info()
    z = x.make_json(json_type='dict')   # get a 'reduced' json dict (reduced (or clean) = without unnececary info)
    z2 = x.make_json(json_type='str')   # get a 'reduced json string
    #print (z)
    sucesses += 1
    print(z2)
    clean_jsons.append(z)

print('sucesses: ', sucesses)

with open(OUTFILENAME, 'w') as out:
    for json in clean_jsons:
        out.write('{}\n'.format(json))