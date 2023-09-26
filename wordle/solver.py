import numpy as np

from utils.constants import *
from .entropy import *
from .word_list import *
from .next_guess_cache import *

class Solver:
    def __init__(self, word_len=5):
        self.e = Entropy(word_len)
        self.p = Pattern(word_len)
        self.ngc = NextGuessCache()
    
    def solve(self):
        wl = WordList()
        possible_words = wl.get_words()
        guess = self.e.best_guess(possible_words, start=True)
        print("QUIT - quit, RESTART - new wordle, enter key - choose suggested guess")
        print("pattern: grey - 0, yellow - 1, green - 2")
        # best_words, best_entropies = self.e.all_entropies(possible_words, start=True)
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
            pattern = self.p.pattern_from_string(pattern_str)
            print(f"guess: {chosen_word} {self.p.pattern_to_string(pattern)}")
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
            best_words, best_entropies = self.e.all_entropies(possible_words, start=False)
            guess = self.e.best_guess(possible_words, start=False)
            print(f"you should choose word {guess}")
