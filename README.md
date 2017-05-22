# CFextraction

<b>update_badworkerfile.py</b>

A small command line application to build files contianing the id's untrusted and flagged users.

Use it like this: python update_badworkerfile arg1 arg2 arg3

arg1 = folder with the crowdflower worker sets. example: /home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/worksets/
This folder may only contain crowdflower worksets (i.e. the worker files downloaded from crowdflower)
It does not matter whether the worksets are already added to the file. 

arg2 = the filename where the untrusted user ids will be written to

arg3 = the filename where the flagged user ids will be written to


<b>make_tabfile.py</b>

Example of how the objects can be used.
This script creates a file for manual quality control of the crowdflowerdata.

The location of the file that you want to analyze should be hardcoded in the script. This is done by defining the variables 'PATH' and 'filename'
'PATH' should contain the location where the inputfile can be found
'filename' should contain the actual filename

Also the variable 'OUTPUTFILE' can be definde. This is the name of the tab-file that is created.


<b>reduce_json.py</b>

Does the same as make_tabfile.py. But writes to a .json-file instead of a .tab-file. Advantage of this is that the problem with quotes is automatically solved.


<b>JsonLoader.py</b>

Usage:
jsonloader = JSONLoader()
jsonlist = jsonloader.read_json2list(filename)

read_json2list assumes that every line in the file contains 1 json.

The file with json can either be a zip containing the json or the json-file itself. The reason it accepts zip-files is that if you download the json from crowdflower, it is zipped.

A list with json-dictionaries is returned. Every item in the list is 1 line from the inputfile.

<b>SentenceInfoGetter.py</b>

Usage:
initialize
sig = SentenceInfoGetter(single_json)
extract the info
sig.extract_info()
return a 'cleaned' json
z = sig.make_json(json_type')

Initialisation
At initialization you must give a single crowdflower json as argument. This is one item from the list created with JSONLoader.read_json2list
Optional arguments:
threshold (default = 2): The consensus threshold. Only include entities that are annotated by at least n crowdflower users.
thresholdcriteria (default = 'entities') other possibilities: 'all' and 'urls'. What creteria must be used for checking if an entity is marked by more than n crowdflower users. Only the entity itself ('entities'), the wikipedia urls ('urls') or everyting ('all')
emptyvalue (default = 'NULL'): what string must be inserted when a certain field of the json is empty.

extract_info
Extracts the information from the crowdflower json.

make_json()
returns a new json with only the extracted information from the crowdflower json.

Arguments:
json_type  (default = 'str'): other option : 'dict'. determines whether to return a json string or a json dict.



<b>JSON2Tab.py</b>

Usage:
Innitialize 
filemaker = JSON2tab(clean_jsons)
Takes a list of clean json dicts: the jsons created with the sentenceinfogetter.
Make tabfile
filemaker.make_tabfile(outfilename=OUTFILENAME)
Takes a filename and writes a tabfile to that file

This class is designed specifically for writing the tabfile for the manual quality control.
