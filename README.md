# Extended AFK - Auto Key Presser

A simple GUI application for automatically pressing keyboard keys at random intervals to prevent AFK (Away From Keyboard) timeouts.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## Features

- **Customizable Keys**: Select any keyboard keys via click-to-detect system
- **Configurable Intervals**: Set minimum and maximum intervals between key presses
- **Activity Log**: Real-time log display showing when keys are pressed
- **Persistent Settings**: Automatically saves and loads your configuration

## Download & Installation

You can download Extended AFK from the [GitHub Releases page](https://github.com/Osiris-RK/extended-afk/releases).

### Standalone Executable

**`ExtendedAFK.exe`** - Portable version (no installation required)

1. Download `ExtendedAFK.exe` from the releases page
2. **Right-click** the .exe and select **"Run as Administrator"**
   - Admin rights are required for keyboard simulation
3. Configure your keys and run the application


### Running from Source

1. Install Python 3.8 or higher
2. Clone the repository:
   ```bash
   git clone https://github.com/Osiris-RK/extended-afk.git
   cd extended-afk
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## System Requirements

- Windows 10 or later (64-bit)
- Administrator privileges (for keyboard simulation)

## Usage

1. **Configure Keys**:
   - Click "Select Key..." to detect a key press
   - Press any key when prompted
   - Click "Add Key..." to add more keys
   - Click "Delete" to remove a key

2. **Set Intervals**:
   - Configure minimum and maximum intervals (in minutes)
   - The application will randomly wait between these intervals

3. **Options**:
   - Check "Press each key twice" to press each key two times with a 1-second delay

4. **Start/Stop**:
   - Click "START PRESSING KEYS" to begin
   - Click "STOP PRESSING KEYS" to pause
   - Configuration is locked while running

5. **Monitor Activity**:
   - Watch the Activity Log for timestamped key press events
   - Logs are also saved to: `%APPDATA%\extended-afk\logs\extended-afk.log`

## Important Notes

### Administrator Privileges

The keyboard simulation library requires **administrator privileges** to function. Always run the application as administrator.

### Antivirus Warnings

Some antivirus software may flag keystroke simulation tools as potentially unwanted. This is a false positive. The application:
- Is open source
- Only simulates keypresses locally
- Does not send data anywhere
- Does not record your keystrokes

If your antivirus blocks the application, you may need to add it to your exclusions list.

### Settings Location

Settings are stored at: `%APPDATA%\extended-afk\settings.json`

Log files are stored at: `%APPDATA%\extended-afk\logs\extended-afk.log`

## Support the Project

Extended AFK is a free, open-source tool created to help prevent AFK timeouts. If you find it useful and would like to support the development, here are ways you can help:

### Donate

Your financial support helps fund development of new features:

💳 **[PayPal Donation](https://paypal.me/RighteousKill)** - Support via PayPal

💰 **[Venmo Donation](https://venmo.com/u/Amr-Abouelleil)** - Support via Venmo

### Contribute

- **Report bugs** with steps to reproduce
- **Request features** you'd like to see
- **Share feedback** and suggestions
- **Submit code contributions** via GitHub

### Join the Community

💬 **[Discord Community](https://discord.gg/BNzRegKZ7k)** - Join Osiris DevWorks for support and discussions

Even if you can't donate, your feedback and bug reports are invaluable!

---

## Credits

Developed by Osiris DevWorks

## License

This software is provided as-is for personal use. Use responsibly and in accordance with the terms of service of any applications or games you use it with.
