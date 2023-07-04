import time
from time import sleep
import adafruit_vl6180x as vl6180
from libBNO055 import BNO055
from SERIALE import Serial
from SENS_DIST import VL6180X
from led import Led
import RPi.GPIO as GPIO





class Movimenti:
	
	
	
	def init(self):
		
		byte_fermo = self.byte_fermo = 0
		byte_avanti = self.byte_avanti = 1
		byte_destra = self.byte_destra = 5
		byte_sinistra = self.byte_sinistra = 6
		byte_indietro = self.byte_indietro = 2
		
		self.ser = Serial()
		
		
	
		self.bno = BNO055()
		if self.bno.begin() is not True:
			print("Error initializing device")
			exit()
	


	def destra(self):
		self.ser.write(self.byte_fermo)
		self.bno.begin()
		gradi = self.bno.readAngle()
		while (gradi < 85) or (356 <= gradi <= 360) or (gradi < 2) or (gradi > 361):
			self.ser.write(self.byte_destra)
			gradi = self.bno.readAngle()
			self.ser.read()
		# print(gradi)
		self.ser.write(self.byte_fermo)

		sleep(0.5)
		print("girato a destra")    

	def sinistra(self):
		ser.write(self.byte_fermo)
		self.bno.begin()
		gradi = self.bno.readAngle()
		while (gradi > 275) or (0 <= gradi <= 3) or (gradi < 2) or (gradi > 361):
			self.write(self.byte_sinistra)
			self.ser.read()
			gradi = self.bno.readAngle()
		self.ser.write(self.byte_fermo)
		sleep(0.5)
		print("girato a sinistra")
		
		
if __name__ == '__main__':  
	mov = Movimenti()
	mov.init()
	
	
	while True:
		#mov.destra()
		
		mov.ser.write(1)
		mov.ser.read()
		sleep(2)
		mov.ser.write(0)
		sleep(2)
		'''
			avanti = laser.read(0)
			
			#print(avanti)
			if(avanti<90):
				mov.ser.write(mov.byte_fermo)
				sleep(0.5)
				led.led_ON()
				mov.destra()
				
			else:
				mov.ser.write(mov.byte_avanti)
				mov.ser.read()
				led.led_OFF()
				
			#if (GPIO.input(13) or GPIO.input(20) or GPIO.input(26) ) == True:
			if(avanti<90):
				mov.ser.write(mov.byte_fermo)
				sleep(0.5)
				led.led_ON()
				mov.destra()
				
				while (GPIO.input(16)) == False:
					mov.ser.write(mov.byte_indietro)
					mov.ser.read()
					
					
			mov.ser.write(mov.byte_avanti)
			mov.ser.read()
			led.led_OFF()
		except KeyboardInterrupt:
			for i in range( 0, 5):
				mov.ser.write(mov.byte_fermo)
				led.led_OFF()
		 '''
		

