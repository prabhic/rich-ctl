# Rich API Documentation

This document provides reference documentation for key components of the Rich library that are relevant to the rich-ctl project. This reference is particularly focused on the text rendering and width measurement components that need to be extended for Complex Text Layout (CTL) support.

## Table of Contents

1. [Rich Segment Module](#rich-segment-module)
2. [Console Module](#console-module)
3. [Text Styling and Markup](#text-styling-and-markup)
4. [Width Calculation](#width-calculation)
5. [Key Classes for CTL Integration](#key-classes-for-ctl-integration)

## Rich Segment Module

The `rich.segment` module is a core component of Rich that handles text segments with styling. This is where the width calculation for text happens.

### Key Components

#### `Segment` Class

```python
class Segment:
    """A piece of text with associated style.
    
    Args:
        text (str): A piece of text.
        style (Optional[Style]): An optional style to apply to the text.
        control (Optional[Control]): Optional control codes embedded within the text.
    """
    
    def __init__(
        self, text: str, style: Optional[Style] = None, control: Optional[Control] = None
    ) -> None:
        ...
```

#### `cell_length` Function

```python
@staticmethod
def cell_length(text: str) -> int:
    """Get the cell length of text.
    
    Args:
        text (str): A piece of text.
    
    Returns:
        int: The number of cells required to display the text.
    """
    # This is a staticmethod that calculates the cell length of text
    # This is what we need to patch for CTL support
```

#### `cached_cell_len` Function

The function we need to patch for proper CTL support:

```python
@lru_cache(maxsize=4096)
def cached_cell_len(text: str) -> int:
    """Get the cell length of text, caching results.
    
    Args:
        text (str): A piece of text.
    
    Returns:
        int: The number of cells required to display the text.
    """
    # This is a module-level function that calculates and caches cell lengths
    # Our patching strategy targets this function
```

## Console Module

The `rich.console` module provides the `Console` class, which is the main entry point for rendering text to the terminal.

### Key Components

#### `Console` Class

```python
class Console:
    """A high level console interface.
    
    Args:
        width (Optional[int]): The width of the console in characters, or None to auto-detect.
        height (Optional[int]): The height of the console in lines, or None to auto-detect.
        file (IO, optional): A file object where the console should write to. Defaults to stdout.
        color_system (Optional[str]): The color system supported by the terminal, or None to auto-detect.
        markup (bool, optional): Enable console markup. Defaults to True.
        highlight (bool, optional): Enable automatic highlighting. Defaults to True.
        record (bool, optional): Enable recording of console output. Defaults to False.
        emoji (bool, optional): Enable emoji code. Defaults to True.
        legacy_windows (bool, optional): Enable legacy Windows mode. Defaults to False.
        _environ (dict, optional): Environment variables. Defaults to os.environ.
    """
```

#### Console `print` Method

```python
def print(
    self,
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    style: Optional[StyleType] = None,
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
) -> None:
    """Print to the console.
    
    Args:
        objects: Objects to print to the console.
        sep: String to write between print data, defaults to " ".
        end: String to write at end of print data, defaults to "\\n".
        style: A style to apply to output. Defaults to None.
        justify: Justify method: "left", "center", "full", or "right". Defaults to None.
        overflow: Overflow method: "crop", "fold", or "ellipsis". Defaults to None.
        no_wrap: Disable word wrapping. Defaults to None.
        emoji: Enable emoji, or None for Console default. Defaults to None.
        markup: Enable markup, or None for Console default. Defaults to None.
        highlight: Enable highlighting, or None for Console default. Defaults to None.
        width: Width of output, or None for console width. Defaults to None.
        height: Height of output, or None for no height. Defaults to None.
        crop: Crop output to width and height. Defaults to True.
        soft_wrap: Enable soft wrapping mode. Defaults to None.
    """
```

## Text Styling and Markup

Rich provides a powerful markup system for styling text. For the rich-ctl project, we need to ensure our CTL support works with all styling features.

### Style Class

```python
class Style:
    """A terminal style with color and attributes.
    
    Args:
        color: Color for the foreground.
        bgcolor: Color for the background.
        bold: Enable bold text.
        dim: Enable dim text.
        italic: Enable italic text.
        underline: Enable underlined text.
        blink: Enable blinking text.
        blink2: Enable fast blinking text.
        reverse: Enable reversed text.
        conceal: Enable concealed text.
        strike: Enable strikethrough text.
        underline2: Enable doubly underlined text.
        frame: Enable framed text.
        encircle: Enable encircled text.
        overline: Enable overlined text.
        link: Link URL.
    """
```

## Width Calculation

Rich includes several functions for calculating the width (in terminal cells) of text, which is critical for proper formatting.

### Key Functions

#### `get_character_cell_size`

```python
def get_character_cell_size(character: str) -> int:
    """Get the cell size of a character.
    
    Args:
        character: A single character.
    
    Returns:
        The cell size of the character (1 or 2).
    """
```

#### `cell_len`

```python
def cell_len(text: str) -> int:
    """Get the number of cells required to display text.
    
    Args:
        text: Text to display.
    
    Returns:
        The number of cells required to display the text.
    """
```

## Key Classes for CTL Integration

For the rich-ctl project, these are the most important components to focus on:

1. **`rich.segment.cached_cell_len`**: The main function we need to patch for CTL support
2. **`Segment`**: The class representing a piece of text with styling
3. **`Console`**: Our main entry point for creating a CTL-aware console

### Integration Points

The key integration points for our CTL functionality are:

1. **Text Normalization**: Converting input text to NFC form
2. **Glyph Shaping**: Using HarfBuzz to properly shape complex scripts
3. **Width Calculation**: Patching Rich's width calculation to use our cluster-aware measurements
4. **Line Wrapping**: Ensuring line breaks only occur at appropriate cluster boundaries

### Example Patching Strategy

```python
# Store original function for later restoration
_original_cached_cell_len = rich.segment.cached_cell_len

# Create our CTL-aware replacement function
@functools.lru_cache(maxsize=1024)
def ctl_cell_len(text: str) -> int:
    # Fast path for ASCII text
    if not text or text.isascii():
        return _original_cached_cell_len(text)
    
    # CTL-aware width calculation for non-ASCII text
    # ... HarfBuzz shaping and measurement ...
    
    return cell_count

# Patch Rich's module-level function
rich.segment.cached_cell_len = ctl_cell_len
```

## Important Notes for rich-ctl Development

1. Any changes to the width calculation must be backward compatible with ASCII text
2. The patching should be reversible to restore original Rich behavior if needed
3. Performance is critical for this component as it's called frequently
4. Testing across different terminal environments is essential
5. Line breaking logic may need special handling for complex scripts
