# Conway's Game of Life

A Python implementation of Conway's Game of Life using Pygame. This project provides a simple, interactive simulation where you can observe the evolution of cellular automata.

## Features

-   **Interactive Simulation**: Start, stop, and reset the simulation at any time.
-   **Draw Your Own Patterns**: "Paint" initial cell configurations directly onto the grid by clicking and dragging the mouse.
-   **Preset Patterns**: Load classic Game of Life patterns like the Glider or Pulsar from a configuration file.
-   **Panning and Zooming**: Navigate the grid easily with right-click panning and a smooth, screen-centered zoom slider.

## Requirements

-   Python 3.x
-   Pygame
-   NumPy

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/conway-game-of-life.git
    cd conway-game-of-life
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

Simply run the `main.py` file from your terminal:

```bash
python main.py
```

## Controls

### Mouse

-   **Left-Click + Drag**: Sets cells to "alive" when the simulation is paused. Use this to draw your starting pattern.
-   **Right-Click + Drag**: Pans the view across the grid.
-   **Zoom Slider**: Use the slider at the bottom right to zoom in and out. The zoom is centered on the screen.

### Keyboard

-   **Spacebar**: Toggles the simulation between "Start" and "Stop".
-   **R Key**: Resets the grid to a completely empty state.

## Configuration

You can change the starting pattern by editing the `config.py` file.

1.  Open `config.py`.
2.  Find the `STARTING_PATTERN` variable.
3.  Change its value to one of the following options:
    -   `"Empty"` (default)
    -   `"Blinker"`
    -   `"Toad"`
    -   `"Beacon"`
    -   `"Pulsar"`
    -   `"Glider"`

Example:
```python
# in config.py
STARTING_PATTERN = "Glider"
```

Save the file and run `main.py` to see the new pattern loaded at startup. 