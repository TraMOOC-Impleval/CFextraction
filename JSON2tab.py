import json
import re


class JSON2tab:
    '''
    A class for writing the JSON acquired with SentenceInfoGetter to a tab separated file.
    '''
    def __init__(self, listofjsons):
        self.listofjsons = listofjsons

    def get_source_entities(self, singlejson):
        '''
        extracts the source entities for a single sentence from a json that is created by SentenceInfoGetter.
        :param singlejson: <json dict> A json of only one sentence from SentenceInfoGetter.
        :return: <str> returns a string containing the source entities separated by comma + space (', ')
        '''
        source_entities = []
        for item in singlejson["entities"]:
            source_entities.append(item["source_entity"])

        return ', '.join(source_entities)

    def get_target_entities(self, singlejson):
        '''
        extracts the target entities for a single sentence from a json that is created by SentenceInfoGetter.
        :param singlejson: <json dict> A json of only one sentence from SentenceInfoGetter.
        :return: <str> returns a string containing the target entities separated by comma + space (', ')
        '''
        target_entities = []
        for item in singlejson["entities"]:
            target_entities.append(item["target_entity"])

        return ', '.join(target_entities)


    def get_source_urls(self, singlejson):
        '''
        extracts the source urls for a single sentence from a json that is created by SentenceInfoGetter.
        :param singlejson: <json dict> A json of a single sentence from SentenceInfoGetter.
        :return: <str> returns a string containing the source urls separated by '@'
        '''
        source_urls = []
        for item in singlejson["entities"]:
            source_urls.append(item["source_url"])

        return '@'.join(source_urls)

    def get_target_urls(self, singlejson):
        '''
        extracts the target urls for a single sentence from a json that is created by SentenceInfoGetter.
        :param singlejson: <json dict> A json of a single sentence from SentenceInfoGetter.
        :return: <str> returns a string containing the target urls separated by '@'
        '''
        target_urls = []
        for item in singlejson["entities"]:
            target_urls.append(item["target_url"])

        return '@'.join(target_urls)

    def get_nr_judgments(self, singlejson):
        '''

        :param singlejson: <json dict> A json of a single sentence from SentenceInfoGetter.
        :return: <str> The number of judgements for this sentence.
        '''
        return singlejson['nr_judgments']

    def isgolden(self, value):
        '''
        Checks whether the sentence is a golden sentence. I.E. it is a sentence to determine the trustworthyness of a worker.
        :param value: <str> A value for the sentence ID
        :return: <int> returns 0 (False) if the sentence is golden. Else returns 1 (True)
        '''
        value = str(value)

        if re.match(r'[0-9]+', value):
            return 0
        else:
            return 1


    def get_line(self, singlejson, discardthreshold = 3):
        '''
        Gathers all information to be put in a single line in the tab-file.
        :param singlejson: <json dict> A single json (created by SentenceInfoGetter) representing one sentence.
        :param discardthreshold: <int> the minimum number of judgments for a sentence not to be discarded.
        :return linestr: <str> A string to be printed to the tab file
        :return discard: <bool> A boolean indicating whether a sentence must be discarded
        '''
        course = singlejson['course_id']
        source_sentence = singlejson["source_sentence"]

        target_sentence = singlejson["target_sentence"]

        golden = self.isgolden(singlejson["sentence_id"])

        source_context = singlejson['source_context']
        source_entities = self.get_source_entities(singlejson)
        target_entities = self.get_target_entities(singlejson)
        source_urls = self.get_source_urls(singlejson)
        target_urls = self.get_target_urls(singlejson)

        nrjudgment = self.get_nr_judgments(singlejson)

        if nrjudgment < discardthreshold:
            discard = True
        else:
            discard = False

        linelist = [course, source_context, target_sentence, source_sentence, str(golden), source_entities,
                    target_entities, source_urls, target_urls, '', '', '', '', '', '', '']

        linelist = [item if type(item) == str else 'NULL' for item in linelist]
        linestr = '\t'.join(linelist) + '\n'

        return linestr, discard

    def make_tabfile(self, outfilename='outfile.tab'):
        '''
        Writes the data in a list of jsons to a tabfile.
        :param outfilename: Filename of the output-tabfile
        :return: None
        '''
        out = open(outfilename, 'wt', encoding='utf-8')

        header = 'course\tsource_context\tsource sentence\ttarget_sentence\tgolden\tentity source\tentity target\turl source\turl target\t# correct topics marked\t# missed topics source\t# correct translation target\t# missed translations\t# correct wikilinks\t# missed wikilinks\tcomments\n'
        out.write(header)

        for singlejson in self.listofjsons:
            line, discard = self.get_line(singlejson)
            if not discard:
                out.write(line)

        out.close()
