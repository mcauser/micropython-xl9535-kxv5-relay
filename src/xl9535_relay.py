"""
MicroPython XL9535 KxV5 Relay
https://github.com/mcauser/micropython-xl9535-kxv5-relay

Supports variants:
* XL9535-K1V5
* XL9535-K2V5
* XL9535-K4V5
* XL9535-K8V5
* XL9535-K16V5

MIT License
Copyright (c) 2024 Mike Causer
"""

__version__ = '1.0.0'

# registers
# XL9535_INPUT_PORT0 = const(0x00)
# XL9535_INPUT_PORT1 = const(0x01)
XL9535_OUTPUT_PORT0 = const(0x02)
# XL9535_OUTPUT_PORT1 = const(0x03)
XL9535_INVERSION_PORT0 = const(0x04)
# XL9535_INVERSION_PORT1 = const(0x05)
XL9535_CONFIG_PORT0 = const(0x06)
# XL9535_CONFIG_PORT1 = const(0x07)

class XL9535_KXV5:
	def __init__(self, i2c, address=0x20):
		self._i2c = i2c
		self._address = address
		self._buf2 = bytearray(2)
		self.init()

	def check(self):
		if self._i2c.scan().count(self._address) == 0:
			raise OSError(f'XL9535 not found at I2C address {self._address:#x}')
		return True

	def init(self):
		self._buf2[0] = 0x00
		self._buf2[1] = 0x00

		# set inversion off so reading INPUT_PORTx reads the same as OUTPUT_PORTx
		# saves having to XOR (n ^ 0xff) to invert on each read
		self._i2c.writeto_mem(self._address, XL9535_INVERSION_PORT0, self._buf2)

		# all relays (outputs) off (NC<->COM-x-NO), blue LED off
		# high bit means relay on (NC-x-COM<->NO), blue LED on
		self._i2c.writeto_mem(self._address, XL9535_OUTPUT_PORT0, self._buf2)

		# all circuits (configs) enabled
		# low bit means enabled
		self._i2c.writeto_mem(self._address, XL9535_CONFIG_PORT0, self._buf2)

	# get/set a single relay
	def relay(self, num, value=None):
		assert 0 <= num <= 15, 'num should be in range 0-15'
		p = num // 8
		b = 1 << (num % 8)
		self._i2c.readfrom_mem_into(self._address, XL9535_OUTPUT_PORT0, self._buf2)
		if value is None:
			# get relay status
			return self._buf2[p] & b == b
		else:
			# set relay status
			self._buf2[p] &= ~b  # unset bit
			if value:
				self._buf2[p] |= b  # reset bit
			self._i2c.writeto_mem(self._address, XL9535_OUTPUT_PORT0, self._buf2)

	# get/set a single circuit
	def circuit(self, num, value=None):
		assert 0 <= num <= 15, 'num should be in range 0-15'
		p = num // 8
		b = 1 << (num % 8)
		self._i2c.readfrom_mem_into(self._address, XL9535_CONFIG_PORT0, self._buf2)
		self._buf2[0] ^= 0xff
		self._buf2[1] ^= 0xff
		if value is None:
			# get circuit status
			return self._buf2[p] & b == b
		else:
			# set circuit status
			self._buf2[p] &= ~b  # unset bit
			if value:
				self._buf2[p] |= b  # reset bit
			self._buf2[0] ^= 0xff
			self._buf2[1] ^= 0xff
			self._i2c.writeto_mem(self._address, XL9535_CONFIG_PORT0, self._buf2)

	# get/set all relays
	def relays(self, value=None):
		self._i2c.readfrom_mem_into(self._address, XL9535_OUTPUT_PORT0, self._buf2)
		if value is None:
			# get all relays
			return (self._buf2[1] << 8) | self._buf2[0]
		else:
			# set all relays
			assert 0 <= value <= 65535, 'value should be in range 0-65535'
			self._buf2[0] = value
			self._buf2[1] = value >> 8
			self._i2c.writeto_mem(self._address, XL9535_OUTPUT_PORT0, self._buf2)

	# get/set all circuits
	def circuits(self, value=None):
		self._i2c.readfrom_mem_into(self._address, XL9535_CONFIG_PORT0, self._buf2)
		if value is None:
			# get all circuits
			return ((self._buf2[1] << 8) | self._buf2[0]) ^ 0xffff
		else:
			# set all circuits
			assert 0 <= value <= 65535, 'value should be in range 0-65535'
			self._buf2[0] = value ^ 0xff
			self._buf2[1] = (value >> 8) ^ 0xff
			self._i2c.writeto_mem(self._address, XL9535_CONFIG_PORT0, self._buf2)
