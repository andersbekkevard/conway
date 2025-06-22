# Legacy patterns.py - kept for backward compatibility
# This file maintains the old hardcoded patterns for any remaining dependencies

# Glider pattern
GLIDER = [
    (1, 0), (2, 1), (0, 2), (1, 2), (2, 2)
]

# Blinker pattern
BLINKER = [
    (0, 1), (1, 1), (2, 1)
]

# Toad pattern
TOAD = [
    (1, 0), (2, 0), (3, 0),
    (0, 1), (1, 1), (2, 1)
]

# Beacon pattern
BEACON = [
    (0, 0), (1, 0), (0, 1),
    (3, 2), (2, 3), (3, 3)
]

# Pulsar pattern
PULSAR = [
    (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
    (0, 2), (5, 2), (7, 2), (12, 2),
    (0, 3), (5, 3), (7, 3), (12, 3),
    (0, 4), (5, 4), (7, 4), (12, 4),
    (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
    (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
    (0, 8), (5, 8), (7, 8), (12, 8),
    (0, 9), (5, 9), (7, 9), (12, 9),
    (0, 10), (5, 10), (7, 10), (12, 10),
    (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12),
]

# Gosper Glider Gun pattern
GOSPER_GUN = [
    (0, 4), (0, 5), (1, 4), (1, 5),
    (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8), (13, 2), (13, 8),
    (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6), (17, 5),
    (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5),
    (24, 0), (24, 1), (24, 5), (24, 6),
    (34, 2), (34, 3), (35, 2), (35, 3)
]

# Pentadecathlon pattern
PENTADECATHLON = [
    (5, 4), (5, 5), (4, 6), (6, 6), (5, 7), (5, 8), (5, 9), (5, 10), (4, 11), (6, 11), (5, 12), (5, 13)
]

# Diehard pattern
DIEHARD = [
    (0, 1), (1, 1), (1, 2), (5, 2), (6, 0), (6, 2), (7, 2)
]

# Acorn pattern
ACORN = [
    (0, 1), (2, 0), (2, 1), (4, 1), (5, 1), (6, 1), (7, 1)
]

# Puffer Train pattern
PUFFER_TRAIN = [
    # Engine 1
    (0, 0), (2, 0), (4, 0),
    (0, 1), (4, 1),
    (4, 2),
    (3, 3), (4, 3),
    # Engine 2
    (8, 0), (10, 0), (12, 0),
    (8, 1), (12, 1),
    (12, 2),
    (11, 3), (12, 3),
    # Connection
    (6, 4), (7, 4),
    (5, 5), (6, 5), (7, 5), (8, 5),
    (6, 6), (7, 6)
]

# R-pentomino pattern
R_PENTOMINO = [
    (1, 0), (2, 0),
    (0, 1), (1, 1),
    (1, 2)
]

EMPTY = []

# A dictionary to easily access patterns by name (legacy)
PATTERNS = {
    "Empty": EMPTY,
    "Blinker": BLINKER,
    "Toad": TOAD,
    "Beacon": BEACON,
    "Pulsar": PULSAR,
    "Glider": GLIDER,
    "Gosper_Gun": GOSPER_GUN,
    "Pentadecathlon": PENTADECATHLON,
    "Diehard": DIEHARD,
    "Acorn": ACORN,
    "Puffer_Train": PUFFER_TRAIN,
    "R_Pentomino": R_PENTOMINO,
}

# Pattern metadata for documentation (legacy)
PATTERN_INFO = {
    "Empty": "Blank canvas for manual drawing",
    "Blinker": "Simple period-2 oscillator",
    "Toad": "Period-2 oscillator",
    "Beacon": "Period-2 oscillator",
    "Pulsar": "Period-3 oscillator",
    "Glider": "Traveling pattern that moves diagonally",
    "Gosper_Gun": "First discovered infinite growth pattern - produces gliders",
    "Pentadecathlon": "Period-15 oscillator",
    "Diehard": "Vanishes after exactly 130 generations",
    "Acorn": "Takes 5206 generations to stabilize into 633 cells",
    "Puffer_Train": "Moving pattern that leaves debris trail behind",
    "R_Pentomino": "Evolves for 1103 generations into complex structure",
}