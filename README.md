# Curses Program Port

This project contains a port of a C program using curses to Python using the built-in curses module.

## Project Structure

- `original_c/` - Contains the original C source code
- `python/` - Contains the Python implementation

## Porting Process

The Python implementation will maintain the same functionality as the original C program while following Python best practices. The port will use Python's built-in `curses` module which provides similar functionality to the C curses library.

## Running the Code

### C Version
```bash
cd original_c
gcc -o program program.c -lncurses
./program
```

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