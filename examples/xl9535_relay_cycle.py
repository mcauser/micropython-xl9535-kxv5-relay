# SPDX-FileCopyrightText: 2024 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython XL9535 KxV5 Relay
https://github.com/mcauser/micropython-xl9535-kxv5-relay
"""

import xl9535_relay
from machine import I2C, Pin
import time

i2c = I2C(0)
board = xl9535_relay.XL9535_KXV5(i2c, 0x20)
board.init()

# turn all relays on, one-by-one
for i in range(16):
    board.relays(1 << i)
    time.sleep_ms(200)

# turn all on
board.relays(0xFFFF)
time.sleep_ms(1000)

# turn all off
board.relays(0x0000)
