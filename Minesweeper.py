# Minesweeper using tkinter for the GUI.
# ElectriZ

# Import
import random as rd

class Cell:
    """Start class Cell"""
    
    def __init__(self):
        """Cell -> None
        Constructor of the Cell class"""
        self.__value = 0
        self.__hidden = True
        self.__flag = False
        
    def is_hidden(self):
        """Cell -> bool
        return True if the cell is hidden"""
        return self.__hidden
    
    def is_visible(self):
        """Cell -> bool
        return True if the cell is visible"""
        return not self.__hidden
    
    def is_bomb(self):
        """Cell -> bool
        return True if the cell is a bomb"""
        return self.__value == -1
    
    def is_empty(self):
        """Cell -> bool
        return True if the cell is empty"""
        return self.__value == 0
    
    def increment_value(self):
        """Cell -> None
        Increment cell"""
        if not self.is_bomb():
            self.__value += 1
            
    def show_yourself(self):
        """Cell -> None
        Show cell"""
        self.__hidden = False
        self.__flag = False
        
    def __str__(self):
        """Cell -> str
        returns the cell in text format"""
        if self.is_hidden():
            return "-"
        elif self.is_bomb():
            return "*"
        elif self.is_empty():
            return " "
        return str(self.__value)
    
    def set_value(self, val):
        """Set cell value
        Args:
        - val (int): Value
        """
        self.__value = val
        
    def value(self):
        """Cell -> int
        return the value contained in the cell"""
        return self.__value
    
    def is_flag(self):
        """Cell -> bool
        return True if the cell is a flag"""
        return self.__flag
    
    def lay_flag(self):
        """Cell -> None
        Set flag value to True"""
        self.__flag = True
        
    def remove_flag(self):
        """Cell -> None
        Set flag value to False"""
        self.__flag = False
        
class Minesweeper:
    def __init__(self, nb_row=10, nb_col=20):
        """Minesweeper, int, int -> None
        Create a minesweeper"""
        
        assert not(nb_row < 2), "The number of rows cannot be less than 2"
        self.__nb_row = nb_row
        assert not(nb_row < 2), "The number of columns cannot be less than 2"
        self.__nb_col = nb_col
        self.__board = []
        for i in range(nb_row):
            row = []
            for j in range(nb_col):
                row.append(Cell())
            self.__board.append(row)
            
    def get_nb_row(self):
        """Minesweeper -> int
        return the number of rows on the board"""
        return self.__nb_row
    
    def get_nb_col(self):
        """Minesweeper -> int
        return the number of columns on the board"""
        return self.__nb_col
    
    def display_separation_row(self):
        """Minesweeper -> str
        return separation"""
        width = len(str(self.__nb_row - 1))
        ret = " " * width + " "
        width = len(str(self.__nb_col - 1))
        for i in range(self.__nb_col):
            ret += "+" + "-" * width
        return ret + "+"
    
    def show_row(self, row):
        """Minesweeper -> str
        return row"""
        width = len(str(self.__nb_row - 1))
        ret = str(row).center(width, " ") + " "
        width = len(str(self.__nb_col - 1))
        for cell in self.__board[row]:
            if cell.is_hidden():
                ret += "|" + cell.str() * width
            elif cell.est_bombe() or cell.is_empty():
                ret += "|" + cell.str() * width
            else:
                ret += "|" + cell.str().center(width, " ")
        return ret + "|"
    
    def show_board(self):
        """Minesweeper -> str
        Displays the board on the console"""
        width = len(str(self.__nb_row - 1))
        ret = " " * width + " "
        width = len(str(self.__nb_col - 1))
        for i in range(self.__nb_col):
            ret += " " + str(i).center(width, " ")
        ret += " -> X\n"
        for row in range(self.__nb_row):
            ret += self.display_separation_row() + "\n"
            ret += self.show_row(row) + "\n"
        ret += self.display_separation_row()
        print(ret)
        print("|\nv\nY")
        
    def lay_bombs(self, nb_bomb=15):
        """Minesweeper, int -> None
        Place bombs on the board

        Args:
        - nb_bomb (int, optional): Number of bombs. Default number -> 15.
        """
        assert not(nb_bomb > (self.__nb_row * self.__nb_col - 1))
        counter = 0
        while counter < nb_bomb:
            coord = (rd.randint(0, self.__nb_row - 1), rd.randint(0, self.__nb_col - 1))
            if self.__board[coord[0]][coord[1]].is_bomb():
                continue
            counter += 1
            self.__board[coord[0]][coord[1]].set_value(-1)
            for row, col in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if (((coord[0] + row) >= 0) and ((coord[0] + row) <= (self.__nb_row - 1))) and (((coord[1] + col) >= 0) and ((coord[1] + col) <= (self.__nb_col - 1))):
                    self.__board[coord[0] + row][coord[1] + col].increment_value()
                    
    def game_done(self, row, col):
        """Minesweeper, int, int -> int
        Returns the game status:
        - 0 : Not finished
        - 1 : Lost
        - 2 : Won

        Args:
        - row (int): Number of row
        - col (int): Number of columns

        Returns:
            int: Game status
        """
        if self.__board[row][col].is_bomb():
            return 1
        for line in self.__board:
            for cell in line:
                if cell.is_hidden() and not(cell.is_bomb()):
                    return 0
        return 2
    
    def show(self, row, col):
        """Minesweeper, int, int -> None
        Show given cell

        Args:
        - row (int): Number of lines
        - col (int): Number of columns
        """
        cell = self.__board[row][col]
        cell.show_yourself()
        if cell.is_empty():
            self.show_cell(row, col)
            
    def show_cell(self, row, col):
        """Minesweeper, int, int -> None
        Show if necessary, the cells around the given one

        Args:
        - row (int): Number of lines
        - col (int): Number of columns
        """
        for row_around, col_around in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            coord = (row + row_around, col + col_around)
            if ((coord[0] >= 0) and (coord[0] <= (self.__nb_row - 1))) and ((coord[1] >= 0) and (coord[1] <= (self.__nb_col - 1))):
                if self.__board[coord[0]][coord[1]].is_hidden():
                    self.show(coord[0], coord[1])
                    
    def reinit(self):
        """Minesweeper -> None
        Reset the board"""
        self.__board = []
        for i in range(self.__nb_row):
            row = []
            for j in range(self.__nb_col):
                row.append(Cell())
            self.__board.append(row)
            
    def value(self, row, col):
        """Minesweeper, int, int -> int
        Returns cell value at coordinates

        Args:
        - row (int): Number of lines
        - col (int): Number of columns
        """
        return self.__board[row][col].value()
    
    def is_hidden(self, row, col):
        """Minesweeper, int, int -> bool
        Returns True if the cell at the given coordinates is hidden

        Args:
        - row (int): Number of lines
        - col (int): Number of columns
        """
        return self.__board[row][col].is_hidden() 
    
    def is_flag(self, row, col):
        """Minesweeper, int, int -> bool
        Returns True if the cell at the given coordinates is a flag"""
        return self.__board[row][col].is_flag()
    
    def lay_flag(self, row, col):
        """Minesweeper, int, int -> None
        Place a flag at the given coordinates"""
        self.__board[row][col].lay_flag()
        
    def remove_flag(self, row, col):
        """Minesweeper, int, int -> None
        Remove the flag at the given coordinates"""
        self.__board[row][col].remove_flag()