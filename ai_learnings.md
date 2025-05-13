# AI Learnings for rich-ctl

This document captures best practices, insights, and lessons learned during development.

## 1. Correct Attribute Names for Rich Library Integration
**Context:** Error when running demo.py due to incorrect Rich API attribute name  
**Incorrect:**
```python
_original_measure_cell = Segment.cell_len
# ...
Segment.cell_len = staticmethod(_patched_measure_cell)
```

**Correct:**
```python
_original_measure_cell = Segment.cell_length
# ...
Segment.cell_length = staticmethod(_patched_measure_cell)
```

**Best-Practice:**
1. Verify API attribute names directly from the library's source code or documentation
2. When monkey-patching external libraries, be extra careful about exact method and attribute names
3. Use IDE autocomplete or inspect library objects to confirm attribute names

**Refs:** Rich Segment class API, PR #1

## 2. Proper Usage of functools.lru_cache with Monkey Patching
**Context:** TypeError when running demo.py: "unsupported operand type(s) for +: 'int' and 'functools._lru_cache_wrapper'"  
**Incorrect:**
```python
@functools.lru_cache(maxsize=1024)
def _patched_measure_cell(text: str) -> int:
    # function implementation
    return get_cluster_width(text)

# Later in the code
Segment.cell_length = staticmethod(_patched_measure_cell)
```

**Correct:**
```python
# Define a function to calculate cell width with caching
_cached_get_cluster_width = functools.lru_cache(maxsize=1024)(get_cluster_width)

def _patched_measure_cell(text: str) -> int:
    # function implementation
    return _cached_get_cluster_width(text)

# Later in the code
Segment.cell_length = staticmethod(_patched_measure_cell)
```

**Best-Practice:**
1. When monkey-patching methods that will be used in calculations, apply lru_cache to the underlying function, not to the patched method itself
2. Decorated functions return wrapper objects that may not behave as expected in arithmetic operations
3. Test thoroughly when combining decorators with module/class attribute assignment

## 3. Using Proper Function Closure for Method Patching
**Context:** TypeError when running demo.py: "unsupported operand type(s) for +: 'int' and 'function'"  
**Incorrect:**
```python
# Directly assigning a function to a class method
def _patched_measure_cell(text: str) -> int:
    if not text or text.isascii():
        return _original_measure_cell(text)
    return get_cluster_width(text)

Segment.cell_length = staticmethod(_patched_measure_cell)
```

**Correct:**
```python
# Create a closure to properly capture the original method
def _get_patched_cell_length() -> Callable:
    # Keep a reference to the original function
    original_fn = _original_cell_length
    
    # Create a new function that delegates to our implementation
    def patched_cell_length(text_input: str) -> int:
        if not text_input or text_input.isascii():
            return original_fn(text_input)
        return get_cluster_width(text_input)
    
    return patched_cell_length

# Patch with the result of the function, not the function itself
Segment.cell_length = staticmethod(_get_patched_cell_length())
```

**Best-Practice:**
1. When monkey-patching methods, use closures to properly capture and maintain references to original functionality
2. Return the actual function from your factory function, not just a reference to another function
3. Test patched methods in the actual context they'll be used in (e.g., with other library code that uses them)

## 4. Understanding Library Internals Before Patching
**Context:** Continued TypeError when running demo.py even after proper closure techniques  
**Incorrect:**
```python
# Trying to patch at the class attribute level
_original_cell_length = Segment.cell_length

# Later in the code
Segment.cell_length = staticmethod(_get_patched_cell_length())
```

**Correct:**
```python
# Patch at the module level where the actual function is defined
_original_cached_cell_len = rich.segment.cached_cell_len

# Direct replacement with our implementation
@functools.lru_cache(maxsize=1024)
def ctl_cell_len(text: str) -> int:
    # Implementation details
    pass

# Later in the code
rich.segment.cached_cell_len = ctl_cell_len
```

**Best-Practice:**
1. Inspect library internals thoroughly before attempting to monkey patch
2. Target the actual function at its module level rather than class attributes that might be using descriptors
3. Use inspection tools to understand how the library's objects are structured before patching

<!-- 
Template for new entries:

## N. ‹Title / One‑liner›
**Context:** why it surfaced  
**Incorrect:** ‹bad‑code›  
**Correct:** ‹good‑code›  
**Best‑Practice:** 1‑3 takeaways  
**Refs:** link(s) / doc id(s)
-->
