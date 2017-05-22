import zipfile
import json
'''
contains a class for reading the jsonfiles outputted by crowdflower.com
'''
class JSONLoaderException(Exception):
    '''
    A custom exception for this class
    '''
    def __init__(self, msg):
        '''
        :param msg: the message to be raised together with this exception
        '''
        self.msg = msg

    def print_exception(self):
        print ("JsonLoader custom exception: ", self.msg)


class JSONLoader:
    def __init__(self):
        pass


    def readfromjson(self, filename, returntype = 'json'):
        '''
        Reads a json file and returns a list of json-objects. One json-object per line in the file.
        :param filename: <str> Filename of file to read. Should end with '.json'
        :param returntype: <str> type of object returned. A list of json-objects or a list of json-strings
        :return: list of json-objecst
        '''
        assert filename.endswith('.json')
        assert returntype == 'json' or returntype == 'jsonstring'

        with open(filename, 'rt') as f:
            data = f.readlines()

        if returntype == 'json':
            json_list = [json.loads(line, encoding='utf-8') for line in data]
            return json_list
        elif returntype == 'jsonstring':
            return data


    def readfromzip(self, filename, returntype = 'json'):
        '''
        Reads a json file that is compressed in a zip
        :param filename: <str> filename to read. Filename should end with .zip
        :param returntype: <str> type of object returned. A list of json-objects or a list of json-strings
        :return: a list of json objects

        '''
        assert filename.endswith('.zip')
        assert returntype == 'json' or returntype == 'jsonstring'

        zf = zipfile.ZipFile(filename, 'r')
        if len(zf.namelist()) > 1:
            raise JSONLoaderException('Multiple files in zip. Expected only 1 file')

        data =zf.read(zf.namelist()[0]).decode('utf-8')
        zf.close()

        data = data.splitlines()

        if returntype == 'json':
            json_list = [json.loads(line, encoding='utf-8') for line in data]
            return json_list
        elif returntype == 'jsonstring':
            return data


    def read_json2list(self, filename, filetype = None, returntype = 'json'):
        '''
        :param filename: <str> filename with path
        :param filetype: <str> type of the file to read: either 'zip' or 'json'
        :param returntype: <str> type of object returned. A list of json-objects or a list of json-strings
        :return: a list of json objects.
        '''
        assert returntype == 'json' or returntype == 'jsonstring'

        if filename.endswith('.json') or filetype == 'json':
            json_list = self.readfromjson(filename, returntype=returntype)
        elif filename.endswith('.zip') or filetype == 'zip':
            json_list = self.readfromzip(filename, returntype=returntype)

        self.nrjsons = len(json_list)

        return json_list


