from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep
class piastre:
	def init(self):
		port = 1
		bus = smbus.SMBus(port)

		apds = APDS9960(bus)

	def intH(channel):
		print("INTERRUPT")
	def prova(self):
		#GPIO.setmode(GPIO.BOARD)
		#GPIO.setup(7, GPIO.IN)
			# Interrupt-Event hinzufuegen, steigende Flanke
			#GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)
			port = 1
			bus = smbus.SMBus(port)

			apds = APDS9960(bus)
			#print("=================")
			apds.enableLightSensor()
			oval = -1
			
			while True:
				self.situazione = 0
				sleep(0.05)
				if apds.isLightAvailable():
					val = apds.readAmbientLight()
					r = apds.readRedLight()
					g = apds.readGreenLight()
					b = apds.readBlueLight()
					
					#if val != oval:
					#print("<>AmbientLight={} (R: {}, G: {}, B: {})".format(val, r, g, b))
					#	oval = val
					#	break
					if r>3000 and g>5500 and b>6500:
						print("bianco")
						self.situazione = 1
						return self.situazione
						break
					if r>250 and g>800 and b>1300 and b<2000:
						print("blu")
						self.situazione = 2
						return self.situazione
						break
					if r<250 and g<450 and b<550:
						print("nero")
						self.situazione = 3
						return self.situazione
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
        try:
            #sn.sensori_check()
            sn.prova()
        except Exception as e:
            print ("errore", e)
