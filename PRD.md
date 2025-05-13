# Product Requirements Document (PRD) for **rich-ctl**

**Document Version:** 0.1

**Date:** 2025-05-13

**Author:** rich‑ctl Core Team

---

## 1. Executive Summary

**rich-ctl** is a lightweight Python library that extends [Rich](https://github.com/Textualize/rich) and Textual to provide **Complex Text Layout (CTL)** support—glyph shaping, grapheme cluster measurement, and optional bidi reordering—for Indic (e.g., Telugu, Devanagari), Arabic, Hebrew, and other scripts. By integrating HarfBuzz shaping and cluster-aware width logic at the application layer, `rich-ctl` enables Python TUIs to render complex scripts correctly in **any** terminal without requiring downstream hacks.

### Key Benefits

* **Immediate Value**: Works across macOS, Linux, and Windows terminals (including Alacritty, GNOME Terminal, Windows Terminal).
* **Zero Terminal Patch**: No custom emulator build required.
* **Easy Integration**: One-line drop-in replacement of `Console()`.
* **Open-Source Impact**: Provides a demonstrable path toward upstream Rich/Textual inclusion.

---

## 2. Goals & Objectives

1. **Functional**

   * Shape Unicode text into glyph clusters using HarfBuzz.
   * Measure each cluster’s advance in monospace cells.
   * Monkey‑patch Rich/Textual to use cluster widths for wrapping and alignment.
   * Provide optional bidi reordering via FriBidi or python-bidi.
2. **Non-Functional**

   * **Performance**: < 5% overhead on typical TUI workloads (caching shaped clusters).
   * **Compatibility**: Support Python 3.8+, Rich ≥ 13.0.
   * **Maintainability**: 80%+ test coverage, CI pipelines, semantic versioning.
   * **Usability**: Single import, minimal configuration.

---

## 3. Scope

### In-Scope

* Core CTL pipeline: normalize, shape, measure, patch.
* CLI helper for manual testing.
* Unit tests for Telugu, Hindi, Arabic examples.
* Documentation (README, API reference).

### Out-of-Scope (v0.x)

* Live text editing widgets.
* Full Unicode bidi algorithm implementation (only basic RTL support).
* GUI/text-image fallback in terminals via graphics protocol.

---

## 4. Stakeholders

| Role              | Name/Team              | Interest                   |
| ----------------- | ---------------------- | -------------------------- |
| Product Owner     | Prabhanjan Kumar       | Correct rendering for TUIs |
| Dev Team Lead     | \[Your Name]           | Architecture & delivery    |
| TUI Library Users | Rich/Textual community | Multi-language support     |
| QA Engineers      | Test contributors      | Reliability & performance  |

---

## 5. Functional Requirements

### 5.1 Text Shaping

* **FR-1**: Normalize input text to NFC.
* **FR-2**: Use HarfBuzz to map input string → list of `(cluster_text, advance_px)`.

### 5.2 Width Measurement

* **FR-3**: Convert `advance_px` → `cell_count` given a configurable `cell_width_px`.
* **FR-4**: Expose override hook for custom cell mappings (e.g. double-width East Asian clusters).

### 5.3 Rich/Textual Patching

* **FR-5**: Override `rich.segment.Segment.measure_cell` to use cluster-aware widths.
* **FR-6**: Ensure line-wrapping in `Text.render` occurs only at cluster boundaries.

### 5.4 Bidi Support (Optional)

* **FR-7**: Integrate `python-bidi` to reorder RTL runs before shaping.
* **FR-8**: Provide configuration flag `bidi=True/False` on `Console()`.

### 5.5 Testing & Documentation

* **FR-9**: Unit tests for at least three scripts (Telugu, Arabic, Devanagari).
* **FR-10**: End-to-end example CLI to demonstrate plugin behavior.
* **FR-11**: Generate API docs via Sphinx or MkDocs.

---

## 6. Non-Functional Requirements

* **NFR-1**: Target <20 ms shaping time for 100-character string (with caching).
* **NFR-2**: Ensure <50 KB additional install size (uHarfbuzz, regex, bidi).
* **NFR-3**: 90%+ code coverage on CI (GitHub Actions).
* **NFR-4**: Support Python 3.8–3.12 on Linux/macOS/Windows.

---

## 7. High-Level Architecture

```text
┌──────────────┐   ┌───────────┐   ┌───────────────┐   ┌─────────────┐
│ Your App     │ → │ shape.py  │ → │ measure.py    │ → │ patch.py    │
│ (Rich/Textual)│   │ (Harfbuzz)│   │ (pixels→cells)│   │ (Rich hook) │
└──────────────┘   └───────────┘   └───────────────┘   └─────────────┘
```

---

## 8. Component Descriptions

### 8.1 `shape.py`

* **Input**: Unicode `str`.
* **Process**:

  1. `unicodedata.normalize('NFC', text)`.
  2. Create HarfBuzz buffer, set direction/script.
  3. Call `hb.shape(font, buffer)` → glyph positions.
  4. Map glyph runs back to original character clusters.
* **Output**: `List[Cluster(text: str, advance_px: int)]`.

### 8.2 `measure.py`

* **Function**: `px_to_cells(advance_px: int, cell_width_px: int = 8) -> int`
* **Logic**: `ceil(advance_px / cell_width_px)`.
* **Extensibility**: hook for `east_asian_width` or custom mappings.

### 8.3 `patch.py`

* **On import**: Apply monkey-patches:

  * `Segment.measure_cell`: if cell matches a known cluster, return `cluster_cell_count`.
  * Override wrap logic in `Console.print` to respect clusters.
* **API**: `install_rich_ctl(console: Console, **options)` to patch selectively.

### 8.4 `cli.py` (Optional)

* **Command**: `rich-ctl echo [TEXT]`
* **Behavior**: Prints shaped/measured text to stdout for manual testing.

---

## 9. User Stories & Acceptance Criteria

| ID   | User Story                                                                         | Acceptance Criteria                                                         |
| ---- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| US-1 | As a Python developer, I want to print Telugu text in my Rich app without overlap. | Given `console.print("తెలుగు")`, characters render joined, non-overlapping. |
| US-2 | As a developer, I want Arabic text to display right-to-left and joined.            | With `bidi=True`, `console.print("مرحبا")` appears correctly bidi-shaped.   |
| US-3 | As a maintainer, I want high test coverage.                                        | 90%+ coverage on Linux, macOS, Windows CI pipelines.                        |
| US-4 | As a user, I want minimal performance overhead.                                    | Shaping + rendering of 1 KB text < 50 ms.                                   |

---

## 10. Roadmap & Milestones

| Milestone      | Description                                          | Due Date   |
| -------------- | ---------------------------------------------------- | ---------- |
| **v0.1-alpha** | shape.py prototype + measure.py + patch.py stubs     | 2025-05-20 |
| **v0.1-beta**  | Core pipeline + tests for Telugu + Arabic + demo     | 2025-05-30 |
| **v0.1-rc**    | Bidi support + docs + publish to PyPI                | 2025-06-10 |
| **v1.0**       | Stabilization, community feedback, release on GitHub | 2025-07-01 |

---

## 11. Dependencies

* **Python** ≥ 3.8
* **Rich** ≥ 13.0
* **uharfbuzz** or **vharfbuzz** (HarfBuzz Python binding)
* **regex** (for grapheme clustering, `\X` support)
* **python-bidi** (optional bidi)
* **pytest** for testing

---

## 12. Risks & Mitigations

| Risk                                    | Mitigation                                                 |
| --------------------------------------- | ---------------------------------------------------------- |
| HarfBuzz binding complexities           | Start with `uharfbuzz` minimal wrapper; wrap install in CI |
| Performance overhead                    | Implement LRU cache for shaped clusters                    |
| Compatibility with future Rich versions | Pin Rich dependency, subscribe to changelog                |
| Terminal shaping conflicts              | Auto-detect emulator capabilities, allow feature toggle    |

---

## 13. Glossary

* **CTL**: Complex Text Layout—shaping, reordering, positioning of non-Latin scripts.
* **Grapheme Cluster**: A user-perceived character (base + combining marks).
* **Bidi**: Bidirectional text handling (mixing LTR/RTL scripts).
* **GSUB/GPOS**: OpenType tables for glyph substitution and positioning.

---

*End of PRD.md*
