"""
Width measurement module for rich-ctl.

This module provides functions to convert pixel advances to terminal cell counts.
"""

import math
from typing import Callable, Dict, Optional


def px_to_cells(advance_px: int, cell_width_px: int = 8) -> int:
    """
    Convert pixel advance to terminal cell count.
    
    Args:
        advance_px: The pixel advance of a glyph cluster.
        cell_width_px: The width of a single terminal cell in pixels (default: 8).
    
    Returns:
        The number of terminal cells required to display the glyph cluster.
    """
    if advance_px <= 0:
        return 0
    
    # Use ceiling to ensure we allocate enough cells
    # even if the advance is slightly larger than n cells
    return math.ceil(advance_px / cell_width_px)


# Type for a custom width mapping function
WidthMapperFunc = Callable[[str, int], Optional[int]]


class WidthRegistry:
    """
    Registry for custom width mappers that can override the default px_to_cells logic.
    
    This allows for special handling of specific scripts or character classes,
    such as East Asian full-width characters.
    """
    
    def __init__(self):
        self._mappers: Dict[str, WidthMapperFunc] = {}
    
    def register(self, name: str, mapper: WidthMapperFunc) -> None:
        """
        Register a custom width mapper.
        
        Args:
            name: A unique name for the mapper.
            mapper: A function that takes (text, default_width) and returns
                   a custom width, or None to use the default width.
        """
        self._mappers[name] = mapper
    
    def get_cell_width(self, text: str, default_width: int) -> int:
        """
        Get the cell width for a text cluster, applying any custom mappers.
        
        Args:
            text: The text cluster.
            default_width: The default width in cells.
        
        Returns:
            The width in cells, possibly modified by custom mappers.
        """
        for mapper in self._mappers.values():
            custom_width = mapper(text, default_width)
            if custom_width is not None:
                return custom_width
        
        return default_width


# Singleton registry instance
registry = WidthRegistry()


# Example mapper for East Asian full-width characters
def east_asian_width_mapper(text: str, default_width: int) -> Optional[int]:
    """
    Width mapper for East Asian full-width characters.
    
    This is just a simple example - a real implementation would use unicodedata.east_asian_width
    to identify full-width characters and handle them appropriately.
    
    Args:
        text: The text cluster.
        default_width: The default width in cells.
    
    Returns:
        Double the width for East Asian full-width characters, None otherwise.
    """
    # This is a simplified implementation
    # In reality, we would check each character's east_asian_width property
    return None  # No special handling in this example


# Register the East Asian width mapper by default
# registry.register('east_asian', east_asian_width_mapper)