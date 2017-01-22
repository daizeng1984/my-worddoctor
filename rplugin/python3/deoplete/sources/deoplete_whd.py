import logging
import os
import re
import sys
import time

from .base import Base

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'whd' # Your source name
        self.mark = '[whd]' # Your source mark
        self.rank = 500
        self.filetypes = ['markdown']
        self.input_pattern = '[\w|\W]+\s\w*' # What trigger your completion

    # Complete position
    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def _get_words_from_file(self, filename):
        with open (filename) as f:
            words = [re.findall(r"[\w']+", line) for line in f]
            return [w for sub in words for w in sub]

    #Profile?
    #@profiler.profile
    def gather_candidates(self, context):
        ORDER = 2
        DELIMITER = '+'
        # if you own a whd degree, you should be able to know:
        whdKnowledgeResource='/tmp/obama08.txt' #TODO ask user to set it

        # Dummy output
        words = self._get_words_from_file(whdKnowledgeResource)
        lowercaseWords = [x.lower() for x in words]

        # Build dictionary for whd knowledge
        knowledge = {}
        for i in range(ORDER, len(lowercaseWords)) :
            key = DELIMITER.join(lowercaseWords[i-ORDER:i])
            knowledge.setdefault(key, set([]))
            knowledge[key].add(lowercaseWords[i])

        # get the most recent two words (lowercase)
        inputLine = context['input']
        inputWords = [x.lower() for x in re.findall(r"[\w']+", inputLine)]

        while (len(inputWords) < ORDER) :
            inputWords.append('')

        inputKey=DELIMITER.join(inputWords[-ORDER:])

        hints = knowledge.setdefault(inputKey, [])

        result = [ {'word':x} for x in hints ]
        return result
