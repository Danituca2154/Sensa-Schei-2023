import time
from time import sleep
import adafruit_vl6180x as vl6180
from libBNO055 import BNO055
from SERIALE import Serial
from SENS_DIST import VL6180X
from led import Led
import RPi.GPIO as GPIO




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(12, GPIO.OUT) #led scivolidestra
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)# buzz

GPIO.setup(13, GPIO.IN)# fc1 destra
GPIO.setup(20, GPIO.IN)# fc2 centro
GPIO.setup(26, GPIO.IN)# fc3 sinistra
GPIO.setup(16, GPIO.IN)# fc4 dietro

class Movimenti:
	
	
	
	def init(self):
		
		byte_fermo = self.byte_fermo = 0
		byte_avanti = self.byte_avanti = 1
		byte_destra = self.byte_destra = 5
		byte_sinistra = self.byte_sinistra = 6
		byte_indietro = self.byte_indietro = 2
		byte_prova = self.byte_prova = 33
		byte_provaa = self.byte_provaa = 34
		self.condizione=0
		self.costante = 1300
		self.ser= Serial()
		
		
	
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
		self.ser.write(self.byte_fermo)
		self.bno.begin()
		gradi = self.bno.readAngle()
		while (gradi > 275) or (0 <= gradi <= 3) or (gradi < 2) or (gradi > 361):
			self.ser.write(self.byte_sinistra)
			print(self.ser.read())
			gradi = self.bno.readAngle()
		self.ser.write(self.byte_fermo)
		sleep(0.5)
		print("girato a sinistra")
		
	def cm30(self):
		mov.ser.write(mov.byte_prova)
		while (self.condizione < 130):
			self.condizione = mov.ser.read()
			print(self.condizione)
			print('_________________________________________')
			
		mov.ser.write(mov.byte_fermo)
		self.condizione=0
		sleep(2)
		
		
if __name__ == '__main__':  
	mov = Movimenti()
	mov.init() 
	led = Led()
	laser = VL6180X()
	while True:
			mov.destra()
			'''
			avanti = laser.read(0)
			
			#print(avanti)
			if(avanti<90):
				mov.ser.write(mov.byte_fermo)
				sleep(0.5)
				led.led_ON()
				mov.destra()
				
			else:
				mov.ser.write(mov.byte_prova)
				print(mov.ser.read())
				led.led_OFF()
			'''
			'''	
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
			led.led_OFF()'''
		
		

