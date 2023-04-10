from movimenti import Sensore
from time import sleep
import board
import busio
import smbus
from smbus import SMBus
from servo import Servo
import digitalio
from PIL import Image, ImageDraw, ImageFont
import subprocess
import cv2
import numpy as np
import time
from PIL import Image
from nuove_camere import videocamere
import RPi.GPIO as GPIO
import multiprocessing




arduino = 0x10
bus = SMBus(1)
i2c = busio.I2C(board.SCL, board.SDA)
byte_stop = 0x17
byte_fermo = 0

servo = Servo()
sn = Sensore()
sp = videocamere()
sn.init()
servo.init()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)# buzz
GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(27, GPIO.OUT) #led scivolidestra

GPIO.setup(16, GPIO.IN) #DIETRO SINISTRA
GPIO.setup(20, GPIO.IN) # dietro mezzo
GPIO.setup(21, GPIO.IN) #dietro destra
GPIO.setup(26, GPIO.IN) #davanti destra
GPIO.setup(19, GPIO.IN) #davanti centro
GPIO.setup(13, GPIO.IN) #davanti sinistra

GPIO.output(23, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW)

Finecorsa_BS = 16
Finecorsa_BM = 20
Finecorsa_BD = 21
Finecorsa_FD = 26
Finecorsa_FM = 19
Finecorsa_FS = 13
LED_D = 27
LED_S = 22
BUZZ = 23
letto = 41

byte_aspetta5secvittima = 0x18
byte_riparti = 0x19

		
def movimento():
	while True:
		try:
			bus.write_byte(arduino, byte_riparti)
			sn.avvio()
			
		except Exception as e:
			print("errore movimento", e)

      
def video(queue):
	while True:
		try:
			img, img1 = sp.telecamere()
			lettera = sp.get_letter(img, 'sinistra')
			lettera1 = sp.get_letter(img1, 'destra')
			lettera_def = sp.definitivo(lettera, lettera1)
			if lettera_def != 40:
				queue.put(lettera_def)
			else:
				color = sp.get_color(img, 'sinistra')
				color1 = sp.get_color(img1, 'destra')
				color_def = sp.definitivo(color, color1)
				queue.put(color_def)
			
		except Exception as e:
			print("errore cam", e)
			
		
def H_sinistra():
	GPIO.output(LED_S, GPIO.HIGH)	
	print("H_S")
	sleep(0.5)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.sinistra()	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.sinistra()	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.sinistra()
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	sleep(0.5)
	GPIO.output(LED_S, GPIO.LOW)

def H_destra():	
	GPIO.output(LED_D, GPIO.HIGH)	
	print("H_D")
	sleep(0.5)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.destra()	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.destra()	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.destra()	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	sleep(0.5)
	GPIO.output(LED_D, GPIO.LOW)	




def S_sinistra():
	GPIO.output(LED_S, GPIO.HIGH)	
	print("S_S")
	sleep(0.5)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.sinistra()
	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_S, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_S, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.sinistra()
	
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

def S_destra():
	GPIO.output(LED_D, GPIO.HIGH)	
	print("S_D")
	sleep(0.5)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.destra()
	
	GPIO.output(BUZZ, GPIO.LOW)
	GPIO.output(LED_D, GPIO.LOW)
	sleep(0.5)
	
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(BUZZ, GPIO.HIGH)
	servo.destra()
	
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


	
def U_sinistra():
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
			
def U_destra():
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


def rosso_sinistra():
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
	servo.sinistra()	
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

def rosso_destra():
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
	servo.destra()	
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


def giallo_sinistra():
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
	servo.sinistra()	
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

def giallo_destra():
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
	servo.destra()	
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

def verde_sinistra():
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
	
def verde_destra():
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
	while True:
		try:
			queue = multiprocessing.Queue()
			p1 = multiprocessing.Process(target=movimento)
			p2 = multiprocessing.Process(target = video, args = (queue,))
			
			p1.start()
			p2.start()
			while True:
				GPIO.output(LED_D, GPIO.LOW)
				GPIO.output(LED_S, GPIO.LOW)
				variabile = queue.get()
				print(variabile)
				#print(pause_flag.value)
				byte_ritorno=0
				if variabile==1:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						giallo_sinistra()
						
					
				if variabile==2:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						rosso_sinistra()
						
					
				if variabile==3:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						verde_sinistra()
						
						
				if variabile==4:
					if (letto != variabile):
						
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						giallo_destra()
						
						
					
				if variabile==5:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						rosso_destra()
						
					
				if variabile==6:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						verde_destra()
						
						
						
						
						
						
				if variabile==7:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						U_sinistra()
						
						
				if variabile==8:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						H_sinistra()
						
						
				if variabile==9:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						S_sinistra()
						
						
				if variabile==10:
					if (letto != variabile):
					
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						U_destra()
						
						
				if variabile==11:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						H_destra()
						
					
						
				if variabile==12:
					if (letto != variabile):
						
						letto = variabile
						bus.write_byte(arduino, byte_aspetta5secvittima)
						S_destra()
						
						
				
						
			
				
			p1.join()
			p2.join()
		except Exception as e:
			 print("errore", e)
	
