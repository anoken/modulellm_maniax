#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import os

# 各LEDの明るさを設定
def set_led(r=0, g=0, b=0):
    os.system(f"echo {r} > /sys/class/leds/R/brightness")
    os.system(f"echo {g} > /sys/class/leds/G/brightness")
    os.system(f"echo {b} > /sys/class/leds/B/brightness")

set_led(100, 100, 100)  # RGB全て100の明るさに設定


