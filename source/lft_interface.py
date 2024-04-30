"""GUI for life_for_two"""

import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from life_for_two import *


def on_closing():
    """terminates the program whenever the user closes a window"""
    sys.exit()


def close_window():
    """called when pressing the "CONTINUE" button, validates input"""
    try:
        # try block, fails if the user has entered a string 
        height, width = height_var.get(), width_var.get()
        if height % 1 == 0 and width % 1 == 0:
            if MIN_DIMENSION <= height <= MAX_DIMENSION and MIN_DIMENSION <= width <= MAX_DIMENSION:
                game_settings.destroy()
                return
    except:
        pass
    # is displayed both in the case of an exception or invalid input
    messagebox.showwarning("Invalid Input", f"Please enter numbers between {MIN_DIMENSION} and {MAX_DIMENSION}.")
    height_var.set(MIN_DIMENSION)
    width_var.set(MIN_DIMENSION)


def create_grid(field, field_width, field_height, grid, starting_cells, play_button):
    """Creates an interactive grid of cells"""
    for i in range(field_height):
        for j in range(field_width):
            x1, y1 = j*CELL_SIZE, i*CELL_SIZE
            x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE

            id = grid.create_rectangle(x1, y1, x2, y2, fill=GRAY_COLOR, activeoutline="gray40", outline=GRAY_BORDER)
            # sets up a mouse click event for the square, uses lambda to pass more variables to the select cells function
            grid.tag_bind(id, '<Button-1>', lambda event, j=j, i=i, id=id: 
                select_cell(event, j, i, id, field, grid, starting_cells, play_button))


def end_game(event):
    """uses a global variable to end the game by triggering evaluation in render_field function"""
    global end_flag
    end_flag = True


def render_field(field, field_height, field_width, edge_wrapping, 
                 default_rules, grid, game_window, powerups):
    """renders the field using tkinter's after method, which calls the function after a set delay"""
    reds_rules, blues_rules = default_rules, default_rules
    for powerup in powerups:
        if powerup.active_red > 0:
            reds_rules = powerup
        if powerup.active_blue > 0:
            blues_rules = powerup

        powerup = count_down(powerup)

    field, red_count, blue_count = update_field(field, edge_wrapping, field_height,
                                                field_width, reds_rules, blues_rules, grid)

    if 0 in [red_count, blue_count] or end_flag:
        evaluate(red_count, blue_count, game_window)
        return

    # Using lambda keyword again to be able to pass more variable to the function
    game_window.after(REFRESH_RATE, lambda: render_field(field, field_height, field_width, edge_wrapping, 
                                                         default_rules, grid, game_window, powerups))
    

def start_game():
    """called when pressing the "PLAY" button, exits cell selecting and starts the game"""
    play_button.destroy()

    # removes highlight on hover for every square in canvas
    for id in range(1, field_height*field_width+1):
        grid.itemconfig(id, activeoutline="")

    for row, powerup in enumerate(GameRules.powerups):
        # adds a label and a progress bar for both players for each buff
        powerup.red_label.grid(row=row, column=0)
        powerup.progress_bar_red.grid(row=row, column=1, sticky='w')
        powerup.blue_label.grid(row=row, column=2, sticky='e')
        powerup.progress_bar_blue.grid(row=row, column=3)
        
        # binds the respective key for each power-up
        game_window.bind(powerup.key_red, lambda event:
                     activate_powerup(event, GameRules.powerups))
        game_window.bind(powerup.key_blue, lambda event:
                     activate_powerup(event, GameRules.powerups))
    
    render_field(field, field_height, field_width, edge_wrapping, 
                 default_rules, grid, game_window, GameRules.powerups)


game_settings = tk.Tk()
screen_width = game_settings.winfo_screenwidth()
screen_height = game_settings.winfo_screenheight()
game_settings.title("Game Settings")
game_settings.geometry(f"849x849+{(screen_width-849)//2}+{(screen_height-949)//2}")
game_settings.resizable(False, False)

