# CFextraction

<b>update_badworkerfile.py</b>

A small command line application to build files contianing the id's untrusted and flagged users.

Use it like python update_badworkerfile arg1 arg2 arg3

arg1 = folder with the crowdflower worker sets. example: /home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/worksets/
This folder may only contain crowdflower worksets (i.e. the worker files downloaded from crowdflower)
It does not matter whether the worksets are already added to the file. 

arg2 = the filename where the untrusted user ids will be written to

arg3 = the filename where the flagged user ids will be written to
