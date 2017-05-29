import csv

class BadWorkers(object):
    def __init__(self):
        self.flaggedworkers = set([])
        self.untrustedworkers = set([])
        print('yay')
        pass

    def __contains__(self, item):
        if item in self.flaggedworkers:
            return True
        elif item in self.untrustedworkers:
            return True
        else:
            return False

    def is_flagged(self, id):
        if id in self.flaggedworkers:
            return True
        else:
            return False

    def is_untrusted(self, id):
        if id in self.untrustedworkers:
            return True
        else:
            return False

    def update_from_workerfile(self, filename):
        contr = open(filename, 'r')
        readerContr = csv.reader(contr)
        header = True

        for row in readerContr:
            if not header:
                if (row[11] != ''):
                    self.flaggedworkers.add(row[0])
                elif (float(row[15]) < 0.6):
                    self.untrustedworkers.add(row[0])
            else:
                header = False
        contr.close()

    def write_to_file(self, filename, type = 'flagged'):
        with open(filename, 'wt') as out:
            if type == 'flagged':
                for id in self.flaggedworkers:
                    id = str(int(id))
                    out.write('{}\n'.format(id))

            elif type == 'untrusted':
                for id in self.untrustedworkers:
                    id = str(int(id))
                    out.write('{}\n'.format(id))


    def write_to_files(self, untrustedfilename, flaggedfilename):
        self.write_to_file(flaggedfilename, 'flagged')
        self.write_to_file(untrustedfilename, 'untrusted')

    def read_from_file(self, filename, type):
        with open (filename, 'rt') as f:
            data = f.readlines()
            if type == 'flagged':
                for item in data:
                    self.flaggedworkers.add(item.strip())
            elif type == 'untrusted':
                for item in data:
                    self.untrustedworkers.add(item.strip())
            else:
                print('burp')

    def read_from_files(self, flaggedfilename, untrustedfilename):
        self.read_from_file(flaggedfilename, 'flagged')
        self.read_from_file(untrustedfilename, 'untrusted')


if __name__ == '__main__':
    X = BadWorkers()
    #X.update_from_workerfile('/home/hdevos/TRAMOOC/crowdflowerdata/crowdflowerprocessor/cz-workset987586.csv')

    print(X.flaggedworkers)
    print(X.untrustedworkers)

    #X.write_to_files('untrusted.txt', 'flagged.txt')
    X.read_from_files('untrusted.txt', 'flagged.txt')

    print(X.flaggedworkers)
    print(X.untrustedworkers)

    print('4041275' in X)