# Minesweeper using tkinter for the GUI.
# ElectriZ

# Import
import Minesweeper
import tkinter as tk

class MinesweeperView:
    """Initialize MinesweeperView class"""
    def __init__(self, minesweeper):
        self.__minesweeper = minesweeper
        self.__width, self.__height = (self.__minesweeper.get_nb_col(), self.__minesweeper.get_nb_row())
        self.__buttons = []
        self.__images = []
        self.__root = tk.Tk()
        self.__root.title("Minesweeper")
        
        self.__image_cache = tk.PhotoImage(file="./assets/cache.gif")
        images = ["nothing", "one", "two", "three", "four", "five", "six", "seven", "eight", "mine"]
        for image in images:
            self.__images.append(tk.PhotoImage(file="./assets/{}.gif".format(image)))        
        self.__image_drapeau = tk.PhotoImage(file="./assets/flag.gif")
        
        frame_game = tk.Frame(self.__root)
        for row in range(self.__height):
            for col in range(self.__width):
                self.__buttons.append(tk.Button(frame_game, image=self.__image_cache, command=None))
                self.__buttons[-1].grid(row=row, column=col)
        frame_game.pack()
        
        # Creating command buttons
        frame_foot = tk.Frame(self.__root)
        btn_restart = tk.Button(frame_foot, text="Restart", command=self.ctrl_reinit)
        btn_restart.grid(row=0, column=0)
        btn_quit = tk.Button(frame_foot, text="Quit", command=self.__root.destroy)
        btn_quit.grid(row=0, column=1)
        self.__lbl_end = tk.Label(frame_foot, text="", fg="red")
        self.__lbl_end.grid(row=0, column=2)
        frame_foot.pack()
        self.start()
        
    def ctrl_reinit(self):
        """ MinesweeperView -> Reset the model and update the view"""
        self.__minesweeper.reinit()
        self.__minesweeper.lay_bombs()
        for i, bouton in enumerate(self.__buttons):
            row, col = (i // self.__width, i % self.__width)
            bouton["state"] = tk.NORMAL
            bouton["command"] = self.create_func_show_cell(row, col)
            bouton.bind("<Button-3>", self.create_flag_management_control(row, col))
        self.__lbl_end["text"] = ""
        self.redraw()
        
    def start(self):
        """Starts the event listener loop"""
        self.ctrl_reinit()
        self.__root.mainloop()
        
    def create_func_show_cell(self, row, col):
        """int, int -> fonc
        return function"""
        def ctrl_montre_case():
            if self.__minesweeper.is_hidden(row, col) and not self.__minesweeper.is_flag(row, col):
                self.__minesweeper.show(row, col)
                self.redraw()
                end_val = self.__minesweeper.game_done(row, col)
                if end_val == 2:
                    end_text = "Congratulations you won !"
                elif end_val == 1:
                    end_text = "Lost ! You hit a bomb !"
                if end_val != 0:
                    self.__lbl_end["text"] = end_text
                    self.disable_buttons()
        return ctrl_montre_case
    
    def disable_buttons(self):
        """MinesweeperView -> None
        Disable all buttons"""
        for boutton in self.__buttons:
            boutton["state"] = tk.DISABLED
            
    def redraw(self):
        """MinesweeperView -> None
        Redraw the board"""
        for i, boutton in enumerate(self.__buttons):
            row, col = i // self.__width, i % self.__width
            if self.__minesweeper.is_flag(row, col):
                boutton["image"] = self.__image_drapeau
            elif self.__minesweeper.is_hidden(row, col):
                boutton["image"] = self.__image_cache
            else:
                boutton["image"] = self.__images[self.__minesweeper.value(row, col)]
                
    def create_flag_management_control(self, row, col):
        """int, int -> Fonc
        Retourne une fonction"""
        def flag_management_control(event):
            if self.__minesweeper.is_hidden(row, col):
                if self.__minesweeper.is_flag(row, col):
                    self.__minesweeper.remove_flag(row, col)
                else:
                    self.__minesweeper.lay_flag(row, col)
                self.redraw()
        return flag_management_control

                
if __name__ == "__main__" :
    dem = MinesweeperView(Minesweeper.Minesweeper())