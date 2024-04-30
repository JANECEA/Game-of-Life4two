"""Contains essential functions and constants to run lft_interface.py"""

import tkinter as tk
from tkinter import ttk
from enum import Enum


MIN_DIMENSION = 15
MAX_DIMENSION = 35
CELL_SIZE = 25
REFRESH_RATE = 200
RED_COLOR = 'firebrick2'
BLUE_COLOR = 'deepskyblue1'
GRAY_COLOR = 'gray10'
GRAY_BORDER = 'gray20'

num_selected = 0
end_flag = False


def check_neighbours(field, edge_wrapping, field_height, field_width, y, x):
    """returns the number of RED and BLUE neighbours for the given cell"""
    red_neighbours = 0
    blue_neighbours = 0

    for coord_y in range(-1 + y, 2 + y):
        if edge_wrapping:
            coord_y = coord_y % field_height
        elif not (0 <= coord_y < field_height):
            # skips the iteration if we're reaching outside of the field
            continue

        for coord_x in range(-1 + x, 2 + x):
            if edge_wrapping:
                coord_x = coord_x % field_width
            elif not (0 <= coord_x < field_width):
                continue

            color = field[coord_y][coord_x]
            if color == CellStatus.RED:
                red_neighbours += 1
            elif color == CellStatus.BLUE:
                blue_neighbours += 1

    return red_neighbours, blue_neighbours


def new_status(status, red_neighbours, blue_neighbours, reds_rules, blues_rules):
    """determines new status of the cell based on the current rules"""
    if status == CellStatus.DEAD:
        if 0 in [blue_neighbours, red_neighbours]:
            if red_neighbours in reds_rules.born:
                return CellStatus.RED 
            if blue_neighbours in blues_rules.born:
                return CellStatus.BLUE
        # uses "born" rules of both players in case there are both RED and BLUE neighbours
        else:
            if red_neighbours + blue_neighbours in reds_rules.born + blues_rules.born:
                if red_neighbours > blue_neighbours:
                    return CellStatus.RED
                else:
                    return CellStatus.BLUE
    # removes the cell itself from the neighbour count in case it's alive
    elif status == CellStatus.RED and red_neighbours-1 in reds_rules.survive:
        return CellStatus.RED
    elif status == CellStatus.BLUE and blue_neighbours-1 in blues_rules.survive:
        return CellStatus.BLUE
    # returns dead if no conditions are met
    return CellStatus.DEAD


def update_field(field, edge_wrapping, field_height, field_width, reds_rules, blues_rules, grid):
    """updates the field along with the displayed grid"""
    red_count, blue_count = 0, 0
    # makes a new copy of the field
    new_field = [list(row) for row in field]

    for y in range(field_height):
        for x in range(field_width):

            red_neighbours, blue_neighbours = check_neighbours(field, edge_wrapping, field_height, field_width, y, x)
            cell = new_status(field[y][x], red_neighbours, blue_neighbours, reds_rules, blues_rules)
            new_field[y][x] = cell
            # converts coordinates to id (which is indexed from 1)
            id = y*field_width + x + 1
            if cell == CellStatus.RED:
                red_count += 1
                grid.itemconfig(id, fill=RED_COLOR, outline=RED_COLOR)
            elif cell == CellStatus.BLUE:
                blue_count += 1
                grid.itemconfig(id, fill=BLUE_COLOR, outline=BLUE_COLOR)
            else:
                grid.itemconfig(id, fill=GRAY_COLOR, outline=GRAY_BORDER)

    return new_field, red_count, blue_count


def get_input(height_var, width_var, edge_wrap_var, starting_cells_var):
    """extracts entered variables, and creates the field after game_settings was closed"""
    field_height = int(height_var.get())
    field_width = int(width_var.get())
    edge_wrapping = edge_wrap_var.get()
    starting_cells = starting_cells_var.get()
    # initiates the field as a nested list of DEAD cells
    field = [[CellStatus.DEAD for _ in range(field_width)] for _ in range(field_height)]

    return field_height, field_width, edge_wrapping, starting_cells, field


def select_cell(event, x, y, id, field, grid, starting_cells, play_button):
    """checks if a cell can be selected, and updates the field and the grid if it can"""
    # event is an object that has to be passed to the function in tkinter keybinds
    # uses a global variable to keep track of the number of selected cells
    global num_selected
    # allows the players to pick a cells that aren't taken
    if field[y][x] == CellStatus.DEAD and num_selected < 2*starting_cells:
        if num_selected % 2 == 0:
            grid.itemconfig(id, fill=RED_COLOR)
            field[y][x] = CellStatus.RED
        else:
            grid.itemconfig(id, fill=BLUE_COLOR)
            field[y][x] = CellStatus.BLUE

        num_selected += 1
        if num_selected >= 2*starting_cells:
            play_button.place(relx=0.5, rely=0.5, anchor="center")


