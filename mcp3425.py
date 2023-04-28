#!/usr/bin/python3
# -*- coding: utf-8 -*-
import smbus
import time
from typing import Final

class MCP3425:
    def __init__(self, bus=1, addr=0x68):
        self.bus = smbus.SMBus(bus)
        self.addr = addr

    def read(self):
        self.bus.write_byte(self.addr, 0x10)
        time.sleep(0.1)

        data = self.bus.read_i2c_block_data(self.addr, 0x00, 2)
        return self.convert_data(data[0], data[1])
    
    def convert_data(self, lsb, msb):
        value = ((msb << 8) | lsb) & 0xffff
        return value