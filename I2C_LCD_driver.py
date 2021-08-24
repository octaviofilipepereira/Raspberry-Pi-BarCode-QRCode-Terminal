#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

"""
###
#
# Raspberry Pi BarCode Terminal v1.1.3
#
###
#
# Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
# Made available under GNU GENERAL PUBLIC LICENSE
###
#
# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1
"""

import smbus
import time


class i2c_device:
    def __init__(self, port, addr):
        self.addr = addr
        self.bus = smbus.SMBus(port)

# Write a single command
    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        time.sleep(0.001)

# Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        time.sleep(0.001)

# Write a block of data
    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        time.sleep(0.001)

# Read a single byte
    def read(self):
        return self.bus.read_byte(self.addr)

# Read
    def read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)


class lcd:
    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    # flags for backlight control
    LCD_BACKLIGHT           = 0x08
    LCD_NOBACKLIGHT         = 0x00

    # display line addresses
    LCD_1ST_ROW             = 0x00
    LCD_2ND_ROW             = 0x40
    LCD_3RD_ROW             = 0x14
    LCD_4TH_ROW             = 0x54

    En = 0b00000100  # Enable bit
    Rw = 0b00000010  # Read/Write bit
    Rs = 0b00000001  # Register select bit

    # initializes objects and lcd
    def __init__(self, bus=1, addr=0x27):
        self.device = i2c_device(bus, addr)

        self.write(0x03)
        self.write(0x03)
        self.write(0x03)
        self.write(0x02)

        self.displayshift = (self.LCD_CURSORMOVE | self.LCD_MOVERIGHT)
        self.displaymode = (self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT)
        self.displaycontrol = (self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF)

        self.write(self.LCD_FUNCTIONSET | self.LCD_2LINE | self.LCD_5x8DOTS | self.LCD_4BITMODE)
        self.write(self.LCD_CLEARDISPLAY)
        self.write(self.LCD_CURSORSHIFT | self.displayshift)
        self.write(self.LCD_ENTRYMODESET | self.displaymode)
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)
        time.sleep(0.001)

    # clocks EN to latch command
    def strobe(self, data):
        self.device.write_cmd(data | self.En | self.LCD_BACKLIGHT)
        time.sleep(0.001)
        self.device.write_cmd(((data & ~self.En) | self.LCD_BACKLIGHT))
        time.sleep(0.001)

    def write_four_bits(self, data):
        self.device.write_cmd(data | self.LCD_BACKLIGHT)
        self.strobe(data)

    # write a command to lcd
    def write(self, cmd, mode=0):
        self.write_four_bits(mode | (cmd & 0xF0))
        self.write_four_bits(mode | ((cmd << 4) & 0xF0))

    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    # works!
    def writeChar(self, charValue):
        self.write(charValue, 1)
  
    # put string function with optional char positioning
    def display(self, string, line=1, col=0):
        if line <= 1:
            position = self.LCD_1ST_ROW + col
        elif line == 2:
            position = self.LCD_2ND_ROW + col
        elif line == 3:
            position = self.LCD_3RD_ROW + col
        elif line >= 4:
            position = self.LCD_4TH_ROW + col

        self.write(self.LCD_SETDDRAMADDR + position)

        for char in string:
            self.writeChar(ord(char))

    # prints several lines in the lcd
    def message(self, text):
        lineIndex = 1
        for line in text.splitlines():
            self.display(line, lineIndex)
            lineIndex += 1
    
    # clear lcd and set to home
    def clear(self):
        self.write(self.LCD_CLEARDISPLAY)
        self.write(self.LCD_RETURNHOME)

    def displayOn(self):
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def displayOff(self):
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursorOn(self):
        self.displaycontrol |= self.LCD_CURSORON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursorOff(self):
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blinkOn(self):
        self.displaycontrol |= self.LCD_BLINKON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blinkOff(self):
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def scrollDisplayLeft(self):
        self.displayshift = self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT
        self.write(self.LCD_CURSORSHIFT | self.displayshift)

    def scrollDisplayRight(self):
        self.displayshift = self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT
        self.write(self.LCD_CURSORSHIFT | self.displayshift)

    def leftToRight(self):
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscrollOn(self):
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscrollOff(self):
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def backlightOn(self):
        self.device.write_cmd(self.LCD_BACKLIGHT)

    def backlightOff(self):
        self.device.write_cmd(self.LCD_NOBACKLIGHT)

    # add custom characters (0 - 7)
    def createChar(self, fontdata):
        self.write(self.LCD_SETCGRAMADDR)
        for line in fontdata:
            for char in line:
                self.writeChar(char)

