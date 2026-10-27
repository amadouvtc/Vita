# VITA Hardware & Unit Economics Benchmarks (Week 5)

This directory contains the Python benchmark and analytical tools from **Week 5**, documenting our migration from the Raspberry Pi 4 to the Orange Pi 5 (Rockchip RK3588S), running **Qwen 2.5 1.5B**, and examining the commercial dilemma of unit economics.

## Scripts Included

1. **`01_orangepi5_gpio_setup.py`**:
   - Maps the 26-pin expansion header of the Orange Pi 5 to our audio hardware (INMP441 I2S microphones, MAX98357A I2S DAC, PTT tactile switch, and RGB status LED).

2. **`02_qwen1_5b_npu_benchmark.py`**:
   - Measures token throughput, Time-to-First-Token (TTFT), and total voice turn latency of Qwen 2.5 1.5B comparing the Raspberry Pi 4 CPU (~1.9 tok/s) against the Orange Pi 5 RK3588 (~18.6 tok/s).

3. **`03_unit_economics_bom_calculator.py`**:
   - Compares the Bill of Materials (BOM) cost between the initial 50€ target (5X markup on a 250€ retail price) versus the 147.50€ Orange Pi 5 reality (1.69X markup).

## Running Benchmarks

```bash
python3 01_orangepi5_gpio_setup.py
python3 02_qwen1_5b_npu_benchmark.py
python3 03_unit_economics_bom_calculator.py
```
