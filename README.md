# [ColorSort](https://test.pypi.org/project/color-sort-game/)
Recreating the classic color sort game in Python.

## How to install?
### Method 1: Using pip
1. Install the package using pip
   ```
   pip install -i https://test.pypi.org/simple/ color-sort-game
   ```
   Note: If you are using Linux, you might have to use one of the following commands
   ```
   pip3 install -i https://test.pypi.org/simple/ color-sort-game
   pipx install -i https://test.pypi.org/simple/ color-sort-game
   ```
2. Run the game
   ```
    color-sort
   ```
### Method 2: Using source code
1. Get the code.
   You can either download the code or clone it using git.
   ```
   git clone https://github.com/jaygupta-2k/color-sort-cli.git
   ```
2. Open the directory in your terminal/move into the directory
   ```
   cd color-sort-cli
   ```
3. Install the package
   ```
   pip install .
   ```
   Note: If you are using Linux, you might have to use the following command
   ```
   pip3 install .
   ```
4. Run the game
   ```
   color-sort
   ```

## Web UI (Development)
If you want to run the game in your browser instead of the terminal:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the web server:
   ```
   python webapp.py
   ```
3. Open http://localhost:5000 in your browser.

The browser UI resets the game when you refresh the page, and you can move colors by clicking one stack (source) then another (destination).

## To-do
- [X] Write an algorithm to solve the game.
- [X] Improve hints function logic.
- [ ] Allow users to configure stack sizes or themes via CLI flags or config files.
- [ ] Add scroll to the game screen, preferably using mouse.