# Curses Program Port

This a port of https://github.com/cymonsgames/CymonsGames/tree/master/taipan to python-curses.

I've mostly has the game logic separated from curses with generous help from AI.

It's still a hair buggy, but it's ready to be forked for the next steps.

The next fork will be moving from curses, to textual, or some modern TUI, and then making it responsive.

## Porting Process

The Python implementation will maintain the same functionality as the original C program while following Python best practices. The port will use Python's built-in `curses` module which provides similar functionality to the C curses library.

## Running the Code

### Python Version (with Poetry)
```bash
# Install dependencies
poetry install

# Run the game
poetry run python python/taipan.py

# Or activate the virtual environment first
poetry shell
python python/taipan.py
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone <repository-url>
cd taipan-vanilla

# Install dependencies
poetry install

# Run the game
poetry run python python/taipan.py
``` 