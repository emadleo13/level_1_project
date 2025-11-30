import random

class TicTacToe:
    def __init__(self) -> None:
        self.board = [' '] * 10    #list(map(str, range(10)))
        self.player_turn = 'X'
        
        
    def show_board(self) -> None:
        print('\n')
        print(self.board[7] + '|' + self.board[8] + '|' + self.board[9])
        print('-+-+-')
        print(self.board[4] + '|' + self.board[5] + '|' + self.board[6])
        print('-+-+-')
        print(self.board[1] + '|' + self.board[2] + '|' + self.board[3])
        print('\n')
        
    def swap_player_turn(self) -> None:
        self.player_turn = 'X' if self.player_turn == 'O' else 'O'
    
    def is_board_filled(self) -> bool:
        return ' ' not in self.board[1:]
    
    def fix_spot(self, cell, player) -> None:
        self.board[cell] = player
        
    def is_player_win(self, player) -> bool:
        win_combinations = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # columns
            (1, 5, 9), (3, 5, 7)              # diagonals
        ]
        for combination in win_combinations:
            if all(self.board[cell] == player for cell in combination) :
                return True
        return False
        
    def get_random_first_player(self) -> str:
        return 'X' if random.randint(0, 1) == 0 else 'O'
    
    def start(self) -> None:
        while True:
            self.show_board()
            print(f"player {self.player_turn} turn")
            cell = int(input("Enter the cell number (1-9) to fix spot:"))
            
            if self.board[cell] == ' ' and cell in range(1,10):
                self.fix_spot(cell, self.player_turn)
                
                if self.is_player_win(self.player_turn):
                    self.show_board()
                    print(f"player {self.player_turn} wins the game!")
                    break
                
                if self.is_board_filled():
                    self.show_board()
                    print("Match Draw!")
                    break
                
                self.swap_player_turn()
            else:
                print("Invalid cell!! Try again")
                    
                
if __name__ == "__main__":
    game = TicTacToe()
    game.start()
                    
                    
                