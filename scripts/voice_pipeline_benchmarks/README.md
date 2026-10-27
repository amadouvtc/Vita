# VITA Voice Pipeline Benchmarks (Week 3)

This directory contains the Python benchmark and diagnostic scripts from **Week 3**, documenting the evolution of VITA's voice stack from classical signal processing to bare-metal local neural execution on the Raspberry Pi 4 host.

## The Three Phases Evaluated

1. **`01_classical_dsp_speech_attempt.py`**:
   - Tests our initial heuristic signal processing approach:
     - STT: MFCC energy bands, zero-crossing rates, and dynamic time warping.
     - TTS: Formant and concatenative diphone synthesis.
   - *Verdict*: Dropped words in kitchen noise and sounded horribly robotic with jarring phase clicks ("stitches").

2. **`02_cloud_api_bridge_prototype.py`**:
   - Tests a temporary cloud API prototype:
     - Device records whole speech, posts audio to a speech-to-text API, receives text.
     - Sends response text to a TTS API, receives audio, and plays over the MAX98357A I2S speaker.
   - *Verdict*: Flawless transcription and human voices, but violated data sovereignty and added 2.5s+ of unpredictable network latency.

3. **`03_host_neural_voice_engine.py`**:
   - The breakthrough: Running modern neural models **directly on the bare-metal host** (no Docker, no containers):
     - STT: `faster-whisper` (CTranslate2 INT8 quantized Whisper `tiny.en` / `base.en`).
     - TTS: `piper-tts` (ONNX Runtime CPU with `en_US-lessac-medium.onnx`).
   - *Verdict*: 100% offline, privacy-first, 22.05 kHz natural speech, sub-1.5s total latency on ARM Cortex-A72 cores.

## Execution

```bash
# Run Phase 1 DSP Benchmark
python3 01_classical_dsp_speech_attempt.py

# Run Phase 2 Cloud API Baseline
python3 02_cloud_api_bridge_prototype.py

# Run Phase 3 Local Neural Voice Engine
python3 03_host_neural_voice_engine.py
```
