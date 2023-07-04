import time
from libBNO055 import BNO055
from SERIALE import Serial



class PIDController:
	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.last_time = time.time()
		self.setpoint = 0.0
		self.error_sum = 0.0
		self.last_error = 0.0
		self.ser = Serial()

	def prova(self):
		self.ser.clean()
		sus = self.ser.piastre()
		if sus == 'serial error':
			sus = 0
		else: 
			sus = sus*3.92
		return sus
			
		
if __name__ == '__main__':
	sn = PIDController(100, 20, 0.1)
	bno = BNO055()
	while True:
		suk = sn.prova()
		print(suk)
