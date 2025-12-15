"""Custom logging handler for tkinter Text widget"""
import logging
import tkinter as tk
from datetime import datetime


class TextHandler(logging.Handler):
    """Logging handler that writes to a tkinter Text widget"""

    def __init__(self, text_widget):
        """
        Initialize the handler.

        Args:
            text_widget: tkinter.Text widget to write log messages to
        """
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = 1000  # Limit number of lines to prevent memory issues

    def emit(self, record):
        """
        Emit a log record to the text widget.

        Args:
            record: logging.LogRecord to emit
        """
        try:
            # Format the log message
            msg = self.format(record)

            # Insert into text widget (must be done on the main thread)
            def append():
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, msg + '\n')

                # Auto-scroll to bottom
                self.text_widget.see(tk.END)

                # Limit number of lines
                self._trim_lines()

                self.text_widget.configure(state='disabled')

            # Schedule on main thread
            self.text_widget.after(0, append)

        except Exception:
            self.handleError(record)

    def _trim_lines(self):
        """Trim text widget to maximum number of lines"""
        try:
            # Get current line count
            line_count = int(self.text_widget.index('end-1c').split('.')[0])

            if line_count > self.max_lines:
                # Delete oldest lines
                lines_to_delete = line_count - self.max_lines
                self.text_widget.delete('1.0', f'{lines_to_delete}.0')
        except Exception:
            pass  # Ignore errors during trimming


class SimpleFormatter(logging.Formatter):
    """Simple formatter for GUI display"""

    def format(self, record):
        """
        Format the log record.

        Args:
            record: logging.LogRecord to format

        Returns:
            str: Formatted log message
        """
        # Format: [HH:MM:SS] message
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        return f"[{timestamp}] {record.getMessage()}"
