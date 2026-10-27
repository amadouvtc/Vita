#!/usr/bin/env python3
"""
VITA Prototype - Week 5: Unit Economics & Bill of Materials (BOM) Calculator
Analyzes the commercial dilemma encountered in Week 5:
- Target Retail Price: 250€ (One-time consumer purchase, no subscription).
- Target Hardware Markup: 5X (Standard consumer hardware gross margin).
- Ideal BOM Target: 50.00€ (Achievable with Raspberry Pi 4 Model B).
- Real-World BOM on Orange Pi 5: ~147.50€ (Gross margin collapses to 1.69X).
"""

TARGET_RETAIL_PRICE_EUR = 250.00

# Architecture A: Raspberry Pi 4 Target (Theoretical / Low Speed)
PI4_BOM = {
    "SBC Compute Core (RPi 4 8GB)": 45.00,
    "MicroSD Storage (32GB U3)": 4.50,
    "Power Supply (5.1V / 3A USB-C)": 5.00,
    "Microphones (Dual INMP441 I2S)": 2.20,
    "Audio Amp (MAX98357A + 3W Speaker)": 3.80,
    "Thermal (Passive Al Heatsink + 30mm Fan)": 2.50,
    "HMI (Arcade Button + RGB LED + Resistors)": 1.50,
    "Custom Acrylic / 3D Printed Enclosure": 4.50
}

# Architecture B: Orange Pi 5 Reality (High Speed, Expensive)
OPI5_BOM = {
    "SBC Compute Core (Orange Pi 5 16GB RK3588S)": 105.00,
    "High-Speed Storage (64GB eMMC 5.1 / NVMe)": 16.50,
    "Power Delivery (5V / 4A 20W DC Adapter)": 9.50,
    "Microphones (Dual INMP441 I2S Array)": 2.20,
    "Audio Amp (MAX98357A + Chamber Speaker)": 4.80,
    "Thermal (Solid Copper Heatsink + PWM Fan)": 5.50,
    "HMI (PTT Switch + Common-Cathode RGB LED)": 1.50,
    "Custom Anodized Aluminum Enclosure": 8.50
}

def analyze_bom():
    print("==========================================================")
    print(" VITA Week 5: Commercial Unit Economics & BOM Breakdown   ")
    print("==========================================================")
    print(f"Target Consumer Retail Price : {TARGET_RETAIL_PRICE_EUR:.2f} €\n")
    
    total_pi4 = sum(PI4_BOM.values())
    margin_pi4 = TARGET_RETAIL_PRICE_EUR / total_pi4
    
    print("--- Option A: Raspberry Pi 4 Model B (Initial Target) ---")
    for item, cost in PI4_BOM.items():
        print(f"  • {item:42s} : {cost:6.2f} €")
    print(f"  TOTAL HARDWARE BOM COST     : {total_pi4:6.2f} €")
    print(f"  HARDWARE GROSS MARKUP       : {margin_pi4:6.2f}X (Target: 5.0X - HEALTHY)")
    
    total_opi5 = sum(OPI5_BOM.values())
    margin_opi5 = TARGET_RETAIL_PRICE_EUR / total_opi5
    
    print("\n--- Option B: Orange Pi 5 / RK3588S (Current Reality) ---")
    for item, cost in OPI5_BOM.items():
        print(f"  • {item:42s} : {cost:6.2f} €")
    print(f"  TOTAL HARDWARE BOM COST     : {total_opi5:6.2f} €")
    print(f"  HARDWARE GROSS MARKUP       : {margin_opi5:6.2f}X (CRITICAL COMPRESSION!)")
    
    print("\n---------------- Financial Takeaway ------------------")
    print(f"  Gross Profit per Unit (Pi 4)  : +{TARGET_RETAIL_PRICE_EUR - total_pi4:.2f} € (Covers logistics, R&D, warranty)")
    print(f"  Gross Profit per Unit (OPi 5) : +{TARGET_RETAIL_PRICE_EUR - total_opi5:.2f} € (Vulnerable to retail margins & tariffs)")
    print("  STRATEGIC DECISION: Continue development on Orange Pi 5.")
    print("  We must validate the zero-latency user experience first,")
    print("  then optimize silicon costs in later production revisions.")
    print("==========================================================")

if __name__ == "__main__":
    analyze_bom()
