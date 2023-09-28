import numpy as np

from utils.constants import *
from utils.time import *
from .entropy import *
from .word_list import *
from .next_guess_cache import *

class Solver:
    def __init__(self, word_len=5):
        self.word_len = word_len
        self.e = Entropy(word_len)
        self.p = Pattern(word_len)
        self.ngc = NextGuessCache(GAME_CACHE_FILE)
    
    def validate_input(self, word, pattern):
        if len(word) != self.word_len or len(pattern) != self.word_len:
            print(f'word "{word}" or pattern "{pattern}" does not have 5 letters')
            return False
        
        """
        if word not in self.all_words:
            print(f'"{word}" is not a valid word')
            return False
        """

        is_valid = True
        for i, c in enumerate(pattern):
            if c not in "012":
                print(f'{i}-th character is not one of: - (grey), y (yellow), g (green)')
                is_valid = False
        
        return is_valid
    
    def solve(self):
        wl = WordList()
        possible_words = wl.get_words()
        print("QUIT - quit, RESTART - new wordle, enter key - choose suggested guess")
        print("pattern: grey - 0, yellow - 1, green - 2")
        # best_words, best_entropies = self.e.all_entropies(possible_words, start=True)
        
        guess = self.ngc.get([], 0)
        if not guess:
            guess = self.e.best_guess(possible_words, start=True)
        guesses = []
        print(f"you should choose word {guess}")
        while True:
            chosen_word = input("what word did you choose? ")
            if chosen_word == "QUIT":
                break
            if chosen_word == "RESTART":
                self.solve()
                break
            if chosen_word == "":
                chosen_word = guess
            pattern_str = input(f"what is result of word? ")
            if pattern_str == "":
                print("----------")
                self.solve()
                break
            if not self.validate_input(chosen_word, pattern_str):
                print("input was invalid, try again")
                continue
            pattern = self.p.pattern_from_string(pattern_str)
            print(f"guess: {chosen_word} {self.p.pattern_to_string(pattern)}")
            guesses.append(chosen_word)
            possible_words = self.e.get_possible_words(chosen_word, pattern, possible_words)
            if len(possible_words) <= 0:
                print("no words were found :(")
                print("----------")
                self.solve()
                break
            elif len(possible_words) == 1:
                print("found word!", possible_words[0])
                print("----------")
                self.solve()
                break
            elif len(possible_words) < 5:
                print("possible_words:", possible_words)
            guess = self.ngc.get(guesses, pattern)
            if not guess:
                guess = self.e.best_guess(possible_words, start=False)
                self.ngc.add(guesses, pattern, guess)
            print(f"you should choose word {guess}")
            self.ngc.cache()
