import json
import time

class JudgmentData:
    '''
    A class to keep track of what judgments have been made about a certain sentence.
    JudgmentData contains information on how often a certain judgment has been made.
    NOTE: this is not a standalone class. Only designed for used within the SentenceInfoGetter class. If used outside of SentenceInfoGetter: use with care.
    '''
    def __init__(self, source_entity, target_entity, source_url, target_url, occurence = 0):
        '''
        :param source_entity: the entity in the source language
        :param target_entity: the entity in the target language
        :param source_url: the url of the wikipedia of the entity in the source language
        :param target_url: the url of the wikipedia of the entity in the target language
        :param occurence: how often has this judgment been made? Default 0
        '''
        self.source_entity = source_entity
        self.target_entity = target_entity
        self.source_url = source_url
        self.target_url = target_url
        self.occurence = occurence

    def __eq__(self, other):
        '''
        Checks if two instances of JudgmentData are similar
        :param other: other instance fo JudgmentData to check against self
        :return: <bool>: true if both instances are the same, False otherwise
        '''
        if not self.has_equal_entities(otherdata=other):
            return False
        if not self.has_equal_urls(otherdata=other):
            return False
        return True

    def __str__(self):
        '''
        :return: printable string of self
        '''
        return "-----\nsource entity: {}\nsource url: {}\n\ntarget entity: {}\ntarget url: {}\n\noccurence: {}\n\n".format(
            self.source_entity, self.source_url, self.target_entity, self.target_url, self.occurence)

    def has_equal_entities(self, otherdata):
        '''
        Checks whether self and otherdata have the same
        :param otherdata: an instance of JudgmentData to be compared with self
        :return: <bool>: true if self and otherdata have same entities, false otherwise
        '''
        assert isinstance(otherdata, JudgmentData)

        if not self.source_entity == otherdata.source_entity:
            return False
        if not self.target_entity == otherdata.target_entity:
            return False

        return True

    def has_equal_urls(self, otherdata):
        '''
        Checks whether self and otherdata have the same urls
        :param otherdata: other Judgmentdata object
        :return: <bool>: true if self and otherdata have same urls, false otherwise
        '''
        assert isinstance(otherdata, JudgmentData)

        if not self.target_url == otherdata.target_url:
            return False
        if not self.source_url == otherdata.source_url:
            return False

        return True

    def is_in_list(self, somelist, criteria = 'all'):
        '''
        Checks if an item similar to self is already in a given list.
        :param somelist: a list to compare self with
        :param criteria: On what attribute must be judged whether an item is in the list?
        :return: <bool>, <int>: bool: is item in list: int: if item in list: at what index?
        '''
        assert type(somelist) == list

        if len(somelist) <= 0:
            return False, None

        if criteria == 'all':
            for i, item in enumerate(somelist):
                if item == self:
                    return True, i
            return False, None

        elif criteria == 'entities':
            for i, item in enumerate(somelist):
                if self.has_equal_entities(item):
                    return True, i
            return False, None

        elif criteria == 'urls':
            for i, item in enumerate(somelist):
                if self.has_equal_urls(item):
                    return True, i
            return False, None


