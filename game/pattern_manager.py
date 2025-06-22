import json
import os
import re
from typing import Dict, List, Tuple, Optional


class RLEParser:
    """Parser for Run Length Encoded (RLE) Conway's Game of Life patterns."""
    
    @staticmethod
    def parse_rle(rle_string: str) -> List[Tuple[int, int]]:
        """
        Parse RLE format string into coordinate list.
        
        Args:
            rle_string (str): RLE encoded pattern string
            
        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinates for live cells
        """
        # Remove whitespace and split by $ (row separator) and ! (end marker)
        rle_string = rle_string.strip().replace('\n', '').replace(' ', '')
        if rle_string.endswith('!'):
            rle_string = rle_string[:-1]
        
        rows = rle_string.split('$')
        coordinates = []
        
        for y, row in enumerate(rows):
            x = 0
            i = 0
            while i < len(row):
                # Parse run count (optional)
                run_count = ""
                while i < len(row) and row[i].isdigit():
                    run_count += row[i]
                    i += 1
                
                count = int(run_count) if run_count else 1
                
                if i < len(row):
                    char = row[i]
                    if char == 'o':  # Live cell
                        for _ in range(count):
                            coordinates.append((x, y))
                            x += 1
                    elif char == 'b':  # Dead cell
                        x += count
                    i += 1
        
        return coordinates
    
    @staticmethod
    def parse_rle_header(header_line: str) -> Tuple[int, int, str]:
        """
        Parse RLE header line to extract dimensions and rule.
        
        Args:
            header_line (str): Header line like "x = 3, y = 3, rule = B3/S23"
            
        Returns:
            Tuple[int, int, str]: Width, height, and rule string
        """
        # Extract width
        x_match = re.search(r'x\s*=\s*(\d+)', header_line)
        width = int(x_match.group(1)) if x_match else 0
        
        # Extract height
        y_match = re.search(r'y\s*=\s*(\d+)', header_line)
        height = int(y_match.group(1)) if y_match else 0
        
        # Extract rule
        rule_match = re.search(r'rule\s*=\s*([A-Za-z0-9/]+)', header_line)
        rule = rule_match.group(1) if rule_match else "B3/S23"
        
        return width, height, rule


