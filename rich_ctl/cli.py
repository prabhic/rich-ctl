"""
Command-line interface for rich-ctl.

Provides a simple CLI for demonstrating rich-ctl capabilities.
"""

import argparse
import sys
import os
from typing import List, Optional

from rich.console import Console as RichConsole

from .shape import shape_text
from .measure import px_to_cells
from .fonts import get_font, list_available_fonts
from .__init__ import CTLConsole


def echo_command(text: str, bidi: bool = False, script: Optional[str] = None, debug: bool = False) -> None:
    """
    Echo text to the console with rich-ctl rendering.
    
    Args:
        text: The text to echo.
        bidi: Whether to enable bidirectional text support.
        script: Optional script tag (e.g., 'arab', 'deva', 'telu').
        debug: Whether to print debug information.
    """
    # Create a rich-ctl console with the specified options
    ctl_console = CTLConsole(bidi=bidi)
    
    # Print the text with rich-ctl
    ctl_console.print("[bold]With rich-ctl:[/bold]")
    ctl_console.print(text)
    
    # For comparison, also show how the text would render with standard Rich
    std_console = RichConsole()
    std_console.print("\n[bold]With standard Rich:[/bold]")
    std_console.print(text)
    
    # Print debug information if requested
    if debug:
        # Shape text with the specified script
        shaped_text = shape_text(text, script=script) if script else shape_text(text)
        
        # Print debug information
        ctl_console.print("\n[bold]Debug information:[/bold]")
        ctl_console.print(f"Script: {script if script else 'auto'}")
        
        # Print information about each cluster
        for i, cluster in enumerate(shaped_text):
            cell_width = px_to_cells(cluster.advance_px)
            ctl_console.print(f"Cluster {i+1}: '{cluster.text}' - {cluster.advance_px}px - {cell_width} cells")
        
        # Print total width information
        total_px = sum(cluster.advance_px for cluster in shaped_text)
        total_cells = px_to_cells(total_px)
        ctl_console.print(f"\nTotal width: {total_px}px - {total_cells} cells")


def fonts_command(script: Optional[str] = None) -> None:
    """
    List available fonts, optionally filtering by script.
    
    Args:
        script: Optional script tag to filter by (e.g., 'arab', 'deva')
    """
    console = CTLConsole()
    fonts = list_available_fonts(script)
    
    if script:
        console.print(f"[bold]Available fonts for script '{script}':[/bold]")
    else:
        console.print("[bold]Available fonts:[/bold]")
    
    if fonts:
        for font in fonts:
            console.print(f"- {font}")
        console.print(f"\nFound {len(fonts)} fonts.")
    else:
        console.print("No matching fonts found.")


def examples_command() -> None:
    """
    Show example texts in various scripts.
    """
    console = CTLConsole()
    
    examples = [
        ("Telugu", "తెలుగు", "telu"),
        ("Hindi", "हिन्दी", "deva"),
        ("Arabic", "مرحبا", "arab"),
        ("Tamil", "தமிழ்", "taml"),
        ("Mixed", "English, తెలుగు, हिन्दी, مرحبا", None),
    ]
    
    console.print("[bold]Example texts:[/bold]")
    
    for name, text, script in examples:
        console.print(f"\n[bold]{name} ({script if script else 'mixed'}):[/bold]")
        console.print(text)


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv if None).
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = argparse.ArgumentParser(description="rich-ctl: Complex Text Layout for Rich")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Echo command
    echo_parser = subparsers.add_parser("echo", help="Echo text with rich-ctl rendering")
    echo_parser.add_argument("text", help="Text to echo")
    echo_parser.add_argument("--bidi", action="store_true", help="Enable bidirectional text support")
    echo_parser.add_argument("--script", help="Script tag (e.g., 'arab', 'deva', 'telu')")
    echo_parser.add_argument("--debug", action="store_true", help="Print debug information")
    
    # Fonts command
    fonts_parser = subparsers.add_parser("fonts", help="List available fonts")
    fonts_parser.add_argument("--script", help="Filter fonts by script tag (e.g., 'arab', 'deva')")
    
    # Examples command
    examples_parser = subparsers.add_parser("examples", help="Show example texts in various scripts")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args(argv)
    
    if args.command == "echo":
        echo_command(args.text, args.bidi, args.script, args.debug)
        return 0
    elif args.command == "fonts":
        fonts_command(args.script)
        return 0
    elif args.command == "examples":
        examples_command()
        return 0
    elif args.command == "version":
        from . import __version__
        print(f"rich-ctl version {__version__}")
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())