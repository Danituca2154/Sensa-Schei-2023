from time import sleep
import pigpio

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)# buzz
GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(27, GPIO.OUT) #led scivolidestra


GPIO.output(23, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW)


LED_D = 27
LED_S = 22
BUZZ = 6

class Servo:

	
	def init(self):
		self.SERVO = 18
		self.pi = pigpio.pi()
		self.pi.set_mode(self.SERVO, pigpio.OUTPUT)
		self.pi.set_servo_pulsewidth(self.SERVO, 1650) # posizione neutra
		
	def sinistra(self):
		self.pi.set_servo_pulsewidth(self.SERVO, 2200) # posizione massima
		sleep(0.5)
		self.pi.set_servo_pulsewidth(self.SERVO, 1650) # posizione neutra
		sleep(0.5)
	def destra(self):
		self.pi.set_servo_pulsewidth(self.SERVO, 1200) # posizione minima
		sleep(0.5)
		self.pi.set_servo_pulsewidth(self.SERVO, 1650) # posizione neutra
		sleep(0.5)
		
				
	def H_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("H_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def H_destra(self):	
		GPIO.output(LED_D, GPIO.HIGH)	
		print("H_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	

	def S_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("S_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def S_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("S_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		
	def U_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("U_S")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
				
	def U_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("U_D")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def rosso_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("Rosso_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def rosso_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("Rosso_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def giallo_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("Giallo_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def giallo_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("giallo_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def verde_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("Verde_S")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		
	def verde_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("Verde_D")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		

if __name__ == '__main__':
	servo = Servo()
	servo.init()
	while True:
		servo.rosso_destra()
		sleep(2)
		servo.rosso_sinistra()
		sleep(2)
		
		
