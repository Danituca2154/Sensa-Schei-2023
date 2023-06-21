import time
from time import sleep
import adafruit_vl6180x as vl6180
from libBNO055 import BNO055
from SERIALE import Serial
from SENS_DIST import VL6180X
from led import Led
import RPi.GPIO as GPIO
from piastre import piastre
#from pidgyro import PIDController
import asyncio
from multiprocessing import Process, Queue
queue = Queue()

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

class Movimenti:
	
	
	
	def init(self):
		byte_fermo = self.byte_fermo = 0
		byte_avanti = self.byte_avanti = 1
		byte_destra = self.byte_destra = 5
		byte_destralenta = self.byte_destralenta = 22
		byte_sinistra = self.byte_sinistra = 6
		byte_indietro = self.byte_indietro = 2
		byte_resetimpulsi = self.byte_resetimpulsi = 33
		byte_provaa = self.byte_provaa = 34
		byte_resetimpulsi2 = self.byte_resetimpulsi2 = 35
		self.impulsi=0
		self.impulsi2=0	
		self.costante = 1300
		self.colore = 0
		self.nero = 0
		self.inclinazione  = 0
		
		self.ser= Serial()
		self.piastre = piastre()
		self.bno = BNO055()
		self.led = Led()
		self.laser = VL6180X()
		self.bno.begin()
		#self.pid = PIDController(100, 20, 0.1)
	#gyroscopio---------------------------------------------------------------------

	def update(self, process_variable):
		current_time = time.time()
		if self.up==0:
			dt=1000
			self.up=1
		else:
			dt = current_time - self.last_time
			
		
		error = self.setpoint - process_variable 
		#print('ERROREEEEEEEEEE', error)
		# Gestione del reset del giroscopio a 360 gradi
		if error < -180:
			error += 360
		elif error > 180:
			error -= 360
		self.arduino = self.ser.read()
		if self.arduino == 'serial error':
			self.arduino = 0
		
		if self.ferma_cicli == False and self.arduino != 80:
			self.error_sum += error * dt
			d_error = (error - self.last_error) / dt
			output = self.Kp * error + self.Ki * self.error_sum + self.Kd * d_error
			if output>3000:
				output=3000
			if output<-3000:
				output=-3000
			self.last_time = current_time
			self.last_error = error

			return output
		else:
			output = 0
			return output

	def controlpid(self, asse):
		# Esempio di utilizzo del PIDController con un giroscopio che si resetta a 360 gradi
		gyro_value = 0  # Valore del giroscopio
		self.setpoint = self.asse
		#print('setpoint', self.setpoint)
		Kp = 80
		Ki = 20
		Kd = 1
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.error_sum = 0.0
		self.last_error = 0.0
		self.last_time = time.time()
		impulsi_old = 0
		self.up =0
		self.situazione = 0
		# Impostazione dei coefficienti del PID
		#pid = PIDController(Kp, Ki, Kd)
		serial = Serial()
		while True:
			self.arduino = self.ser.read()
			#print('arduino :', self.arduino)
			if self.arduino == 'serial error':
				self.arduino = 0
			if self.arduino != 80:
				# Simulazione della lettura del giroscopio
				# Nel tuo caso, dovrai leggere il valore reale dal tuo giroscopio
				gyro_value = self.bno.readAngle()
				#print('bnooooooooooo0000000    ', gyro_value)
				# Calcola l'output del controllore PID
				output = self.update(gyro_value)
				#print('output: ',output)
				# Utilizza l'output per controllare i due motori separatamente
				right_motor_speed = -output
				left_motor_speed = output
				
				# Effettua altre azioni per controllare i motori e gestire il movimento
				serial.clean()
				impulsi = serial.setavanti(3000-right_motor_speed, 3000-left_motor_speed)
				if impulsi != 'serial error':
					impulsi_old = impulsi
				if impulsi == 'serial error':
					impulsi = impulsi_old
					#print('errore con gli impulsi bro')  
				#print('sususuusus',impulsi)
				if (GPIO.input(13) == True or GPIO.input(20) == True or GPIO.input(26) == True):  #centro destra sinistra
					#print('ecococo')
					self.situazione = 'finecorsa'
					self.ferma_cicli = True
					break
				self.nero = self.piastre.prova()
				if self.nero=='nero':
					print("piastra nera")
					self.situazione = 'nero'
					self.ferma_cicli = True
				if (impulsi>230 or self.ferma_cicli == True): 
					#importantissima
					impulsi=0
					break
				time.sleep(0.01)  # Attendi per un breve periodo prima di ripetere il ciclo
			else:
				#mov.dritta()
				self.ser.setfermo(0)
	
	
	
	#-------------------------------------------------------------------------------------
	def destra(self):
		z_in = self.bno.readAngle()

		if z_in > 273.6:
			obiettivo = z_in - 273.6
			z_at = z_in + 1
			while ((z_at >= z_in) or (z_at < obiettivo)):
				z_at = self.bno.readAngle()
				if z_at < 0 or z_at > 360:
					z_at = z_in + 1
				if z_at < obiettivo-16 or 350<z_at<360:
					self.ser.setdestra(3000)
				else:
					self.ser.setdestra(1000)
			#print('SONO 11111111111111111111111111')
			self.ser.setfermo(0)
		else:
			obiettivo = z_in + 85.4
			z_at = z_in - 1
			while (z_at < obiettivo):
				z_at = self.bno.readAngle()
				#print(z_at)
				if z_at < 0 or z_at > 360:
					z_at = obiettivo - 1
				if z_at > obiettivo-16:
					self.ser.setdestra(1000)
				else:
					self.ser.setdestra(3000)
			#print('SONO 22222222222222222222222222')
			self.ser.setfermo(0)
		print("girato a destra")
	
	def sinistra(self):
		z_in = self.bno.readAngle()
		if z_in < 84:
			obiettivo = z_in + 276
			z_at = z_in - 2
			while ((z_at <= z_in) or (z_at > obiettivo)):
				z_at = self.bno.readAngle()
				if z_at < 0 or z_at > 360:
					z_at = z_in - 2
				if 20<z_at<80:
					self.ser.setsinistra(3000)
				else:
					self.ser.setsinistra(1000)
			#print('SONO 11111111111111111111111111')
			self.ser.setfermo(0)
		else:
			obiettivo = z_in - 84
			z_at = z_in - 2
			while (z_at > obiettivo):
				z_at = self.bno.readAngle()
				if z_at < 0 or z_at > 360:
					z_at = z_in - 2
				if z_at<obiettivo+25:	
					self.ser.setsinistra(1000)
				else:
					self.ser.setsinistra(3000)
			#print('SONO 22222222222222222222222222')
			self.ser.setfermo(0)
		print("girato a sinistra")
	def riposizionamento(self):
		#print('riposizionamento')
		while (GPIO.input(16) == False):
			self.ser.setindietro(1000)
		self.ser.setfermo(0)
		sleep(0.1)
		self.impulsi=0
		self.ser.azzeroimpulsi()
		while (self.impulsi < 12):
			self.impulsi = self.ser.setavanti(3000, 3000)
			if self.impulsi=='serial error':
				self.impulsi = 0
			#print('eccogliimpulis')
			#print(self.impulsi)
			sleep(0.01)
		#print(self.impulsi)
		self.ser.setfermo(0)
		#print('fatto')
		sleep(0.01)
		
		
	def cm30(self):
		#p_tempo = Process(target=tempo, args=(queue, ))
		#p_tempo.start()
		self.dritta()
		self.situazione = 0
		self.led.led_sotto_ON()
		self.impulsi = 0	
		self.ser.azzeroimpulsi()
		sleep(0.001)
		#self.initial_offset = mov.bno.readAngle()
		self.bno.begin()
		self.asse = self.bno.readAngle()
		#print('ASSSSEEEEEEE', self.asse)
		self.ferma_cicli = False
		self.ser.clean()
		while True:
			self.controlpid(self.asse)
			self.ferma_cicli = True
			break
		self.ser.setfermo(0)
		sleep(0.01)
		#self.inclinazione = self.bno.inclinazione()
		if self.situazione=='finecorsa':
			if self.laser.read(0)<15:
				self.ser.azzeroimpulsi()
				while (self.impulsi2 < 24):
					self.impulsi2 = self.ser.setindietro(3000)
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo(0)
		if (GPIO.input(20) == True):
			#print('finecorsa destra')
			self.ser.azzeroimpulsi()
			self.impulsi2=0
			while (self.impulsi2 < 60):
				self.impulsi2 = self.ser.setindietro(3000)
				if self.impulsi2 == 'serial error':
					self.impulsi2 = 3
			self.ser.setfermo(0)
			z_in = self.bno.readAngle()
			if z_in < 30:
				obiettivo = z_in + 330
				z_at = z_in - 2
				while ((z_at <= z_in) or (z_at > obiettivo)):
					z_at = self.bno.readAngle()
					if z_at < 0 or z_at > 360:
						z_at = z_in - 2
					self.ser.setsinistra(1000)
				self.ser.setfermo(0)
			else:
				obiettivo = z_in - 30
				z_at = z_in - 2
				while (z_at > obiettivo):
					z_at = self.bno.readAngle()
					if z_at < 0 or z_at > 360:
						z_at = z_in - 2	
					self.ser.setsinistra(1000)
			self.ser.setfermo(0)
			self.dritta
			self.ser.setfermo(0)
		if (GPIO.input(26) == True):
			#print('finecorsa sinistra')
			self.ser.azzeroimpulsi()
			self.impulsi2=0
			while (self.impulsi2 < 60):
				self.impulsi2 = self.ser.setindietro(3000)
				if self.impulsi2 == 'serial error':
					self.impulsi2 = 3
			self.ser.setfermo(0)
			z_in = self.bno.readAngle()
			if z_in > 330:
				obiettivo = z_in - 330
				z_at = z_in + 1
				while ((z_at >= z_in) or (z_at < obiettivo)):
					z_at = self.bno.readAngle()
					if z_at < 0 or z_at > 360:
						z_at = z_in + 1
					self.ser.setdestra(1000)
				self.ser.setfermo(0)
			else:
				obiettivo = z_in + 30
				z_at = z_in - 1
				while (z_at < obiettivo):
					z_at = self.bno.readAngle()
					#print(z_at)
					if z_at < 0 or z_at > 360:
						z_at = obiettivo - 1
					self.ser.setdestra(1000)
				self.ser.setfermo(0)
			self.dritta
			self.ser.setfermo(0)
		elif self.nero =='nero':
			self.ser.azzeroimpulsi()
			while (self.impulsi2 < 120):
				self.impulsi2 = self.ser.setindietro(3000)
				if self.impulsi2 == 'serial error':
					self.impulsi2 = 3
			self.ser.setfermo(0)
		self.colori = self.piastre.ferma()
		if self.colori == 'blu':
			return 'blu'
		elif self.colori == 'argento':
			return 'argento'
		elif self.situazione == 'nero':
			return 'nero'
		elif self.situazione == 'finecorsa':
			return 'ostacolo'
		elif self.situazione == 3:
			return 'discesa'
		elif self.situazione == 4:
			return 'salita'
		else:
			return 301
		
		self.impulsi = 0 
		self.impulsi2 = 0
		sleep(0.1)
	def dritta(self):
		if(self.laser.read(1) <120 and (self.laser.read(4)+12)>70 and (self.laser.read(4)+12)<170): # sx dav, sx dietro, sx dietro
				while((self.laser.read(1)/(self.laser.read(4)+12))<0.95):
					self.ser.setdestra(700)
		self.ser.setfermo(0)
		sleep(0.01)
		
		if((self.laser.read(4)+12) <120 and self.laser.read(1)>70 and self.laser.read(1)<170): # sx dietro, sx dav, sx dav
			while((self.laser.read(4)+12)/(self.laser.read(1))<0.96):
				self.ser.setsinistra(700)
		self.ser.setfermo(0)
		sleep(0.01)
		if(self.laser.read(2) <120 and (self.laser.read(3)+15)>70 and (self.laser.read(3)+15)<170): # dx dav, dx dietro, dx dietro
			while((self.laser.read(2)/(self.laser.read(3)+15))<0.98):
				self.ser.setsinistra(700)
		self.ser.setfermo(0)
		sleep(0.01)
		if((self.laser.read(3)+15) <120 and self.laser.read(2)>70 and self.laser.read(2)<170):
			while(((self.laser.read(3)+15)/self.laser.read(2))<0.98):
				self.ser.setdestra(700)
		self.ser.setfermo(0)
		sleep(0.01)
		
	def check_sens(self):
		muri = []
		if self.laser.read(0) > 250:
			muri.append("avanti")
		if self.laser.read(2) > 250 or self.laser.read(3) > 250:
			muri.append("destra")
		if self.laser.read(1) > 250 or self.laser.read(4) > 250:
			muri.append("sinistra")
		return muri
	
	
if __name__ == '__main__':  
	mov = Movimenti()
	mov.init() 
	led = Led()
	laser = VL6180X()
	mov.bno.begin()
	sleep(1)	
	while True:
		
		if laser.read(5)<120:
			mov.riposizionamento()
		if laser.read(0)<150:
			mov.destra()
		if laser.read(5)<120:
			mov.riposizionamento()
		mov.cm30()
		sleep(0.1)
		'''
		mov.dritta()
		sleep(1)
		'''

