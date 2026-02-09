# Changelog
## 🐛 [1.08.05] - 2026-02-11
### Windows factory vesion Downloads
### Fixes
-add design hub
- updload the factory vesion and add teams test.
- [AAT_factory.exe application](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT_factory.exe)
- [AAT.exe application](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT.exe)
## 🐛 [1.07.10] - 2025-07-11
### Windos facoty vesion Downloads
### Fixes
- updload the factory vesion.
## 🐛 [1.07.07] - 2025-07-01
### MAC OS Downloads
- [AAT.dmg application](https://github.com/AAT-RR/AAT/releases/download/MAC_OS/AAT.dmg)
### Fixes
- change UI layout and add fix ini issue for macos
## 🐛 [1.07.06] - 2025-06-29
### Windos Downloads
- [AAT.exe application](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT.exe)
### Fixes
- change UI layout and add ini use manual
## 🐛 [1.07.04] - 2025-06-27
### Fixes
- fix display wav bug
- add language change per user request
- fix the bug of phase through ICP
### Downloads
- [IPC_phase_sample.py script](https://github.com/AAT-RR/AAT/releases/download/Window_OS/IPC_phase_sample.py)
## 🐛 [1.06.07] - 2025-06-21
### Fixes
- Addressed various GUI bugs like smooth.  
## 🐛 [1.06.06] - 2025-06-20
### Fixes
- Addressed various GUI bugs.
## 🐛 [1.06.05] - 2025-06-20
### Downloads
- [restart.py script](https://github.com/AAT-RR/AAT/releases/download/Window_OS/restart.py)
### Features & Improvements
- Added Inter-Process Communication (IPC) command for application reboot functionality.
- Enhanced A-weighting control via IPC.
- Introduced optional reboot capability for faster testing in manufacturing environments.
## 🐛 [1.06.04] - 2025-06-20
### Downloads
- [AAT v1.06.04 application](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT_v1.06.04.exe)
### Features & Improvements
- Improved code logic to support multi-channel analysis for Tonal Noise Scan and FFT plots from single audio files.
## 🐛 [1.06.03] - 2025-06-19
### Improvements
- Addressed various GUI issues.
- Released new manual book version 1.06.02.
- Added channel selection functionality for tonal noise testing.
### 🐛 Bug Fixes [1.06.02] - 2025-06-18
- Fixed A-weighting bug in Tonal Noise Scan when controlled via IPC.
- Improved tonal test execution speed based on user requests.
### 🧰 [1.06.01] - 2025-06-18
### Improvements
- Tonal noise scan functionalities improved.
### Changed - 2025-05-01
- Updated API version to v1.6.0.
## 🐛 [1.05.01] - 2025-04-28
### Fixes
- Addressed a critical bug causing incorrect tonal noise identification under specific high-noise conditions.
- Improved stability of real-time plotting when handling extremely large audio files.
## 🚀 [1.05.00] - 2025-04-12
### Features & Improvements
- **Advanced STI Analysis:** Integrated new algorithms for more robust Speech Transmission Index calculations in reverberant environments.
- **Enhanced IPC Debugging:** Added more detailed logging for Inter-Process Communication, aiding in troubleshooting automation scripts.
## 🐛 [1.04.09] - 2025-03-29
### Fixes
- Resolved an issue where the limit checker sometimes failed to apply custom thresholds correctly for specific frequency bands.
- GUI responsiveness improved when navigating through multiple historical measurement plots.

## 🚀 [1.04.08] - 2025-03-15
### Features & Improvements
- **Batch Processing for Noise Reduction:** Introduced a new feature allowing noise reduction processes to be applied to multiple files in a batch.
- **Customizable Report Generation:** Users can now define custom templates for exporting test results, including specific plot types and data tables.
## 🐛 [1.04.07] - 2025-02-27
### Fixes
- Resolved an issue where the application would occasionally list phantom audio devices on certain Windows systems.
- Corrected minor display inconsistencies in the main application window when resizing.

## 🚀 [1.04.06] - 2025-02-14
### Features & Improvements
- **FFT Peak Tracking:** Added a new feature to FFT plots to automatically identify and track dominant frequency peaks over time.
- **IPC Command Enhancements:** Expanded the IPC command set to include more granular control over measurement parameters.

## 🐛 [1.04.05] - 2025-01-30
### Fixes
- Addressed a memory leak issue that occurred when repeatedly loading and unloading large audio files for waveform plotting.
- Corrected phase misalignment issues when merging mono files into multichannel audio.

## 🚀 [1.04.04] - 2025-01-16
### Features & Improvements
- **User-Defined Measurement Sequences:** Implemented the ability to define and save sequences of tests, streamlining multi-step acoustic evaluations.
- **Performance Optimization for Tonal Noise Scan:** Significant speed improvements in tonal noise analysis for real-time applications.

## 🐛 [1.04.03] - 2024-12-28
### Fixes
- Corrected an error where license validation could fail under specific network configurations.
- Fixed an intermittent crash when closing the application while a measurement was in progress.

## 🚀 [1.04.02] - 2024-12-14
### Features & Improvements
- **Multi-Monitor Support:** Improved GUI layout and window management for multi-monitor setups.
- **Enhanced Data Export Options:** Added support for exporting raw measurement data in various formats (e.g., CSV, JSON).

## 🐛 [1.04.01] - 2024-11-29
### Fixes
- Resolved an issue with signal connections being lost after certain GUI interactions in headless mode.
- Fixed a rendering glitch in plots embedded within the application's graphics view.

## 🚀 [1.04.00] - 2024-11-15
### Features & Improvements
- **Real-time Spectral Subtraction Visualization:** Added live visualization of the spectral subtraction process.
- **IPC Server Reliability:** Improved stability and error handling for Inter-Process Communication.

## 🐛 [1.03.09] - 2024-10-30
### Fixes
- Addressed a bug where adaptive filters would occasionally fail to converge for certain types of noise.
- Corrected a display issue with selections in the device listing.

## 🚀 [1.03.08] - 2024-10-17
### Features & Improvements
- **Automated Device Calibration Workflow:** Introduced a guided workflow for calibrating audio input devices using known reference signals.
- **Python 3.8 Compatibility:** Ensured full compatibility with Python 3.8 environments.

## 🐛 [1.03.07] - 2024-09-26
### Fixes
- Fixed an issue where waveform plots might show incorrect timestamps for long recordings.
- Resolved a minor visual artifact when zooming in on graphical plots.

## 🚀 [1.03.06] - 2024-09-12
### Features & Improvements
- **Configurable Averaging for Measurements:** Added options to configure temporal and spectral averaging for various measurements.
- **CLI Mode Improvements:** Enhanced command-line interface options to allow more flexible automated testing.

## 🐛 [1.03.05] - 2024-08-30
### Fixes
- Corrected a bug in the tonal noise algorithm where very low-frequency tones were sometimes missed.
- Addressed an issue causing file dialogs to freeze on some network drives.

## 🚀 [1.03.04] - 2024-08-16
### Features & Improvements
- **Preservation of Settings:** Application now remembers last used file paths, device selections, and measurement settings across sessions.
- **Improved Log Messaging:** Enhanced log messages to include timestamps and severity levels for better debugging.

## 🐛 [1.03.03] - 2024-07-29
### Fixes
- Fixed a crash that occurred when attempting to split a single-channel audio file.
- Resolved an issue with input dialogs not being centered correctly on secondary monitors.

## 🚀 [1.03.02] - 2024-07-15
### Features & Improvements
- **Simplified IPC Connection Setup:** Streamlined the IPC server initialization process for headless and GUI modes.
- **Export to Image Formats:** Added options to export plots directly to common image formats (e.g., PNG, JPEG).

## 🐛 [1.03.01] - 2024-06-27
### Fixes
- Corrected an off-by-one error in the limit checker when defining upper and lower frequency bounds.
- Fixed a visual bug in slider controls when rapidly changing values.

## 🚀 [1.03.00] - 2024-06-13
### Features & Improvements
- **Headless Mode IPC Support:** Fully enabled headless operation with robust IPC communication for automated testing environments.
- **API Version Update:** Major update to internal API, improving overall code structure and maintainability.

## 🐛 [1.02.09] - 2024-05-31
### Fixes
- Addressed an issue where sweep tone analysis would sometimes misinterpret pilot tones in noisy environments.
- Improved handling of invalid audio file paths, preventing application crashes.

## 🚀 [1.02.08] - 2024-05-17
### Features & Improvements
- **Integrated User Manual:** Added direct access to the user manual within the application.
- **Enhanced Error Reporting:** More detailed error messages are now displayed, guiding users to potential solutions.

## 🐛 [1.02.07] - 2024-04-26
### Fixes
- Fixed a bug where audio file interactions could lead to corrupted files on specific network shares.
- Resolved an issue where timer events were occasionally delayed, affecting real-time measurements.

## 🚀 [1.02.06] - 2024-04-12
### Features & Improvements
- **Spectrum Comparison Tool:** Introduced a tool to compare multiple FFT spectra, useful for A/B testing and trend analysis.
- **Improved Device Hot-Swapping:** Enhanced recognition and handling of audio device disconnections and reconnections.

## 🐛 [1.02.05] - 2024-03-29
### Fixes
- Corrected an issue where spectral subtraction would sometimes introduce unwanted artifacts at very low frequencies.
- Fixed a crash when attempting to plot an empty waveform.

## 🚀 [1.02.04] - 2024-03-15
### Features & Improvements
- **Data Annotation on Plots:** Users can now add custom text annotations and markers to waveform and FFT plots.
- **Undo/Redo Functionality:** Implemented basic undo/redo for common GUI actions.

## 🐛 [1.02.03] - 2024-02-28
### Fixes
- Resolved an issue where adaptive filter parameters were not correctly saved between sessions.
- Fixed a bug causing message boxes to appear behind the main window.

## 🚀 [1.02.02] - 2024-02-14
### Features & Improvements
- **Custom Frequency Range for Scans:** Allowed users to define custom start and end frequencies for tonal noise scans.
- **Improved Application Startup Time:** Optimized loading of modules and resources to reduce startup delays.

## 🐛 [1.02.01] - 2024-01-30
### Fixes
- Corrected a rare race condition during IPC server thread shutdown.
- Fixed a display bug in the graphics view when rapidly switching between different plot types.

## 🚀 [1.02.00] - 2024-01-16
### Features & Improvements
- **Integrated Licensing System:** Implemented a new licensing system to handle product activation and usage.
- **Automated Software Updates:** Introduced an in-app notification system for new versions and a simplified update process.

## 🐛 [1.01.09] - 2023-12-28
### Fixes
- Resolved issues with signal disconnections during rapid changes in audio device selection.
- Fixed a minor GUI layout issue in the settings panel.

## 🚀 [1.01.08] - 2023-12-14
### Features & Improvements
- **Customizable Color Schemes:** Added options for users to personalize the GUI's color scheme.
- **Performance Profiling Tools:** Integrated internal tools to help identify and optimize performance bottlenecks.

## 🐛 [1.01.07] - 2023-11-29
### Fixes
- Corrected a bug where merging mono files could produce silent channels if input files were not perfectly aligned.
- Addressed an issue with the graphics scene not refreshing properly after certain plot modifications.

## 🚀 [1.01.06] - 2023-11-15
### Features & Improvements
- **Advanced Thresholding for Compliance:** Expanded limit checker with more complex rule-based thresholding for automated pass/fail criteria.
- **Improved Help Documentation:** Enhanced tooltips and context-sensitive help for various GUI elements.

## 🐛 [1.01.05] - 2023-10-30
### Fixes
- Fixed a crash that occurred when trying to access non-existent audio input devices.
- Resolved an issue with saving configuration files to read-only directories.

## 🚀 [1.01.04] - 2023-10-17
### Features & Improvements
- **Flexible Audio File Support:** Broadened support for various audio file formats.
- **Automatic Gain Control (AGC) Toggle:** Added an option to enable/disable AGC on input devices for consistent measurements.

## 🐛 [1.01.03] - 2023-09-29
### Fixes
- Corrected a bug in spectral subtraction where very short noise samples led to inaccurate results.
- Fixed an issue where the application window would sometimes open off-screen.

## 🚀 [1.01.02] - 2023-09-15
### Features & Improvements
- **Interactive Plot Zoom & Pan:** Enhanced graphics view to allow intuitive zooming and panning on plots.
- **Improved Audio Device Selection:** More robust detection and display of available audio input devices.

## 🐛 [1.01.01] - 2023-08-30
### Fixes
- Resolved an issue where adaptive filters would occasionally introduce clipping at high input levels.
- Fixed a bug in tonal noise causing false positives for very brief transient sounds.

## 🚀 [1.01.00] - 2023-08-16
### Features & Improvements
- **Initial IPC Server Implementation:** Added the foundational IPC server for basic remote control and automation.
- **Basic Tonal Noise Scan:** Introduced the core functionality to identify and analyze dominant tones.

## 🐛 [1.00.08] - 2023-07-31
### Fixes
- Addressed minor GUI layout issues on high-DPI displays.
- Improved stability when rapidly changing audio input sources.

## 🚀 [1.00.07] - 2023-07-17
### Features & Improvements
- **Basic A-weighting Filter:** Implemented A-weighting for sound pressure level measurements.
- **Configurable Sample Rates:** Added ability to select desired sample rates for recordings.

## 🐛 [1.00.06] - 2023-06-28
### Fixes
- Fixed a bug where waveform plots would sometimes fail to render for very short audio snippets.
- Resolved an issue causing the application to crash when exiting prematurely during a recording.

## 🚀 [1.00.05] - 2023-06-14
### Features & Improvements
- **Improved File Import/Export Dialogs:** Enhanced file dialogs for better usability and file type filtering.
- **Basic FFT Plotting:** Implemented Fast Fourier Transform (FFT) plotting for spectral analysis.

## 🐛 [1.00.04] - 2023-05-30
### Fixes
- Corrected a bug preventing message boxes from displaying properly in certain error scenarios.
- Minor performance improvements for GUI rendering.

## 🚀 [1.00.03] - 2023-05-15
### Features & Improvements
- **Basic Recording Functionality:** Implemented the core audio recording feature.
- **Waveform Visualization:** Added initial waveform plotting to display recorded audio.

## 🐛 [1.00.02] - 2023-04-26
### Fixes
- Resolved an issue where the application window would occasionally appear minimized on startup.
- Fixed a typo in a log message.

## 🚀 [1.00.01] - 2023-04-12
### Features & Why create
- **Initial GUI Framework:** Laid the groundwork for the main application window.
- **Project Setup:** Established the core project structure, including module imports and basic application initialization.
- AAT (Acoustic Analysis Tool) was born out of a shared frustration among acoustic and test engineers, particularly within certain tech companies in the US Bay Area, whose names remain unmentionable for confidentiality reasons. Witnessing firsthand the daily struggles they faced with inadequate or overly complex tools for visualizing and analyzing acoustic data, I envisioned a straightforward, intuitive application. The primary motivation was to create a tool that made it 'easy to see the picture' 
– to quickly and clearly visualize complex acoustic measurements, empowering engineers to identify issues and validate designs with greater efficiency and less hassle.

