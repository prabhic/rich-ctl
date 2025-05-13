"""
Rendering helpers for rich-ctl.

This module provides functions to improve the rendering of complex scripts in terminals.
"""

import re
import unicodedata
from typing import Dict, List, Optional, Tuple, Set

# Scripts that typically require complex text layout
COMPLEX_SCRIPTS = {
    'Deva',  # Devanagari
    'Telu',  # Telugu
    'Taml',  # Tamil
    'Beng',  # Bengali
    'Gujr',  # Gujarati
    'Khmr',  # Khmer
    'Knda',  # Kannada
    'Laoo',  # Lao
    'Mlym',  # Malayalam
    'Mymr',  # Myanmar
    'Thai',  # Thai
    'Arab',  # Arabic
    'Hebr',  # Hebrew
}

# Zero-width joiner and non-joiner
ZWJ = '\u200D'
ZWNJ = '\u200C'

def get_script(char: str) -> str:
    """
    Get the Unicode script for a character.
    
    Args:
        char: A single character.
        
    Returns:
        The Unicode script name.
    """
    if not char:
        return 'Unknown'
    try:
        # Get the script for the character
        script = unicodedata.name(char).split()[0]
        return script
    except (ValueError, IndexError):
        return 'Unknown'

def needs_complex_rendering(text: str) -> bool:
    """
    Determine if text requires complex rendering.
    
    Args:
        text: The text to check.
        
    Returns:
        True if the text contains scripts that need complex rendering.
    """
    if not text:
        return False
    
    # Check if text is pure ASCII
    if text.isascii():
        return False
    
    # Check for scripts that need complex rendering
    for char in text:
        script = get_script(char)
        if script in COMPLEX_SCRIPTS:
            return True
    
    return False

def insert_spacing(text: str) -> str:
    """
    Insert spacing between characters to improve rendering of complex scripts.
    
    Args:
        text: The text to process.
        
    Returns:
        Text with spacing inserted.
    """
    if not needs_complex_rendering(text):
        return text
    
    # Insert thin spaces between characters for complex scripts
    # This is a simple approach - could be refined based on script-specific rules
    result = []
    for char in text:
        result.append(char)
        script = get_script(char)
        if script in COMPLEX_SCRIPTS:
            # Add a thin space after each complex script character
            # This helps prevent overlapping
            result.append('\u200A')  # Hair space
    
    return ''.join(result)

def improve_rendering(text: str) -> str:
    """
    Apply various techniques to improve the rendering of complex scripts.
    
    Args:
        text: The text to process.
        
    Returns:
        Text with improved rendering properties.
    """
    if not text or text.isascii():
        return text
    
    # Normalize to NFC
    text = unicodedata.normalize('NFC', text)
    
    # Insert spacing for better rendering
    text = insert_spacing(text)
    
    return text
