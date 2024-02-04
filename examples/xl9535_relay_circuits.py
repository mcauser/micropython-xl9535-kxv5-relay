# SPDX-FileCopyrightText: 2024 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython XL9535 KxV5 Relay
https://github.com/mcauser/micropython-xl9535-kxv5-relay
"""

import xl9535_relay
from machine import I2C, Pin

i2c = I2C(0)
board = xl9535_relay.XL9535_KXV5(i2c, 0x20)
board.init()

# turn all relays on
board.relays(0xFFFF)

# turn all circuits on
board.circuits(0xFFFF)

# turn circuit A0 off
board.circuit(0, False)
# relay A0 switches off

# turn circuit A1 off
board.circuit(1, False)
# relay A1 switches off

# what relays are on?
board.relays()
# 65535
# 65535 == 0b_1111_1111_1111_1111 == 0xFFFF
# all of them are on

# what circuits are on?
board.circuits()
# 65532
# 65532 == 0b_1111_1111_1111_1100 == 0xFFFC
# circuits A0 and A1 off, the rest on

# having two independent controls for each relay means one
# can store the desired relay state and the other can be used
# as a toggle without affecting the desired relay state
