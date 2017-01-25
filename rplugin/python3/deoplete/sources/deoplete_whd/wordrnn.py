import logging
import os
import re
import sys
import time

from .whdstrategy import WhdStrategy

# A class that use word RNN to generate hints
class WordRNN(WhdStrategy):

    def __init__(self, context):
        WhdStrategy.__init__(self, context)
    
    def generate_hints(self, inputLine):
        return []
