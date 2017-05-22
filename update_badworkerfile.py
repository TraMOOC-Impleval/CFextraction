from flaggedWorkers import BadWorkers
import sys
import os

def main(PATH, untrustedfilename, flaggedfilename):
    files = os.filelist(PATH)
    badworkers = BadWorkers()

    for file in files:
        filename = PATH + file
        badworkers.update_from_workerfile(filename)

    badworkers.write_to_files(untrustedfilename, flaggedfilename)


if __name__ == '__main__':
    PATH = 'XXX'
    if len(sys.argv) >= 4:
        PATH = sys.argv[1]
        untrustedfilename = sys.argv[2]
        flaggedfilename = sys.argv[3]

    else:
        while True:
            PATH = input('Enter a valid folder: ')
            untrustedfilename = input('Enter a filename for untrusted file: ')
            flaggedfilename = input('Enter a filename for flagged file: ')
            if os.path.exists(PATH):
                break
            else:
                print('Folder {} does not exist.'.format(PATH))
    if not PATH.endswith('/'):
        PATH = PATH + '/'

    main(PATH, untrustedfilename, flaggedfilename)