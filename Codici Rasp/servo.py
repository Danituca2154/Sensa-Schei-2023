import time

class Servo:

	
	def init(self):
		import pigpio
		self.SERVO = 18
		self.pi = pigpio.pi()
		self.pi.set_mode(self.SERVO, pigpio.OUTPUT)
		self.pi.set_servo_pulsewidth(self.SERVO, 1750) # posizione neutra
		
	def sinistra(self):
		self.pi.set_servo_pulsewidth(self.SERVO, 2200) # posizione massima
		time.sleep(0.5)
		self.pi.set_servo_pulsewidth(self.SERVO, 1750) # posizione neutra
		time.sleep(0.5)
	def destra(self):
		self.pi.set_servo_pulsewidth(self.SERVO, 1300) # posizione minima
		time.sleep(0.5)
		self.pi.set_servo_pulsewidth(self.SERVO, 1750) # posizione neutra
		time.sleep(0.5)

if __name__ == '__main__':
	servo = Servo()
	servo.init()
	while True:
		servo.sinistra()
		time.sleep(1)
		servo.destra()
		time.sleep(1)
