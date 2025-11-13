import random

def monty_hall_game(switch_doors: bool) -> bool:
    """
    Simulates a single round of the Monty Hall game.
    """
    # Setup doors and randomly place the car behind one of them and goats behind the others
    doors = ["car", "goat", "goat"]
    random.shuffle(doors)
    
    # Contestant makes an initial choice
    initial_choice = random.choice([0,1,2])
    
    # Monty reveals a door that has a goat behind it and is not the contestant's initial choice
    doors_revealed = [i for i in range (3) if i != initial_choice and doors[i] == "goat"]
    door_revealed = random.choice(doors_revealed)
    
    # Contestant makes the final choice
    if switch_doors:
        final_choice = [i for i in range (3) if i != initial_choice and i != door_revealed][0]
    else:
        final_choice = initial_choice
        
    return doors[final_choice] == "car"

# Simulate multiple games and calculate winning percentages
def simulate_games(num_games: int = 10000) -> tuple[float,float]:
    num_wins_without_switching = sum(monty_hall_game(switch_doors = False) for _ in range(num_games))
    num_wins_with_switching = sum(monty_hall_game(switch_doors= True) for _ in range(num_games))
    
    return num_wins_without_switching, num_wins_with_switching


# Run the simulation and print results
if __name__ == "__main__":
    num_games = 1000
    num_wins_without_switching, num_wins_with_switching = simulate_games(num_games)
    print(f"Winning percentage without switching doors: {(num_wins_without_switching/num_games)}")
    print(f"Winning percentage with switching doors: {(num_wins_with_switching/num_games)}")