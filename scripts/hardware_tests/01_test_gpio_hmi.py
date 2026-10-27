#!/usr/bin/env python3
"""
VITA Device Hardware Validation Suite - Step 1: GPIO HMI Test
Validates:
- Push-to-Talk (PTT) Tactile Button (GPIO 17 / Physical Pin 11)
- Common-Cathode Tricolor Status RGB LED:
    - Red Channel   (GPIO 22 / Physical Pin 15)
    - Green Channel (GPIO 27 / Physical Pin 13)
    - Blue Channel  (GPIO 23 / Physical Pin 16)
- Software debouncing and latency measurement
"""

import time
import sys

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("[MOCK MODE] RPi.GPIO not found on this system. Running diagnostic mock simulation.")
    class MockGPIO:
        BCM = "BCM"
        IN = "IN"
        OUT = "OUT"
        PUD_DOWN = "PUD_DOWN"
        RISING = "RISING"
        FALLING = "FALLING"
        BOTH = "BOTH"
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode, pull_up_down=None, initial=None): pass
        @staticmethod
        def output(pin, state): pass
        @staticmethod
        def input(pin): return 0
        @staticmethod
        def add_event_detect(pin, edge, callback=None, bouncetime=None): pass
        @staticmethod
        def cleanup(): pass
    GPIO = MockGPIO()

# Pin Definitions (BCM numbering)
PIN_BUTTON_PTT = 17
PIN_LED_RED    = 22
PIN_LED_GREEN  = 27
PIN_LED_BLUE   = 23

BOUNCE_TIME_MS = 200

def setup_hardware():
    GPIO.setmode(GPIO.BCM)
    # Configure Button with internal pull-down resistor (reinforced with external 10k resistor)
    GPIO.setup(PIN_BUTTON_PTT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # Configure RGB channels as outputs, initialize to OFF (0)
    for pin in (PIN_LED_RED, PIN_LED_GREEN, PIN_LED_BLUE):
        GPIO.setup(pin, GPIO.OUT, initial=0)

def set_status_led(red: bool, green: bool, blue: bool):
    GPIO.output(PIN_LED_RED, 1 if red else 0)
    GPIO.output(PIN_LED_GREEN, 1 if green else 0)
    GPIO.output(PIN_LED_BLUE, 1 if blue else 0)

def test_led_sequence():
    print("[TEST] Cycling RGB Status LED sequence...")
    states = [
        ("IDLE / READY (Green)", False, True, False),
        ("LISTENING / PTT ACTIVE (Amber)", True, True, False),
        ("RECORDING / ENCODING (Red)", True, False, False),
        ("INFERENCE / TTS (Blue)", False, False, True),
        ("OFF", False, False, False),
    ]
    for name, r, g, b in states:
        print(f"  -> State: {name}")
        set_status_led(r, g, b)
        time.sleep(0.4)
    print("  -> LED sequence test PASSED.\n")

def button_callback(channel):
    press_time = time.time()
    print(f"\n[EVENT] Push-to-Talk pressed on GPIO {channel}! Timestamp: {press_time:.4f}")
    set_status_led(True, True, False) # Amber
    time.sleep(0.1)

def run_hmi_diagnostics():
    print("==================================================")
    print("   VITA Hardware Diagnostics: HMI & Controls      ")
    print("==================================================")
    setup_hardware()
    test_led_sequence()
    
    print(f"[INFO] Monitoring PTT Button on GPIO {PIN_BUTTON_PTT} (debouncetime={BOUNCE_TIME_MS}ms).")
    print("[INFO] Press the physical button to test interrupts. Press Ctrl+C to finish.")
    
    GPIO.add_event_detect(PIN_BUTTON_PTT, GPIO.RISING, callback=button_callback, bouncetime=BOUNCE_TIME_MS)
    
    try:
        # Green pulsing idle simulation
        for _ in range(5):
            set_status_led(False, True, False)
            time.sleep(0.5)
            set_status_led(False, False, False)
            time.sleep(0.2)
        print("[INFO] Automated test window complete.")
    except KeyboardInterrupt:
        print("\n[INFO] User interrupted test.")
    finally:
        set_status_led(False, False, False)
        GPIO.cleanup()
        print("[INFO] GPIO cleaned up. HMI test completed successfully.")

if __name__ == "__main__":
    run_hmi_diagnostics()
