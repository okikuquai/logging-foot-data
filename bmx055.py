#!/usr/bin/python3
# -*- coding: utf-8 -*-
import smbus
import time
from typing import Final

class BMX055:
    def __init__(self, bus=1, addr_acc=0x19, addr_gyro=0x69, addr_mag=0x13):
        self.bus = smbus.SMBus(bus)
        self.addr_acc = addr_acc
        self.addr_gyro = addr_gyro
        self.addr_mag = addr_mag

        # Initialize Accelerometer
        self.bus.write_byte_data(self.addr_acc, BMX055Command.ACCD_RANGE, 0x03)
        self.bus.write_byte_data(self.addr_acc, BMX055Command.ACCD_BW, 0x08)
        self.bus.write_byte_data(self.addr_acc, BMX055Command.ACCD_PMU_LPW, 0x00)
        self.bus.write_byte_data(self.addr_acc, BMX055Command.ACCD_PMU_LOW_POWER, 0x00)
        self.bus.write_byte_data(self.addr_acc, BMX055Command.ACCD_ACCD_HBW, 0x00)

        # Initialize Gyroscope
        self.bus.write_byte_data(self.addr_gyro, BMX055Command.GYR_RANGE, 0x04)
        self.bus.write_byte_data(self.addr_gyro, BMX055Command.GYR_BW, 0x07)
        self.bus.write_byte_data(self.addr_gyro, BMX055Command.GYR_LPM1, 0x00)
        self.bus.write_byte_data(self.addr_gyro, BMX055Command.GYR_LPM2, 0x80)

        # Initialize Magnetometer
        self.bus.write_byte_data(self.addr_mag, BMX055Command.MAG_POWER, 0x82)
        self.bus.write_byte_data(self.addr_mag, BMX055Command.MAG_OPMODE, 0x06)

    def readAccel(self):
        data = self.bus.read_i2c_block_data(self.addr_acc, BMX055Command.ACCD_X_LSB, 6)
        x = self.convert_data(data[0], data[1])
        y = self.convert_data(data[2], data[3])
        z = self.convert_data(data[4], data[5])
        return BMX055ACCELERATION(x, y, z)

    def readGyro(self):
        data = self.bus.read_i2c_block_data(self.addr_gyro, BMX055Command.GYR_X_LSB, 6)
        x = self.convert_data(data[1], data[0])
        y = self.convert_data(data[3], data[2])
        z = self.convert_data(data[5], data[4])
        return BMX055GYROSCOPE(x, y, z)

    def readMag(self):
        data = self.bus.read_i2c_block_data(self.addr_mag, BMX055Command.MAG_DATA_X_LSB, 6)
        x = self.convert_data(data[1], data[0])
        y = self.convert_data(data[3], data[2])
        z = self.convert_data(data[5], data[4])
        return [x, y, z]

    def convert_data(self, lsb, msb):
        value = (msb << 8) | lsb
        if value > 32767:
            value -= 65536
        return value

