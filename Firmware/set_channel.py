#!/usr/bin/python

import smbus
import argparse

import TCA9548A

if __name__ == '__main__':
    
    bus_number=1       # 0 for rev1 boards etc.
    address=0x70
    
    plexer = TCA9548A.Multiplexer(1)
    plexer.set_channel(address,[0,1,2,3,4,5,6,7])
    
    print "Now run i2cdetect"

