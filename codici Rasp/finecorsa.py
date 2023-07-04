import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(12, GPIO.OUT) #led scivolidestra
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)# buzz

GPIO.setup(13, GPIO.IN)# fc1 centro
GPIO.setup(20, GPIO.IN)# fc2 destra
GPIO.setup(26, GPIO.IN)# fc3 sinistra
GPIO.setup(16, GPIO.IN)# fc4 dietro

while True:
	if (GPIO.input(16) ) == True:
		GPIO.output(6, GPIO.HIGH)
	
	GPIO.output(6, GPIO.LOW)
