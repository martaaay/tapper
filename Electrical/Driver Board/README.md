Changes:
 - Feed in from battery / USB. Power drv2605 directly off this line and add a 3v3 regular (TPS73633) for the pull up resistors and mux
 - Figure out how to add the one-off driver on the i2c line. See this chip for buffering i2c with EN pin: PCA9515B
 - Drop the display line
 - Add a small led for power


The scheme of having one i2c line that goes to one motor driver and the 8-way i2c mux does not work because
the 8-way i2c mux exposes the i2c lines behind it to the master i2c line, which collides with the address of the one lone
motor sitting on the i2c line.
