"""Minimal K40 Whisperer workspace mockup with a 5 mm coordinate grid.

This module defines a Tkinter based canvas that represents the working
area of a laser cutter.  The canvas draws a grid line every 5 mm so that
users can more easily align their artwork prior to sending it to the
machine.  The real project includes many more features; this file exists
solely so we can demonstrate the coordinate grid overlay requested in
this exercise.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import tkinter as tk


@dataclass
class WorkspaceConfig:
    """Configuration describing the physical workspace."""

    width_mm: float = 300.0
    height_mm: float = 200.0
    pixels_per_mm: float = 4.0
    grid_step_mm: float = 5.0

    @property
    def size_pixels(self) -> Tuple[int, int]:
        return (
            int(round(self.width_mm * self.pixels_per_mm)),
            int(round(self.height_mm * self.pixels_per_mm)),
        )


class WorkspaceCanvas(tk.Canvas):
    """Canvas that draws a millimeter grid across the workspace."""

    def __init__(self, master: tk.Misc, config: WorkspaceConfig | None = None, **kwargs) -> None:
        self.config_data = config or WorkspaceConfig()
        width_px, height_px = self.config_data.size_pixels
        defaults = dict(
            width=width_px,
            height=height_px,
            background="#f9f9f9",
            highlightthickness=0,
        )
        defaults.update(kwargs)
        super().__init__(master, **defaults)

        self._grid_tag = "workspace-grid"
        self.bind("<Configure>", self._handle_resize)
        self._draw_grid()

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def _mm_to_px(self, value_mm: float) -> float:
        return value_mm * self.config_data.pixels_per_mm

    def _draw_grid(self) -> None:
        self.delete(self._grid_tag)
        width = int(self.winfo_width())
        height = int(self.winfo_height())
        step_px = self._mm_to_px(self.config_data.grid_step_mm)

        if step_px <= 0:
            return

        # Draw vertical lines.
        x = 0
        idx = 0
        while x <= width:
            color = "#c8c8c8" if idx % 2 else "#b0b0b0"
            self.create_line(x, 0, x, height, fill=color, tags=self._grid_tag)
            idx += 1
            x = round(idx * step_px)

        # Draw horizontal lines.
        y = 0
        idx = 0
        while y <= height:
            color = "#c8c8c8" if idx % 2 else "#b0b0b0"
            self.create_line(0, y, width, y, fill=color, tags=self._grid_tag)
            idx += 1
            y = round(idx * step_px)

        # Draw axes in a darker colour to highlight the origin.
        self.create_line(0, height, width, height, fill="#5a5a5a", width=2, tags=self._grid_tag)
        self.create_line(0, 0, 0, height, fill="#5a5a5a", width=2, tags=self._grid_tag)

    # ------------------------------------------------------------------
    # Event callbacks
    # ------------------------------------------------------------------
    def _handle_resize(self, event: tk.Event[tk.Misc]) -> None:  # type: ignore[type-arg]
        self.after_idle(self._draw_grid)


class Application(tk.Tk):
    """Small demo window so the grid can be viewed manually."""

    def __init__(self) -> None:
        super().__init__()
        self.title("K40 Whisperer Workspace Mock")
        self.resizable(True, True)

        config = WorkspaceConfig()
        workspace = WorkspaceCanvas(self, config)
        workspace.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Provide a legend so it's clear the grid uses a 5 mm spacing.
        legend = tk.Label(
            self,
            text="Grid spacing: %.1f mm" % config.grid_step_mm,
            anchor="w",
        )
        legend.pack(fill=tk.X, padx=20, pady=(0, 20))


if __name__ == "__main__":
    Application().mainloop()
