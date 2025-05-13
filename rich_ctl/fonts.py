"""
Font utilities for rich-ctl.

This module provides font loading and discovery functions for HarfBuzz shaping.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional, Dict, List

import uharfbuzz as hb

# Cache for loaded fonts to avoid reloading the same font multiple times
_font_cache: Dict[str, hb.Font] = {}


def get_system_font_paths() -> List[Path]:
    """
    Get common system font directories for the current platform.
    
    Returns:
        List of Path objects to font directories
    """
    system = platform.system()
    paths = []
    
    if system == "Windows":
        # Windows font paths
        win_font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        paths.append(Path(win_font_dir))
        
    elif system == "Darwin":  # macOS
        # macOS font paths
        paths.extend([
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path.home() / "Library" / "Fonts"
        ])
        
    else:  # Linux and others
        # Common Linux font paths
        paths.extend([
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path.home() / ".fonts",
            Path.home() / ".local" / "share" / "fonts"
        ])
    
    # Return only paths that exist
    return [p for p in paths if p.exists()]


def find_font_file(font_name: str) -> Optional[Path]:
    """
    Find a font file by name in system font directories.
    
    This is a basic implementation that checks for common extensions.
    A more robust implementation would parse font metadata.
    
    Args:
        font_name: Name of the font to find (e.g., "DejaVuSans")
    
    Returns:
        Path to the font file if found, None otherwise
    """
    extensions = [".ttf", ".otf", ".ttc"]
    
    for font_dir in get_system_font_paths():
        # Check for exact name match with extensions
        for ext in extensions:
            font_path = font_dir / f"{font_name}{ext}"
            if font_path.exists():
                return font_path
            
            # Check case-insensitive
            for path in font_dir.glob(f"*{ext}"):
                if font_name.lower() in path.stem.lower():
                    return path
    
    return None


def get_bundled_font_path() -> Optional[Path]:
    """
    Get the path to a bundled font for fallback.
    
    Returns:
        Path to bundled font if available, None otherwise
    """
    # TODO: Bundle a font with the package for fallback
    # For now, try to find a common font on the system
    fallback_fonts = [
        "DejaVuSans",
        "NotoSans",
        "FreeSans",
        "Arial",
        "Helvetica"
    ]
    
    for font_name in fallback_fonts:
        font_path = find_font_file(font_name)
        if font_path:
            return font_path
            
    return None


def load_font_from_path(font_path: Path) -> hb.Font:
    """
    Load a font file into a HarfBuzz font object.
    
    Args:
        font_path: Path to the font file
    
    Returns:
        HarfBuzz font object
    
    Raises:
        ValueError: If the font cannot be loaded
    """
    try:
        # Read the font file
        with open(font_path, 'rb') as font_file:
            # Create a blob from the font data
            blob = hb.Blob(font_file.read())
            
        # Create a face from the blob
        face = hb.Face(blob)
        
        # Create a font from the face
        font = hb.Font(face)
        
        # Scale the font to a reasonable size (default to 36pt at 72dpi)
        font.scale = (36 * 64, 36 * 64)
        
        return font
    except Exception as e:
        raise ValueError(f"Failed to load font from {font_path}: {e}")


def get_font(font_path: Optional[str] = None, font_name: Optional[str] = None) -> hb.Font:
    """
    Get a HarfBuzz font object for text shaping.
    
    This function tries to load a font in the following order:
    1. From the specified path if provided
    2. By name from system fonts if provided
    3. From a bundled font as fallback
    
    Args:
        font_path: Optional path to a font file
        font_name: Optional name of a system font to find
    
    Returns:
        HarfBuzz font object
    
    Raises:
        ValueError: If no suitable font can be found or loaded
    """
    # Use cached font if available
    cache_key = str(font_path) if font_path else str(font_name)
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    # Try user-specified font path
    if font_path:
        path = Path(font_path)
        if path.exists():
            font = load_font_from_path(path)
            _font_cache[cache_key] = font
            return font
    
    # Try to find system font by name
    if font_name:
        path = find_font_file(font_name)
        if path:
            font = load_font_from_path(path)
            _font_cache[cache_key] = font
            return font
    
    # Try to find a suitable fallback font
    fallback_path = get_bundled_font_path()
    if fallback_path:
        font = load_font_from_path(fallback_path)
        _font_cache["fallback"] = font
        return font
    
    raise ValueError("No suitable font found for text shaping")


def list_available_fonts(script: Optional[str] = None) -> List[str]:
    """
    List available fonts, optionally filtering by script support.
    
    This is a basic implementation that simply checks font file names.
    A more sophisticated implementation would check actual script support
    in the font metadata.
    
    Args:
        script: Optional script tag to filter by (e.g., 'arab', 'deva')
    
    Returns:
        List of available font names
    """
    available_fonts = []
    
    # Script-specific font patterns to look for
    script_patterns = {
        "arab": ["arab", "nastaliq", "naskh"],
        "deva": ["devanagari", "deva"],
        "telu": ["telugu", "telu"],
        "taml": ["tamil", "taml"],
        "beng": ["bengali", "beng"],
    }
    
    patterns = script_patterns.get(script, []) if script else []
    
    for font_dir in get_system_font_paths():
        for ext in [".ttf", ".otf", ".ttc"]:
            for font_path in font_dir.glob(f"*{ext}"):
                font_name = font_path.stem
                
                # If filtering by script, check if font name contains any pattern
                if script and not any(p in font_name.lower() for p in patterns):
                    continue
                    
                available_fonts.append(font_name)
    
    return sorted(available_fonts)
