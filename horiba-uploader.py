#!/usr/bin/python3 -u

# -u option oben anhängen für ausgabe
#
import os
import horiba
import time
import datetime
import csv
import logging

from influxdb import InfluxDBClient


def output():
	print("NO:   %+4.2f" % NO.NO)
	print("NO2:  %+4.2f" % NO.NO2)
	print("NOx:  %+4.2f" % NO.NOX)

def UpdateInflux():
	influx_data = [
	{
	"measurement": "Alphasense_KF112",
	"tags": {
	"host": "TU-BERLIN",
	"Sensor": "HORIBA"
	},
	"fields": {
	"Horiba1_NO": NO.NO,
	"Horiba1_NO2": NO.NO2,
	"Horiba1_NOX": NO.NOX
		}
	}
	]
	if (
			NO.NO  < 2000
		and	NO.NO2 < 2000
		and	NO.NOX < 2000

                and     NO.NO  > -10
                and     NO.NO2 > -10
                and     NO.NOX > -10

	):
		client.write_points(influx_data)

logfile_enable = False
Influx_enable = True

if logfile_enable == True:
	LOG_FILENAME = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
	FORMAT = ('%(asctime)s, %(message)s')
	logging.basicConfig(format=FORMAT,datefmt='%Y-%m-%d_%H:%M:%S',filename=LOG_FILENAME, level=logging.DEBUG,)
	logging.getLogger("requests").setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)
	logging.debug("NO" + "," + "NO2" + "," +"NOX")

if Influx_enable == True:
	client = InfluxDBClient('130.149.67.141', 8086, 'messcontainer', 'Impaktor', 'ALPHASENSE')
	#client = InfluxDBClient('luftguete.dedyn.io/influxdb/', 443, 'messcontainer', 'Impaktor', 'MESSCONTAINER')


NO = horiba.NOMonitor('/dev/ttyUSB0')

update_freq = 10-2

NO.connect()

try:
	while True:
		NO.update()
		os.system('clear')
		output()

		if NO.error == False:
			if Influx_enable == True:
				UpdateInflux()
			if logfile_enable == True:
				logging.debug(str(NO.NO) + "," + str(NO.NO2) + "," + str(NO.NOX))
		else:
			print("Serial Error!")

		time.sleep(update_freq)

except KeyboardInterrupt:
	os.system('clear')

except Exception as e:
	print (e.message, e.args)

NO.disconnect()
print("disconnected...")
time.sleep(0.3)
exit()


