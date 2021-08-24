#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
####
#
# Raspberry Pi BarCode/QRCode Terminal v1.1.3
# This is a part of the BarCode Software Manager
# Submit readed data from barcode or qr code to an API main server
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

import json
import hashlib
import uuid
import os


def config_get(callSign=''):
    """Return setup data from the configuration file.

    Return values:

    result      -- Operation sucess (True of False)

    errorCode   -- None | Error code to display

    errorText   -- None | Error text to display

    apiEndPoint -- None | URL for the POST/GET method

    terminalkey -- None | the terminal hash

    requireAuth -- None | if the server is password protected
    """

    configFile = "config.json"

    apiEndPoint = None
    terminalkey = None
    requireAuth = None

    try:

        #
        # Check if config.json already exists
        #

        if os.path.isfile('./' + configFile):

            with open(configFile) as json_file:

                config = json.load(json_file)

            if callSign in config:

                for ctg in config[callSign]:

                    if 'apiEndPoint' in ctg:
                        apiEndPoint = ctg['apiEndPoint']

                    if 'terminalkey' in ctg:
                        terminalkey = ctg['terminalkey']

                    if 'requireAuth' in ctg:
                        requireAuth = ctg['requireAuth']

        return True, None, None, apiEndPoint, terminalkey, requireAuth

    except Exception:

        errorCode = '0x999999999999999999999999'
        errorText = 'Config parsing error!     '

        return False, errorCode, errorText, None, None, None


def config_set(callSign='', apiEndPoint='', requireAuth=''):
    """Writes a configuration file with setup data.

    Saved values:

    apiEndPoint -- URL for the POST/GET method

    terminalkey -- the terminal hash

    requireAuth -- if the server is password protected
    """

    configFile = "config.json"

    try:

        #
        # Prefill values by trying to fetch from existing file
        #

        result, errorCode, errorText, curApiEndPoint, curTerminalkey, curRequireAuth = config_get(callSign)

        #
        # Preserve the terminal key
        #

        if curTerminalkey is not None:

            terminalkey = curTerminalkey

        else:

            terminalkey = uuid.uuid1()
            terminalkey = terminalkey.hex
            terminalkey = hashlib.sha256(terminalkey.encode('utf-8')).hexdigest()

        #
        # Set configuration values
        #

        config = {}

        config[callSign] = []

        config[callSign].append({
            'apiEndPoint': apiEndPoint,
            'terminalkey': terminalkey,
            'requireAuth': requireAuth
        })

        #
        # Write the config.json file
        # If the file does not exist, it gets created
        #

        with open(configFile, 'w+') as outfile:

            json.dump(config, outfile)

        return True, None, None, apiEndPoint, terminalkey, requireAuth

    except Exception as e:

        print(e)

        errorCode = "0x999999999999999999999999"
        errorText = "Unable to write config!"

        return False, errorCode, errorText, None, None, None
