from utils.constants import *
from wordle.simulate import *
from wordle.word_list import *
from wordle.solver import *

def main():
    """
    s = Simulate()
    wl = WordList(False)
    possible_words = wl.get_words()
    s.simulate(possible_words)
    """
    
    solver = Solver()
    solver.solve()

if __name__ == "__main__":
    main()