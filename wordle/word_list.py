import numpy as np
from utils.constants import *

class WordList:
    def __init__(self, is_long=True):
        self.word_list = []
        self.filename = LONG_WORD_LIST_FILE if is_long else SHORT_WORD_LIST_FILE
        with open(self.filename) as fp:
            self.word_list.extend([word.strip() for word in fp.readlines()])
    
    def get_words(self):
        return self.word_list
    
    def __len__(self):
        return len(self.word_list)