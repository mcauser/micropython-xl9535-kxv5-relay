import xl9535_relay
from machine import I2C, Pin
import time

i2c = I2C(0)
board = xl9535_relay.XL9535_KXV5(i2c, 0x20)
board.init()

# turn relay A0 on
board.relay(0, True)

# turn relay A1 on
board.relay(1, True)

# turn relay A2 on
board.relay(2, True)


# turn relay A0 off
board.relay(0, False)

# turn relay A1 off
board.relay(1, False)

# turn relay A2 off
board.relay(2, False)


# toggle A0 a few times
for _ in range(5):
	board.relay(0, True)
	time.sleep_ms(200)
	board.relay(0, False)
	time.sleep_ms(200)


# turn all relays on
board.relays(65535)

# turn all relays off
board.relays(0)
