import math
from libBNO055 import BNO055
from SERIALE import Serial
from time import sleep

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
	def ruota_di_90_gradi(self, gradi_attuali):
		angolo_destinazione = (gradi_attuali + 86.4) % 360
		# Chiamare qui la funzione per ruotare verso angolo_destinazione con il tuo sistema di riferimento
		return angolo_destinazione

	def ruota_di_180_gradi(self, gradi_attuali):
		self.angolo_destinazione = (gradi_attuali + 180) % 360
		# Chiamare qui la funzione per ruotare verso angolo_destinazione con il tuo sistema di riferimento
		return angolo_destinazione
	def destra(self):
			mov.ser.setfermo(0)
			gradi = self.bno.readAngle()
			angolo_destinazione = self.ruota_di_90_gradi(gradi)
			print(gradi)
			while (gradi < angolo_destinazione) or (356 <= gradi <= 360) or (gradi < 2) or (gradi > 361):
				if gradi < 70:
					mov.ser.setdestra(3000)
				else:
					mov.ser.setdestra(1000)
				gradi = self.bno.readAngle() 
				print(gradi)
			mov.ser.setfermo(0)
			sleep(0.5)
			print("girato a destra") 
	import time

	def esegui_giri_infiniti(self):
		angolo_totale = 0

		while True:
			angolo_giroscopio = self.leggi_angolo_giroscopio()  # Funzione per leggere l'angolo dal giroscopio

			# Calcola l'angolo effettivo tenendo conto del reset a 360 gradi
			angolo_effettivo = (angolo_giroscopio + angolo_totale) % 360

			# Calcola la differenza di angolo rispetto all'angolo desiderato (90 gradi)
			angolo_da_raggiungere = (angolo_totale + 90) % 360
			differenza_angolo = (angolo_da_raggiungere - angolo_effettivo) % 360

			# Esegui le operazioni desiderate in base alla differenza di angolo
			if differenza_angolo < 45:
				# Girare a destra
				# Esegui le operazioni per girare a destra
				# ...
					
				mov.ser.setdestra(1000)
				# Aggiorna l'angolo totale
				angolo_totale = (angolo_totale + 90) % 360
			else:
				# Girare a sinistra
				# Esegui le operazioni per girare a sinistra
				# ...
				mov.ser.setsinistra(1000)
				# Aggiorna l'angolo totale
				angolo_totale = (angolo_totale - 90) % 360

			# Fai una pausa per evitare di sovraccaricare il processore
			sleep(0.1)

	def leggi_angolo_giroscopio(self):
		# Simulazione della lettura dell'angolo dal giroscopio
		# Sostituisci questa funzione con la tua implementazione reale
		gradi = self.bno.readAngle()
		# Ritorna un valore compreso tra 0 e 359
		return  gradi


		
if __name__ == '__main__':  
	mov = prova()
	mov.init()
	ser = Serial()
	mov.bno.begin()
	
	sleep(1)
	while True:
		mov.esegui_giri_infiniti()
		sleep(2)
		'''
		# Rotazione di 180 gradi
		gradi = ruota_di_180_gradi(gradi)
		print(gradi)'''
