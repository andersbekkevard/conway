# File-Based Pattern System

This document describes the new file-based pattern system that replaces hardcoded patterns with a flexible, extensible configuration system.

## System Overview

The pattern system has been completely refactored from hardcoded arrays to a file-based configuration system using JSON files and RLE format support.

### Key Components

1. **PatternManager Class** (`game/pattern_manager.py`)
   - Centralized pattern loading and management
   - Supports both JSON and RLE format patterns
   - Provides category organization
   - Offers backward compatibility API

2. **Directory Structure**
   ```
   patterns/
   ├── pattern_config.json     # Main configuration
   ├── simple/                 # Beginner patterns
   │   ├── empty.json
   │   ├── glider.json
   │   ├── blinker.json
   │   └── pulsar.json
   ├── intermediate/           # Intermediate patterns
   │   ├── pentadecathlon.json
   │   ├── puffer_train.json
   │   ├── diehard.json
   │   └── loafer_spaceship.json
   └── complex/               # Advanced patterns
       ├── gosper_gun.json
       ├── acorn.json
       ├── r_pentomino.json
       └── and_gate.json
   ```

3. **Pattern Configuration** (`patterns/pattern_config.json`)
   - Defines categories and their organization
   - Specifies pattern ordering and display names
   - Maintains metadata about the pattern collection

## JSON Pattern Format

Each pattern is stored as a JSON file with metadata and coordinates:

```json
{
  "metadata": {
    "name": "Glider",
    "description": "Traveling pattern that moves diagonally",
    "category": "simple",
    "discovered_by": "John Conway",
    "period": 4,
    "speed": "c/4",
    "size": {"width": 3, "height": 3}
  },
  "pattern": {
    "coordinates": [[1, 0], [2, 1], [0, 2], [1, 2], [2, 2]],
    "rle": "bob$2bo$3o!"
  }
}
```

## RLE Format Support

The system supports Run Length Encoded (RLE) format, the standard for Conway's Game of Life patterns:

- **Header parsing**: Extracts dimensions and rules from `x = w, y = h, rule = B3/S23`
- **Pattern parsing**: Converts RLE string to coordinate arrays
- **Metadata extraction**: Reads comments and pattern information

## Category System

Patterns are organized into three complexity levels:

### Simple (Row 1)
- **empty**: Blank canvas for manual drawing
- **glider**: Basic traveling pattern
- **blinker**: Simple oscillator
- **pulsar**: Period-3 oscillator

### Intermediate (Row 2)
- **pentadecathlon**: Period-15 oscillator
- **puffer_train**: Moving pattern with debris trail
- **diehard**: Finite-life pattern (130 generations)
- **loafer_spaceship**: Modern c/7 spaceship

### Complex (Row 3)
- **gosper_gun**: Infinite growth glider gun
- **acorn**: Long evolution (5206 generations)
- **r_pentomino**: Complex evolution (1103 generations)  
- **and_gate**: Computational logic gate

## UI Integration

The pattern selection screen now displays:
- **Category labels** on the left side of each row
- **4 patterns per row** organized by complexity
- **Integrated pattern cards** with descriptions
- **Clean, organized layout** showing progression from simple to complex

## Backward Compatibility

The system maintains full backward compatibility:
- `patterns.py` now provides a bridge to the file-based system
- All existing APIs continue to work
- Legacy hardcoded references are dynamically loaded from files
- No breaking changes to existing code

## Adding New Patterns

To add a new pattern:

1. Create a JSON file in the appropriate category directory
2. Add the pattern name to `pattern_config.json`
3. The pattern will automatically appear in the selection screen

## Benefits

- **Extensibility**: Easy to add new patterns without code changes
- **Organization**: Clear categorization by complexity level
- **Maintainability**: Pattern data separated from logic code
- **Community**: JSON format enables easy pattern sharing
- **Standards**: RLE support for importing existing patterns
- **Metadata**: Rich information about each pattern's properties

This system transforms the Conway's Game of Life implementation from a static pattern collection to a dynamic, extensible pattern platform suitable for educational progression and advanced computational demonstrations.