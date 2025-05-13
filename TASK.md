# Tasks for rich-ctl

## Text Shaping
- [*] FR-1: Normalize input text to NFC
- [*] FR-2: Use HarfBuzz to map input string → list of (cluster_text, advance_px)
- [*] TS-1: Implement proper font loading for HarfBuzz shaping
- [*] TS-2: Add font discovery for system fonts

## Width Measurement
- [*] FR-3: Convert advance_px → cell_count given a configurable cell_width_px
- [*] FR-4: Expose override hook for custom cell mappings

## Rich/Textual Patching
- [*] FR-5: Override rich.segment.Segment.measure_cell to use cluster-aware widths
- [x] FR-6: Ensure line-wrapping in Text.render occurs only at cluster boundaries

## Bidi Support (Optional)
- [ ] FR-7: Integrate python-bidi to reorder RTL runs before shaping
- [ ] FR-8: Provide configuration flag bidi=True/False on Console()

## Testing & Documentation
- [*] FR-9: Unit tests for at least three scripts (Telugu, Arabic, Devanagari)
- [*] FR-10: End-to-end example CLI to demonstrate plugin behavior
- [x] FR-11: Generate API docs via Sphinx or MkDocs

## Basic Test Implementation
- [x] BT-1: Create font utility module with font loading functions
- [x] BT-2: Implement basic Telugu text shaping test
- [x] BT-3: Fix the CLI example script for testing with real text
- [x] BT-4: Create a simple demo script that compares Rich vs. rich-ctl rendering
- [x] BT-5: Fix the empty font blob in the shaping implementation
