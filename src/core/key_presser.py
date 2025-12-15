"""Key pressing logic with threading support"""
import keyboard
import time
import random
import threading
import logging
from queue import Queue

logger = logging.getLogger(__name__)


class KeyPresser:
    """Handles automatic key pressing in a background thread"""

    def __init__(self, keys, min_interval_minutes, max_interval_minutes, press_twice=True, status_callback=None):
        """
        Initialize key presser.

        Args:
            keys: List of key names to press
            min_interval_minutes: Minimum interval between presses (in minutes)
            max_interval_minutes: Maximum interval between presses (in minutes)
            press_twice: Whether to press each key twice
            status_callback: Optional callback function for status updates (receives message string)
        """
        self.keys = keys
        self.min_interval = min_interval_minutes * 60  # Convert to seconds
        self.max_interval = max_interval_minutes * 60  # Convert to seconds
        self.press_twice = press_twice
        self.status_callback = status_callback

        # Threading control
        self._thread = None
        self._stop_event = threading.Event()
        self._running = False

    def start(self):
        """Start the key pressing thread"""
        if self._running:
            logger.warning("Key presser already running")
            return

        self._stop_event.clear()
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Key presser started")
        self._send_status("Key presser started")

    def stop(self):
        """Stop the key pressing thread"""
        if not self._running:
            logger.warning("Key presser not running")
            return

        self._stop_event.set()
        self._running = False

        # Wait for thread to finish (with timeout)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        logger.info("Key presser stopped")
        self._send_status("Key presser stopped")

    def is_running(self):
        """
        Check if key presser is currently running.

        Returns:
            bool: True if running, False otherwise
        """
        return self._running

    def _run(self):
        """Main thread worker function"""
        try:
            # Initial delay
            logger.info("Starting in 5 seconds...")
            self._send_status("Starting in 5 seconds...")

            if self._wait_interruptible(5):
                return

            # First key press
            self._press_keys()

            # Main loop
            while not self._stop_event.is_set():
                # Calculate random interval
                interval = random.randint(int(self.min_interval), int(self.max_interval))
                minutes = interval // 60

                logger.info(f"Next key press in {minutes} minutes")
                self._send_status(f"Next key press in {minutes} minutes")

                # Wait for interval (or stop event)
                if self._wait_interruptible(interval):
                    break

                # Press keys
                self._press_keys()

        except Exception as e:
            logger.error(f"Error in key presser thread: {e}", exc_info=True)
            self._send_status(f"Error: {e}")
        finally:
            self._running = False

    def _wait_interruptible(self, seconds):
        """
        Wait for specified seconds, but can be interrupted by stop event.

        Args:
            seconds: Number of seconds to wait

        Returns:
            bool: True if interrupted, False if wait completed normally
        """
        return self._stop_event.wait(seconds)

    def _press_keys(self):
        """Press the configured keys"""
        try:
            for key in self.keys:
                keyboard.press_and_release(key)
                logger.debug(f"Pressed key: {key}")

                if self.press_twice:
                    time.sleep(1)  # Delay between presses
                    keyboard.press_and_release(key)
                    logger.debug(f"Pressed key again: {key}")

                # Small delay between different keys
                time.sleep(0.5)

            keys_str = ", ".join(self.keys)
            logger.info(f"Keys pressed: {keys_str}")
            self._send_status(f"Keys pressed: {keys_str}")

        except Exception as e:
            logger.error(f"Error pressing keys: {e}", exc_info=True)
            self._send_status(f"Error pressing keys: {e}")

    def _send_status(self, message):
        """
        Send status message via callback.

        Args:
            message: Status message string
        """
        if self.status_callback:
            try:
                self.status_callback(message)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")
