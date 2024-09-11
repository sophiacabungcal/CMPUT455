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
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def show(self, args):
        # shows the current state of the grid, one line per row, followed by the command status
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def play(self, args):
        # Place the digit (0 or 1) at the given (x,y) coordinate
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def legal(self, args):
        # check if this move (in the same format as in play) is legal
        # check triples & balance constraint
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
    
    def get_command_status():
        # return the command status
        raise NotImplementedError("This command is not yet implemented.")
        return True

    def check_triple():
        # check if the move creates a triple
        # return True if it does, False otherwise
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def check_balance():
        # check if the move violates the balance constraint
        # return True if it does, False otherwise
        raise NotImplementedError("This command is not yet implemented.")
        return True



    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()