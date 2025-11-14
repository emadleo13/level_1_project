import random

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print("Type 'q' to quit the game at any time.")
print("You start with a score of 100, and lose 10 points for each incorrect guess.")
print("Let's begin!")
print("-" * 148)
def validate_input(input_num):
    if not input_num.isdigit():
        print("Sorry, that's not invalid input, please enter digit only.")
        return False
    
    input_num = int(input_num)
    if input_num < 1 or input_num > 100:
        print("Sorry, please enter a number betwen 1 & 100.")
        return False
    
    return True

def start_game():
    rand_num = random.randint(1, 100)
    score = 100
    attempts = 0
    
    
    while True:
        input_num = input("Enter your guess between 1 to 100:\n")
        attempts += 1
        
        if input_num.lower() == "q":
            print("Goodbye!")
            break
        if not validate_input(input_num):
            continue
        
        
        input_num = int(input_num)
        if input_num == rand_num:
            print(f"you guessed correctly ! in take {attempts} and your score is {score}")
            
            wanna_play = input("Do you want to play again? (y/n): ")
            if wanna_play.lower() == "y":
                rand_num = random.randint(1, 100)
                score = 100
                attempts = 0 
                continue
            else:
                print("Thanks for playing! Goodbye!")
                break
        
        elif input_num < rand_num:
            print("Your guess is too low.")
            score -= 10
            attempts += 1
        else:
            print("Your guess is too high.")
            score -= 10
            attempts += 1
        if score <= 0:
            print(f"Game over! thr correct number was {rand_num}")
            break
        
if __name__ == "__main__":
    start_game()
               
                
