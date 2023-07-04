import math
from libBNO055 import BNO055
from SERIALE import Serial
from time import sleep
import adafruit_vl6180x as vl6180
from SENS_DIST import VL6180X
class prova():
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
		self.bno = BNO055()

	
	def destra(self):
		z_in = self.bno.readAngle()
		self.ser.setdestra(3000)
		sleep(0.1)
		if z_in > 273.6:
			obiettivo = z_in - 273.6
			z_at = self.bno.readAngle()
			while ((z_at >= z_in) or (z_at < obiettivo)):
					z_at = self.bno.readAngle()
					#print(z_at)
					if z_at < 0 or z_at > 360:
						z_at = z_in 
					if z_at < obiettivo-16 or 350<z_at<360:
						self.ser.setdestra(3000)
					else:
						self.ser.setdestra(1000)
			#print('SONO 11111111111111111111111111')
			self.ser.setfermo(0)
		else:
			obiettivo = z_in + 85.4
			z_at = self.bno.readAngle()
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
		#print('FLAG', flag)
		#print('sono entrato in sinistra')
			self.ser.setsinistra(3000)
			sleep(0.1)
			z_in = self.bno.readAngle()
			if z_in < 84:
				obiettivo = z_in + 276
				z_at = self.bno.readAngle()
				while ((z_at <= z_in) or (z_at > obiettivo) ):
						z_at = self.bno.readAngle()
						#print(z_at)
						if z_at < 0 or z_at > 360:
							z_at = z_in 
						if 20<z_at<80:
							self.ser.setsinistra(3000)
						else:
							self.ser.setsinistra(1000)
				#print('SONO 11111111111111111111111111')
				self.ser.setfermo(0)
			else:
				obiettivo = z_in - 84
				z_at = self.bno.readAngle()
				while (z_at > obiettivo):
						z_at = self.bno.readAngle()
						if z_at < 0 or z_at > 360:
							z_at = z_in
						if z_at<obiettivo+25:	
							self.ser.setsinistra(1000)
						else:
							self.ser.setsinistra(3000)
				#print('SONO 22222222222222222222222222')
				self.ser.setfermo(0)
			print("girato a sinistra")
			
			
	# Funzione per controllare i motori e muovere la macchinina
	def controlla_motori(self, velocita):
		print(velocita)
		imp = self.ser.setavanti(3000-velocita, 3000+velocita)
		if imp == 'serial error':
			imp = 0
		#print(imp)
		return imp
	def calcola_output_pid(self, error, imp):
		if imp!= 80:
			self.P = self.Kp * error
			self.integral_error += error
			self.I = self.Ki * self.integral_error
			self.D = self.Kd * (error - self.last_error)
			self.last_error = error

			# Calcola l'uscita totale del PID
			output = self.P + self.I + self.D
			return output
		else: 
			output = 0
			return output
	def cm30(self):
		self.Kp = 20
		self.Ki = 0.2
		self.Kd = 0.1
		# Variabili globali
		self.angolo_iniziale = self.bno.readAngle()
		self.distanza_desiderata = 228
		self.posizione_attuale = 0
		angolo_corrente = 0
		self.last_error = 0
		self.integral_error = 0
		# Ciclo di controllo
		while self.posizione_attuale < self.distanza_desiderata:
			self.angolo_corrente = self.bno.readAngle()
			self.errore = self.angolo_corrente - self.angolo_iniziale
			if self.errore < -180:
				self.errore += 360
			elif self.errore > 180:
				self.errore -= 360
			self.output_pid = self.calcola_output_pid(self.errore, self.posizione_attuale)
			self.posizione_attuale = self.controlla_motori(self.output_pid)
			# Attendere un breve periodo di tempo per il movimento della macchinina
			sleep(0.1)
		self.ser.setfermo(0)
		
if __name__ == '__main__':  
	mov = prova()
	mov.init()
	ser = Serial()
	mov.bno.begin()
	laser = VL6180X()
	sleep(1)
	while True:
		if laser.read(0)<150:
			mov.destra()
		if laser.read(5)<120:
			mov.ser.setindietro(1000)
			sleep(1)
			mov.ser.setavanti(1000, 1000)
			sleep(0.3)
			mov.ser.setfermo(0)
		mov.cm30()
		sleep(0.1)

		'''
		# Rotazione di 180 gradi
		gradi = ruota_di_180_gradi(gradi)
		print(gradi)'''
