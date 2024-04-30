# Programming Documentation


## File: `run.bat`
``` batch
@echo  off
cd /d %~dp0
start /min cmd /c python lft_interface.py
```
Determines the current directory of the run.bat file and runs lft_interface.py from it in a minimized command prompt window.



## File: `lft_interface.py`

GUI for the "Life for Two" program

### Code Flow
1.  Initializes the game settings window (`game_settings`) using Tkinter.
2.  Captures user input for field dimensions, edge wrapping, and starting cells.
3.  Waits for user input to close and closes the settings window when valid input is provided.
4.  Initializes the game window (`game_window`) and sets up the game grid using Tkinter Canvas.
5.  Allows users to select cells in the grid and starts the game when the play button is clicked.
6.  Defines default game rules and power-ups with their keybindings.
7.  Stops rendering and evaluates the state of the field when Escape key is hit or all cells of either color die.

### Functions

#### `on_closing()`
Terminates the program whenever the user closes a window.

#### `close_window()`
Called when pressing the "CONTINUE" button, validates input. If the input is valid, it closes the game settings window; otherwise, it displays a warning message.

#### `create_grid()`
Creates an interactive grid of cells. The grid is displayed using the Tkinter Canvas widget, and cells can be selected by clicking on them.

#### `render_field()`
Renders the field using Tkinter's `.after()` method, which calls the function after a set delay. Updates the game field based on the rules and interactions, and continues rendering until evaluation is triggered.

#### `start_game()`
Called when pressing the "PLAY" button, disables cell selecting and starts the game. Sets up power-up labels and progress bars, and binds keys for power-up activation. Also calls render_field() for the first time.



## File: `life_for_two.py`
This file contains essential functions and constants used in the `lft_interface.py` file.

### Code Flow
1.  Initializes global variables and constants for the game.
2.  Defines utility functions for checking cell neighbors, determining new cell status, and updating the game field.
3.  Defines functions for handling user input, power-up activation, and game evaluation.
4.  Creates a class `GameRules` to manage default rules and power-ups.

### Variables and Constants
-   `min_dimension`, `max_dimension`: Minimum and maximum dimensions for the game field.
-   `cell_size`: Size of each cell in the grid in pixels.
-   `refresh_rate`: Refresh rate for updating the game field.
-   `red_color`, `blue_color`: Strings representing colors in Tkinter for red and blue cells.
-   `gray_color`: String representing a color in Tkinter for dead cells.
-   `gray_border`:  String representing a color in Tkinter for the border for cells in the grid.
-   `DEAD`, `RED`, `BLUE`: Constants representing cell states in the nested list (field).
-   `num_selected`, `end_flag`: Global variables for tracking the number of selected cells and ending the game.

### Functions

#### `check_neighbours()`
Returns the number of RED and BLUE neighbours for the given cell.

#### `new_status()`
Determines the new status of a cell based on the current rules.

#### `update_field()`
Creates a copy of the current field and calls `check_neighbours()` and `new_status()` for every cell in the new field. Also updates the canvas in the process.

#### `get_input()`
Converts Tkinter variables into python ints and initializes the game field as a nested list.

#### `select_cell()`
Called when a cell is clicked on in the grid. Updates the field and the grid when certain conditions are met. Uses a global variable to keep track of the number of selected cells.

#### `activate_powerup()`
Activates a power up if it's not on cooldown and disables other powerups for the player who called it.

#### `evaluate()`
Evaluates the current state of the field based on the number of RED and BLUE cells and shows the winner / draw.

#### `count_down()`
Updates countdown along with their progress bars.

#### `end_game()`
Uses a global variable to end the game by triggering evaluation in `render_field()` function.


### Classes

#### `GameRules`
Manages default rules and power-ups along with their UI elements

#### `create_prog_bar()`
Part of the GameRules class. Creates a progress bars for each power-up.

####  `__init__()`
Initializes default rules or power-ups.
