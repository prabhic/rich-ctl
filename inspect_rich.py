#!/usr/bin/env python3
"""
Script to inspect Rich's Segment class implementation to better understand how to patch it.
"""

import inspect
from rich.segment import Segment
from rich.console import Console

# Create a segment
segment = Segment("Hello")

# Inspect the Segment class
print("=== Segment Class Attributes ===")
for name, value in inspect.getmembers(Segment):
    if not name.startswith('_'):
        print(f"{name}: {type(value)}")

# Inspect a Segment instance
print("\n=== Segment Instance Attributes ===")
for name, value in inspect.getmembers(segment):
    if not name.startswith('_'):
        print(f"{name}: {type(value)}")

# Inspect the cell_length attribute specifically
print("\n=== cell_length Attribute ===")
print(f"Segment.cell_length: {type(Segment.cell_length)}")
try:
    print(f"segment.cell_length: {type(segment.cell_length)}")
    print(f"segment.cell_length value: {segment.cell_length}")
except Exception as e:
    print(f"Error accessing segment.cell_length: {e}")

# Print the source code for Segment class if possible
print("\n=== Segment Source Code ===")
try:
    print(inspect.getsource(Segment))
except Exception as e:
    print(f"Couldn't get source: {e}")

# Create a test function that adds cell_length values
print("\n=== Testing Cell Length Addition ===")
def test_cell_length_addition():
    segments = [Segment("A"), Segment("B"), Segment("C")]
    try:
        total = sum(s.cell_length for s in segments)
        print(f"Total cell length: {total} (type: {type(total)})")
    except Exception as e:
        print(f"Error summing cell lengths: {e}")

test_cell_length_addition()