class SentenceInfoGetter(object):
    '''
    A class to extract info from a crowdflower-json and return it in json-format
    '''
    def __init__(self, sentence_json, badworkers, thetime, threshold = 2, thresholdcriteria = 'entities', emptyvalue = 'NULL'):
        '''

        :param sentence_json: the crowdflowerjson of a sentence
        :param threshold: threshold for self.extract_entities: how often should an entity be marked by contributers to be extracted.
        :param thresholdcriteria: parameter for self.extract_entities: to what criteria most be looked? entities, urls or both?
        '''
        sentence_json = self.preprocess_Json(sentence_json, badworkers, thetime)



        self.CrowdFlowerJson = sentence_json
        self.threshold = threshold
        self.thresholdcriteria = thresholdcriteria
        self.emptyvalue = emptyvalue

    def preprocess_Json(self, json, badworkers, thetime):

        judgments = json['results']['judgments']
        for i in range(len(judgments)-1, -1, -1):
            if str(judgments[i]["worker_id"]) in badworkers:
                removed = json['results']['judgments'].pop(i)

                print('judgment removed: {}'.format(removed))
                logfilename = 'removed' + '_' + thetime + '.txt'
                with open(logfilename, 'a') as logfile:
                    logfile.write(str(removed))
                    logfile.write('\n')

        return json

    def get_sentence_id(self):
        '''
        Extracts or determines (depends on todo below) the sentence id
        :return: <str> string of integer.
        '''
        return self.CrowdFlowerJson['results']['judgments'][0]['unit_data']['sentence_id']


    def get_source_sentence(self):
        '''
        Extracts the source sentence from the crowdflowerjson
        :return: <str> the sentence in the source language
        '''
        try:
            return self.CrowdFlowerJson['data']['target_sentence']
        except KeyError:
            return self.emptyvalue

    def get_target_sentence(self):
        '''
        Extracts the targetsentence from the crowdflowerjson
        :return: <str>. The sentence in the target language
        '''
        try:
            return self.CrowdFlowerJson['data']['source_sentence']
        except KeyError:
            return self.emptyvalue


    def get_source_context(self):
        try:
            return self.CrowdFlowerJson['data']['source_context']
        except KeyError:
            return self.emptyvalue

    def get_target_context(self):
        try:
            return self.CrowdFlowerJson['data']['target_context']
        except KeyError:
            return self.emptyvalue

    def get_course_id(self):
        try:
            return self.CrowdFlowerJson['data']['course']
        except KeyError:
            return self.emptyvalue

    def get_entities(self):
        '''
        This function reads self.crowdflowerdata It returns a  list of all entities that occur more than self.threshold.
        This function uses self.thresholdcriteria. This parameter sets on what criterium must be looked wheter an entitie occurs more than twice.
            only the entities or must it also watch at the urls. By default it only looks at entities.
        :return: <list> A list of JudgmentData objects that contains all the entities that occur more than self.threshold
        '''
        judgments = self.CrowdFlowerJson['results']['judgments']

        judgdatlist = []

        for judgment in judgments:
            try:
                source_entities = judgment['data']['entity_source']
                source_entities_list = source_entities.strip(',').split(',')
            except KeyError:
                source_entities_list = [self.emptyvalue]

            try:
                source_urls = judgment['data']['url_source']
                source_urls_list = source_urls.strip(',').split(',')
            except KeyError:
                source_urls_list = [self.emptyvalue]

            try:
                target_entities = judgment['data']['entity_target']
                target_entities_list = target_entities.strip(',').split(',')
            except KeyError:
                target_entities_list = [self.emptyvalue]

            try:
                target_urls = judgment['data']['url_target']
                target_urls_list = target_urls.strip(',').split(',')
            except KeyError:
                target_urls_list = [self.emptyvalue]

            for combi in zip(source_entities_list, source_urls_list, target_entities_list, target_urls_list):

                judgdat = JudgmentData(source_entity=combi[0], source_url=combi[1], target_entity=combi[2], target_url=combi[3], occurence=1)

                isinlist, pos = judgdat.is_in_list(somelist=judgdatlist, criteria=self.thresholdcriteria)

                if isinlist:
                    judgdatlist[pos].occurence += 1

                else:
                    judgdatlist.append(judgdat)

        self.nrjudgments = len(judgments)

        if self.nrjudgments < 3:
            print ('Sentence {} has less than 3 judgements.'.format(self.sentence_id))

        returnlist = [item for item in judgdatlist if int(item.occurence) >= self.threshold]

        return returnlist

    def extract_info(self):
        '''
        This function extracts the desired information from the Crowdflower Json
        :return: Returns nothing (None)
        '''
        self.sentence_id = self.get_sentence_id()
        self.source_sentence = self.get_source_sentence()
        self.target_sentence = self.get_target_sentence()
        self.source_context = self.get_source_context()
        self.target_context = self.get_target_context()

        self.entities = self.get_entities()

        self.course_id = self.get_course_id()


    def make_json(self, json_type = 'str'):
        '''
        This function returns a json object containing information about the sentence
        :param json_type: <str> what should be returned? A json-string ('str') or a json-dict ('dict')?
        :return: either a json-string or a json-dict containing the information from the object
        '''
        assert json_type == 'str' or json_type == 'dict'
        entities = []
        for item in self.entities:
            entity = {}
            entity["source_entity"] = item.source_entity
            entity["source_url"] = item.source_url
            entity['target_entity'] = item.target_entity
            entity['target_url'] = item.target_url

            entities.append(entity)

        data = {'sentence_id': self.sentence_id,'course_id' : self.course_id , 'source_sentence': self.source_sentence, 'target_sentence': self.target_sentence ,
                'source_context': self.source_context, 'target_context': self.get_target_context(), 'entities':entities, 'nr_judgments': self.nrjudgments}

        if json_type == 'str':
            return json.dumps(data)
        elif json_type == 'dict':
            return data
