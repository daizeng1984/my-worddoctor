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
        vars = context['vars']
        self.mc_order = vars.get('deoplete#sources#whd#order', 2)
        self.mc_delimiter = vars.get('deoplete#sources#whd#delimiter', '+')
        self.learning_texts = vars.get(
                'deoplete#sources#whd#learning_texts', 
                [os.path.dirname(__file__) + '/./test/obama08.txt'])
        self.learning_texts = [os.path.expandvars(x) for x in self.learning_texts]
        words = self._get_words_from_file()
        self.mc_knowledge = self._generate_dictionary(words)

    def _get_words_from_file(self):
        # TODO handle loading check etc.
        ret = []
        for filename in self.learning_texts:
            try:
                with open (filename) as f:
                    words = [re.findall(r"[\w']+", line) for line in f]
                    ret.extend([w for sub in words for w in sub])
                #TODO handle file separation ret.extend(['' for i in range(0, self.mc_order)])
            except EnvironmentError:
                print('WhD: error loading the file: ' + filename)
        return ret

    def _generate_dictionary(self, words):
        # TODO add ranking for words and order them!
        # Change to lower case
        lowercaseWords = [x.lower() for x in words]

        # Build dictionary for whd knowledge
        knowledge = {}
        for i in range(self.mc_order, len(lowercaseWords)) :
            key = self.mc_delimiter.join(lowercaseWords[i-self.mc_order:i])
            knowledge.setdefault(key, {})
            knowledge[key].setdefault(lowercaseWords[i], 0)
            knowledge[key][lowercaseWords[i]] = knowledge[key][lowercaseWords[i]] + 1;

        # Sort the words based on frequency
        for key,val in knowledge.items():
            knowledge[key]=sorted(list(val.keys()), key=lambda k:val[k])

        return knowledge
        
    def generate_hints(self, inputLine):
        
        # get the most recent two words (lowercase)
        inputWords = [x.lower() for x in re.findall(r"[\w']+", inputLine)]

        while (len(inputWords) < self.mc_order) :
            inputWords.append('')

        inputKey=self.mc_delimiter.join(inputWords[-self.mc_order:])

        hints = self.mc_knowledge.setdefault(inputKey, {})
        
        return hints
