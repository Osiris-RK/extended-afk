# Changelog

All notable changes to Extended AFK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

## [1.0.2] - 2024-12-17

### Added
- Complete release infrastructure with CHANGELOG.md and RELEASE_PROCESS.md
- Discord notification automation for releases (channel ID: 1450835473949003817)
- Custom `/release` Claude command for streamlined releases
- Extended AFK icon in README header

### Changed
- Removed administrator privilege warning and all related references
- Application now runs without requiring administrator mode
- Updated README.md to remove administrator requirements
- Changed "Press Twice" checkbox label to "Use Toggle Behavior" for better clarity

### Fixed
- Improved requirements.txt with explicit ttkbootstrap and python-dotenv dependencies

## [1.0.1] - 2024-12-15

### Fixed
- Fixed window border obstruction and improved theme integration
- Fixed GUI freezing issues with queue-based logging
- Fixed application freeze with proper threading

### Changed
- Added ttkbootstrap theme support for modern Windows appearance
- Improved key pressing implementation with better error handling
- Updated UI with simplified button text ("Start" / "Stop")
- Unchecked "Press Twice" by default for better UX

### Added
- Administrator privileges warning (deprecated in later release)
- Queue-based logging to prevent GUI freezing
- Per-key settings with individual "Press Twice" checkboxes

## [1.0.0] - 2024-12-15

### Added
- Initial release of Extended AFK Auto Key Presser
- Windows-style GUI with modern appearance
- Customizable key selection (up to 3 keys)
- Random interval configuration (minutes-based)
- Per-key "Press Twice" option
- Real-time activity log
- Persistent settings in %APPDATA%
- Separate START and STOP buttons
- Support for any keyboard key via detection dialog
- Rotating log files (5MB max, 3 backups)
