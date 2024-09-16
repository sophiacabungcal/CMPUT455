# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }
        self.width = 0
        self.height = 0
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game(self, args):
        # creates a new game on an empty rectangular grid of width n and height m (both in the range from 1 and 20)
        # only requires the command status as output (1 or -1)
        if not self.is_args_valid(args, self.validate_game_args):
            raise ValueError("Invalid arguments for game command")

        self.width = int(args[0])
        self.height = int(args[1])
        self.board = [['.' for _ in range(self.width)] for _ in range(self.height)]

        return True
    
    def show(self, args):
        # shows the current state of the grid, one line per row, followed by the command status
        if not self.is_args_valid(args, self.validate_show_args):
            raise ValueError("Invalid arguments for show command")
        
        for row in self.board:
            print(''.join(row))
        
        return True
    
    def play(self, args):
        # Place the digit (0 or 1) at the given (x,y) coordinate
        illegal_msg = '= illegal move: '
        
        # args check
        args_valid = self.is_args_valid(args, self.validate_legal_args)
        if args_valid[0] != True:
            print(illegal_msg + f'{" ".join(args)} ' + args_valid[1] + '\n')
            return False
        
        move_x = int(args[0])
        move_y = int(args[1])
        move_digit = args[2]
        
        # triple check
        triple_violation = self.check_triple_violation(move_x, move_y, move_digit)
        if triple_violation[0] != False:
            print(illegal_msg + f'{" ".join(args)} ' + triple_violation[1] + '\n')
            return False
        
        #  balance check
        balance_violation = self.check_balance_violation(move_x, move_y, move_digit)
        if balance_violation[0] != False:
            print(illegal_msg + f'{" ".join(args)} ' + balance_violation[1] + '\n')
            return False
        
        self.board[move_y][move_x] = move_digit
        
        return True
    
    def legal(self, args):
        # check if this move (in the same format as in play) is legal
        # triples & balance constraint
        # command status always 1
        if not self.is_args_valid(args, self.validate_legal_args)[0]:
            print("no")
            return True

        move_x = int(args[0])
        move_y = int(args[1])
        move_digit = args[2]

        if self.check_balance_violation(move_x, move_y, move_digit)[0] or self.check_triple_violation(move_x, move_y, move_digit)[0]:
            # methods return true if not legal
            print("no")
        else:
            print("yes")
        
        return True
    
    def genmove(self, args):
        # generates and plays a random move and gives the move as its response
        # move format is the same as for play: x y digit
        # If there is no legal move, output resign
        # command status always 1
        pos_moves = []
        
        for digit in ('0','1'):
            for row in range(self.height):
                for col in range(self.width):
                    if self.board[row][col] != '.': continue  # skip occupied
                    args_valid = self.is_args_valid((str(col),str(row),digit), self.validate_legal_args)
                    triple_violation = self.check_triple_violation(col, row, digit)
                    balance_violation = self.check_balance_violation(col, row, digit)
                    if args_valid[0] and not triple_violation[0] and not balance_violation[0]:
                        pos_moves.append([col, row, digit])
                        
        if not pos_moves:
            print('resign')
        else:
            move = random.choice(pos_moves)
            gcol, grow, gdigit = move[0], move[1], move[2]
            self.board[grow][gcol] = gdigit
            print(f'{gcol} {grow} {gdigit}')
            
        return True
    
    def winner(self, args):
        # checks if the game is over and outputs one of the following game results: 1 2 unfinished
        # player who makes final move wins (ie. player with no legal moves left loses)
        # command status always 1

        # if there's more than 1 legal moves left: unfinished

        # if only 1 legal move left, check whose turn it is - whoever's turn it is will be the winner since that will be the last move
        pos_moves = []
        move_count = 0
            
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == '.':
                    pos_moves.append([row, col, "1"])
                    pos_moves.append([row, col, "0"])
                else:
                    move_count += 1
                    
        if not pos_moves: 
            print((move_count + 1) % 2 + 1)
            return True

        for move in pos_moves:
            row, col, digit = move
            args_valid = self.is_args_valid((str(col),str(row),digit), self.validate_legal_args)
            triple_violation = self.check_triple_violation(col, row, digit)
            balance_violation = self.check_balance_violation(col, row, digit)
            
            if args_valid[0] and not triple_violation[0] and not balance_violation[0]:
                print('unfinished')
                return True

        print((move_count + 2) % 2)
                    
        return True
    
    #======================================================================================
    # Aux functions
    #======================================================================================
    def get_element(self, y, x):
        '''
        returns the element at the given coordinates
        '''
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Coordinates out of bounds")

        return self.board[y][x]
    
    def is_args_valid(self, args, validation_func):
        '''
        checks if the arguments are valid
        return True if they are, False if not
        '''
        return validation_func(args)
    
    def validate_game_args(self, args):
        '''
        Validates if the arguments for the game command are valid
        must be 2 arguments, both integers, between 1 and 20
        '''
        if len(args) != 2:
            return False
        #if not args[0].isdigit() or not args[1].isdigit():
        #    return False
        
        width, height = int(args[0]), int(args[1])
        if not (1 <= width <= 20 and 1 <= height <= 20):
            return False
        
        return True
    
    def validate_show_args(self, args):
        '''
        Validates if the arguments for the show command are valid
        must be no arguments and the board should be instatiated
        '''
        return len(args) == 0 and self.board is not None and len(self.board) > 0

    def validate_legal_args(self, args):
        '''
        validates if the arguments for the legal command are valid
        must have 3 arguments: x y digit
        x (args[0]) and y (args[1]) must be ints between 1 to 20
        digit must be either 1 or 0
        '''
        if len(args) != 3:
            return False, 'wrong number of arguments'
        if not args[0].isdigit() or not args[1].isdigit():
            return False, 'wrong coordinate'
        if args[2] not in ['1', '0']:
            return False, 'wrong number'
        
        x, y = int(args[0]), int(args[1])
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False, 'wrong coordinate'

        # occupied check
        if self.board[y][x] != '.':
            return False, 'occupied'
        
        return True, ''
    

    def check_triple_violation(self, x, y, digit):
        '''
        Checks if the move creates a triple (ie. does the move create a row / column of 3 of the same digit)
        return True if it is a violation, False otherwise
        '''
        three_msg = 'three in a row'
        
        # If the board is too small, no triple can occur
        if self.width < 3 and self.height < 3:
            return False, ''
        
        # Horizontal check (row-wise, so y is constant, x changes)
        if x <= self.width - 3:
            if self.get_element(y, x + 1) == digit and self.get_element(y, x + 2) == digit:
                return True, three_msg
        if x >= 2:
            if self.get_element(y, x - 1) == digit and self.get_element(y, x - 2) == digit:
                return True, three_msg
        if 1 <= x <= self.width - 2:
            if self.get_element(y, x - 1) == digit and self.get_element(y, x + 1) == digit:
                return True, three_msg

        # Vertical check (column-wise, so x is constant, y changes)
        if y <= self.height - 3:
            if self.get_element(y + 1, x) == digit and self.get_element(y + 2, x) == digit:
                return True, three_msg
        if y >= 2:
            if self.get_element(y - 1, x) == digit and self.get_element(y - 2, x) == digit:
                return True, three_msg
        if 1 <= y <= self.height - 2:
            if self.get_element(y - 1, x) == digit and self.get_element(y + 1, x) == digit:
                return True, three_msg

        return False, ''   
    
    def check_balance_violation(self, x, y, digit):
        '''
        Checks if the move violates the balance constraint 
        (ie. count of both 0s & 1s in each row / column cannot exceed half the length of that row or column (rounded up for odd lengths))
        return True if it is a violation, False otherwise
        '''
        # Calculate the maximum allowed count for 0s and 1s
        max_count_row = self.width // 2 + (self.width % 2 > 0)
        max_count_col = self.height // 2 + (self.height % 2 > 0)

        current_row_digit_count = sum(1 for j in range(self.width) if self.get_element(y, j) == digit)
        current_col_digit_count = sum(1 for i in range(self.height) if self.get_element(i, x) == digit)
    
        current_row_digit_count += 1
        current_col_digit_count += 1

        if current_row_digit_count > max_count_row or current_col_digit_count > max_count_col:
            return True, f'too many {digit}'

        return False, ''

    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()