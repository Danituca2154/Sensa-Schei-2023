from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep
from led import Led
class piastre:
	def init(self):
		port = 0
		bus = smbus.SMBus(port)
		apds = APDS9960(bus)
		self.led = Led()
	def intH(channel):
		print("INTERRUPT")
	def prova(self):
		#GPIO.setmode(GPIO.BOARD)
		#GPIO.setup(7, GPIO.IN)
			# Interrupt-Event hinzufuegen, steigende Flanke
			#GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)
			port = 0
			bus = smbus.SMBus(port)

			apds = APDS9960(bus)
			#print("=================")
			apds.enableLightSensor()
			apds.enableProximitySensor()
			oval = -1
			#self.led.led_sotto_ON()
			while True:
				self.situazione = 0
				sleep(0.05)
				
				#prox = apds.getLEDBoost()
				#print('prossimità: ',prox)
				if apds.isLightAvailable():
					val = apds.readAmbientLight()
					r = apds.readRedLight()
					g = apds.readGreenLight()
					b = apds.readBlueLight()
					#self.led.led_sotto_OFF()
					#if val != oval:
					
					#print("<>AmbientLight={} (R: {}, G: {}, B: {})".format(val, r, g, b))
					#	oval = val
					#	break7
					'''
					if r>3000 and g>3000 and b>3500:
						print("bianco/argento")
						val = apds.readAmbientLight()
						if val<16000 :
							print("bianco")
						if val>16000 :
							print("argento")
							return 'argento'
						break'''
					if r>250 and g>800 and b>1300 and b<2000:
						print("blu")
						self.situazione = 2
						return 'blu'
						break
					if r<330 and g<620 and b<700:
						print("nero")
						self.situazione = 3
						return 'nero'
						break
					
					else:
						#print("niente")
						self.situazione = 4
						
						return self.situazione
						break
	def ferma(self):
	#GPIO.setmode(GPIO.BOARD)
	#GPIO.setup(7, GPIO.IN)
		# Interrupt-Event hinzufuegen, steigende Flanke
		#GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)
		port = 0
		bus = smbus.SMBus(port)

		apds = APDS9960(bus)
		#print("=================")
		apds.enableLightSensor()
		apds.enableProximitySensor()
		oval = -1
		#self.led.led_sotto_ON()
		while True:
			self.situazione = 0
			sleep(0.05)
			
			#prox = apds.getLEDBoost()
			#print('prossimità: ',prox)
			if apds.isLightAvailable():
				val = apds.readAmbientLight()
				r = apds.readRedLight()
				g = apds.readGreenLight()
				b = apds.readBlueLight()
				#self.led.led_sotto_OFF()
				#if val != oval:
				
				#print("<>AmbientLight={} (R: {}, G: {}, B: {})".format(val, r, g, b))
				#	oval = val
				#	break
				if r>3000 and g>3000 and b>3500:
					print("bianco/argento")
					val = apds.readAmbientLight()
					if val<16000 :
						print("bianco")
					if val>16000 :
						print("argento")
						return 'argento'
					break
				if r>250 and g>800 and b>1300 and b<2000:
					print("blu")
					self.situazione = 2
					return 'blu'
					break
				
				else:
					#print("niente")
					self.situazione = 4
					
					return self.situazione
					break

			
if __name__ == '__main__':
	sn = piastre()
	sn.init()
	while True:
	   
		#sn.sensori_check()
		sn.prova()
	  
