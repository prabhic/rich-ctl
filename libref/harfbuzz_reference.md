# HarfBuzz and Complex Text Layout Reference

This document provides reference information about HarfBuzz and Complex Text Layout (CTL) concepts relevant to the rich-ctl project.

## Table of Contents

1. [HarfBuzz Basics](#harfbuzz-basics)
2. [Complex Text Layout Concepts](#complex-text-layout-concepts)
3. [Common Scripts and Their Challenges](#common-scripts-and-their-challenges)
4. [Python Bindings for HarfBuzz](#python-bindings-for-harfbuzz)
5. [Integration Strategy](#integration-strategy)

## HarfBuzz Basics

HarfBuzz is an OpenType text shaping engine. It is used to convert a sequence of Unicode input into properly positioned glyph output, taking into account the complex rules for positioning and substitution in different writing systems.

### Key Components

#### Buffer

The buffer is the primary object in HarfBuzz that holds text and processes it:

```python
# Creating a buffer
buf = hb.Buffer()
buf.direction = "ltr"  # or "rtl", "ttb", "btt"
buf.script = "latn"    # ISO 15924 script tag
buf.language = "en"    # ISO 639 language tag
buf.add_str("Hello")   # Add text to the buffer
```

#### Face and Font

The font object represents a font file and its capabilities:

```python
# Loading a font
blob = hb.Blob(font_data)  # font_data is the binary content of a font file
face = hb.Face(blob)
font = hb.Font(face)
```

#### Shaping

The core operation in HarfBuzz is shaping, which converts text to glyph positions:

```python
# Shaping text
hb.shape(font, buf)
infos = buf.glyph_infos      # Glyph IDs and cluster information
positions = buf.glyph_positions  # X and Y positioning information
```

## Complex Text Layout Concepts

### Grapheme Clusters

Grapheme clusters are user-perceived characters that may consist of multiple Unicode code points:

- Example: "é" can be represented as `U+0065 U+0301` (e + combining acute accent)
- In CTL, a grapheme cluster is considered the atomic unit for selection, deletion, etc.

### Combining Marks

Combining marks are characters that modify the appearance of preceding characters:

- They include diacritics, vowel marks, and other modifiers
- In Indic scripts, they can appear above, below, or around base characters

### Ligatures

Ligatures are single glyphs that represent multiple characters:

- Common in Latin (fi, fl) but essential in Arabic and many other scripts
- Requires tracking which input characters map to which output glyphs

### Reordering

Some scripts require reordering of characters for proper display:

- Arabic and Hebrew display right-to-left (RTL)
- Indic scripts often reorder vowel marks and consonants

## Common Scripts and Their Challenges

### Arabic

- Contextual shaping: Characters change form based on their position
- Right-to-left direction
- Mandatory ligatures

### Indic Scripts (Devanagari, Telugu, Tamil, etc.)

- Complex character clusters with consonants and vowel marks
- Consonant stacking (conjuncts)
- Reordering of vowel marks

### Hebrew

- Right-to-left direction
- Combining marks for vowels (niqqud)

## Python Bindings for HarfBuzz

The rich-ctl project uses `uharfbuzz`, a Python binding for HarfBuzz:

```python
import uharfbuzz as hb

# Create a buffer
buf = hb.Buffer()
buf.direction = "ltr"
buf.script = "deva"  # Devanagari
buf.language = "hi"  # Hindi
buf.add_str("हिन्दी")  # "Hindi" in Hindi

# Load font
with open("path/to/font.ttf", "rb") as f:
    font_data = f.read()
blob = hb.Blob(font_data)
face = hb.Face(blob)
font = hb.Font(face)

# Shape text
hb.shape(font, buf)

# Get results
glyph_infos = buf.glyph_infos
glyph_positions = buf.glyph_positions

# Process results
for info, pos in zip(glyph_infos, glyph_positions):
    glyph_id = info.codepoint
    cluster = info.cluster
    x_advance = pos.x_advance
    y_advance = pos.y_advance
    x_offset = pos.x_offset
    y_offset = pos.y_offset
```

## Integration Strategy

For rich-ctl, we need to:

1. **Normalize text**: Convert to NFC form
2. **Shape text**: Use HarfBuzz to get proper glyph positions
3. **Map to clusters**: Group shaped glyphs into logical clusters
4. **Calculate widths**: Convert glyph advances to terminal cell counts
5. **Patch Rich**: Override cell length calculations with our cluster-aware measurements

### Key Functions in rich-ctl

```python
def shape_text(text: str, script: str = None) -> List[Cluster]:
    """
    Shape text using HarfBuzz and return a list of clusters with advance widths.
    """
    # 1. Normalize text
    normalized = unicodedata.normalize('NFC', text)
    
    # 2. Create HarfBuzz buffer
    buf = hb.Buffer()
    buf.direction = "ltr"  # or detect from script
    buf.script = script or detect_script(text)
    buf.language = "en"    # or detect from script
    buf.add_str(normalized)
    
    # 3. Load and use appropriate font
    font = get_font_for_script(script)
    
    # 4. Shape text
    hb.shape(font, buf)
    
    # 5. Map glyph information to clusters
    clusters = []
    # ... process buf.glyph_infos and buf.glyph_positions ...
    
    return clusters

def px_to_cells(advance_px: int, cell_width_px: int = 8) -> int:
    """
    Convert pixel advance to terminal cell count.
    """
    return math.ceil(advance_px / cell_width_px)
```
