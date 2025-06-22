# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Conway's Game of Life - Project Context

## ⚠️ VIRTUAL ENVIRONMENT REQUIREMENTS ⚠️

**ALWAYS activate the virtual environment before running Python/pip commands:**

```bash
# Activate venv (REQUIRED FIRST STEP)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Verify activation (prompt should show (venv))
which python              # Should show path with /venv/
```

**Running the Application:**
```bash
# Easy way (recommended)
python run.py

# Manual way
source venv/bin/activate
python main.py
```

---

## Project Overview

Interactive Conway's Game of Life implementation using Pygame with a pattern selection screen, real-time drawing, zoom/pan controls, and optimized numpy-based simulation engine.

**Application Flow:**
1. Pattern selection screen (3x4 grid of 12 patterns)
2. Main simulation with drawing controls
3. Runtime pattern switching via "New Pattern" button

## Core Architecture

### Key Files
- **`main.py`** - Main game loop, UI orchestration, camera controls
- **`game/game_logic.py`** - GameController (MVC Controller)
- **`game/grid.py`** - Grid simulation (MVC Model) with numpy optimization
- **`game/config.py`** - Centralized configuration constants
- **`game/patterns.py`** - 12 predefined patterns with metadata
- **`game/ui_elements.py`** - Button, Slider, and PatternCard UI components
- **`game/pattern_selection.py`** - Interactive pattern selection screen

### Dependencies
- `pygame` - GUI and graphics
- `numpy` - Efficient grid operations  
- `scipy` - Convolution for neighbor counting

## Pattern System

### Available Patterns (3x4 Grid)
- **Still Life**: Empty (special gray), Block, Loaf
- **Oscillators**: Blinker, Toad, Beacon (period-2), Pulsar (period-3), Pentadecathlon (period-15)
- **Traveling**: Glider
- **Complex**: Gosper_Gun (infinite growth), Diehard (dies after 130 gen), Acorn (stabilizes after 5206 gen)

### Pattern Features
- **Integrated card design** - Title and description in one UI element
- **Square aesthetic** - Matches cellular automaton theme
- **Automatic centering** - All patterns center on grid when loaded
- **Special Empty styling** - Lighter gray to signify importance

## User Controls

### Drawing & Interaction
- **Left Click + Drag** - Draw/erase cells (only when paused)
- **Right Click + Drag** - Pan the view
- **Space Bar** - Toggle pause/play
- **'R' Key** - Clear grid

### UI Controls  
- **Start/Stop Button** - Toggle simulation
- **Clear Button** - Clear all cells
- **New Pattern Button** - Open pattern selection
- **Draw/Erase Button** - Toggle drawing mode
- **Speed Slider** - 1-60 FPS simulation speed
- **Zoom Slider** - 0.1x-3.0x zoom level

## Performance Features

### Simulation Engine
- **scipy convolution** - Efficient neighbor counting with `[[1,1,1],[1,0,1],[1,1,1]]` kernel
- **Toroidal topology** - Edges wrap around
- **Vectorized operations** - Entire grid updates simultaneously
- **Memory efficient** - Uses `uint8` numpy arrays

### Rendering Optimization
- **Viewport culling** - Only draws visible cells
- **Three coordinate systems** - Screen, world, and grid coordinates
- **Centered zooming** - Maintains screen center focus

## Typography & UI Design

### Font System
- **High-quality fonts** - Arial with fallbacks to system fonts
- **Consistent sizing** - Purpose-specific font sizes (button, UI label, title, etc.)
- **Antialiasing** - Crisp text rendering throughout

### Visual Design
- **Square aesthetic** - All buttons and cards use square corners
- **Grayscale palette** - Clean, minimal color scheme
- **Visual hierarchy** - Clear distinction between titles and descriptions
- **Hover effects** - Interactive feedback on all clickable elements

## Development Guidelines

### Code Style
- **MVC Architecture** - Strict separation of concerns
- **Configuration centralization** - All constants in `Config` class
- **Event-driven UI** - Components handle their own events
- **Coordinate system discipline** - Clear separation of coordinate types

### Common Tasks
- **Add patterns** - Extend PATTERNS dictionary in `patterns.py`
- **Modify UI** - Update Button/Slider/PatternCard classes in `ui_elements.py`
- **Tune performance** - Adjust constants in `config.py`
- **Change simulation** - Modify `Grid.update()` convolution method

### Testing Approach
- **Manual testing** - Run application and verify interactions
- **Pattern verification** - Test all 12 patterns load and center correctly
- **Performance monitoring** - Check FPS with complex patterns
- **UI testing** - Verify no text overlap, proper spacing, hover effects

This implementation provides a clean, performant Conway's Game of Life with modern UI design and optimized real-time simulation.