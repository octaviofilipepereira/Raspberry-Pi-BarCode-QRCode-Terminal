#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
####
#
# Raspberry Pi BarCode/QRCode Terminal v1.1.3
# This is a part of the BarCode Software Manager
# Submit readed data from barcode or qr code terminal to an API main server
#
####
#
# Last Modification: 24-08-2021
# Author: Octávio Filipe Gonçalves | Salustiano Silva
# Copyright: MagicBrain, Lda, OFPG, Lda
# Email: magicbrain at magicbrain.pt
#
####
#
# Licence: This program is license under GNU/GPL v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""

import os
import subprocess
import time
import I2C_LCD_driver
import sys
import curses
from curses import ascii
import serial

from config import config_get
from config import config_set
from psmapi import json_post_readout
from psmapi import json_response
from psmapi import json_post_checkin

clear = lambda: os.system('clear')

I2CBUS = 1 # i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
ADDRESS = 0x27 # LCD Address
lcd = I2C_LCD_driver.lcd(I2CBUS, ADDRESS)
lcd.clear()
lcd.backlightOn()

callSign = 'readout'

result, errorCode, errorText, apiEndPoint, terminalKey, requireAuth = config_get(callSign)

if apiEndPoint is None:
    apiEndPoint = 'EndPointUrlInterface'
    requireAuth = True
    result, errorCode, errorText, apiEndPoint, terminalKey, requireAuth = config_set(callSign, apiEndPoint, requireAuth)
if not result:
    lcd.clear()
    lcd.display(errorCode + errorText , 1)
    time.sleep(0.1)
else:
	lcd.clear()
	lcd.display("    LCD-COMPANY-NAME    ", 1)
	lcd.display(" By YOUR-NAME  ", 2)
	time.sleep(0.2)
	lcd.clear()
	lcd.display("   Waiting For   ", 1)
	lcd.display("BarCode", 2)
	time.sleep(0.2)

def main(stdscr):

    input_data = 1

while 1:
	input_data = raw_input()
	if input_data == "RELOADINTERFACE":
		lcd.clear()
		lcd.display("   Reloading   ", 1)
		lcd.display("   Interface   ", 2)
		time.sleep(1.5)
		lcd.clear()
		print(chr(27) + "[2J")
		os.execv(sys.executable, ['python'] + sys.argv)
	elif input_data == "SHUTDOWNINTERFACE":
		lcd.clear()
		print(chr(27) + "[2J")
		cmdCommand = "sudo shutdown -h now"
		process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
	else:
		inputCodeRead = json_post_readout(apiEndPoint=apiEndPoint, terminalId=0, terminalkey=terminalKey, requireAuth=False, barcodeReadout=input_data)
		outputLine1, outputLine2 = json_response(inputCodeRead)
		"""
		# Some Debug
		print outputLine1
		print outputLine2
		print(apiEndPoint)
		sys.exit()
		"""
		lcd.clear()
		"""
		# If we want to show the read input_data to lcd
		lcd.display("AF:" + input_data , 1)
		"""
		lcd.display("   Barcode Readed   ", 1)
		lcd.display("   Registering...   ", 1)
		lcd.clear()
		lcd.display(outputLine1 , 1)
		lcd.display(outputLine2 , 2)
		# print(chr(27) + "[2J")
		clear()
		time.sleep(0.2)

if __name__ == '__main__':
    curses.wrapper(main)
