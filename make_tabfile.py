'''
This script reads a json file and writes a tabfile for a manual control
'''
from SentenceInfoGetter import SentenceInfoGetter
from JsonLoader import JSONLoader
from JSON2tab import JSON2tab
import sys

# Path to the folder where the results are located
PATH = '/home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/'

# Name of the file with the results (may be a json or a zip)
totfilename = sys.argv[1]
outfilename = filename.split('.')[0] + '.prep.tab'


badworkers = BadWorkers()
badworkers.update_from_workerfile('/home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/cz-workset987586.csv')
badworkers.read_from_files('untrusted.txt', 'flagged.txt')


# Get the location of the file


# Make a jsonloaderobject and read the jsons
jsonloader = JSONLoader()
jsonlines = jsonloader.read_json2list(totfilename, returntype='json')  

# Initialize list of jsons
clean_jsons = []

thetime = str(time.time())   # creates a timestamp in order to make a unique file of removed items

sucesses = 0 # <-- counts nr of successful parses
for jsonline in jsonlines:   #

    single_json = jsonline

    # Initialise the sentence info getter
    x = SentenceInfoGetter(single_json, badworkers, thetime)


    x.extract_info()
    z = x.make_json(json_type='dict')   # get a 'reduced' json dict (reduced (or clean) = without unnececary info)
    z2 = x.make_json(json_type='str')   # get a 'reduced json string
    #print (z)
    sucesses += 1
    print(z2)
    clean_jsons.append(z)

print('sucesses: ', sucesses)

filemaker = JSON2tab(clean_jsons)
filemaker.make_tabfile(outfilename)
