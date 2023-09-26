import numpy as np

from utils.constants import *
from .pattern_matrix import *
from .pattern import *
import math
import os

class Entropy:
    def __init__(self, word_len=5):
        self.word_len = word_len
        self.p = Pattern(word_len)
        self.pm = PatternMatrix()
        self.all_words = self.pm.get_all_words()

    # get all possible words after guess and its pattern
    def get_possible_words(self, guess, pattern, word_list):
        all_patterns = self.pm.get_pattern_matrix([guess], word_list).flatten()
        return list(np.array(word_list)[all_patterns == pattern])
    
    def get_word_buckets(self, guess, possible_words):
        buckets = [[] for x in range(3 ** self.word_len)]
        patterns = self.pm.get_pattern_matrix([guess], possible_words).flatten()
        for pattern, word in zip(patterns, possible_words):
            buckets[pattern].append(word)
        return buckets
    
    def entropy(self, guess, possible_words):
        entropy = 0
        total = len(possible_words)
        self.buckets = self.get_word_buckets(guess, possible_words)
        entropy = sum([0 if len(bucket) <= 0 else (len(bucket) / total) * (- math.log2(len(bucket) / total)) for bucket in self.buckets])
        return entropy

    def best_guess(self, possible_words, start=False):
        best_words, _ = self.all_entropies(possible_words, 1, start)
        return best_words[0]

    def all_entropies(self, possible_words, top=10, start=False):
        # print_time("start all_entropies function")

        if start and not os.path.exists(STARTING_ENTROPY_FILE):
            print_time("generating starting entropies from scratch")
            entropies = [self.entropy(word, possible_words) for word in self.all_words]
            np.save(STARTING_ENTROPY_FILE, entropies)
            print_time("finished generating entropies from scratch")
        self.entropies = np.load(STARTING_ENTROPY_FILE)

        if not start:
            self.entropies = [self.entropy(word, possible_words) for word in self.all_words]

        # print_time("found entropies")

        sorted_indices = np.argsort(self.entropies)
        top_indices = sorted_indices[:-(top + 1):-1]
        best_words = np.array(self.all_words)[top_indices]
        best_entropies = np.array(self.entropies)[top_indices]
        """
        for word, entropy in zip(best_words, best_entropies):
            print(f"word {word} has entropy {entropy}")
        """
        return best_words, best_entropies
