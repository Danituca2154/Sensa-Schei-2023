from libBNO055 import BNO055
from time import sleep
import RPi.GPIO as GPIO
import asyncio
import cv2
import numpy as np
import pytesseract
from PIL import Image
import time
import RPi.GPIO as GPIO
import random
from piastre import piastre
from multiprocessing import Process, Queue
from SERIALE import Serial
from SENS_DIST import VL6180X



class sensor:
	misura = None
	def define(self, pin = -1, address = -1):
		self.pin = pin
		self.address = address

class Sensore:
	import RPi.GPIO as GPIO
	def init(self):
		from time import sleep
		import board
		import busio
		import smbus
		from smbus import SMBus
		import adafruit_vl6180x
		import adafruit_tca9548a
		from libBNO055 import BNO055
		import random
		
		#import RPi.GPIO as GPIO
	
		self.ser= Serial()
		
		self.piastre = piastre()
		self.laser = VL6180X
		
		
		self.bno = BNO055()
		
		while self.bno.begin() is not True:
			print("Error initializing device")
			self.bno.begin()
		
		self.GPIO.setmode(GPIO.BCM)
		self.GPIO.setwarnings(False)
		self.GPIO.setup(6, GPIO.OUT)# buzz
		self.GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
		self.GPIO.setup(12, GPIO.OUT)#led scivolidestra

		self.GPIO.setup(13, GPIO.IN)# fc1 destra
		self.GPIO.setup(20, GPIO.IN)# fc2 centro
		self.GPIO.setup(26, GPIO.IN)# fc3 sinistra
		self.GPIO.setup(16, GPIO.IN)# fc4 dietro
		
		
		self.GPIO.output(6, GPIO.LOW)
		self.GPIO.output(12, GPIO.LOW)
		self.GPIO.output(22, GPIO.LOW)

		
		self.Finecorsa_BM = 16
		
		self.Finecorsa_FD = 13
		self.Finecorsa_FM = 20
		self.Finecorsa_FS = 23
		self.LED_D = 12
		self.LED_S = 22
		self.BUZZ = 6
		check = 0
		self.sus = 0
		self.assedritto = 0
		self.stato = 0
		self.byte_fermo = 0
		self.byte_avanti = 1
		self.byte_30cm = 2
		self.byte_5cm = 3
		self.byte_destra = 5
		self.byte_sinistra = 6
		self.byte_indietro = 7
		self.byte_correzzione_destra = 8
		self.byte_correzzione_sinistra = 9
		self.byte_carroarmato_destra = 11
		self.byte_carroarmato_sinistra = 12
		self.byte_ripartidestra = 13
		self.byte_ripartisinistra = 14
		self.byte_addossoalmurosinistra = 15
		self.byte_addossoalmurodestra = 16
		self.byte_stop = 17
		self.byte_aspetta5secvittima = 18
		self.byte_10cmindietro = 28
		self.byte_sinistralenta = 21
		self.byte_destralenta = 22
		self.byte_ostacolosinistra = 23
		self.byte_ostacolodestra = 24
		self.byte_salita_discesa = 25
		self.byte_correzzione_destra = 26
		self.byte_correzzione_sinistra = 27
		self.byte_stopd = 31
		self.byte_stopsi = 32
		self.byte_att = 0
		self.bytearduino = 0
		
		self.c = 0
		self.conteggio = 0
		self.conteggio2 = 0
		self.controllo = 0
		self.controllopiastre = 0
		self.nero=0
		self.xavier = 0
		self.condizione = 0
		
		
	
	
		
	
	def sensori_check(self):
		check=0
		self.inclinazione = self.bno.inclinazione()
		#destra
		#if(self.ds_fronte.range<120) and (self.ds_sinistra_davanti.range<160) and (self.ds_destra_davanti.range>120) and (self.ds_destra_dietro.range>120):   #per fare girare a destra
		if(self.read(0)<120) and (self.read(1)<160) and (self.read(2)>120) and (self.read(3)>120):   #per fare girare a destra
			check=1
			self.controllo = 1
		#sinistra
		#elif(self.ds_fronte.range<120) and (self.ds_destra_davanti.range<160) and (self.ds_sinistra_davanti.range>120) and (self.ds_sinistra_dietro.range>120): #per girare a sinistra
		elif (self.read(0)<120) and (self.read(2)<160) and (self.read(1)>120) and (self.read(4)>120):
			check=2
			self.controllo = 1
		#solo muro--> destra
		elif(self.read(0)<120) and (self.read(2)>120) and (self.read(1)>120):  # solo muro
			check=3
			self.controllo = 1
		#davanti libero, destra libera, sinistra libera, retro libero  --> destra
		elif(self.read(0) > 190) and (self.read(2)>160) and (self.read(3)>160) and (self.read(1)>160) and (self.read(3).range>160) and (self.read(5)>160) and self.controllo==0:
			check=4
			self.controllo=1
		#davanti libero, destra libera, sinistra occupata, retro libero --> destra
		elif(self.read(0)> 190) and (self.read(2)>120) and (self.read(3)>120) and (self.read(1)<160) and (self.read(4)<160) and (self.read(5)>120) and self.controllo==0:
			check=5
			self.controllo=1
		#davanti libero, destra occupata, sinistra libera, retro libero -->30cm
		elif(self.read(0)> 190) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)>160) and (self.read(4)>160) and (self.read(5)>120) and self.controllo==0:
			check=8
			self.controllo=1
			self.controllopiastre=0
		#davanti libero, destra occupata, sinistra occupata, retro libero --> 30cm
		elif(self.read(0)>190) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)<160) and (self.read(4)<160) and self.controllo==0:  # solo muro
			check=100
			self.controllo = 1
			self.controllopiastre=0
		#tiene conto di una salita e quindi la macchina non torna indietro
		elif(self.read(5).range<120) and (self.inclinazione>12):
			check=100
			self.controllopiastre=0
		#riposizionamento (retro occupato)
		elif(self.read(5).range<120) and (self.c==0) and (self.inclinazione<12) and (self.read(2)>120) and (self.read(3)>120) and (self.read(1)>120) and (self.read(4)>120):
			check=6
		#vicolo cieco--> destra destra
		elif(self.read(0)<120) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)<160) and (self.read(4)<160):  #vicolo cieco
			check=7
		
		else:
			check=100
			
		if (self.read(0) < 130 and self.read(0) > 100):
			check=10
			self.controllopiastre=0
		return check
		
		
	def sensori_check_sinistra(self):
		check=0
		self.inclinazione = self.bno.inclinazione()
		#destra
		#if(self.ds_fronte.range<120) and (self.ds_sinistra_davanti.range<160) and (self.ds_destra_davanti.range>120) and (self.ds_destra_dietro.range>120):   #per fare girare a destra
		if(self.read(0)<120) and (self.read(1)<160) and (self.read(2)>120) and (self.read(3)>120):   #per fare girare a destra
			check=1
			self.controllo = 1
		#sinistra
		#elif(self.ds_fronte.range<120) and (self.ds_destra_davanti.range<160) and (self.ds_sinistra_davanti.range>120) and (self.ds_sinistra_dietro.range>120): #per girare a sinistra
		elif (self.read(0)<120) and (self.read(2)<160) and (self.read(1)>120) and (self.read(4)>120):
			check=2
			self.controllo = 1
		#solo muro--> destra
		elif(self.read(0)<120) and (self.read(2)>120) and (self.read(1)>120):  # solo muro
			check=3
			self.controllo = 1
		#davanti libero, destra libera, sinistra libera, retro libero  --> destra
		elif(self.read(0) > 190) and (self.read(2)>160) and (self.read(3)>160) and (self.read(1)>160) and (self.read(3).range>160) and (self.read(5)>160) and self.controllo==0:
			check=4
			self.controllo=1
		#davanti libero, destra libera, sinistra occupata, retro libero --> destra
		elif(self.read(0)> 190) and (self.read(2)>120) and (self.read(3)>120) and (self.read(1)<160) and (self.read(4)<160) and (self.read(5)>120) and self.controllo==0:
			check=5
			self.controllo=1
		#davanti libero, destra occupata, sinistra libera, retro libero -->30cm
		elif(self.read(0)> 190) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)>160) and (self.read(4)>160) and (self.read(5)>120) and self.controllo==0:
			check=8
			self.controllo=1
			self.controllopiastre=0
		#davanti libero, destra occupata, sinistra occupata, retro libero --> 30cm
		elif(self.read(0)>190) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)<160) and (self.read(4)<160) and self.controllo==0:  # solo muro
			check=100
			self.controllo = 1
			self.controllopiastre=0
		#tiene conto di una salita e quindi la macchina non torna indietro
		elif(self.read(5).range<120) and (self.inclinazione>12):
			check=100
			self.controllopiastre=0
		#riposizionamento (retro occupato)
		elif(self.read(5).range<120) and (self.c==0) and (self.inclinazione<12) and (self.read(2)>120) and (self.read(3)>120) and (self.read(1)>120) and (self.read(4)>120):
			check=6
		#vicolo cieco--> destra destra
		elif(self.read(0)<120) and (self.read(2)<160) and (self.read(3)<160) and (self.read(1)<160) and (self.read(4)<160):  #vicolo cieco
			check=7
		
		else:
			check=100
			
		if (self.read(0) < 130 and self.read(0) > 100):
			check=10
			self.controllopiastre=0
		return check
		
	
	
	def destra(self):
		self.ser.write(self.byte_fermo)
		self.bno.begin()
		gradi = self.bno.readAngle()
		while (gradi < 81) or (358 <= gradi <= 360) or (gradi < 1) or (gradi > 361):
			self.ser.write(self.byte_destra)
			gradi = self.bno.readAngle()
		self.ser.write(self.byte_fermo)
		print("girato a destra")
		

	def sinistra(self):
		self.ser.write(self.byte_fermo)
		self.bno.begin()
		gradi = self.bno.readAngle()
		while (gradi > 277) or (0 <= gradi <= 2) or (gradi < 1) or (gradi > 361):
			self.ser.write(self.byte_sinistra)
			gradi = self.bno.readAngle()
		
		self.ser.write(self.byte_fermo)
		sleep(0.5)
		print("girato a sinistra")
		return 'sinistra'
		
	def riposizionamento(self):
		# while (GPIO.input(self.Finecorsa_BS) and GPIO.input(self.Finecorsa_BM) and GPIO.input(self.Finecorsa_BD)) == False:
		while (GPIO.input(self.Finecorsa_BM) == False) and self.bytearduino != 69:
			self.ser.write(self.byte_indietro)
		self.ser.write(self.byte_fermo)
		sleep(0.1)
		self.ser.write(self.byte_5cm)
		
		self.c = self.ser.read()
		if self.c == 0x6:
			self.ser.write(self.byte_fermo)
			sleep(0.1)
			
			
	def inmezzo(self):
		print("in mezzo")
		#caso in cui è storta:
		self.inclinazione = self.bno.inclinazione()
		if -5<self.inclinazione<5:
			if(self.ds_sinistra_davanti.range <120 and self.ds_sinistra_dietro.range>90 and self.ds_sinistra_dietro.range<160):
				while((self.ds_sinistra_davanti.range/self.ds_sinistra_dietro.range)<0.95) and self.bytearduino != 69:
					if self.byte_att != self.byte_carroarmato_destra:
						self.byte_att = self.byte_carroarmato_destra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_sinistra_dietro.range <120 and self.ds_sinistra_davanti.range>90 and self.ds_sinistra_davanti.range<160):
				while((self.ds_sinistra_dietro.range/self.ds_sinistra_davanti.range)<0.95):
					if self.byte_att != self.byte_carroarmato_sinistra:
						self.byte_att = self.byte_carroarmato_sinistra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_destra_davanti.range <120 and self.ds_destra_dietro.range>90 and self.ds_destra_dietro.range<160):
				while((self.ds_destra_davanti.range/self.ds_destra_dietro.range)<0.95):
					if self.byte_att != self.byte_carroarmato_sinistra:
						self.byte_att = self.byte_carroarmato_sinistra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_destra_dietro.range <120 and self.ds_destra_davanti.range>90 and self.ds_destra_davanti.range<160):
				while((self.ds_destra_dietro.range/self.ds_destra_davanti.range)<0.95):
					if self.byte_att != self.byte_carroarmato_destra:
						self.byte_att = self.byte_carroarmato_destra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			#----------------------------------------------------------------------------------------------------------------------------------------------------
			#caso in cui è troppo vicina o lontana dai muri:
			if(self.ds_destra_dietro.range <70 and self.ds_destra_davanti.range<70):
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi > 340) or (0 <= gradi <= 2) or (gradi < 1) or (gradi > 361):
					if (self.byte_att != self.byte_sinistra):
						self.byte_att = self.byte_sinistra
						self.bus.write_byte(self.arduino, self.byte_sinistra)
					gradi = self.bno.readAngle()
					if 200<gradi<340:
						if (self.byte_att != self.byte_stopsi):
							self.byte_att = self.byte_stopsi
							self.bus.write_byte(self.arduino, self.byte_stopsi)
				if (self.byte_att != self.byte_fermo):
					self.byte_att = self.byte_fermo
					self.bus.write_byte(self.arduino, self.byte_fermo)
				while ((self.ds_destra_davanti.range/self.ds_destra_dietro.range)>1.05):
					if self.byte_att != self.byte_carroarmato_destra:
						self.byte_att = self.byte_carroarmato_destra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
				if (self.byte_att != self.byte_fermo):
					self.byte_att = self.byte_fermo
					self.bus.write_byte(self.arduino, self.byte_fermo)
					sleep(0.1)
				
			if(self.ds_sinistra_dietro.range <70 and self.ds_sinistra_davanti.range<70):
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi < 20) or (358 <= gradi <= 360) or (gradi < 1) or (gradi > 361):
					if (self.byte_att != self.byte_destra):
						self.byte_att = self.byte_destra
						self.bus.write_byte(self.arduino, self.byte_destra)
					gradi = self.bno.readAngle()
					if gradi>20:
						if (self.byte_att != self.byte_stopd):
							self.byte_att = self.byte_stopd
							self.bus.write_byte(self.arduino, self.byte_stopd)
				if (self.byte_att != self.byte_fermo):
					self.byte_att = self.byte_fermo
					self.bus.write_byte(self.arduino, self.byte_fermo)
				while ((self.ds_sinistra_davanti.range/self.ds_sinistra_dietro.range)>1.05):
					
					if self.byte_att != self.byte_carroarmato_sinistra:
						self.byte_att = self.byte_carroarmato_sinistra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
				if (self.byte_att != self.byte_fermo):
					self.byte_att = self.byte_fermo
					self.bus.write_byte(self.arduino, self.byte_fermo)
					sleep(0.1) 
			if(self.ds_sinistra_dietro.range >110 and self.ds_sinistra_davanti.range>110 and self.ds_sinistra_dietro.range <165 and self.ds_sinistra_davanti.range<165):
				self.sinistra()
				while(self.ds_fronte.range > 80) and self.bytearduino != 69:
					self.bus.write_byte(self.arduino, self.byte_avanti)
				self.bus.write_byte(self.arduino, self.byte_fermo)
				self.destra()
			if(self.ds_destra_dietro.range >110 and self.ds_destra_davanti.range>110 and self.ds_destra_dietro.range <165 and self.ds_destra_davanti.range<165):
				self.destra()
				while(self.ds_fronte.range > 80) and self.bytearduino != 69:
					self.bus.write_byte(self.arduino, self.byte_avanti)
				self.bus.write_byte(self.arduino, self.byte_fermo)
				self.sinistra()
			  
			#-----------------------------------------------------------------------------------------------------------------------------------------------------
			#caso in cui è storta:
			if(self.ds_sinistra_davanti.range <100 and self.ds_sinistra_dietro.range>90 and self.ds_sinistra_dietro.range<160):
				while((self.ds_sinistra_davanti.range/self.ds_sinistra_dietro.range)<0.93):
					if self.byte_att != self.byte_carroarmato_destra:
						self.byte_att = self.byte_carroarmato_destra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_sinistra_dietro.range <100 and self.ds_sinistra_davanti.range>90 and self.ds_sinistra_davanti.range<160):
				while((self.ds_sinistra_dietro.range/self.ds_sinistra_davanti.range)<0.93):
					if self.byte_att != self.byte_carroarmato_sinistra:
						self.byte_att = self.byte_carroarmato_sinistra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_destra_davanti.range <100 and self.ds_destra_dietro.range>90 and self.ds_destra_dietro.range<160):
				while((self.ds_destra_davanti.range/self.ds_destra_dietro.range)<0.93):
					if self.byte_att != self.byte_carroarmato_sinistra:
						self.byte_att = self.byte_carroarmato_sinistra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)
			if(self.ds_destra_dietro.range <100 and self.ds_destra_davanti.range>90 and self.ds_destra_davanti.range<160):
				while((self.ds_destra_dietro.range/self.ds_destra_davanti.range)<0.93):
					if self.byte_att != self.byte_carroarmato_destra:
						self.byte_att = self.byte_carroarmato_destra
						self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
					self.bytearduino = self.bus.read_byte(self.arduino)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			sleep(0.1)      
		
	ferma_cicli = False
	async def first_task(self):
		byte_ritorno = 0
		ferma_cicli = False
		while (self.ferma_cicli == False):
			byte_ritorno = self.bus.read_byte(self.arduino)
			#print(byte_ritorno)  
			await asyncio.sleep(0.001)
			if byte_ritorno == 5:
				self.ferma_cicli = True
				self.byte_att = self.byte_stop
				self.bus.write_byte(self.arduino, self.byte_stop)
				break
		self.byte_att = self.byte_stop
		self.bus.write_byte(self.arduino, self.byte_stop)      
		#print("finito1")
		return byte_ritorno

	async def second_task(self):
		sus = 0
		suk = 1
		sup = 1
		while (self.ferma_cicli == False):
			self.inclinazione = self.bno.inclinazione()
			try:
				self.nero = self.piastre.prova()
			except Exception as e:
				print ("errore", e)
				self.nero=0
				self.byte_att = self.byte_stop
				self.bus.write_byte(self.arduino, self.byte_stop)
				sleep(0.1)
			if self.nero==3:
				sus = 6
				print("piastra nera")
				self.condizione = 1
				self.ferma_cicli = True
			if (GPIO.input(self.Finecorsa_FD) == True or GPIO.input(self.Finecorsa_FM) == True or GPIO.input(self.Finecorsa_FS) == True):
				self.byte_att = self.byte_stop
				self.bus.write_byte(self.arduino, self.byte_stop)
				sus = 5
				print("eccoococo")
				self.condizione = 2
				self.ferma_cicli = True
			if (self.inclinazione < -20):
				print("discesa")
				while (self.inclinazione<-4) or (self.inclinazione<-30) or (self.inclinazione>30) or (self.inclinazione ==-0.0625):
					if (self.ds_destra_davanti.range<90) and (self.ds_destra_dietro.range<90) and (self.ds_sinistra_davanti.range<90 and self.ds_sinistra_davanti.range<90):
						if self.byte_att !=  self.byte_salita_discesa:
							self.byte_att = self.byte_salita_discesa
							sus = 5
					if (self.ds_destra_davanti.range<80) and (self.ds_destra_dietro.range<80):
						if self.byte_att !=  self.byte_correzzione_destra:
							self.byte_att = self.byte_correzzione_destra
							self.bus.write_byte(self.arduino, self.byte_correzzione_destra)
					if (self.ds_sinistra_davanti.range<80) and (self.ds_sinistra_dietro.range<80):
						if self.byte_att !=  self.byte_correzzione_sinistra:
							self.byte_att = self.byte_correzzione_sinistra
							self.bus.write_byte(self.arduino, self.byte_correzzione_sinistra)
					self.inclinazione = self.bno.inclinazione()
				if (self.byte_att != self.byte_5cm):
				   self.byte_att = self.byte_5cm
				   self.bus.write_byte(self.arduino, self.byte_5cm)
				   self.bus.write_byte(self.arduino, 0x1)
				   self.c = (self.bus.read_byte(self.arduino))
				if self.c == 0x6:
				   self.byte_att = self.byte_fermo
				   self.bus.write_byte(self.arduino, self.byte_fermo)
				   sleep(0.1)
				self.condizione = 3
				self.ferma_cicli = True
			if (self.inclinazione > 15):
				print("salita")
				while (self.inclinazione>3.5) or (self.inclinazione<-30) or (self.inclinazione>30) or (self.inclinazione ==-0.0625):
					if (self.ds_destra_davanti.range<90) and (self.ds_destra_dietro.range<90) and (self.ds_sinistra_davanti.range<90 and self.ds_sinistra_davanti.range<90):
						if self.byte_att !=  self.byte_salita_discesa:
							self.byte_att = self.byte_salita_discesa
							sus = 5
					if (self.ds_destra_davanti.range<80) and (self.ds_destra_dietro.range<80):
						if self.byte_att !=  self.byte_correzzione_destra:
							self.byte_att = self.byte_correzzione_destra
							self.bus.write_byte(self.arduino, self.byte_correzzione_destra)
					if (self.ds_sinistra_davanti.range<80) and (self.ds_sinistra_dietro.range<80):
						if self.byte_att !=  self.byte_correzzione_sinistra:
							self.byte_att = self.byte_correzzione_sinistra
							self.bus.write_byte(self.arduino, self.byte_correzzione_sinistra)
					self.inclinazione = self.bno.inclinazione()
				if (self.byte_att != self.byte_5cm):
				   self.byte_att = self.byte_5cm
				   self.bus.write_byte(self.arduino, self.byte_5cm)
				   self.bus.write_byte(self.arduino, 0x1)
				   self.c = (self.bus.read_byte(self.arduino))
				if self.c == 0x6:
				   self.byte_att = self.byte_fermo
				   self.bus.write_byte(self.arduino, self.byte_fermo)
				   sleep(0.1)
				self.condizione = 4
				self.ferma_cicli = True
			await asyncio.sleep(0.001)
			#print("finito2")
		return sus

	async def main(self):
		results = await asyncio.gather(self.first_task(), self.second_task())
		self.first_task_result, self.second_task_result = results
		self.ferma_cicli = False
		
	def cm30(self):
		
		self.byte_att = self.byte_30cm
		self.bus.write_byte(self.arduino, self.byte_30cm)
		self.first_task_result = 0
		self.second_task_result = 0
		# self.third_task_result = 0
		while True:
			asyncio.run(self.main())
			if (self.first_task_result == 5) or (self.second_task_result == 5) or (self.second_task_result == 6):
				break
		if self.second_task_result == 6:
			self.c=0
			self.byte_att = self.byte_10cmindietro
			self.bus.write_byte(self.arduino, self.byte_10cmindietro)
			while self.c != 0x6:
			   self.c = (self.bus.read_byte(self.arduino))
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			return 'nero'
		self.amogus = self.piastre.prova()
		if self.amogus == 2:
			if self.byte_att != self.byte_fermo:
				self.byte_att = self.byte_fermo
				self.bus.write_byte(self.arduino, self.byte_fermo)
			print("piastra blu 5sec")
			sleep(5)
			self.condizione = 5
		if self.amogus == 5:
			print("placca argentata")
			self.condizione = 6
			
		sleep(0.1)
		while ((GPIO.input(self.Finecorsa_FD) == True) and (GPIO.input(self.Finecorsa_FS) == False) and (GPIO.input(self.Finecorsa_FM) == False)) and self.bytearduino != 69:
			 if self.byte_att != self.byte_ostacolodestra:
					self.byte_att = self.byte_ostacolodestra
					self.bus.write_byte(self.arduino, self.byte_ostacolodestra)
			 sleep(0.4)
			 if GPIO.input(self.Finecorsa_FM) == True:
				 break
		#if self.byte_att == self.byte_ostacolodestra:
			#self.cm30()
		while ((GPIO.input(self.Finecorsa_FD) == False) and (GPIO.input(self.Finecorsa_FS) == True) and (GPIO.input(self.Finecorsa_FM) == False)) and self.bytearduino != 69:
			if self.byte_att != self.byte_ostacolosinistra:
					self.byte_att = self.byte_ostacolosinistra
					self.bus.write_byte(self.arduino, self.byte_ostacolosinistra)
			sleep(0.4)
			if GPIO.input(self.Finecorsa_FM) == True:
				break
		#if self.byte_att == self.byte_ostacolosinistra:
			#self.cm30()
			 
		# print(self.conteggio)
		# print(self.conteggio2)
		'''
		if (self.ds_destra_davanti.range<140 and self.ds_destra_dietro.range>190) or (self.ds_sinistra_davanti.range<140 and self.ds_sinistra_dietro.range>190):
			print("ci sono")
			if self.byte_att != self.byte_indietro:
				self.byte_att = self.byte_indietro
				self.bus.write_byte(self.arduino, self.byte_indietro)
			sleep(1)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
		if (self.ds_destra_davanti.range>190 and self.ds_destra_dietro.range<140) or (self.ds_sinistra_davanti.range>190 and self.ds_sinistra_dietro.range<140):
			print("ci sono")
			if self.byte_att != self.byte_avanti:
				self.byte_att = self.byte_avanti
				self.bus.write_byte(self.arduino, self.byte_avanti)
			sleep(0.7)
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
		'''
		self.byte_att = self.byte_stop
		self.bus.write_byte(self.arduino, self.byte_stop)
		if self.byte_att != self.byte_fermo:
			self.byte_att = self.byte_fermo
			self.bus.write_byte(self.arduino, self.byte_fermo)
			# print("avanti")
			sleep(0.1)
			'''
			self.inmezzo()
			if self.byte_att != self.byte_fermo:
				self.byte_att = self.byte_fermo
				self.bus.write_byte(self.arduino, self.byte_fermo)
				sleep(0.1)
			'''
		self.c = 0
		self.controllo = 0
		self.controllopiastre =0
		print('MARTINOOOOO', self.condizione)
		if self.condizione == 0:
			return 301
		if self.condizione == 1:
			return 'nero'
		if self.condizione == 2:
			return 'ostacolo'
		if self.condizione == 3:
			return 'discesa'
		if self.condizione == 4:
			return 'salita'
		if self.condizione == 5:
			return 'blu'
		if self.condizione == 6:
			return 'argento'
		self.condizione = 0

	def avvio(self):
		import random
		self.bytearduino=0
		print("arduino dice: ",self.bytearduino)
		check = self.sensori_check()
		print("regola destra: ",check)
		self.xavier = self.xavier + 1
		if check == 1:
			if self.bytearduino == 69:
				print("salta azione check 1")
			else:
				self.destra()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione check 1")
			else:
				self.inmezzo()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 1")
			else:
				self.cm30()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 1")
			else:
				self.inmezzo()
		#---------------------------------------------------------------------	
		elif check == 2:
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 2")
			else:
				self.sinistra()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 2")
			else:
				self.inmezzo()
			if self.bytearduino == 69:
				print("salta azione 2")
			else:
				self.cm30()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 2")
			else:
				self.inmezzo()
		#----------------------------------------------------------------------
		elif check == 3:
			random_number = random.randint(1, 2)
			print ("random: ",random_number)
			if random_number == 1:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.destra()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.inmezzo()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.cm30()
			if random_number == 2:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.sinistra()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.inmezzo()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 3")
				else:
					self.cm30()
		#----------------------------------------------------------------------
		elif check == 4:
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 4")
			else:
				self.cm30()
		#-----------------------------------------------------------------------
		elif check == 5:
			random_number = random.randint(1, 2)
			print ("random: ",random_number)
			if random_number == 1:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.destra()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.inmezzo()
			if random_number == 2:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.cm30()
					
		#------------------------------------------------------------------------	
		elif check == 6:
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 6")
			else:
				self.riposizionamento()
		#------------------------------------------------------------------------	
		elif check == 7:
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 7")
			else:
				self.destra()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione7 ")
			else:
				self.destra()
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 7")
			else:
				self.inmezzo()
		#------------------------------------------------------------------------
		elif check == 8:
			random_number = random.randint(1, 2)
			print ("random: ",random_number)
			if random_number == 1:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.sinistra()
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.inmezzo()
			if random_number == 2:
				self.bytearduino = self.bus.read_byte(self.arduino)
				if self.bytearduino == 69:
					print("salta azione 5")
				else:
					self.cm30()
		#------------------------------------------------------------------------		
		elif check == 100:
			self.bytearduino = self.bus.read_byte(self.arduino)
			if self.bytearduino == 69:
				print("salta azione 100")
			else:
				self.cm30()
		#------------------------------------------------------------------------	
		elif check == 10:
			while(self.ds_fronte.range < 160 and self.ds_fronte.range > 100):
				if self.byte_att != self.byte_avanti:
					self.byte_att = self.byte_avanti
					self.bus.write_byte(self.arduino, self.byte_avanti)
			if self.byte_att != self.byte_fermo:
				self.byte_att = self.byte_fermo
				self.bus.write_byte(self.arduino, self.byte_fermo)
				sleep(0.1)
			self.inmezzo()	


				
if __name__ == '__main__':
	sn = Sensore()
	sn.init()
	
	while True:
		try:
			sn.destra()
			
		except Exception as e:
			print ("errore", e)
		
		