def activate_powerup(event, powerups):
    """activates a powerup and deactivates other powerups for the player"""
    for powerup in powerups:
        # checks if the power-up was called and if it isn't on cooldown
        if event.char == powerup.key_red:
            if 0 == powerup.cooldown_red:
                # deactivates all power-ups before activating the called one
                for i in range(len(powerups)):
                    powerups[i].active_red = 0
                
                powerup.active_red = powerup.duration
                powerup.cooldown_red = powerup.cooldown
            return

        if event.char == powerup.key_blue: 
            if 0 == powerup.cooldown_blue:
                for i in range(len(powerups)):
                    powerups[i].active_blue = 0
                    
                powerup.active_blue = powerup.duration
                powerup.cooldown_blue = powerup.cooldown
            return


def evaluate(red_count, blue_count, game_window):
    """evaluates the current state of the field and displays the winner / draw"""
    if red_count > blue_count:
        result, result_color = "Red Won!", 'firebrick1'
    elif blue_count > red_count:
        result, result_color = "Blue Won!", 'deepskyblue'
    else:
        result, result_color = "It's a Draw!", "gray50"

    result_banner = tk.Label(game_window, text=result, bg=result_color, 
                             fg='white', font=("MS Sans Serif", 40))
    result_banner.place(relheight=0.2, relwidth=1, relx=0.5, rely=0.5, anchor='center')


def count_down(powerup):
    """updates countdowns"""
    powerup.progress_bar_red["value"] = powerup.cooldown_red
    powerup.progress_bar_blue["value"] = powerup.cooldown_blue

    if powerup.active_red > 0:
        powerup.active_red -= 1
    if powerup.active_blue > 0:
        powerup.active_blue -= 1

    if powerup.cooldown_red > 0:
        powerup.cooldown_red -= 1
    if powerup.cooldown_blue > 0:
        powerup.cooldown_blue -= 1
        
    return powerup


class CellStatus(Enum):
    DEAD = '.'
    RED = 'o'
    BLUE = 'x'


class GameRules:
    """class to manage default rules and power-ups"""
    # list of all powerups
    powerups = []
    
    def create_prog_bar(self):
        """creates a progress bar to display the cooldown of the power-up"""
        blue_style = ttk.Style()
        blue_style.theme_use('clam')
        blue_style.configure("blue.Horizontal.TProgressbar", troughcolor=GRAY_COLOR, bordercolor=GRAY_BORDER,
                             background=BLUE_COLOR, lightcolor=BLUE_COLOR, darkcolor=BLUE_COLOR)
        self.progress_bar_red = ttk.Progressbar(self.bar_placement, orient='horizontal',
                                                style="red.Horizontal.TProgressbar",
                                                mode='determinate', maximum=self.cooldown)

        red_style = ttk.Style()
        red_style.theme_use('clam')
        red_style.configure("red.Horizontal.TProgressbar", troughcolor=GRAY_COLOR, bordercolor=GRAY_BORDER,
                            background=RED_COLOR, lightcolor=RED_COLOR, darkcolor=RED_COLOR)
        self.progress_bar_blue = ttk.Progressbar(self.bar_placement, orient='horizontal',
                                                 style="blue.Horizontal.TProgressbar",
                                                 mode='determinate', maximum=self.cooldown)

        return self.progress_bar_red, self.progress_bar_blue


    def __init__(self, survive, born, key_red, key_blue, duration,
                 cooldown, cooldown_red, cooldown_blue, bar_placement):
        """initializes default rules or powerup"""
        self.survive = survive
        self.born = born
        self.key_red = key_red
        self.key_blue = key_blue
        self.duration = duration
        self.cooldown = cooldown
        self.active_red = 0
        self.active_blue = 0
        self.cooldown_red = cooldown_red
        self.cooldown_blue = cooldown_blue
        self.bar_placement = bar_placement

        if self.duration is not None:
            self.progress_bar_red, self.progress_bar_blue = GameRules.create_prog_bar(self)
            # creates labels to show keybinds
            self.red_label = tk.Label(self.bar_placement, text=f" {self.key_red.upper()}: ", 
                                      bg=GRAY_COLOR, fg='white', width=2, font="Courier")
            self.blue_label = tk.Label(self.bar_placement, text=f" {self.key_blue.upper()}: ", 
                                       bg=GRAY_COLOR, fg='white', width=2, font="Courier")
            
            self.powerups.append(self)
