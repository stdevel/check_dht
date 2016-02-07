#!/usr/bin/env python
# -*- coding: utf-8 -*-

# check_dht.py - Nagios/Icinga plugin for checking
# DHT humidity/temperature sensor connected using GPIO
#
# 2016 By Christian Stankowic
# <info at stankowic hyphen development dot net>
# https://github.com/stdevel
#

import sys
from optparse import OptionParser
import Adafruit_DHT
import logging



def process_values(temperature, humidity):
	#process temperature
	if options.warningTempThres == 0: temp = "OK"
	elif temperature < options.warningTempThres: temp = "OK"
	elif temperature > options.warningTempThres and temperature < options.criticalTempThres: temp = "WARNING"
	elif temperature > options.criticalTempThres: temp = "CRITICAL"
	
	#process humidity
	if options.warningHumiThres == 0: humi = "OK"
	elif humidity < options.warningHumiThres: humi = "OK"
	elif humidity > options.warningHumiThres and humidity < options.criticalHumiThres: humi = "WARNING"
	elif humidity > options.criticalHumiThres: humi = "CRITICAL"
	
	#set unit
	if options.tempUnit == "fahrenheit": unit = "°F"
	else: unit = "°C"
	
	#print result and exit based on state
	if options.tempOnly == True:
		print "{0}: temperature is {1} {2}".format(temp, temperature, unit)
	elif options.humiOnly == True:
		print "{0}: humidity is {1}%".format(humi, humidity)
	else:
		state = { 'OK': 0, 'WARNING': 1, 'CRITICAL': 2 }
		overall = temp
		if state[humi] > state[temp]: overall = humi
		print "{0}: temperature is {1} {2}, humidity is {3}% | temperature={4} humidity={5}".format(overall, temperature, unit, humidity, temperature, humidity)
		sys.exit(state[overall])



if __name__ == "__main__":
	#define description, version and load parser
	desc='''%prog is used to check temperature and humidity of DHT sensors such as DHT11, DHT22 and AM2302.
	
	Checkout the GitHub page for updates: https://github.com/stdevel/check_dht'''
	
	parser = OptionParser(description=desc,version="%prog version 0.1")
	
	#-d / --debug
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs (default: no)")
	
	#-H / --humidity-only
	parser.add_option("-H", "--humidity-only", dest="humiOnly", default=False, action="store_true", help="only checks humidity (default: no)")

	#-t / --temperature-only
	parser.add_option("-t", "--temperature-only", dest="tempOnly", default=False, action="store_true", help="only checks temperature (default: no)")

	#-T / --temperature-unit
	parser.add_option("-T", "--temperature-unit", dest="tempUnit", default="celsius", type="choice", action="store", metavar="[celsius|fahrenheit]", choices=["celsius","fahrenheit"], help="defines the unit for temperature (default: celsius)")
	
	#-g / --sensor-pin
	parser.add_option("-g", "--sensor-pin", dest="sensorPin", default=4, action="store", type="int", metavar="PIN", help="GPIO pin of the DHT sensor (default: 4)")
	
	#-s / --sensor-type
	parser.add_option("-s", "--sensor-type", dest="sensorType", default="DHT22", type="choice", action="store", metavar="[DHT11|DHT22|AM2302]", choices=["DHT11","DHT22","AM2302"], help="defines the sensor type (default: DHT22)")
	
	#-w / --warning-temperature
	parser.add_option("-w", "--warning-temperature", dest="warningTempThres", action="store", type="int", default=0, metavar="TEMPERATURE", help="Warning temperature threshold")
	
	#-c / --critical-temperature
	parser.add_option("-c", "--critical-temperature", dest="criticalTempThres", action="store", type="int", default=0, metavar="TEMPERATURE", help="Critical temperature threshold")
	
	#-W / --warning-humidity
	parser.add_option("-W", "--warning-humidity", dest="warningHumiThres", action="store", type="int", default=0, metavar="TEMPERATURE", help="Warning humidity threshold")
	
	#-C / --critical-humidity
	parser.add_option("-C", "--critical-humidity", dest="criticalHumiThres", action="store", type="int", default=0, metavar="TEMPERATURE", help="Critical humidity threshold")
	
        #parse arguments
        (options, args) = parser.parse_args()
	
	
	
	#load logger
	LOGGER = logging.getLogger('check_dht')
	if options.debug:
		logging.basicConfig(level=logging.DEBUG)
		LOGGER.setLevel(logging.DEBUG)
	else:
		logging.basicConfig()
		LOGGER.setLevel(logging.INFO)
	

        #show parameters
        if options.debug: LOGGER.debug(options)
	
	#abort if requires parameters not specified
	if (
		(options.tempOnly == True and options.warningTempThres == 0)
		or
		(options.tempOnly == True and options.criticalTempThres == 0)
		or
		(options.humiOnly == True and options.warningHumiThres == 0)
		or
		(options.humiOnly == True and options.criticalHumiThres == 0)
		or
		(options.tempOnly == False and options.humiOnly == False and (options.warningTempThres == 0 or options.criticalTempThres == 0 or options.warningHumiThres == 0 or options.criticalHumiThres == 0))
	):
		print "UNKNOWN: Warning and/or critical threshold(s) missing"
		sys.exit(3)
	
	#define and read sensor
	sensor_args = { 'DHT11': Adafruit_DHT.DHT11, 'DHT22': Adafruit_DHT.DHT22, 'AM2302': Adafruit_DHT.AM2302 }
	try:
		sensor = sensor_args[options.sensorType]
		humidity, temperature = Adafruit_DHT.read_retry(sensor, options.sensorPin)
		#convert to Fahrenheit if specified
		if options.tempUnit == "fahrenheit":
			temperature = temperature * 9/5.0 + 32
			LOGGER.debug("Converted to Fahrenheit: '" + str(temperature) + "'")
		#round values
		temperature = float('{0:0.1f}'.format(temperature))
		humidity = float('{0:0.1f}'.format(humidity))
		LOGGER.debug("Temperature is: " + str(temperature) + ", humidity is: " + str(humidity))
		#calculate result and die in a fire
		process_values(temperature, humidity)
	except RuntimeError as e:
		print "UNKNOWN: Error raised: '" + str(e) + "'"
		sys.exit(3)
