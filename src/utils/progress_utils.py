"""
Progress tracking utilities for data extraction tools

Provides progress bars and status updates for long-running operations.
"""
import sys
from typing import Optional, Iterator, Any
from contextlib import contextmanager
import time


class ProgressBar:
    """Simple progress bar for terminal output"""

    def __init__(
        self,
        total: int,
        prefix: str = "Progress",
        length: int = 50,
        fill: str = "█"
    ):
        """
        Initialize progress bar.

        Args:
            total: Total number of items
            prefix: Prefix text for progress bar
            length: Character length of bar
            fill: Character to use for filled portion
        """
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.current = 0
        self.start_time = time.time()

    def update(self, current: Optional[int] = None):
        """
        Update progress bar.

        Args:
            current: Current progress (if None, increment by 1)
        """
        if current is not None:
            self.current = current
        else:
            self.current += 1

        percent = min(100, (self.current * 100) // self.total)
        filled_length = (self.length * self.current) // self.total
        bar = self.fill * filled_length + '-' * (self.length - filled_length)

        # Calculate ETA
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"

        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% ({self.current}/{self.total}) {eta_str}')
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write('\n')

    def finish(self):
        """Complete the progress bar"""
        self.update(self.total)


@contextmanager
def progress_context(iterable: Iterator[Any], prefix: str = "Processing", total: Optional[int] = None):
    """
    Context manager for showing progress while iterating.

    Args:
        iterable: Items to iterate over
        prefix: Prefix text for progress bar
        total: Total number of items (if known)

    Yields:
        Items from iterable with progress tracking

    Example:
        with progress_context(files, "Processing files", len(files)) as items:
            for item in items:
                # Process item
    """
    try:
        items = list(iterable)
    except TypeError:
        # Not a list, try to get length
        items = iterable

    if total is None:
        try:
            total = len(items)
        except TypeError:
            total = 0

    if total > 0:
        progress = ProgressBar(total, prefix=prefix)

        def tracked_items():
            for item in items:
                yield item
                progress.update()

        yield tracked_items()
        progress.finish()
    else:
        # No progress bar if we don't know the total
        yield items


class Spinner:
    """Simple spinner for indeterminate progress"""

    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    def __init__(self, message: str = "Processing..."):
        """
        Initialize spinner.

        Args:
            message: Message to display with spinner
        """
        self.message = message
        self.frame_index = 0
        self.active = False

    def spin(self):
        """Update spinner frame"""
        if self.active:
            frame = self.FRAMES[self.frame_index]
            sys.stdout.write(f'\r{frame} {self.message}')
            sys.stdout.flush()
            self.frame_index = (self.frame_index + 1) % len(self.FRAMES)

    def start(self):
        """Start spinner"""
        self.active = True
        self.spin()

    def stop(self, final_message: Optional[str] = None):
        """
        Stop spinner.

        Args:
            final_message: Optional final message to display
        """
        self.active = False
        if final_message:
            sys.stdout.write(f'\r{final_message}\n')
        else:
            sys.stdout.write('\r' + ' ' * (len(self.message) + 3) + '\r')
        sys.stdout.flush()
