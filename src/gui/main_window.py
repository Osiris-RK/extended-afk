"""Main GUI window for Extended AFK application"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import logging
from PIL import Image, ImageTk
import os

from ..core.settings import AppSettings
from ..core.key_presser import KeyPresser
from ..utils.resource_path import get_resource_path
from .key_selector import select_key
from .text_handler import TextHandler, SimpleFormatter

logger = logging.getLogger(__name__)

# Colors matching sc-profile-editor
BG_COLOR = "#f0f0f0"
FRAME_BG = "#ffffff"
ACCENT_COLOR = "#c9a961"
TEXT_COLOR = "#333333"
BUTTON_START_COLOR = "#4CAF50"
BUTTON_STOP_COLOR = "#f44336"


class MainWindow:
    """Main application window"""

    def __init__(self, root):
        """
        Initialize the main window.

        Args:
            root: tkinter.Tk root window
        """
        self.root = root
        self.root.title("Extended AFK - Auto Key Presser")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # Settings manager
        self.settings = AppSettings()

        # Key presser (will be initialized when started)
        self.key_presser = None

        # Key list widgets (for dynamic key management)
        self.key_frames = []

        # Build UI
        self._build_ui()

        # Set up logging handler for GUI
        self._setup_logging()

        # Load initial settings
        self._load_settings()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        logger.info("Application started")

    def _build_ui(self):
        """Build the user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuration section
        self._build_configuration_section(main_container)

        # Start/Stop button
        self._build_control_button(main_container)

        # Activity log section
        self._build_log_section(main_container)

        # Footer with branding
        self._build_footer(main_container)

    def _build_configuration_section(self, parent):
        """Build the configuration section"""
        # Configuration frame
        config_frame = tk.LabelFrame(
            parent,
            text=" Configuration ",
            bg=FRAME_BG,
            font=("Segoe UI", 10, "bold"),
            relief=tk.GROOVE,
            borderwidth=2
        )
        config_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Inner padding
        config_inner = tk.Frame(config_frame, bg=FRAME_BG)
        config_inner.pack(fill=tk.BOTH, padx=10, pady=10)

        # Keys section
        keys_label = tk.Label(
            config_inner,
            text="Keys to Press:",
            bg=FRAME_BG,
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_COLOR
        )
        keys_label.pack(anchor=tk.W, pady=(0, 5))

        # Keys container (scrollable if needed)
        self.keys_container = tk.Frame(config_inner, bg=FRAME_BG)
        self.keys_container.pack(fill=tk.X, pady=(0, 10))

        # Add key button
        add_key_frame = tk.Frame(config_inner, bg=FRAME_BG)
        add_key_frame.pack(fill=tk.X, pady=(0, 15))

        self.add_key_button = tk.Button(
            add_key_frame,
            text="Add Key...",
            command=self._add_key,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=5
        )
        self.add_key_button.pack(side=tk.RIGHT)

        # Interval section
        interval_label = tk.Label(
            config_inner,
            text="Interval (minutes):",
            bg=FRAME_BG,
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_COLOR
        )
        interval_label.pack(anchor=tk.W, pady=(0, 5))

        interval_frame = tk.Frame(config_inner, bg=FRAME_BG)
        interval_frame.pack(fill=tk.X, pady=(0, 15))

        # Min interval
        tk.Label(interval_frame, text="Min:", bg=FRAME_BG, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        self.min_interval_var = tk.IntVar(value=10)
        min_spinbox = tk.Spinbox(
            interval_frame,
            from_=1,
            to=60,
            textvariable=self.min_interval_var,
            width=5,
            command=self._on_settings_changed
        )
        min_spinbox.pack(side=tk.LEFT, padx=(0, 20))

        # Max interval
        tk.Label(interval_frame, text="Max:", bg=FRAME_BG, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        self.max_interval_var = tk.IntVar(value=14)
        max_spinbox = tk.Spinbox(
            interval_frame,
            from_=1,
            to=60,
            textvariable=self.max_interval_var,
            width=5,
            command=self._on_settings_changed
        )
        max_spinbox.pack(side=tk.LEFT)

        # Press twice checkbox
        self.press_twice_var = tk.BooleanVar(value=True)
        press_twice_check = tk.Checkbutton(
            config_inner,
            text="Press each key twice",
            variable=self.press_twice_var,
            command=self._on_settings_changed,
            bg=FRAME_BG,
            fg=TEXT_COLOR,
            font=("Segoe UI", 9),
            activebackground=FRAME_BG
        )
        press_twice_check.pack(anchor=tk.W)

    def _build_control_button(self, parent):
        """Build the start/stop control button"""
        button_frame = tk.Frame(parent, bg=BG_COLOR)
        button_frame.pack(fill=tk.X, padx=5, pady=10)

        self.control_button = tk.Button(
            button_frame,
            text="START PRESSING KEYS",
            command=self._toggle_pressing,
            bg=BUTTON_START_COLOR,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=15
        )
        self.control_button.pack(fill=tk.X)

    def _build_log_section(self, parent):
        """Build the activity log section"""
        # Log frame
        log_frame = tk.LabelFrame(
            parent,
            text=" Activity Log ",
            bg=FRAME_BG,
            font=("Segoe UI", 10, "bold"),
            relief=tk.GROOVE,
            borderwidth=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Text widget with scrollbar
        text_container = tk.Frame(log_frame, bg=FRAME_BG)
        text_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(
            text_container,
            height=10,
            width=60,
            yscrollcommand=scrollbar.set,
            bg="#ffffff",
            fg="#000000",
            font=("Consolas", 9),
            state='disabled',
            wrap=tk.WORD
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

    def _build_footer(self, parent):
        """Build the footer with branding and donation links"""
        # Footer frame
        footer_frame = tk.Frame(parent, bg=BG_COLOR)
        footer_frame.pack(fill=tk.X, padx=5, pady=(10, 0))

        # Osiris DevWorks button (left)
        self._create_osiris_button(footer_frame)

        # Spacer
        tk.Frame(footer_frame, bg=BG_COLOR, width=10).pack(side=tk.LEFT)

        # Support label
        support_label = tk.Label(
            footer_frame,
            text="Support:",
            bg=BG_COLOR,
            fg="#666",
            font=("Segoe UI", 9)
        )
        support_label.pack(side=tk.LEFT, padx=(10, 5))

        # PayPal button
        self._create_paypal_button(footer_frame)

        # Spacer
        tk.Frame(footer_frame, bg=BG_COLOR, width=5).pack(side=tk.LEFT)

        # Venmo button
        self._create_venmo_button(footer_frame)

    def _create_osiris_button(self, parent):
        """Create Osiris DevWorks button"""
        try:
            # Try to load image
            image_path = get_resource_path(os.path.join("assets", "osiris-devworks.png"))
            if os.path.exists(image_path):
                img = Image.open(image_path)
                # Scale to height 40
                ratio = 40 / img.height
                new_width = int(img.width * ratio)
                img = img.resize((new_width, 40), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label = tk.Label(parent, image=photo, bg=BG_COLOR, cursor="hand2")
                label.image = photo  # Keep reference
                label.pack(side=tk.LEFT)
                label.bind("<Button-1>", lambda e: self._open_discord())
            else:
                # Fallback to text
                self._create_text_button(
                    parent,
                    "Osiris DevWorks",
                    "#1a1f2e",
                    ACCENT_COLOR,
                    self._open_discord
                )
        except Exception as e:
            logger.error(f"Failed to load Osiris image: {e}")
            self._create_text_button(
                parent,
                "Osiris DevWorks",
                "#1a1f2e",
                ACCENT_COLOR,
                self._open_discord
            )

    def _create_paypal_button(self, parent):
        """Create PayPal donation button"""
        try:
            # Try to load image
            image_path = get_resource_path(os.path.join("assets", "paypal.png"))
            if os.path.exists(image_path):
                img = Image.open(image_path)
                # Scale to height 40
                ratio = 40 / img.height
                new_width = int(img.width * ratio)
                img = img.resize((new_width, 40), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label = tk.Label(parent, image=photo, bg=BG_COLOR, cursor="hand2")
                label.image = photo  # Keep reference
                label.pack(side=tk.LEFT)
                label.bind("<Button-1>", lambda e: self._open_paypal())
            else:
                # Fallback to text
                self._create_text_button(
                    parent,
                    "PayPal",
                    "#0070ba",
                    "white",
                    self._open_paypal
                )
        except Exception as e:
            logger.error(f"Failed to load PayPal image: {e}")
            self._create_text_button(
                parent,
                "PayPal",
                "#0070ba",
                "white",
                self._open_paypal
            )

    def _create_venmo_button(self, parent):
        """Create Venmo donation button"""
        try:
            # Try to load image
            image_path = get_resource_path(os.path.join("assets", "venmo.png"))
            if os.path.exists(image_path):
                img = Image.open(image_path)
                # Scale to height 40
                ratio = 40 / img.height
                new_width = int(img.width * ratio)
                img = img.resize((new_width, 40), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label = tk.Label(parent, image=photo, bg=BG_COLOR, cursor="hand2")
                label.image = photo  # Keep reference
                label.pack(side=tk.LEFT)
                label.bind("<Button-1>", lambda e: self._open_venmo())
            else:
                # Fallback to text
                self._create_text_button(
                    parent,
                    "Venmo",
                    "#008CFF",
                    "white",
                    self._open_venmo
                )
        except Exception as e:
            logger.error(f"Failed to load Venmo image: {e}")
            self._create_text_button(
                parent,
                "Venmo",
                "#008CFF",
                "white",
                self._open_venmo
            )

    def _create_text_button(self, parent, text, bg, fg, command):
        """Create a styled text button"""
        label = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=1
        )
        label.pack(side=tk.LEFT)
        label.bind("<Button-1>", lambda e: command())

    def _setup_logging(self):
        """Set up logging to the GUI text widget"""
        # Create handler
        handler = TextHandler(self.log_text)
        handler.setLevel(logging.INFO)
        handler.setFormatter(SimpleFormatter())

        # Add to root logger
        logging.getLogger().addHandler(handler)

    def _load_settings(self):
        """Load settings and update UI"""
        # Load keys
        keys = self.settings.get('keys', [])
        for key in keys:
            self._add_key_widget(key)

        # Load intervals
        self.min_interval_var.set(self.settings.get('min_interval_minutes', 10))
        self.max_interval_var.set(self.settings.get('max_interval_minutes', 14))

        # Load press_twice
        self.press_twice_var.set(self.settings.get('press_twice', True))

    def _add_key(self):
        """Add a new key via detection dialog"""
        # Disable control during detection
        self.add_key_button.config(state='disabled')
        self.root.update()

        # Show key selection dialog
        key = select_key(self.root)

        # Re-enable control
        self.add_key_button.config(state='normal')

        if key:
            self._add_key_widget(key)
            self._on_settings_changed()

    def _add_key_widget(self, key_name):
        """
        Add a key widget to the keys container.

        Args:
            key_name: Name of the key
        """
        # Create frame for this key
        key_frame = tk.Frame(self.keys_container, bg=FRAME_BG)
        key_frame.pack(fill=tk.X, pady=2)

        # Key label
        key_label = tk.Label(
            key_frame,
            text=key_name.upper(),
            bg="white",
            fg=TEXT_COLOR,
            font=("Segoe UI", 10),
            width=10,
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=5,
            pady=3
        )
        key_label.pack(side=tk.LEFT, padx=(0, 10))

        # Delete button
        delete_button = tk.Button(
            key_frame,
            text="Delete",
            command=lambda: self._remove_key_widget(key_frame, key_name),
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=2
        )
        delete_button.pack(side=tk.LEFT, padx=(0, 10))

        # Select key button
        select_button = tk.Button(
            key_frame,
            text="Select Key...",
            command=lambda: self._replace_key(key_frame, key_name),
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=2
        )
        select_button.pack(side=tk.LEFT)

        # Store reference
        self.key_frames.append((key_frame, key_name))

    def _remove_key_widget(self, key_frame, key_name):
        """
        Remove a key widget.

        Args:
            key_frame: Frame to remove
            key_name: Key name
        """
        # Remove from list
        self.key_frames = [(f, k) for f, k in self.key_frames if f != key_frame]

        # Destroy widget
        key_frame.destroy()

        # Save settings
        self._on_settings_changed()

    def _replace_key(self, key_frame, old_key_name):
        """
        Replace a key.

        Args:
            key_frame: Frame containing the key
            old_key_name: Current key name
        """
        # Show key selection dialog
        new_key = select_key(self.root)

        if new_key:
            # Update the key name in the frame
            for widget in key_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=new_key.upper())
                    break

            # Update in key_frames list
            for i, (f, k) in enumerate(self.key_frames):
                if f == key_frame:
                    self.key_frames[i] = (f, new_key)
                    break

            # Save settings
            self._on_settings_changed()

    def _on_settings_changed(self):
        """Handle settings change"""
        # Get current keys
        keys = [k for f, k in self.key_frames]

        # Update settings
        self.settings.set('keys', keys)
        self.settings.set('min_interval_minutes', self.min_interval_var.get())
        self.settings.set('max_interval_minutes', self.max_interval_var.get())
        self.settings.set('press_twice', self.press_twice_var.get())

        logger.debug("Settings updated")

    def _toggle_pressing(self):
        """Toggle key pressing on/off"""
        if self.key_presser and self.key_presser.is_running():
            # Stop pressing
            self._stop_pressing()
        else:
            # Start pressing
            self._start_pressing()

    def _start_pressing(self):
        """Start key pressing"""
        # Validate settings
        keys = [k for f, k in self.key_frames]
        if not keys:
            messagebox.showwarning("No Keys", "Please add at least one key to press.")
            return

        min_int = self.min_interval_var.get()
        max_int = self.max_interval_var.get()

        if min_int > max_int:
            messagebox.showwarning(
                "Invalid Interval",
                "Minimum interval cannot be greater than maximum interval."
            )
            return

        # Create key presser
        self.key_presser = KeyPresser(
            keys=keys,
            min_interval_minutes=min_int,
            max_interval_minutes=max_int,
            press_twice=self.press_twice_var.get(),
            status_callback=self._on_key_presser_status
        )

        # Start pressing
        try:
            self.key_presser.start()

            # Update button
            self.control_button.config(
                text="STOP PRESSING KEYS",
                bg=BUTTON_STOP_COLOR
            )

            # Disable configuration
            self._set_config_enabled(False)

        except Exception as e:
            logger.error(f"Failed to start key pressing: {e}")
            messagebox.showerror("Error", f"Failed to start key pressing:\n{e}")

    def _stop_pressing(self):
        """Stop key pressing"""
        if self.key_presser:
            self.key_presser.stop()

        # Update button
        self.control_button.config(
            text="START PRESSING KEYS",
            bg=BUTTON_START_COLOR
        )

        # Enable configuration
        self._set_config_enabled(True)

    def _set_config_enabled(self, enabled):
        """
        Enable or disable configuration controls.

        Args:
            enabled: True to enable, False to disable
        """
        state = 'normal' if enabled else 'disabled'

        # Disable add key button and key widgets
        self.add_key_button.config(state=state)

        for key_frame, _ in self.key_frames:
            for widget in key_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state=state)

    def _on_key_presser_status(self, message):
        """
        Handle status message from key presser.

        Args:
            message: Status message
        """
        logger.info(message)

    def _open_discord(self):
        """Open Osiris DevWorks Discord"""
        webbrowser.open("https://discord.gg/BNzRegKZ7k")

    def _open_paypal(self):
        """Open PayPal donation page"""
        webbrowser.open("https://paypal.me/RighteousKill")

    def _open_venmo(self):
        """Open Venmo donation page"""
        webbrowser.open("https://venmo.com/u/Amr-Abouelleil")

    def _on_close(self):
        """Handle window close event"""
        # Stop key presser if running
        if self.key_presser and self.key_presser.is_running():
            self.key_presser.stop()

        # Close window
        self.root.destroy()
