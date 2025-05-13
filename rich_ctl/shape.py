"""
Text shaping module for rich-ctl.

This module uses HarfBuzz to shape Unicode text into glyph clusters with proper metrics.
"""

import unicodedata
from typing import List, Tuple, Dict, Optional

import uharfbuzz as hb

# LRU cache for shaped clusters to improve performance
from functools import lru_cache

# Import font utilities
from .fonts import get_font


class Cluster:
    """A text cluster with its advance width in pixels."""
    
    def __init__(self, text: str, advance_px: int):
        self.text = text
        self.advance_px = advance_px
    
    def __repr__(self) -> str:
        return f"Cluster(text='{self.text}', advance_px={self.advance_px})"


@lru_cache(maxsize=1024)
def shape_text(text: str, direction: str = "ltr", script: Optional[str] = None,
             language: str = "en") -> List[Cluster]:
    """Shape unicode text into glyph clusters with proper metrics.
    
    Args:
        text: The Unicode text to shape.
        direction: Text direction ('ltr' or 'rtl').
        script: Optional script tag (e.g., 'arab', 'deva', 'telu'). Auto-detected if None.
        language: Language tag (e.g., 'en', 'ar', 'hi').
    
    Returns:
        List of Cluster objects containing the shaped text with advance widths.
    """
    # Normalize text to NFC form (normalize combining marks)
    text = unicodedata.normalize('NFC', text)
    
    if not text:
        return []
    
    # TODO: Script detection if script is None
    if script is None:
        script = "latn"  # Default to Latin script
    
    # Create HarfBuzz buffer
    buf = hb.Buffer()
    buf.direction = direction
    buf.script = script
    buf.language = language
    buf.add_str(text)
    
    # Load a font using the font utilities
    # Try to find a suitable font for the given script
    try:
        # Try to find a script-specific font
        if script == "arab":
            font = get_font(font_name="NotoSansArabic") 
        elif script == "deva":
            font = get_font(font_name="NotoSansDevanagari")
        elif script == "telu":
            font = get_font(font_name="NotoSansTelugu")
        else:
            # Use a default font with Unicode coverage
            font = get_font()
    except ValueError:
        # Fall back to default font if no suitable font is found
        font = get_font()
    
    # Shape the text
    hb.shape(font, buf)
    
    # Extract glyph information
    infos = buf.glyph_infos
    positions = buf.glyph_positions
    
    # Map glyph runs back to original character clusters
    clusters = []
    current_cluster = ""
    current_advance = 0
    
    # This is a simplified implementation
    # A real implementation would need to handle cluster mapping properly
    for i, info in enumerate(infos):
        cluster_idx = info.cluster
        char = text[cluster_idx] if cluster_idx < len(text) else ''
        
        if char and i > 0 and infos[i-1].cluster != cluster_idx:
            # New cluster
            if current_cluster:
                clusters.append(Cluster(current_cluster, current_advance))
            current_cluster = char
            current_advance = positions[i].x_advance
        else:
            # Continue current cluster
            current_cluster += char if char else ''
            current_advance += positions[i].x_advance
    
    # Add the last cluster
    if current_cluster:
        clusters.append(Cluster(current_cluster, current_advance))
    
    return clusters