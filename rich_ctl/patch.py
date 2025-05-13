"""
Rich/Textual patching module for rich-ctl.

This module monkey-patches Rich and Textual to use cluster-aware width measurements.
"""

import functools
import inspect
from typing import Dict, List, Optional, Tuple, Union, Callable

from rich.console import Console
from rich.segment import Segment
import rich.segment

from .shape import shape_text, Cluster
from .measure import px_to_cells, registry


# Cache for shaped clusters to avoid reshaping the same text multiple times
_cluster_cache: Dict[str, List[Cluster]] = {}


# Store original functions for later restoration
_original_cached_cell_len = rich.segment.cached_cell_len


@functools.lru_cache(maxsize=1024)
def ctl_cell_len(text: str) -> int:
    """
    Get the cell length of text, taking into account complex scripts.
    
    Args:
        text: The text to measure.
        
    Returns:
        The width in terminal cells.
    """
    # Fast path for ASCII text
    if not text or text.isascii():
        # Use the original implementation for ASCII text
        return _original_cached_cell_len(text)
    
    # Shape the text to get its pixel advance
    clusters = _cluster_cache.get(text)
    if clusters is None:
        clusters = shape_text(text)
        _cluster_cache[text] = clusters
    
    # Sum the advances of all clusters
    total_advance = sum(cluster.advance_px for cluster in clusters)
    
    # Convert to cell count
    cell_count = px_to_cells(total_advance)
    
    # Apply any custom width mappers
    return registry.get_cell_width(text, cell_count)


def patch_rich() -> None:
    """
    Apply monkey patches to Rich to support complex text layout.
    """
    # Patch the cached_cell_len function at the module level
    rich.segment.cached_cell_len = ctl_cell_len


def unpatch_rich() -> None:
    """
    Remove monkey patches from Rich, restoring original behavior.
    """
    # Restore the original cached_cell_len function
    rich.segment.cached_cell_len = _original_cached_cell_len


def install_rich_ctl(console: Optional[Console] = None, **options) -> None:
    """
    Install rich-ctl patches into Rich and/or Textual.
    
    Args:
        console: Optional Rich console to patch.
        **options: Additional configuration options.
    """
    # Apply all Rich patches
    patch_rich()
    
    # Store the original console.print method if a console is provided
    if console is not None:
        # TODO: Override console.print to ensure line-wrapping occurs only at cluster boundaries
        pass
    
    # Initialize cluster width registry with any custom mappers
    cell_width_px = options.get('cell_width_px', 8)
    
    # If bidi support is enabled, configure it
    if options.get('bidi', False):
        # TODO: Initialize bidi support
        pass