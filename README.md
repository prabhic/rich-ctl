Note: I wanted indic langauge support for python based console applications. Rich library is a great library for console applications. But it does not support complex scripts. So I created this library.
So just tryied this, project. But not solved the essental issue. I think Terminal rendering is not supporting complex scripts. Still investigation to be done what else can be done.

# rich-ctl

A lightweight Python library that extends [Rich](https://github.com/Textualize/rich) and Textual to provide **Complex Text Layout (CTL)** support for Indic, Arabic, Hebrew, and other scripts.

## Features

- **Text Shaping**: Uses HarfBuzz to properly shape complex scripts
- **Width Measurement**: Accurately measures the width of shaped text clusters
- **Rich/Textual Integration**: Monkey-patches Rich to handle CTL scripts correctly
- **Bidi Support**: Optional bidirectional text support via python-bidi

## Installation

```bash
pip install rich-ctl
```

## Quick Start

```python
from rich_ctl import CTLConsole

# Create a CTL-aware console (drop-in replacement for rich.console.Console)
console = CTLConsole()

# Print complex scripts correctly
console.print("తెలుగు")  # Telugu
console.print("हिन्दी")   # Hindi
console.print("مرحبا")    # Arabic (with bidi=True)
```

## Requirements

- Python 3.8+
- Rich 13.0+
- Dependencies: uharfbuzz, regex, python-bidi

## Terminal Rendering Limitations

It's important to understand that while rich-ctl provides correct width measurement and layout for complex scripts, the actual visual rendering quality depends on your terminal's capabilities:

- **What rich-ctl solves:** Correct allocation of space for each character, prevention of text overlap, proper width calculation

- **Terminal-dependent factors:** Glyph shaping (the actual visual form of connected letters), positioning of combining marks, and bidirectional text flow

For optimal CTL rendering, we recommend terminals with good Unicode and font support like:

- **macOS:** iTerm2 with a font that supports your target scripts
- **Linux:** Gnome Terminal, Konsole, or Kitty with appropriate fonts
- **Windows:** Windows Terminal with appropriate fonts

The core value of rich-ctl is ensuring that even when terminals can't perfectly shape text, at least each character gets the proper amount of space.

## Documentation

For detailed documentation, visit [docs](https://github.com/username/rich-ctl/docs).

## License

MIT
