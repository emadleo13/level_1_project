from game_logic.number_generat import generate_random_number
from game_logic.hint_generat import provide_hint
from game_logic.scorer import Scorer
from utils.input_validat import get_valid_input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    number_to_guess = generate_random_number(1, 101)
    scorer = Scorer()
    
    while True:
        guess = get_valid_input("Enter your number guess: ", 1, 101)
        if guess == number_to_guess:
            print(f"Congratulation! your final score is: {scorer.get_score()}")
            break
        else:
            hint = provide_hint(guess, number_to_guess)
            print(hint)
            scorer.decrement_score()
        

if __name__ == "__main__":
    main()