
# Welcome to Download Audio Analysis Tool (AAT) Software for free! 100% Green software! Not malware and other breaches
3 year key: github-2Tl-2jt-68765384dbbd5f36       expired date:11/2/2028
**Version:** _please check release note and will upload the latest verison

The Windows version is available for direct download（latest）:

[Click here to directly download the Windows Executable (AAT.exe)](https://github.com/AAT-RR/AAT/releases/download/Window_OS/AAT.exe)

![Audio Analysis Tool Logo](https://github.com/AAT-RR/AAT/raw/main/aut5.png)

## About the Audio Analysis Tool (AAT)

The Audio Analysis Tool (AAT) is a comprehensive application designed for working with WAV audio files. It supports a range of audio analysis functionalities such as THD, Rub&Buzz, Noise detection, Frequency Response, and Sensitivity calculation. The tool can be run with command-line options or in GUI mode and is compatible with both Windows and macOS.

### Key Features

- **File Management and Playback:** Load WAV files, play them back, and view file details.
- **General Processing Options:** Channel selection, A-weighting, gain adjustment.
- **Audio Analysis Functions:**
  - **Display Audio Waveform**
  - **FFT Spectrum Plot**
  - **Spectrogram Display**
  - **Amplitude Histogram**
  - **Tonal Noise Analysis**
  - **Inter-Channel Phase Analysis**
  - **Sweep Analysis (AAT Test)**
  - **Scan Test (Sweep/Step Analysis)**
  - **Chamber Response & Isolation Analysis**
- **Audio Recording:** Record audio with customizable settings.
- **Signal Generation and Modification**
- **Audio Modification Tools:** Noise cancellation, merging/splitting WAVs.
- **Saving Results and Logs**
- **Menu Bar Functions**

For advanced features like signal generation and modification, Engineer Login is required. Please contact Renee at [shirleyxuxiang@gmail.com](mailto:shirleyxuxiang@gmail.com) for the password and license Key.

### Basic Usage (GUI Mode)

Launch the software without any arguments to use GUI:
```bash
AAT.exe
```

## Screenshots: Tonal Noise Scan Example

![Example](https://github.com/AAT-RR/AAT/raw/main/tonal_noise1.png)

### What is Tonal Noise?

Tonal noise refers to a distinct, continuous frequency component in audio, sounding like a hum or whistle.

#### Causes

- Rotating parts: motors, fans
- Electrical components: transformers
- Fluid movement

![Plot](https://github.com/AAT-RR/AAT/raw/main/5ktonal.png)
![ISO](https://github.com/AAT-RR/AAT/raw/main/5ktonal_1.png)
![Animation](https://github.com/AAT-RR/AAT/raw/main/tonal_noise_analysis_animation.gif)

## Configuration Parameters (`aat.ini`)

Example:
```ini
enable_abnormal_noise_detection = True
noise_freq_range = (1000, 18000)
noise_db_threshold = 15.0
min_abnormal_noise_duration = 0.5
noise_peak_prominence_db = 8.0
noise_peak_width_bins = 2
noise_freq_tracking_tolerance = 80
noise_peak_smoothing_kernel = 5
max_allowed_cumulative_noise_duration = 7.0
enable_cumulative_noise_analysis = True
```

## Command-Line Usage

### Python Example

Download [Python Sample Code](https://github.com/AAT-RR/AAT/releases/download/Window_OS/sample_code_tonal_noise.py)

### WAV Sample File

[Sample WAV](https://github.com/AAT-RR/AAT/releases/download/Window_OS/5k_tonal.wav)

### Command Example

```bash
AAT.exe --console --input_wav "test.wav" --output_result "result.json" --save_plot_image "plot.png" --ini_file "aat.ini"
```

## Support

If you find AAT useful, consider supporting the development. Donations help maintain and improve this tool.

For a free license, email Renee: [shirleyxuxiang@gmail.com](mailto:reneeaat@gmail.com)
