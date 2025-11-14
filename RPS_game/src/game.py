"""
Author: Emad Leo (hamidleo1984@gmail.com)
Date: October 2025
A simple implementation of Rock Paper Scissors game.
"""

import random


class RockPaperScissors:
    """
    Main class for Rock Paper Scissors game.
    """
    def __init__(self, name):
        self.choices = ['rock', 'paper', 'scissors']
        self.player_name = name

    def get_player_choice(self):
        """
        get_player_choice: Prompts the user to enter their choice.
        :return: The user's choice.
        :rtype: str
        
        """
        user_choice = input(f"Enter your choice ({self.choices}):\n")
        print(user_choice)
        if user_choice.lower() in self.choices:
            return user_choice.lower()
        
        print(f"invalid choice, you must select from {self.choices}. ")
        return self.get_player_choice()
        
        
    def get_computer_choice(self):
        """
        Get computer choice from choices: ['rock', 'paper', 'scissors']
        :return: random choice from the list
        :rtype: str
        
        """
        return random.choice(self.choices)
    
    def decide_winner(self, user_choice, computer_choice):
        """
        decide_winner: Determines the winner of the game.

        This method compares the user's choice and the computer's choice
        to decide the winner based on the game rules.

        :param user_choice: The user's choice.
        :type user_choice: str
        :param computer_choice: The computer's choice.
        :type computer_choice: str
        :return: The result of the game.
        :rtype: str
        """
        if user_choice == computer_choice:
            return "play is Tie"
        win_combination = [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]
        
        if user_choice == computer_choice:
            return "play is Tie"
        win_combination = [("rock", "scissors"), ("paper", "rock", "scissors","paper")]
        for win_comb in win_combination:
            if (user_choice == win_comb[0]) & (computer_choice == win_comb[1]):
                return "Congratulation, You won!"
        return "Oh, no! the computer won!"
    # get player_choice
    # get computer_choice
    # decide_winner
    # play
    def play(self):
        """
        Play the Rock Paper Scissors game.
        This method orchestrates the game by getting the player's choice,
        the computer's choice, and deciding the winner.
        """
        user_choice = self.get_player_choice()
        computer_choice = self.get_computer_choice()
        print(f"Computer choice : {computer_choice} ")
        print(self.decide_winner(user_choice, computer_choice))

if __name__ == "__main__":
    while True:
        RockPaperScissors("Karo").play()

        continue_game = input("Do you want to play again? Enter any key to play, Enter q/Q to exit:\n")
        if continue_game.lower()== "q":
            print("Goodbye!!!")
            break