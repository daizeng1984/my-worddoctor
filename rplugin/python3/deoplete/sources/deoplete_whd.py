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

    #Profile?
    #@profiler.profile
    def gather_candidates(self, context):
        # Dummy output
        result = []
        result.append( {
            'word': 'First Word Hints!'
            }
            )
        result.append( {
            'word': 'Second Word Hints!'
            }
            )
        return result
        

