# Conway's Game of Life

An interactive implementation of Conway's Game of Life using Python and Pygame, featuring a modern UI with pattern selection, real-time drawing, and optimized simulation.

## Features

### Interactive Pattern Selection
- **3x4 grid of 12 classic patterns** including Empty, Glider, Oscillators, and complex patterns
- **Integrated card design** with pattern descriptions
- **Special Empty pattern styling** for easy identification of the drawing canvas
- **Square aesthetic** matching the cellular automaton theme

### Real-Time Simulation
- **High-performance engine** using NumPy and SciPy convolution for efficient neighbor counting
- **Toroidal topology** - edges wrap around for seamless simulation
- **Variable speed control** - 1-60 FPS with comfortable 10 FPS default
- **Smooth zoom and pan** - 0.1x to 3.0x zoom with viewport culling

### Drawing & Interaction
- **Live drawing/erasing** on paused simulation
- **Pattern switching** during runtime via "New Pattern" button
- **Camera controls** with mouse pan and zoom
- **Intuitive UI** with square buttons and clean typography

## Quick Start

### Requirements
- Python 3.7+
- Virtual environment (recommended)

### Installation & Running

**Easy way (recommended):**
```bash
python run.py
```
The launcher script automatically handles virtual environment setup, dependency installation, and error handling.

**Manual way:**
```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py
```

## Controls

### Mouse Controls
- **Left Click + Drag** - Draw live cells (only when paused)
- **Right Click + Drag** - Pan the view

### Keyboard Controls
- **Space Bar** - Toggle pause/play simulation
- **R Key** - Clear grid to empty state

### UI Controls
- **Start/Stop Button** - Toggle simulation state
- **Clear Button** - Clear all cells
- **New Pattern Button** - Open pattern selection screen
- **Draw/Erase Button** - Toggle between drawing and erasing cells
- **Speed Slider** - Adjust simulation speed (1-60 FPS)
- **Zoom Slider** - Adjust zoom level (0.1x-3.0x)

## Available Patterns

### Still Life Patterns
- **Empty** - Blank canvas for manual drawing
- **Block** - Simple 2x2 still life
- **Loaf** - Common 4x4 still life

### Oscillators
- **Blinker** - Simple period-2 oscillator
- **Toad** - Period-2 oscillator
- **Beacon** - Period-2 oscillator
- **Pulsar** - Period-3 oscillator
- **Pentadecathlon** - Period-15 oscillator

### Traveling Patterns
- **Glider** - Moves diagonally across the grid

### Complex Patterns
- **Gosper Gun** - First discovered infinite growth pattern that produces gliders
- **Diehard** - Vanishes completely after exactly 130 generations
- **Acorn** - Takes 5206 generations to stabilize into 633 cells

## Technical Details

### Architecture
- **MVC Pattern** with clean separation of concerns
- **NumPy-optimized simulation** using 2D convolution for neighbor counting
- **Pygame rendering** with viewport culling and coordinate system management
- **Event-driven UI** with responsive controls

### Performance
- **Vectorized operations** for entire grid updates
- **Memory efficient** using uint8 arrays
- **Smooth rendering** with only visible cells drawn
- **Real-time controls** with immediate feedback

### Dependencies
- `pygame` - Graphics and UI
- `numpy` - Grid operations and simulation
- `scipy` - Convolution optimization

## Development

The codebase is well-documented and follows clean architecture principles:

- `main.py` - Main game loop and UI orchestration
- `game/grid.py` - Core simulation logic
- `game/patterns.py` - Pattern definitions and metadata
- `game/ui_elements.py` - UI components (Button, Slider, PatternCard)
- `game/pattern_selection.py` - Pattern selection screen
- `game/config.py` - Configuration constants

## License

MIT License - see LICENSE file for details.

## About Conway's Game of Life

Created by mathematician John Conway in 1970, the Game of Life is a cellular automaton that demonstrates how complex behaviors can emerge from simple rules:

1. **Birth** - Dead cell with exactly 3 neighbors becomes alive
2. **Survival** - Live cell with 2 or 3 neighbors stays alive  
3. **Death** - Live cell with fewer than 2 or more than 3 neighbors dies

Despite these simple rules, the Game of Life exhibits fascinating emergent behaviors including stable patterns, oscillators, and even patterns that can simulate universal computation.