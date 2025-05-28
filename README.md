# Welcome to Download Audio Analysis Tool (AAT) Software for free!

**Version:** V1.5.3

The macOS version is available for direct download:
[Click here to directly download the macOS Installer (AAT-installer.dmg)](https://github.com/AAT-RR/AAT/releases/download/MAC_OS/AAT.dmg)

The Windows version is available for direct download:
[Click here to directly download the Windows Executable (AAT.exe)](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT.exe)

Download the default configuration file for Windows:
[Click here to download the aat.ini configuration file](https://github.com/AAT-RR/AAT/releases/download/Window_OS/aat.ini)

![Audio Analysis Tool Logo](https://github.com/AAT-RR/AAT/raw/main/aut5.png)

## About the Audio Analysis Tool (AAT)

The Audio Analysis Tool (AAT) is a comprehensive application designed for working with WAV audio files. It supports a range of audio analysis functionalities such as THD, Rub&Buzz, Noise detection, Frequency Response, and Sensitivity calculation. The tool can be run with command-line options or in GUI mode and is compatible with both Windows and macOS.

### Key Features

* **File Management and Playback:** Easily load single or multiple WAV audio files, select an active file for analysis, and play them back with a clear time display. You can also view detailed file information such as sample rate, bit depth, channels, and file size. Loaded files can be managed by deleting selected ones or clearing all.
* **General Processing Options:** Customize your analysis with options like channel selection (left, right, or both), A-weighting to approximate human hearing, and gain adjustment in dB.
* **Audio Analysis Functions:**
    * **Display Audio Waveform:** Visualize the audio signal's amplitude over time, with options for channel selection, A-weighting, gain, and zoom. You can even plot waveforms for all loaded files for comparison.
    * **FFT Spectrum Plot:** Analyze frequency components, identify tones, and understand spectral balance using Fast Fourier Transform (FFT). Parameters include FFT Size (N) for resolution, plotting all files or delta for comparison, and logarithmic frequency scaling.
    * **Spectrogram Display:** Get a detailed view of how frequency content changes over time, useful for analyzing speech or transient events.
    * **Amplitude Histogram:** Understand the statistical distribution of audio sample amplitudes to assess loudness, dynamic range, and potential clipping.
    * **Tonal Noise Analysis:** Specifically designed to identify discrete, stable frequency tones that stand out from background noise. This includes a robust "Scan Tonal Noise" feature for abnormal noise detection, configurable via an `aat.ini` file or pop-up dialogues. Parameters such as frequency range, dB threshold, minimum duration, peak prominence, and frequency tracking tolerance allow for precise tuning of the detection algorithm.
    * **Inter-Channel Phase Analysis:** Compare the phase relationship between two audio signals across the frequency spectrum, useful for identifying timing offsets or polarity inversions.
    * **Sweep Analysis (AAT Test):** Analyze frequency sweeps for distortion metrics (THD, Rub & Buzz) and fundamental signal power, crucial for speaker and microphone testing.
    * **Scan Test (Sweep/Step Analysis):** Advanced analysis for frequency sweep or step-sweep signals, focusing on tracking steps and pilot tones with detailed frequency behavior over time.
    * **Chamber Response Analysis:** Study acoustic characteristics of rooms by analyzing sound energy decay in specific frequency bands.
    * **Chamber Isolation Analysis:** Estimate how well a barrier blocks sound across different frequencies by comparing sound levels in two user-defined time periods.
* **Audio Recording:** Capture audio directly from connected microphones, with options for single or dual mic recording, adjustable recording length, and automatic naming.
* **Signal Generation and Modification:** Generate new test signals (pure tones with distortion, white noise) or modify loaded audio by adding tones or distortion.
* **Audio Modification Tools:** Includes adaptive noise cancellation (via a reference noise signal) and spectral subtraction for background noise reduction. You can also merge mono WAVs into multi-channel files or split multi-channel WAVs into separate mono files. A feature to extract common sound from multiple files is also available.
* **Saving Results and Logs:** Save plots as images (PNG, JPG, BMP) or plot data to CSV for further analysis. Session logs containing status updates and errors can also be saved to text files, with an option for auto-saving.
* **Menu Bar Functions:** Access fundamental operations like loading files, engineer login (required for advanced features), clearing plots and logs, and refreshing audio devices.

For advanced features like signal generation and modification, Engineer Login is required. Please contact Renee at shirleyxuxiang@gmail.com for the password and license Key.

### Basic Usage (GUI Mode)

You can launch the software without any arguments to use its full graphical user interface:


## AAT Tool Interface Screenshots: Tonal Noise Scan Example

Here are some screenshots of the AAT Tool interface, including an example of the Tonal Noise Scan visualization:

### How Scan Tonal Noise Works (A Simplified Explanation)

Our Scan Tonal Noise feature is designed to automatically find those annoying, constant "whines" or "hums" in your audio files, especially useful for checking products on a production line. Think of it like this:

* We take your audio file and quickly break it down into tiny slices of sound, like looking at snapshots of what frequencies are present over time.
* For each snapshot, we look for any specific musical notes or tones that are significantly louder than the surrounding background noise. It's like finding a single loud whistle in a room full of murmurs.
* Then, we track these loud "notes" over time. If a particular note stays loud and consistent for a certain period, our tool identifies it as a potential "tonal noise."
* Finally, based on some smart rules we've set (like how loud it has to be or how long it has to last), the system decides if this tone is a problem. It can even count how much "problem tone" occurs in total. This helps us quickly tell if a product passes or fails the noise test, without needing a human to listen to every single one.

![Audio Analysis Tool Main Interface](https://github.com/AAT-RR/AAT/raw/main/tonal_noise1.png)

### What is Tonal Noise?

Tonal noise refers to a type of noise characterized by its distinct, stable, and often continuous pitch. Unlike broadband noise, which spreads across a wide range of frequencies, tonal noise is concentrated at one or more specific frequencies, making it sound like a hum, whine, buzz, or whistle.

#### What Causes Tonal Noise?

Tonal noise is usually caused by things that involve repetitive motion or electrical currents. It sounds like a steady hum, whine, buzz, or whistle.

* Tonal noise is identified if a spectral peak is perceptibly higher than neighboring bands.
* The tone can be detected visually in a spectrum or audibly.
* ISO 1996-1:2016 uses subjective and empirical rules for identification.
* **Rotating Parts:** Motors, fans, pumps, and gears.
* **Electrical Components:** Transformers and power supplies, often due to electromagnetic vibrations.
* **Fluid Movement:** Steady flow in pipes.

![Tonal Noise Example Plot](https://github.com/AAT-RR/AAT/raw/main/5ktonal.png)
This plot illustrates tonal noise. The prominent line clearly indicates a continuous, stable tone standing out from other frequencies. This line represents the identified tonal noise component.

![Tonal Noise Detection based on ISO Definition](https://github.com/AAT-RR/AAT/raw/main/5ktonal_1.png)
This image demonstrates how the system identifies tonal noise based on its definition. It highlights spectral peaks that are perceptibly higher than their neighboring frequency bands, indicating the presence of a tonal component as per the ISO standard.

## Command-Line Usage: Scan Tonal Noise Analysis (For Production Lines)

The Audio Analysis Tool (AAT) features a **unique, custom-developed Scan Tonal Noise Analysis function**, which is specifically designed for high-throughput testing environments like **production lines**. This proprietary algorithm excels at rapidly detecting abnormal tonal noise events in audio files, providing quick Pass/Fail judgments and detailed reports. It can be integrated seamlessly into automated test sequences, requiring no human interaction to perform batch analysis and generate machine-readable output.

### How to Call These Commands with Python:

Here's a simple Python sample code that demonstrates how to communicate with the AAT tool via a socket connection and execute audio analysis tasks.

The script performs the following actions:

* **Connects to the server:** Establishes a socket connection to `127.0.0.1` on port `12345`.
* **Gets Server Status (Optional):** Sends a `get_status` command to the server.
* **Loads WAV Files:** Sends an `open_wave_file_gui` command with a list of WAV file paths to be loaded by the server's GUI.
* **Runs Tonal Noise Analysis:** Sends a `run_scan_tonal_noise` command to analyze the loaded files. This command includes parameters for saving a combined plot image and overriding analysis settings like frequency range and threshold.
* **Clears Loaded Files:** Sends a `clear_all_loaded_files` command to clear the WAV files from the server's memory.
* **Saves Log:** Records the entire test process and results into a JSON log file.
* **Prints Summary:** Displays a summary of the test, including overall status, abnormal noise detection, and file-specific results.

**Using Python to call these commands is a very effective method for automation and integration into your testing workflows.**

[Download Python Sample Code for Tonal Noise Analysis](https://github.com/AAT-RR/AAT/releases/download/Window_OS/sample_code_tonal_noise.py)

### Example Commands for Production Line Integration:

To analyze multiple audio files, save detailed results to a JSON file, and generate a combined plot image:






