if __name__ == '__main__':
    try:
        print "Testing I2C_LCD_driver"

        import sys

        I2CBUS = 1  # i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
        ADDRESS = 0x27  # LCD Address

        lcd = lcd(I2CBUS, ADDRESS)

        lcd.display(" I2C_LCD_driver")

        time.sleep(2)  # 2 sec delay

        lcd.display("backlight on/off")
        time.sleep(1)
        lcd.backlightOff()
        time.sleep(1)
        lcd.backlightOn()
        time.sleep(1)
        lcd.clear()

        lcd.display(" display on/off")
        time.sleep(1)
        lcd.displayOff()
        time.sleep(1)
        lcd.displayOn()
        time.sleep(1)
        lcd.clear()

        lcd.display(" cursor on/off")
        time.sleep(1)
        lcd.cursorOn()
        time.sleep(2)
        lcd.cursorOff()
        time.sleep(1)
        lcd.clear()

        lcd.display("  blink on/off")
        time.sleep(1)
        lcd.blinkOn()
        time.sleep(2)
        lcd.blinkOff()
        time.sleep(1)
        lcd.clear()

        lcd.display("scroll display left ")
        time.sleep(0.8)
        lcd.scrollDisplayLeft()
        time.sleep(0.2)
        lcd.scrollDisplayLeft()
        time.sleep(0.2)
        lcd.scrollDisplayLeft()
        time.sleep(0.2)
        lcd.scrollDisplayLeft()
        time.sleep(0.8)

        lcd.display("scroll display right", 2)
        time.sleep(0.8)
        lcd.scrollDisplayRight()
        time.sleep(0.2)
        lcd.scrollDisplayRight()
        time.sleep(0.2)
        lcd.scrollDisplayRight()
        time.sleep(0.2)
        lcd.scrollDisplayRight()
        time.sleep(0.8)
        lcd.clear()

        lcd.display("  custom chars")
        time.sleep(1)
        lcd.clear()

        # let's define a custom icon, consisting of 6 individual characters
        # 3 chars in the first row and 3 chars in the second row
        fontdata1 = [
            # Char 0 - Upper-left
            [0x00, 0x00, 0x03, 0x04, 0x08, 0x19, 0x11, 0x10],
            # Char 1 - Upper-middle
            [0x00, 0x1F, 0x00, 0x00, 0x00, 0x11, 0x11, 0x00],
            # Char 2 - Upper-right
            [0x00, 0x00, 0x18, 0x04, 0x02, 0x13, 0x11, 0x01],
            # Char 3 - Lower-left
            [0x12, 0x13, 0x1b, 0x09, 0x04, 0x03, 0x00, 0x00],
            # Char 4 - Lower-middle
            [0x00, 0x11, 0x1f, 0x1f, 0x0e, 0x00, 0x1F, 0x00],
            # Char 5 - Lower-right
            [0x09, 0x19, 0x1b, 0x12, 0x04, 0x18, 0x00, 0x00],
            # Char 6 - my test
            [0x1f, 0x00, 0x04, 0x0e, 0x00, 0x1f, 0x1f, 0x1f],
        ]

        # Load logo chars (fontdata1)
        lcd.createChar(fontdata1)

        # Write first three chars to row 1 directly
        lcd.write(lcd.LCD_SETDDRAMADDR + lcd.LCD_1ST_ROW)
        lcd.writeChar(0)
        lcd.writeChar(1)
        lcd.writeChar(2)
        # Write next three chars to row 2 directly
        lcd.write(lcd.LCD_SETDDRAMADDR + lcd.LCD_2ND_ROW)
        lcd.writeChar(3)
        lcd.writeChar(4)
        lcd.writeChar(5)
        time.sleep(2)

        lcd.clear()

        # Now let's define some more custom characters
        fontdata2 = [
            # Char 0 - left arrow
            [0x01, 0x03, 0x07, 0x0f, 0x0f, 0x07, 0x03, 0x01],
            # Char 1 - left one bar
            [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
            # Char 2 - left two bars
            [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],
            # Char 3 - left 3 bars
            [0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c],
            # Char 4 - left 4 bars
            [0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e],
            # Char 5 - left start
            [0x00, 0x01, 0x03, 0x07, 0x0f, 0x1f, 0x1f, 0x1f],
            # Char 6 -
            # [ ],
        ]

        # Load logo chars from the second set
        lcd.createChar(fontdata2)

        block = chr(255)  # block character, built-in

        # display two blocks in columns 5 and 6 (i.e. AFTER pos. 4) in row 1
        # first draw two blocks on 5th column (cols 5 and 6), starts from 0
        lcd.display(block * 2, 1, 4)

        duration = 0.2  # define duration of sleep(x)
        # now draw cust. chars starting from col. 7 (pos. 6)

        pos = 6
        lcd.display(unichr(1), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(2), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(3), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(4), 1, pos)
        time.sleep(duration)
        lcd.display(block, 1, pos)
        time.sleep(duration)

        # and another one, same as above, 1 char-space to the right
        pos += 1  # increase column by one
        lcd.display(unichr(1), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(2), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(3), 1, pos)
        time.sleep(duration)
        lcd.display(unichr(4), 1, pos)
        time.sleep(duration)
        lcd.display(block, 1, pos)
        time.sleep(duration)

        # now again load first set of custom chars - smiley
        lcd.createChar(fontdata1)

        lcd.display(unichr(0), 1, 9)
        lcd.display(unichr(1), 1, 10)
        lcd.display(unichr(2), 1, 11)
        lcd.display(unichr(3), 2, 9)
        lcd.display(unichr(4), 2, 10)
        lcd.display(unichr(5), 2, 11)
        time.sleep(2)

        lcd.clear()
        lcd.display("Date:", 1)
        lcd.display("Time:", 2)

        datetime = time.strftime("%Y-%m-%d %Hh%Mm%Ss")
        old_datetime = datetime

        while True:
                lcd.display(datetime[:-9], 1, 6)
                lcd.display(datetime[11:], 2, 7)

                old_datetime = datetime

                while old_datetime == datetime:
                    time.sleep(0.1)
                    datetime = time.strftime("%Y-%m-%d %Hh%Mm%Ss")

    except KeyboardInterrupt:
        lcd.clear()
        lcd.backlightOff()
        print "Exiting"
        sys.exit()
