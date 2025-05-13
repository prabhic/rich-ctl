#!/usr/bin/env python3
"""
rich-ctl Demo Script

This script demonstrates the difference between standard Rich and rich-ctl
rendering of complex scripts like Telugu, Devanagari, and Arabic.

Usage:
    python demo.py
"""

import os
import sys
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table

# Add the parent directory to the path so we can import rich_ctl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich_ctl import CTLConsole
from rich_ctl.shape import shape_text
from rich_ctl.measure import px_to_cells


def main():
    """Main entry point for the demo script."""
    
    # Create standard Rich console and rich-ctl console
    rich_console = RichConsole()
    ctl_console = CTLConsole()
    
    # Title
    rich_console.print(Panel("Rich vs. rich-ctl Rendering Comparison", style="bold green"))
    
    # Define test texts in different scripts
    test_texts = [
        ("Latin", "Hello World!", None),
        ("Telugu", "తెలుగు భాష", "telu"),
        ("Devanagari", "हिन्दी भाषा", "deva"),
        ("Arabic", "مرحبا بالعالم", "arab"),
        ("Tamil", "தமிழ் மொழி", "taml"),
        ("Mixed", "English, తెలుగు, हिन्दी, مرحبا", None),
    ]
    
    # Create a comparison table
    table = Table(title="Rendering Comparison")
    table.add_column("Script", style="cyan")
    table.add_column("Text", style="green")
    table.add_column("Normal Rich", style="yellow")
    table.add_column("rich-ctl", style="bold magenta")
    table.add_column("Clusters", style="blue")
    
    # Add rows for each test text
    for name, text, script in test_texts:
        # Shape the text to get clusters
        clusters = shape_text(text, script=script) if script else shape_text(text)
        
        # Format the cluster information
        cluster_info = ", ".join([
            f"'{c.text}':{px_to_cells(c.advance_px)}cells" for c in clusters
        ])
        
        # Add a row to the table
        table.add_row(
            name,
            text,
            text,  # Normal Rich will render this directly
            text,  # rich-ctl will render this with proper shaping
            cluster_info
        )
    
    # Print the table with rich-ctl
    ctl_console.print(table)
    
    # Show detailed shaping information
    rich_console.print("\n[bold]Detailed Shaping Information:[/bold]")
    
    for name, text, script in test_texts:
        rich_console.print(f"\n[bold cyan]{name}[/bold cyan]: {text}")
        
        # Shape the text and print detailed information
        clusters = shape_text(text, script=script) if script else shape_text(text)
        
        for i, cluster in enumerate(clusters):
            cell_width = px_to_cells(cluster.advance_px)
            rich_console.print(f"  Cluster {i+1}: '{cluster.text}' - {cluster.advance_px}px - {cell_width} cells")
    
    # Instructions for running CLI
    rich_console.print(Panel(
        "Try the CLI for more options:\n"
        "python -m rich_ctl.cli examples\n"
        "python -m rich_ctl.cli echo 'తెలుగు' --script telu --debug",
        title="CLI Examples",
        style="green"
    ))


if __name__ == "__main__":
    main()
