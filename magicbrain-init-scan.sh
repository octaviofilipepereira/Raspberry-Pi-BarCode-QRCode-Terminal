#!/bin/bash

####
#
# Init Script loading Raspberry Pi BarCode/QRCode Terminal
# Note that, all of this program intend to be run with non root user, i.e. pi (default user in raspberry pi)
#
####
#
# Last Modification: 24-08-2021
# Author: Octávio Filipe Gonçalves
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

clear
cd /home/pi/barcode-terminal
sudo python magicbrain-scan.py
