import numpy as np
from utils.constants import *

class Pattern:
    def __init__(self, word_len=5):
        self.word_len = word_len

    def pattern_from_string(self, pattern_string):
        return sum((3 ** i) * int(c) for i, c in enumerate(pattern_string))

    def pattern_to_int_list(self, pattern):
        result = []
        curr = pattern
        for x in range(self.word_len):
            result.append(curr % 3)
            curr = curr // 3
        return result
    
    def pattern_to_string(self, pattern, guess=""):
        d = {MISS: "⬛", MISPLACED: "🟨", EXACT: "🟩"}
        return "".join(d[x] for x in self.pattern_to_int_list(pattern)) + " " + guess
    

