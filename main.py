#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bmx055
import mcp3425
import time
import csv

import datetime

now = datetime.datetime.now()
filename = now.strftime("%Y%m%d_%H%M%S") + ".csv"

if __name__ == '__main__':
    bmx055bus = bmx055.BMX055()
    mcp3425bus = mcp3425.MCP3425()

    csvfile = open('./data/' + filename, "w", newline="")
    try:
        print('If you want to stop logging, press Ctrl + C')
        writer = csv.writer(csvfile)
        writer.writerow(['Pressure','AccelX','AccelY','AccelZ','GyroX','GyroY','GyroZ', 'time'])
        while(True):
            accValue = bmx055bus.readAccel()
            gyroValue = bmx055bus.readGyro()
            pressureValue = mcp3425bus.read()

            writer.writerow([str(pressureValue), str(accValue.x) ,str(accValue.y) ,str(accValue.z) ,str(gyroValue.x) ,str(gyroValue.y) ,str(gyroValue.z), int(time.time())])
    except KeyboardInterrupt:
        print("\r\nKeyboardInterrupt")
    finally:
        csvfile.close()