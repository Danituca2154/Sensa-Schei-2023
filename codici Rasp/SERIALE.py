import serial
import time
from time import sleep
import struct

class Serial:
	
	def __init__(self):
		self.ser = serial.Serial(
			port='/dev/ttyAMA0',
			baudrate = 500000,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout = 0
		)
		self.error = "serial error"
	'''
	def read(self, byte = 2):
	 bn  
		readbyte = self.ser.read(size = byte)
		print(readbyte)
		
	
		'''
		
	def read(self, byte = 1):
		#self.clean()
		start = time.time()
		out = 0
		while(self.ser.in_waiting <= 0):
			if((time.time() - start) > 0.05):
				#print(self.error)
				out = self.error
				break
		if out != 69:
			readbyte = self.ser.read(size = byte)
			if (len(readbyte) != byte):
				#print(self.error)
				out = self.error
			else:
				out = 0
				for i in range(byte):
					out |= readbyte[i]<<(8*i) #+ (readbyte[1]<<8)
		return(out)

	def write(self, byte): 
		self.ser.write(struct.pack('>B',byte))
	#--------------------------------------------------------------------------------------------------------		
	def setavanti(self, velocita1, velocita2):
		impulsi=0
		nByte = 3
		byteOut =[0]*nByte
		bitVel1 = 1
		bitVel2 = 1
		if(velocita1<0):
			velocita1 = -velocita1
			bitVel1 = 0
		if(velocita2<0):
			velocita2 = -velocita2
			bitVel2 = 0
		# primo decide se controllo o velocità, secondo richiede il numero di impulsi, terzo azzera impulsi, quarto coppie motori, sesto e settimo versi motori
		byteOut[0] = (1<<7)|(1<<6)|(0<<5)|(1<<4)|(1<<3)|(bitVel1<<1)|(bitVel2<<0)
		self.write(byteOut[0])
		self.clean()
		impulsi = self.read()
		#print('ecco',impulsi)
		if impulsi == 69:
			self.clean()
		#byte di velocità
		MAXvelocita = 6000
		DIVvelocita = 47.24
		if(velocita1>MAXvelocita):
			velocita1= MAXvelocita
		if(velocita2>MAXvelocita):
			velocita2= MAXvelocita
		velocita1= round(velocita1/DIVvelocita)#max 2^7 (127)
		velocita2= round(velocita2/DIVvelocita)#max 2^7 (127)
		byteOut[1] = velocita1
		self.write(byteOut[1])
		self.clean()
		byteOut[2] = velocita2
		self.write(byteOut[2])
		return impulsi
	#------------------------------------------------------------------------------------------------------------
	def setindietro(self, velocita):
		impulsi=0
		nByte = 3
		byteOut =[0]*nByte
		# primo decide se controllo o velocità, secondo richiede il numero di impulsi, terzo azzera impulsi, quarto coppie motori, sesto e settimo versi motori
		byteOut[0] = (1<<7)|(1<<6)|(0<<5)|(1<<4)|(1<<3)|(0<<1)|(0<<0)
		self.write(byteOut[0])
		self.clean()
		impulsi = self.read()
		#print('ecco',impulsi)
		#byte di velocità
		MAXvelocita = 6000
		DIVvelocita = 47.24
		if(velocita>MAXvelocita):
			velocita= MAXvelocita
		velocita= round(velocita/DIVvelocita)#max 2^7 (127)
		byteOut[1] = velocita
		self.write(byteOut[1])
		byteOut[2] = velocita
		self.write(byteOut[2])
		return impulsi
	#---------------------------------------------------------------------------------------------------------------
	def setdestra(self, velocita):
		nByte = 3
		byteOut =[0]*nByte
		#byte di controllo
		bitVel1= 1
		bitVel2= 0
		if(velocita<0):
			velocita = -velocita
			bitVel = 0
		byteOut[0] = (1<<7)|(0<<6)|(0<<5)|(1<<4)|(1<<3)|(bitVel1<<1)|(bitVel2<<0)
		
		#byte di velocità
		MAXvelocita = 6000
		DIVvelocita = 47.24
		if(velocita>MAXvelocita):
			velocita= MAXvelocita
		velocita= round(velocita/DIVvelocita)#max 2^7 (127)
		#print(velocita)
		byteOut[1] = velocita
		byteOut[2] = velocita
		
		for ind in range(nByte):
			self.write(byteOut[ind])
	#---------------------------------------------------------------------------------------------------------------
	def setsinistra(self, velocita):
		nByte = 3
		byteOut =[0]*nByte
		#byte di controllo
		bitVel1= 0
		bitVel2= 1
		if(velocita<0):
			velocita = -velocita
			bitVel = 0
		byteOut[0] = (1<<7)|(0<<6)|(0<<5)|(1<<4)|(1<<3)|(bitVel1<<1)|(bitVel2<<0)
		
		#byte di velocità
		MAXvelocita = 6000
		DIVvelocita = 47.24
		if(velocita>MAXvelocita):
			velocita= MAXvelocita
		velocita= round(velocita/DIVvelocita)#max 2^7 (127)
		#print(velocita)
		byteOut[1] = velocita
		byteOut[2] = velocita
		
		for ind in range(nByte):
			self.write(byteOut[ind])
	#---------------------------------------------------------------------------------------------------------------
	def setfermo(self, velocita):
		nByte = 3
		byteOut =[0]*nByte
		#byte di controllo
		bitVel1= 0
		bitVel2= 0
		if(velocita<0):
			velocita = -velocita
			bitVel = 0
		byteOut[0] = (1<<7)|(0<<6)|(0<<5)|(0<<4)|(1<<3)|(bitVel1<<1)|(bitVel2<<0)
		byteOut[1] = 0
		byteOut[2] = 0
		
		for ind in range(nByte):
			self.write(byteOut[ind])
	def setfermoflag(self, velocita):
		nByte = 3
		byteOut =[0]*nByte
		#byte di controllo
		bitVel1= 0
		bitVel2= 0
		if(velocita<0):
			velocita = -velocita
			bitVel = 0
		byteOut[0] = (1<<7)|(0<<6)|(0<<5)|(1<<4)|(1<<3)|(bitVel1<<1)|(bitVel2<<0)
		byteOut[1] = 0
		byteOut[2] = 0
		
		for ind in range(nByte):
			self.write(byteOut[ind])
	#-------------------------------------------------------------------------------------------------------------
	def azzeroimpulsi(self):
		nByte = 3
		byteOut =[0]*nByte
		byteOut[0] = (1<<7)|(0<<6)|(1<<5)|(0<<4)|(1<<3)|(1<<1)|(1<<0)
		byteOut[1] = 0
		byteOut[2] = 0
		for ind in range(nByte):
			self.write(byteOut[ind])
		'''
		byteOut[0] = (1<<7)|(1<<6)|(0<<5)|(1<<4)|(1<<3)|(1<<1)|(1<<0)
		#print(self.read())
		byteOut[1] = 0
		byteOut[2] = 0
		for ind in range(nByte):
			self.write(byteOut[ind])'''
	#--------------------------------------------------------------------------------------------------------------
	def piastre(self):
		nByte = 1
		byteOut =[0]*nByte
		byteOut[0] = (1<<7)|(0<<6)|(0<<5)|(1<<4)|(0<<3)|(1<<2)|(0<<1)|(0<<0)
		for ind in range(nByte):
			self.write(byteOut[ind])
		self.clean()
		colore = self.read()
		return colore
		
   
	def clean(self):
		self.ser.flush()
		self.ser.flushInput()


if __name__ == '__main__':  
	serial = Serial()
	sleep(1)
	


	while True:	
		
		
		#serial.setavanti(3000, 3000)
		#print(serial.read())
		
		#serial.write(57)	print(serial.read())
		#sleep(4)
		
		#serial.write(11)	
		#serial.read()
		sleep(0.1)
		
		#print("------------")
