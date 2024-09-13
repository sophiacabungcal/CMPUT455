# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys

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

        print(args)  # TODO: for debugging, remove later

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
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def legal(self, args):
        # check if this move (in the same format as in play) is legal
        # triples & balance constraint
        # command status always 1
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def genmove(self, args):
        # generates and plays a random move and gives the move as its response
        # move format is the same as for play: x y digit
        # If there is no legal move, output resign
        # command status always 1
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def winner(self, args):
        # checks if the game is over and outputs one of the following game results: 1 2 unfinished
        # command status always 1
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    #======================================================================================
    # Aux functions
    #======================================================================================
    def get_element(self, x, y):
        '''
        returns the element at the given coordinates
        '''
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            raise IndexError("Coordinates out of bounds")

        return self.board[x][y]
    
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
        if not args[0].isdigit() or not args[1].isdigit():
            return False
        
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

    def check_triple(self, x, y, digit):
        '''
        Checks if the move creates a triple (ie. does the move create a row / column of 3 of the same digit)
        return True if it does, False otherwise
        '''
        if self.width < 3 or self.height < 3:
            return False
        
        if y <= self.width - 3:
            if self.get_element(x, y + 1) == digit and self.get_element(x, y + 2) == digit:
                return True
        if y >= 2:
            if self.get_element(x, y - 1) == digit and self.get_element(x, y - 2) == digit:
                return True
        if 1 <= y <= self.width - 2:
            if self.get_element(x, y - 1) == digit and self.get_element(x, y + 1) == digit:
                return True

        if x <= self.height - 3:
            if self.get_element(x + 1, y) == digit and self.get_element(x + 2, y) == digit:
                return True
        if x >= 2:
            if self.get_element(x - 1, y) == digit and self.get_element(x - 2, y) == digit:
                return True
        if 1 <= x <= self.height - 2:
            if self.get_element(x - 1, y) == digit and self.get_element(x + 1, y) == digit:
                return True

        return False
    
    def check_balance(self, x, y, digit):
        '''
        Checks if the move violates the balance constraint 
        (ie. count of both 0s & 1s in each row / column cannot exceed half the length of that row or column (rounded up for odd lengths))
        return True if it does, False otherwise
        '''
        # Calculate the maximum allowed count for 0s and 1s
        max_count_row = (self.width + 1) // 2
        max_count_col = (self.height + 1) // 2

        current_row_digit_count = sum(1 for j in range(self.width) if self.get_element(x, j) == digit)
        current_col_digit_count = sum(1 for i in range(self.height) if self.get_element(i, y) == digit)
    
        current_row_digit_count += 1
        current_col_digit_count += 1

        if current_row_digit_count > max_count_row or current_col_digit_count > max_count_col:
            return True

        return False

    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()