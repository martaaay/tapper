import smbus

class Multiplexer(object):
    def __init__(self, bus_number):
        self.bus = smbus.SMBus(bus_number)

    def set_channel(self, address=0x70,channels=[0]):  # values 0-3 indictae the channel, anything else (eg -1) turns off all channels

        channel_mask = 0
        for c in channels:
          channel_mask = channel_mask | (1<<c)
        self.bus.write_byte_data(address,0x04,channel_mask)  #0x04 is the register for switching channels 
