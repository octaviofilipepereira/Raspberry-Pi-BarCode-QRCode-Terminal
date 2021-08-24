# Raspberry-Pi-BarCode-QRCode-Terminal

The Raspberry Pi BarCode/QRCode Terminal is a software that allows you to transform any raspberry pi into a bar code and/or QR Code reading terminal, automatically submitting the information read to an application with the respective API that interprets the data coming from the terminal. reading.

This software has been tested on Raspberry Pi 3b and 4 with Honeywell Genesis 7580g branded USB barcode reader and QR Code. 

# Instalation and Configuration

1. Configuring I2C
Run in Raspberry Pi terminal: 
> sudo raspi-config
  
  Follow this instructions: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
  

2. Put the software files wherever you want, in your Raspberry Pi. 

3. I sugest in PI user home dir. i.e.: /home/pi/barcode-terminal/

4. Test the software, after making this script executable (i.e.: chmod +x /home/pi/barcode-terminal/magicbrain-init-scan.sh):
  > bash /home/pi/barcode-terminal/magicbrain-init-scan.sh
  
5. Don't forget to change the path of the instalation dir, if you choose other location then the example above.
  
6. Run this software on Raspberry Pi startup:
> mv /home/pi/barcode-terminal/magicbrain-init-scan.sh /etc/init.d/ && sudo update-rc.d magicbrain-init-scan.sh defaults

7. Again, don't forget to change the path of the instalation dir, if you choose other location then the example above, located inside magicbrain-init-scan.sh file.
  
