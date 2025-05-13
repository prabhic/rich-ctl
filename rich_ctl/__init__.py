"""
rich-ctl - Complex Text Layout (CTL) support for Rich and Textual
"""

__version__ = "0.1.0"

from rich.console import Console

from .patch import install_rich_ctl
from .shape import shape_text
from .measure import px_to_cells
from .render import improve_rendering


class CTLConsole(Console):
    """
    A Rich Console with Complex Text Layout (CTL) support.
    
    This is a drop-in replacement for rich.console.Console that
    adds support for proper rendering of complex scripts like
    Indic, Arabic, Hebrew, etc.
    """
    
    def __init__(self, *args, bidi=False, improve_display=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.bidi = bidi
        self.improve_display = improve_display
        install_rich_ctl(self)
        
    def print(self, *objects, **kwargs):
        """
        Print to the console with CTL support.
        
        Args:
            *objects: Objects to print to the console.
            **kwargs: Keyword arguments passed to Console.print.
        """
        # Process objects to improve rendering if needed
        if self.improve_display:
            processed_objects = []
            for obj in objects:
                if isinstance(obj, str):
                    processed_objects.append(improve_rendering(obj))
                else:
                    processed_objects.append(obj)
            super().print(*processed_objects, **kwargs)
        else:
            super().print(*objects, **kwargs)


__all__ = ["CTLConsole", "shape_text", "px_to_cells", "install_rich_ctl"]