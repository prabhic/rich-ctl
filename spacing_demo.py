#!/usr/bin/env python3
"""
rich-ctl Spacing Demo

This script demonstrates how character spacing can improve
the rendering of complex scripts in the terminal.
"""

import os
import sys
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table

# Add the parent directory to the path so we can import rich_ctl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich_ctl import CTLConsole
from rich_ctl.render import improve_rendering

# Sample texts in various scripts
SAMPLES = {
    "Telugu": "తెలుగు భాష",
    "Devanagari": "हिन्दी भाषा",
    "Tamil": "தமிழ் மொழி",
    "Arabic": "مرحبا بالعالم",
    "Mixed": "English, తెలుగు, हिन्दी, مرحبا"
}

def main():
    """Main entry point for the spacing demo."""
    
    # Create standard Rich console and rich-ctl console
    rich_console = RichConsole()
    
    # Print title
    rich_console.print(Panel("Character Spacing for Complex Scripts", style="bold green"))
    
    # Create a comparison table
    table = Table(title="Rendering With Spacing")
    table.add_column("Script", style="cyan")
    table.add_column("Original", style="yellow")
    table.add_column("With Spacing", style="magenta")
    
    # Add rows for each test text
    for name, text in SAMPLES.items():
        # Add a row to the table
        spaced_text = improve_rendering(text)
        table.add_row(
            name,
            text,
            spaced_text
        )
    
    # Print the table
    rich_console.print(table)
    
    # Show with rich-ctl console
    rich_console.print("\n[bold]Rich-CTL Console with improved spacing:[/bold]")
    ctl_console = CTLConsole(improve_display=True)
    
    for name, text in SAMPLES.items():
        rich_console.print(f"\n[cyan]{name}:[/cyan]")
        ctl_console.print(f"  {text}")
    
    # Show options
    rich_console.print(Panel(
        "You can disable improved spacing with:\n"
        "CTLConsole(improve_display=False)",
        title="Configuration Options",
        style="green"
    ))


if __name__ == "__main__":
    main()
