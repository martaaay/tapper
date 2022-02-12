#!/usr/bin/python

# DRV2605 reference: http://www.ti.com/lit/ds/symlink/drv2605.pdf
# MSP430TCH5E haptics library reference: http://www.ti.com/lit/ug/slau543/slau543.pdf

import signal
import sys
import time

import smbus
import TCA9548A

from Adafruit_LED_Backpack import Matrix8x8
import Adafruit_GPIO.I2C as I2C

bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
plexer = TCA9548A.Multiplexer(1)
mux_address=0x70
display = Matrix8x8.Matrix8x8(address=0x71, busnum=1)
display.clear()

#motorI = I2C.get_i2c_device(0x5a)

DRV2605_ADDR = 0x5A

DRV2605_REG_STATUS = 0x00
DRV2605_REG_MODE = 0x01
DRV2605_MODE_INTTRIG =  0x00
DRV2605_MODE_EXTTRIGEDGE =  0x01
DRV2605_MODE_EXTTRIGLVL =  0x02
DRV2605_MODE_PWMANALOG =  0x03
DRV2605_MODE_AUDIOVIBE =  0x04
DRV2605_MODE_REALTIME =  0x05
DRV2605_MODE_DIAGNOS =  0x06
DRV2605_MODE_AUTOCAL =  0x07

DRV2605_REG_RTPIN = 0x02
DRV2605_REG_LIBRARY = 0x03
DRV2605_REG_WAVESEQ1 = 0x04
DRV2605_REG_WAVESEQ2 = 0x05
DRV2605_REG_WAVESEQ3 = 0x06
DRV2605_REG_WAVESEQ4 = 0x07
DRV2605_REG_WAVESEQ5 = 0x08
DRV2605_REG_WAVESEQ6 = 0x09
DRV2605_REG_WAVESEQ7 = 0x0A
DRV2605_REG_WAVESEQ8 = 0x0B

DRV2605_REG_GO = 0x0C
DRV2605_REG_OVERDRIVE = 0x0D
DRV2605_REG_SUSTAINPOS = 0x0E
DRV2605_REG_SUSTAINNEG = 0x0F
DRV2605_REG_BREAK = 0x10
DRV2605_REG_AUDIOCTRL = 0x11
DRV2605_REG_AUDIOLVL = 0x12
DRV2605_REG_AUDIOMAX = 0x13
DRV2605_REG_RATEDV = 0x16
DRV2605_REG_CLAMPV = 0x17
DRV2605_REG_AUTOCALCOMP = 0x18
DRV2605_REG_AUTOCALEMP = 0x19
DRV2605_REG_FEEDBACK = 0x1A
DRV2605_REG_CONTROL1 = 0x1B
DRV2605_REG_CONTROL2 = 0x1C
DRV2605_REG_CONTROL3 = 0x1D
DRV2605_REG_CONTROL4 = 0x1E
DRV2605_REG_VBAT = 0x21
DRV2605_REG_LRARESON = 0x22

DRV2605_DEVICE_ID = {3: "DRV2605", 4: "DRV2604", 6: "DRV2604L", 7: "DRV2605L"}

def bRead(register):
  return bus.read_byte_data(DRV2605_ADDR, register)

def bWrite(register, value):
  return bus.write_byte_data(DRV2605_ADDR, register, value)

def readDeviceID():
  status = bRead(DRV2605_REG_STATUS)
  return DRV2605_DEVICE_ID[status >> 5]

def readStatus():
  status = bRead(DRV2605_REG_STATUS)
  if status & 0xF:
    return "abnormal"
  else:
    return "normal"

def enter_standby():
  bWrite(DRV2605_REG_MODE, 0x40)

def exit_standby():
  bWrite(DRV2605_REG_MODE, 0x00)


def selectLibrary(libraryValue):
  # Todo: this has the side effect of setting the HI_Z bit to 0 (which is the default value)
  # Read section 4.2 of http://www.ti.com/lit/ug/slau543/slau543.pdf to determine which library is the best fit for a given actuator
  bWrite(DRV2605_REG_LIBRARY, libraryValue)


def begin():
    for i in range(0, 9):
      print("Channel %s" % i)
      if i == 8:
          pass
          #status = motorI.readU8(DRV2605_REG_STATUS)
          #print("motorI device ID: %s" % DRV2605_DEVICE_ID[status >> 5])
          #print("motorI status: ")
          #if status & 0xF:
          #  print("abnormal")
          #else:
          #  print("normal")
      else:
          plexer.set_channel(mux_address,[i])
          try:
            print("DRV2605 device ID " + readDeviceID())
          except IOError:
            print("Not detected 1")
  
          try:
            print("DRV2605 status " + readStatus())
          except IOError:
            print("Not detected 2")

def shutdown():
  print('Exiting...')
  enter_standby()

def sigint_handler(signal, frame):
  shutdown()
  sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)
begin()
shutdown()
