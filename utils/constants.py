import os
import numpy as np

# file names
DATA_DIR = "data/"
SHORT_WORD_LIST_FILE = DATA_DIR + "possible_words.txt"
LONG_WORD_LIST_FILE = DATA_DIR + "allowed_words.txt"
PATTERN_MATRIX_FILE = DATA_DIR + "pattern_matrix.npy"
STARTING_ENTROPY_FILE = DATA_DIR + "starting_entropy.npy"
NEXT_GUESS_CACHE_FILE = DATA_DIR + "next_guess_cache.pkl"

# character comparisons
MISS = np.uint8(0)
MISPLACED = np.uint8(1)
EXACT = np.uint8(2)
