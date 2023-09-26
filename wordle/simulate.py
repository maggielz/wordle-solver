from typing import Any
from .word_list import *
from .entropy import Entropy
from .pattern import Pattern
from .pattern_matrix import PatternMatrix
import pickle
from .next_guess_cache import *
from statistics import mean


class Simulate:
    def __init__(self, word_len=5):
        self.word_len = word_len
        self.e = Entropy(word_len)
        self.p = Pattern(word_len)
        self.pm = PatternMatrix()
        self.tares_next = {}
        self.ngc = NextGuessCache()

        wl = WordList(False)
        self.possible_words = wl.get_words()
        wl = WordList(True)
        self.all_words = wl.get_words()
    
    def simulate_game(self, word):
        allowed_words = self.all_words
        print(f"simulate game for word {word}")
        start = True
        rounds = 0
        guesses = []
        guess = None
        guess_pattern = -1
        found = False

        while rounds < 6:
            rounds += 1

            if guess_pattern >= 0:
                guess = self.ngc.get(guesses, guess_pattern)
            if not guess and guess_pattern >= 0:
                guess = self.e.best_guess(allowed_words, start)
                self.ngc.add(guesses, guess_pattern, guess)
            elif not guess and guess_pattern < 0:
                guess = self.e.best_guess(allowed_words, start)

            guess_pattern = self.pm.get_pattern(guess, word)
            guesses.append(guess)
            allowed_words = self.e.get_possible_words(guess, guess_pattern, allowed_words)
            print(f"{guess} {self.p.pattern_to_string(guess_pattern)}")
            if start:
                start = False
            if guess_pattern == 3 ** (self.word_len) - 1:
                print(f"found word: {allowed_words[0]} in {rounds} rounds")
                found = True
                break
            elif len(allowed_words) == 1:
                guess = allowed_words[0]
                guess_pattern = self.pm.get_pattern(guess, word)
                rounds += 1
                print(f"{guess} {self.p.pattern_to_string(guess_pattern)}")
                print(f"found word: {allowed_words[0]} in {rounds} rounds")
                found = True
                break
            elif len(allowed_words) < 1:
                print(f"error: could not find word")
                break
                
        self.ngc.cache()

        return found, rounds

    def simulate(self, words):
        total_words = len(words)
        successes = 0
        rounds = []
        failures = []
        for word in words:
            success, num_rounds = self.simulate_game(word)
            successes += 1 if success else 0
            if success:
                rounds.append(num_rounds)
            else:
                failures.append(word)
        
        print(f"successfully found {successes} out of {total_words} words")
        print(f"average number of rounds is {mean(rounds)}")
        print(f"failed rounds {failures}")



