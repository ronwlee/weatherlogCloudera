#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib.request
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from sense_hat import SenseHat

# Load BMP lib
# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import Adafruit_BMP.BMP085 as BMP085

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = BMP085.BMP085()

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

# Oauth JSON File
GDOCS_OAUTH_JSON       = '/home/tc/creds/IOTcloudera-0081d94ed370.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'WeatherLog'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30


def login_open_sheet(oauth_key_file, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		credentials = ServiceAccountCredentials.from_json_keyfile_name(
			oauth_key_file,
													['https://www.googleapis.com/auth/drive'])
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print ('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
		print ('Google sheet login failed with error:', ex)
		sys.exit(1)


print ('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print ('Press Ctrl-C to quit.')
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.
	temp = (sensor.read_temperature()*9/5+32)
	temp = round(temp, 1)
	pressure = (sensor.read_pressure())
	pressure = round(pressure, 1)
	altitude = (sensor.read_altitude())
	altitude = round(altitude, 1)
	sealevelPressure = (sensor.read_sealevel_pressure())
	sealevelPressure = round(sealevelPressure, 1)
	
	# Append the data in the spreadsheet, including a timestamp
	try:
#		print(datetime.datetime.now(), temp, pressure, altitude, sealevelPressure)
		worksheet.append_row([datetime.datetime.now().ctime(), temp,pressure,altitude,sealevelPressure])
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print ('Append error, logging in again')
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	# print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
