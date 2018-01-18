import serial
import time
import math

data_request = "\x02DA\x0304"

class NOMonitor(object):
	"""Horiba NO-Monitor"""
	def __init__(self, tty):
		self.tty = tty
		self.NO  = 0.00
		self.NO2 = 0.00
		self.NOX = 0.00
		self.serial = serial.Serial()
		self.error = False
		self.data = "DATASTRING"

	def connect(self):
		self.serial = serial.Serial(self.tty)
		pass

	def disconnect(self):
		self.serial.close
		pass

	def update(self):

		time.sleep(1)
		self.serial.reset_input_buffer()   					#Reset Port
		self.serial.write(data_request.encode('ascii'))  	# Request DATA
		time.sleep(1)

		bytestoread = self.serial.inWaiting()
		msg = self.serial.read(bytestoread)
		self.data = msg

		NO_b = int(msg[10:15])
		NO_p = int(msg[15:18])


		NO2_b = int(msg[40:45])
		NO2_p = int(msg[45:48])


		NOX_b = int(msg[70:75])
		NOX_p = int(msg[75:78])

		if (bytestoread == 99 and str(msg[1:5].decode()) == 'MD03'): #Check DATA
			self.error = False
			self.NO  = round(NO_b  * math.pow(10,NO_p) ,2)
			self.NO2 = round(NO2_b * math.pow(10,NO2_p),2)
			self.NOX = round(NOX_b * math.pow(10,NOX_p),2)
		else:
			self.error = True


class O3Monitor(object):
	"""Horiba O3-Monitor"""
	def __init__(self, tty):
		self.tty = tty
		self.O3  = 0.00
		self.serial = serial.Serial()
		self.error = False
		self.data = "DATASTRING"

	def connect(self):
		self.serial = serial.Serial(self.tty)
		pass

	def disconnect(self):
		self.serial.close
		pass

	def update(self):

		print("updating!!!")
		
		time.sleep(1)
		self.serial.reset_input_buffer()   					#Reset Port
		self.serial.write(data_request.encode('ascii'))  	# Request DATA
		time.sleep(1)

		bytestoread = self.serial.inWaiting()
		msg = self.serial.read(bytestoread)
		self.data = msg

		O3_b = int(msg[10:15])
		O3_p = int(msg[15:18])
		
		if (bytestoread == 39 and str(msg[1:5].decode()) == 'MD01'): #Check DATA
			self.error = False
			self.O3    = round(O3_b * math.pow(10,O3_p),2)
		else:
			self.error = True


		
		