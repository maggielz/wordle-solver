import numpy as np
import itertools as it
import os

from utils.constants import *
from utils.time import *
from .word_list import *

class PatternMatrix:
    def __init__(self):
        self.pattern_grid_data = dict()
        self.word_len = -1
        self.full_grid, self.words_to_index, self.all_words = self.get_full_pattern_matrix()

    def get_full_grid(self):
        return self.full_grid
    
    def get_words_to_index(self):
        return self.words_to_index
    
    def get_all_words(self):
        return self.all_words

    def words_to_int_arrays(self, words):
        return np.array([[ord(c) for c in word] for word in words], dtype=np.uint8)

    def generate_pattern_matrix(self, words1, words2):
        word_len = len(words1[0])
        self.word_len = word_len
        n_words1 = len(words1)
        n_words2 = len(words2)

        # convert word lists to int arrays of ascii values
        word_arr1, word_arr2 = map(self.words_to_int_arrays, (words1, words2))

        # equality grid[a, b, i, j]: 
        #   true if i-th char of guess a matches j-th char of answer b
        print_time("generate equality_grid")
        equality_grid = np.zeros((n_words1, n_words2, word_len, word_len), dtype=bool)
        print(f"equality_grid.shape {equality_grid.shape}")
        for i, j in it.product(range(word_len), range(word_len)):
            equality_grid[:, :, i, j] = np.equal.outer(word_arr1[:, i], word_arr2[:, j])

        # pattern_matrix[a, b] represents 5-color pattern
        # for guess a, answer b, with 0 -> grey, 1 -> yellow, 2 -> green
        pattern_matrix = np.zeros((n_words1, n_words2, word_len), dtype=np.uint8)
        
        # green pass
        print_time("green pass")
        for i in range(word_len):
            # where letters are in correct index, mark it as exact match
            matches = equality_grid[:, :, i, i].flatten()
            # 
            pattern_matrix[:, :, i].flat[matches] = EXACT

            # if match, mark all elements associated with that letter as covered
            for k in range(word_len):
                equality_grid[:, :, k, i].flat[matches] = False
                equality_grid[:, :, i, k].flat[matches] = False

        # yellow pass
        print_time("yellow pass")
        for i, j in it.product(range(word_len), range(word_len)):
            matches = equality_grid[:, :, i, j].flatten()
            pattern_matrix[:, :, i].flat[matches] = MISPLACED
            for k in range(word_len):
                equality_grid[:, :, k, j].flat[matches] = False
                equality_grid[:, :, i, k].flat[matches] = False
        
        # convert to int value
        pattern_matrix = np.dot(
            pattern_matrix, (3 ** np.arange(word_len)).astype(np.uint8)
        )
        return pattern_matrix

    def generate_full_pattern_matrix(self, words):
        print_time("start generating full pattern matrix")
        pattern_matrix = self.generate_pattern_matrix(words, words)
        np.save(PATTERN_MATRIX_FILE, pattern_matrix)
        return pattern_matrix

    def get_full_pattern_matrix(self):
        wordList = WordList()
        words = wordList.get_words()

        if not self.pattern_grid_data:
            if not os.path.exists(PATTERN_MATRIX_FILE):
                print_time("generating pattern matrix")
                self.generate_full_pattern_matrix(words)
            self.pattern_grid_data['grid'] = np.load(PATTERN_MATRIX_FILE)
            self.pattern_grid_data['words_to_index'] = dict(zip(words, it.count()))
        
        full_grid = self.pattern_grid_data['grid']
        words_to_index = self.pattern_grid_data['words_to_index']
        return full_grid, words_to_index, words

    def get_pattern_matrix(self, words1, words2):
        # returns pattern grid for selected words1 and words2
        indices1 = [self.words_to_index[w] for w in words1]
        indices2 = [self.words_to_index[w] for w in words2]
        return self.full_grid[np.ix_(indices1, indices2)]

    def get_pattern(self, guess, answer):
        grid = self.get_pattern_matrix([guess], [answer])
        return grid[0][0]