class BMX055ACCELERATION:
    x: Final[int]
    y: Final[int]
    z: Final[int]
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class BMX055GYROSCOPE:
    x: Final[int]
    y: Final[int]
    z: Final[int]
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class BMX055Command:
    # Accelerometer
    ACCD_X_LSB = 0x02
    ACCD_X_MSB = 0x03
    ACCD_Y_LSB = 0x04
    ACCD_Y_MSB = 0x05
    ACCD_Z_LSB = 0x06
    ACCD_Z_MSB = 0x07
    ACCD_Z_TEMP = 0x08
    ACCD_INT_STATUS_0 = 0x09
    ACCD_INT_STATUS_1 = 0x0A
    ACCD_INT_STATUS_2 = 0x0B
    ACCD_INT_STATUS_3 = 0x0C
    ACCD_FIFO_STATUS = 0x0E
    ACCD_RANGE = 0x0F
    ACCD_BW = 0x10
    ACCD_PMU_LPW = 0x11
    ACCD_PMU_LOW_POWER = 0x12
    ACCD_ACCD_HBW = 0x13
    ACCD_BGW_SOFTRESET = 0x14
    ACCD_INT_EN_0 = 0x16
    ACCD_INT_EN_1 = 0x17
    ACCD_INT_EN_2 = 0x18
    ACCD_INT_MAP_0 = 0x19
    ACCD_INT_MAP_1 = 0x1A
    ACCD_INT_MAP_2 = 0x1B
    ACCD_INT_SRC = 0x1E
    ACCD_INT_OUT_CTRL = 0x20
    ACCD_INT_RST_LATCH = 0x21
    ACCD_INT_0 = 0x22
    ACCD_INT_1 = 0x23
    ACCD_INT_2 = 0x24
    ACCD_INT_3 = 0x25
    ACCD_INT_4 = 0x26
    ACCD_INT_5 = 0x27
    ACCD_INT_6 = 0x28
    ACCD_INT_7 = 0x29
    ACCD_INT_8 = 0x2A
    ACCD_INT_9 = 0x2B
    ACCD_INT_A = 0x2C
    ACCD_INT_B = 0x2D
    ACCD_INT_C = 0x2E
    ACCD_INT_D = 0x2F
    ACCD_FIFO_CONFIG_0 = 0x30
    ACCD_PMU_SELF_TEST = 0x32
    ACCD_TRIM_NVM_CTRL = 0x33
    ACCD_BGW_SPI3_WDT = 0x34
    ACCD_OFC_CTRL = 0x36
    ACCD_OFC_SETTING = 0x37
    ACCD_OFC_OFFSET_X = 0x38
    ACCD_OFC_OFFSET_Y = 0x39
    ACCD_OFC_OFFSET_Z = 0x3A
    ACCD_TRIM_GP0 = 0x3B
    ACCD_TRIM_GP1 = 0x3C

    # Gyroscope
    GYR_X_LSB = 0x02
    GYR_X_MSB = 0x03
    GYR_Y_LSB = 0x04
    GYR_Y_MSB = 0x05
    GYR_Z_LSB = 0x06
    GYR_Z_MSB = 0x07
    GYR_INT_STATUS_0 = 0x09
    GYR_INT_STATUS_1 = 0x0A
    GYR_INT_STATUS_2 = 0x0B
    GYR_INT_STATUS_3 = 0x0C
    GYR_FIFO_STATUS = 0x0E
    GYR_RANGE = 0x0F
    GYR_BW = 0x10
    GYR_LPM1 = 0x11
    GYR_LPM2 = 0x12
    GYR_RATE_HBW = 0x13
    GYR_BGW_SOFTRESET = 0x14
    GYR_INT_EN_0 = 0x15
    GYR_INT_EN_1 = 0x16
    GYR_INT_MAP_0 = 0x18
    GYR_INT_MAP_1 = 0x19
    GYR_INT_MAP_2 = 0x1A
    GYR_INT_SRC_1 = 0x1B
    GYR_INT_SRC_2 = 0x1C
    GYR_INT_SRC_3 = 0x1D
    GYR_SOFTWARE_RST = 0x3F
    GYR_TAR_X_LSB = 0x42
    GYR_TAR_X_MSB = 0x43
    GYR_TAR_Y_LSB = 0x44
    GYR_TAR_Y_MSB = 0x45
    GYR_TAR_Z_LSB = 0x46
    GYR_TAR_Z_MSB = 0x47
    GYR_FIFO_CONFIG_0 = 0x3D
    GYR_FIFO_CONFIG_1 = 0x3E
    GYR_FIFO_DATA = 0x3F
    GYR_FIFO_STATUS_1 = 0x4A
    GYR_FIFO_STATUS_2 = 0x4B
    GYR_FIFO_STATUS_3 = 0x4C
    GYR_FIFO_STATUS_4 = 0x4D
    GYR_FIFO_STATUS_5 = 0x4E
    GYR_AUTO_GAIN_X = 0x50
    GYR_AUTO_GAIN_Y = 0x51
    GYR_AUTO_GAIN_Z = 0x52

    # Magnetometer
    MAG_DATA_X_LSB = 0x42
    MAG_DATA_X_MSB = 0x43
    MAG_DATA_Y_LSB = 0x44
    MAG_DATA_Y_MSB = 0x45
    MAG_DATA_Z_LSB = 0x46
    MAG_DATA_Z_MSB = 0x47
    MAG_RHALL_LSB = 0x48
    MAG_RHALL_MSB = 0x49
    MAG_INT_STATUS = 0x4A
    MAG_POWER = 0x4B
    MAG_OPMODE = 0x4C
    MAG_REP_XY = 0x51
    MAG_REP_Z = 0x52
    MAG_TRIM_START = 0x5C
    MAG_TRIM_END = 0x6A
    MAG_TRIM_DELTA = 0x71