bg_image = PhotoImage(file="bg_edited.png")
background = tk.Label(game_settings, image=bg_image)
background.place(x=0, y=0, relwidth=1, relheight=1)

width_label = tk.Label(game_settings, text="Field Width: ")
width_var = tk.DoubleVar()
width = tk.Spinbox(game_settings, from_=MIN_DIMENSION,
                   to=MAX_DIMENSION, textvariable=width_var, relief="solid")
width_label.place(anchor="center", x=357, y=350)
width.place(anchor="center", x=465, y=350)

height_label = tk.Label(game_settings, text="Field Height: ")
height_var = tk.DoubleVar()
height = tk.Spinbox(game_settings, from_=MIN_DIMENSION,
                    to=MAX_DIMENSION, textvariable=height_var, relief="solid")
height_label.place(anchor="center", x=355, y=400)
height.place(anchor="center", x=465, y=400)

edge_wrap_var = tk.BooleanVar()
edge_wrap_var.set(True)
checkbox = tk.Checkbutton(
    game_settings, text="Edge Wrapping", variable=edge_wrap_var, relief="solid")
checkbox.place(anchor="center", relx=0.5, y=450)

cells_label = tk.Label(game_settings, bg="white", text="Starting Cells: ")
starting_cells_var = tk.IntVar()
starting_cells_var.set(5)
combobox = ttk.Combobox(game_settings, state="readonly",
                        textvariable=starting_cells_var)
combobox["values"] = (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
cells_label.place(anchor="center", x=352, y=500)
combobox.place(anchor="center", x=468, y=500)

continue_button = tk.Button(game_settings, text="CONTINUE", fg="white", bg="green", relief="solid",
                            activebackground="darkgreen", activeforeground="gray80",
                            pady=10, padx=10, font=("MS Sans Serif", 12), command=close_window)
continue_button.place(anchor="center", relx=0.5, y=570)

game_settings.protocol("WM_DELETE_WINDOW", on_closing)
game_settings.mainloop()


field_height, field_width, edge_wrapping, starting_cells, field = get_input(height_var, width_var,
                                                                            edge_wrap_var, starting_cells_var)


game_window = tk.Tk()
game_window.title("Life for Two")
game_window.resizable(False, False)
window_width, window_height = field_width*CELL_SIZE, field_height*CELL_SIZE
game_window.geometry(f"+{(screen_width-window_width)//2}+{(screen_height-window_height-100)//2}")

grid = tk.Canvas(game_window, width=window_width, height=window_height,
                   highlightbackground=GRAY_COLOR, highlightthickness=1, relief="flat")
grid.pack()

play_button = tk.Button(game_window, text="PLAY!", command=start_game, fg="white", bg="green",
                        relief="solid", activebackground="darkgreen", activeforeground="gray80",
                        pady=10, padx=10, font=("MS Sans Serif", 12),)

create_grid(field, field_width, field_height, grid, starting_cells, play_button)

powerup_frame = tk.Frame(game_window, bg=GRAY_COLOR)
powerup_frame.columnconfigure(1, weight=1)
powerup_frame.columnconfigure(2, weight=1)
powerup_frame.pack(fill="x", expand=True)

# defines default game rules and buffs
default_rules = GameRules((2, 3), (3,), None, None, None, None, None, None, None)
amoeba_powerup = GameRules((1, 3, 5, 8), (3, 5, 7), "q", "i", 3, 15, 10, 10, powerup_frame)
gnarl_powerup = GameRules((1,), (1,), "w", "o", 2, 30, 20, 20, powerup_frame)
explode_powerup = GameRules((2, 3, 5, 6, 7, 8), (3, 7), "e", "p", 3, 20, 20, 20, powerup_frame)

game_window.bind("<Escape>", end_game)
game_window.protocol("WM_DELETE_WINDOW", on_closing)
game_window.mainloop()
