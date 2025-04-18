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
## To-do
- [X] Write an algorithm to solve the game.
- [X] Improve hints function logic.
- [ ] Allow users to configure stack sizes or themes via CLI flags or config files.
- [ ] Add scroll to the game screen, preferably using mouse.