class PatternManager:
    """
    Manages loading and organization of Conway's Game of Life patterns from files.
    
    Supports JSON format patterns with metadata and RLE format parsing.
    Organizes patterns by complexity categories.
    """
    
    def __init__(self, patterns_dir: str = "patterns"):
        """
        Initialize the pattern manager.
        
        Args:
            patterns_dir (str): Directory containing pattern files
        """
        self.patterns_dir = patterns_dir
        self.patterns = {}
        self.pattern_info = {}
        self.categories = {}
        self.rle_parser = RLEParser()
        
        self.load_configuration()
        self.load_patterns()
    
    def load_configuration(self):
        """Load pattern configuration from pattern_config.json."""
        config_path = os.path.join(self.patterns_dir, "pattern_config.json")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.categories = config.get("categories", {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load pattern configuration: {e}")
            # Use default configuration
            self.categories = {
                "simple": {"display_name": "Simple", "order": 1, "patterns": []},
                "intermediate": {"display_name": "Intermediate", "order": 2, "patterns": []},
                "complex": {"display_name": "Complex", "order": 3, "patterns": []}
            }
    
    def load_patterns(self):
        """Load all patterns from category directories."""
        for category_name, category_info in self.categories.items():
            category_dir = os.path.join(self.patterns_dir, category_name)
            
            if not os.path.exists(category_dir):
                continue
            
            for pattern_name in category_info.get("patterns", []):
                self.load_pattern_file(category_name, pattern_name)
    
    def load_pattern_file(self, category: str, pattern_name: str):
        """
        Load a specific pattern file.
        
        Args:
            category (str): Pattern category (simple, intermediate, complex)
            pattern_name (str): Name of the pattern file (without extension)
        """
        # Try JSON format first
        json_path = os.path.join(self.patterns_dir, category, f"{pattern_name}.json")
        if os.path.exists(json_path):
            self.load_json_pattern(json_path, pattern_name)
            return
        
        # Try RLE format
        rle_path = os.path.join(self.patterns_dir, category, f"{pattern_name}.rle")
        if os.path.exists(rle_path):
            self.load_rle_pattern(rle_path, pattern_name)
            return
        
        print(f"Warning: Pattern file not found for {pattern_name} in {category}")
    
    def load_json_pattern(self, file_path: str, pattern_name: str):
        """
        Load pattern from JSON file.
        
        Args:
            file_path (str): Path to JSON pattern file
            pattern_name (str): Pattern name for storage
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract pattern coordinates
            coordinates = data.get("pattern", {}).get("coordinates", [])
            self.patterns[pattern_name] = [tuple(coord) for coord in coordinates]
            
            # Extract metadata
            metadata = data.get("metadata", {})
            self.pattern_info[pattern_name] = metadata.get("description", "")
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading JSON pattern {pattern_name}: {e}")
    
    def load_rle_pattern(self, file_path: str, pattern_name: str):
        """
        Load pattern from RLE file.
        
        Args:
            file_path (str): Path to RLE pattern file
            pattern_name (str): Pattern name for storage
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.strip().split('\n')
            metadata = {}
            rle_data = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('#N'):  # Name
                    metadata['name'] = line[2:].strip()
                elif line.startswith('#C'):  # Comment/Description
                    metadata['description'] = line[2:].strip()
                elif line.startswith('#O'):  # Origin/Author
                    metadata['author'] = line[2:].strip()
                elif line.startswith('x ='):  # RLE header and data
                    rle_data = line + '\n' + '\n'.join(lines[lines.index(line)+1:])
                    break
            
            # Parse RLE data
            if rle_data:
                # Extract pattern data (everything after header)
                rle_lines = rle_data.split('\n')
                pattern_data = ''.join(rle_lines[1:])  # Skip header
                coordinates = self.rle_parser.parse_rle(pattern_data)
                self.patterns[pattern_name] = coordinates
            
            # Store metadata
            self.pattern_info[pattern_name] = metadata.get('description', '')
            
        except (FileNotFoundError, Exception) as e:
            print(f"Error loading RLE pattern {pattern_name}: {e}")
    
    def get_pattern(self, name: str) -> List[Tuple[int, int]]:
        """
        Get pattern coordinates by name.
        
        Args:
            name (str): Pattern name
            
        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinates for live cells
        """
        return self.patterns.get(name, [])
    
    def get_pattern_info(self, name: str) -> str:
        """
        Get pattern description by name.
        
        Args:
            name (str): Pattern name
            
        Returns:
            str: Pattern description
        """
        return self.pattern_info.get(name, "")
    
    def get_patterns_by_category(self) -> Dict[str, List[str]]:
        """
        Get patterns organized by category.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping category names to pattern lists
        """
        result = {}
        for category_name, category_info in self.categories.items():
            result[category_name] = category_info.get("patterns", [])
        return result
    
    def get_categories_ordered(self) -> List[Tuple[str, str]]:
        """
        Get categories in display order.
        
        Returns:
            List[Tuple[str, str]]: List of (category_key, display_name) tuples
        """
        categories = []
        for cat_key, cat_info in self.categories.items():
            categories.append((cat_key, cat_info.get("display_name", cat_key.title())))
        
        # Sort by order field
        categories.sort(key=lambda x: self.categories[x[0]].get("order", 999))
        return categories
    
    def get_all_patterns(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Get all loaded patterns.
        
        Returns:
            Dict[str, List[Tuple[int, int]]]: All patterns with their coordinates
        """
        return self.patterns.copy()
    
    def get_all_pattern_info(self) -> Dict[str, str]:
        """
        Get all pattern descriptions.
        
        Returns:
            Dict[str, str]: All pattern descriptions
        """
        return self.pattern_info.copy()