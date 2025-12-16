"""Custom logging handler for tkinter Text widget"""
import logging
import tkinter as tk
from datetime import datetime
import queue
import threading


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
        # Only show INFO level and above to GUI (not DEBUG)
        self.setLevel(logging.INFO)
        # Use a queue to avoid blocking the GUI event loop
        self.msg_queue = queue.Queue()
        self.main_thread_id = threading.current_thread().ident
        # Start processing queue periodically
        self._schedule_queue_check()

    def emit(self, record):
        """
        Emit a log record to the text widget.

        Args:
            record: logging.LogRecord to emit
        """
        try:
            # Format the log message
            msg = self.format(record)
            # Add to queue without blocking
            self.msg_queue.put_nowait(msg)
        except Exception:
            self.handleError(record)

    def _schedule_queue_check(self):
        """Check the queue periodically and process messages"""
        try:
            while True:
                try:
                    msg = self.msg_queue.get_nowait()
                    self.text_widget.configure(state='normal')
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)
                    self._trim_lines()
                    self.text_widget.configure(state='disabled')
                except queue.Empty:
                    break
        except Exception:
            pass
        # Schedule next check
        self.text_widget.after(100, self._schedule_queue_check)

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
        Format the log record for user-friendly display.

        Args:
            record: logging.LogRecord to format

        Returns:
            str: Formatted log message
        """
        msg = record.getMessage()

        # Format with level indicators for warnings/errors
        if record.levelno >= logging.WARNING:
            return f"⚠ {msg}"
        else:
            return msg
