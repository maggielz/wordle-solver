import pickle
from utils.constants import *

class NextGuessCache:
    def __init__(self, cache_file=NEXT_GUESS_CACHE_FILE):
        self.cache_file = cache_file
        self.matches = {}   # k: ((tares, [guess2], [guess3]), pattern); v: next_guess
        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                self.matches = pickle.load(f)

    def add(self, guesses_so_far, pattern, value):
        self.matches[(tuple(guesses_so_far), pattern)] = value
    
    def has_key(self, guesses_so_far, pattern):
        return (tuple(guesses_so_far), pattern) in self.matches

    def get(self, guesses_so_far, pattern):
        if self.has_key(guesses_so_far, pattern):
            return self.matches[(tuple(guesses_so_far), pattern)]
        else:
            return None
    
    def cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.matches, f)
    
    def clear(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump({}, f)
        self.matches = {}
    
    def print(self):
        print(self.matches)