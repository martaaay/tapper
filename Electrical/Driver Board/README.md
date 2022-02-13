Changes:
 - PCA9515B (i2c bus repeater) is currently SO-08 instead of TSSOP08
 - Need attachment lines for easy powering


Old Bugs:
The scheme of having one i2c line that goes to one motor driver and the 8-way i2c mux does not work because
the 8-way i2c mux exposes the i2c lines behind it to the master i2c line, which collides with the address of the one lone
motor sitting on the i2c line. In this scheme, to access a driver behind the mux, set EN for the I2C buffer to LOW and set the control
address on the MUX. To access the lone driver, set the control address on the MUX to 0 (no address exposed) and set EN on the I2C buffer to High.

Green LED info:
https://www.mouser.com/ProductDetail/638-192VGC 

