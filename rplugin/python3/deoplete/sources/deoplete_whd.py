import logging
import os
import re
import sys
import time

sys.path.insert(1, os.path.dirname(__file__)) # noqa: E261
from deoplete_whd import markovchain, wordrnn

from .base import Base

# A class that will be loaded by deoplete
class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'whd' # Your source name
        self.mark = '[whd]' # Your source mark
        self.rank = 500
        self.filetypes = ['markdown']
        self.input_pattern = '[\w|\W]+\s\w*' # What trigger your completion

    def on_init(self, context):
        self.mc = markovchain.MarkovChain(context)

    # Complete position
    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    #Profile?
    #@profiler.profile
    def gather_candidates(self, context):
        # if you own a whd degree, you should be able to know:
        hints = self.mc.generate_hints(context['input'])
        result = [ {'word':x} for x in hints ]
        return result
