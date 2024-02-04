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

# is the relay board present on the I2C bus?
board.check()
# True

# start with all circuits on, all relays off
board.init()
# True

# is circuit A0 on? should be True
board.circuit(0)
# True

# is relay A0 on? should be False
board.relay(0)
# False

# turn on relay A0
board.relay(0, True)
# A0 blue LED on, relay trips

# turn off circuit A1
board.circuit(1, False)
# nothing happens, but now, toggling relay A1 has no effect

# turn on relay A1
board.relay(1, True)
# with circuit A1 off, relay A1 does not trip and blue LED remains off

# turn on circuit A1
board.circuit(1, True)
# since the relay A1 was on, A1 blue LED on, relay trips
# being able to control both relays and circuits means you can persist the
# relay states while being able to toggle their circuits independently

# turn off relay A0
board.relay(0, False)
# A0 blue LED off, relay off

# what circuits are on? should be all on
board.circuits()
# 65535
# 65535 == 0b_1111_1111_1111_1111 == 0xFFFF
# bit0 = circuit A0 on
# bit1 = circuit A1 on
# ...
# bit14 = circuit B6 on
# bit15 = circuit B7 on

#    Port B    Port A
#  | BBBB BBBB AAAA AAAA |
#  v 7654 3210 7654 3210 v
# 0b_1111_1111_1111_1111

# turn off circuit A0
board.circuit(0, False)
# nothing happens, the relay A0 was off

# what circuits are on? should be all except for A0
board.circuits()
# 65534
# 65534 == 0b_1111_1111_1111_1110 == 0xFFFE
# bit0 = circuit A0 off
# bit1 = circuit A1 on
# bit2 = circuit A2 on
# bit3 = circuit A3 on
# bit4 = circuit A4 on
# bit5 = circuit A5 on
# bit6 = circuit A6 on
# bit7 = circuit A7 on
# bit8 = circuit B0 on
# bit9 = circuit B1 on
# bit10 = circuit B2 on
# bit11 = circuit B3 on
# bit12 = circuit B4 on
# bit13 = circuit B5 on
# bit14 = circuit B6 on
# bit15 = circuit B7 on

# turn circuits A0-A3 on, circuits A4-A7,B0-B7 off
board.circuits(0x000F)

# what circuits are on now? should be A0-A3 on
board.circuits()
# 15
# 15 == 0b_0000_0000_0000_1111 == 0x000F
# bit0 = circuit A0 on
# bit1 = circuit A1 on
# bit2 = circuit A2 on
# bit3 = circuit A3 on
# bit4 = circuit A4 off
# bit5 = circuit A5 off
# bit6 = circuit A6 off
# bit7 = circuit A7 off
# bit8 = circuit B0 off
# bit9 = circuit B1 off
# bit10 = circuit B2 off
# bit11 = circuit B3 off
# bit12 = circuit B4 off
# bit13 = circuit B5 off
# bit14 = circuit B6 off
# bit15 = circuit B7 off

# what relays are on?
board.relays()
# 2
# 2 == 0b_0000_0000_0000_0010 = 0x0002
# bit0 = relay A0 off
# bit1 = relay A1 on
# bit2 = relay A2 off
# bit3 = relay A3 off
# bit4 = relay A4 off
# bit5 = relay A5 off
# bit6 = relay A6 off
# bit7 = relay A7 off
# bit8 = relay B0 off
# bit9 = relay B1 off
# bit10 = relay B2 off
# bit11 = relay B3 off
# bit12 = relay B4 off
# bit13 = relay B5 off
# bit14 = relay B6 off
# bit15 = relay B7 off

# turn all relays on
board.relays(65535)
# 65535 == 0b_1111_1111_1111_1111 == 0xFFFF
# A0 blue LED on, relay trips
# A1 blue LED on, relay trips
# ...
# B6 blue LED on, relay trips
# B7 blue LED on, relay trips

# half of the relays on
board.relays(0b_0101_0101_0101_0101)

# the other half of the relays on
board.relays(0b_1010_1010_1010_1010)

# turn all relays off
board.relays(0)

# turn all circuits off
board.circuits(0)

# turn some relays on
board.relays(0xCAFE)

# turn some circuits on
board.circuits(0xBEEF)

# disconnect yellow jumper J1
# all circuits turn off

# check relays, expecting 0xCAFE
board.relays()
# 51966
# 51966 == 0b_1100_1010_1111_1110 == 0xCAFE

# check circuits, expecting 0xBEEF
board.circuits()
# 48879
# 48879 == 0b_1011_1110_1110_1111 == 0xBEEF

# reconnect yellow jumper J1
# all circuits remain off, all relays on

# check relays, expecting 0xFFFF
board.relays()
# 65535
# 65535 == 0b_1111_1111_1111_1111 == 0xFFFF

# check circuits, expecting 0x0000
board.circuits()
# 0
# 0 == 0b_0000_0000_0000_0000 == 0x0000
