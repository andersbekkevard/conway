# Modern patterns.py - provides backward compatibility through PatternManager
# This file now serves as a bridge between the old hardcoded system and the new file-based system

from .pattern_manager import PatternManager

# Initialize pattern manager
_pattern_manager = PatternManager()

# Create backward compatibility dictionaries
PATTERNS = _pattern_manager.get_all_patterns()
PATTERN_INFO = _pattern_manager.get_all_pattern_info()

# Export the pattern manager for direct access
pattern_manager = _pattern_manager

# For direct access to patterns (backward compatibility)
def get_pattern(name):
    """Get pattern coordinates by name."""
    return _pattern_manager.get_pattern(name)

def get_pattern_info(name):
    """Get pattern description by name."""
    return _pattern_manager.get_pattern_info(name)

def get_patterns_by_category():
    """Get patterns organized by category."""
    return _pattern_manager.get_patterns_by_category()

def get_categories_ordered():
    """Get categories in display order."""
    return _pattern_manager.get_categories_ordered()

# Legacy pattern constants (for any remaining hardcoded references)
# These are loaded dynamically from the file-based system
EMPTY = get_pattern("empty")
GLIDER = get_pattern("glider") 
BLINKER = get_pattern("blinker")
PULSAR = get_pattern("pulsar")
PENTADECATHLON = get_pattern("pentadecathlon")
PUFFER_TRAIN = get_pattern("puffer_train")
DIEHARD = get_pattern("diehard")
LOAFER_SPACESHIP = get_pattern("loafer_spaceship")
GOSPER_GUN = get_pattern("gosper_gun")
ACORN = get_pattern("acorn")
R_PENTOMINO = get_pattern("r_pentomino")
AND_GATE = get_pattern("and_gate")