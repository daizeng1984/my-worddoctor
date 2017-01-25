import logging
import os
import re
import sys
import time

from .whdstrategy import WhdStrategy

# A class that implement "markov chain" word hints
class MarkovChain(WhdStrategy):

    def __init__(self, context):
        WhdStrategy.__init__(self, context)
        self.mc_order = 2
        self.mc_delimiter = '+'
        vars = context['vars']
        self.learning_texts = vars.get(
            'deoplete#sources#whd#learning_texts', [os.path.dirname(__file__) + '/./test/obama08.txt'])
        words = self._get_words_from_file()
        self.mc_knowledge = self._generate_dictionary(words)

    def _get_words_from_file(self):
        # TODO handle loading check etc.
        ret = []
        for filename in self.learning_texts:
            with open (filename) as f:
                words = [re.findall(r"[\w']+", line) for line in f]
                ret.extend([w for sub in words for w in sub])
            #TODO handle file separation ret.extend(['' for i in range(0, self.mc_order)])
        return ret

    def _generate_dictionary(self, words):
        # TODO add ranking for words and order them!
        # Change to lower case
        lowercaseWords = [x.lower() for x in words]

        # Build dictionary for whd knowledge
        knowledge = {}
        for i in range(self.mc_order, len(lowercaseWords)) :
            key = self.mc_delimiter.join(lowercaseWords[i-self.mc_order:i])
            knowledge.setdefault(key, set([]))
            knowledge[key].add(lowercaseWords[i])

        return knowledge
        
    def generate_hints(self, inputLine):
        
        # get the most recent two words (lowercase)
        inputWords = [x.lower() for x in re.findall(r"[\w']+", inputLine)]

        while (len(inputWords) < self.mc_order) :
            inputWords.append('')

        inputKey=self.mc_delimiter.join(inputWords[-self.mc_order:])

        hints = self.mc_knowledge.setdefault(inputKey, [])
        
        return hints
