# VITA Prototype Hardware Diagnostic Suite (Week 2)

This directory contains the Python diagnostic and test scripts developed during **Week 2** to validate all physical hardware interfaces on the Raspberry Pi 4 prototype before running speech-to-text models.

## Scripts Included

1. **`01_test_gpio_hmi.py`**:
   - Tests the Push-to-Talk (PTT) arcade pushbutton on GPIO 17 with hardware/software debouncing.
   - Tests the tricolor status RGB LED (GPIO 22 Red, GPIO 27 Green, GPIO 23 Blue) across all operational states.

2. **`02_test_audio_capture.py`**:
   - Captures 16 kHz 16-bit Mono audio from the dual I2S MEMS microphone array (`hw:1,0`).
   - Calculates RMS amplitude, dBFS level meter, and ambient Signal-to-Noise Ratio (SNR).

3. **`03_test_audio_playback.py`**:
   - Generates an audio test tone and frequency sweep (150 Hz to 3500 Hz).
   - Verifies speaker output and MAX98357A Class-D I2S amplifier clarity without power-on pop.

4. **`04_test_thermal_stress.py`**:
   - Stress-tests all 4 Cortex-A72 cores under simulated ML workloads.
   - Monitors temperature via `vcgencmd measure_temp` and throttling flags via `vcgencmd get_throttled`.
   - Drives closed-loop proportional PWM fan cooling on GPIO 14.

## Running Tests

```bash
# Test HMI (Button & LED)
python3 01_test_gpio_hmi.py

# Test Microphone Capture
python3 02_test_audio_capture.py

# Test Speaker Playback
python3 03_test_audio_playback.py

# Test Thermals & Fan
python3 04_test_thermal_stress.py
```
