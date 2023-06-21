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

	def update(self, process_variable):
		current_time = time.time()
		dt = current_time - self.last_time

		error = self.setpoint - process_variable
		# Gestione del reset del giroscopio a 360 gradi
		if error < -180:
			error += 360
		elif error > 180:
			error -= 360

		self.error_sum += error * dt
		d_error = (error - self.last_error) / dt

		output = self.Kp * error + self.Ki * self.error_sum + self.Kd * d_error

		self.last_time = current_time
		self.last_error = error

		return output
	
	def controlpid(self, asse):
		# Esempio di utilizzo del PIDController con un giroscopio che si resetta a 360 gradi
		gyro_value = 0.0  # Valore del giroscopio
		self.setpoint = asse
		print('setpoint', self.setpoint)
		
		# Impostazione dei coefficienti del PID
		Kp = 60
		Ki = 20
		Kd = 1
		self.error_sum = 0.0
		self.last_error = 0.0
		self.last_time = time.time()
		pid = PIDController(Kp, Ki, Kd)
		
		serial = Serial()
		while True:
			# Simulazione della lettura del giroscopio
			# Nel tuo caso, dovrai leggere il valore reale dal tuo giroscopio
			gyro_value = bno.readAngle()
			print(gyro_value)

			# Calcola l'output del controllore PID
			output = pid.update(gyro_value)
			print('output: ',output)
			# Utilizza l'output per controllare i due motori separatamente
			right_motor_speed = -output
			left_motor_speed = output

			# Effettua altre azioni per controllare i motori e gestire il movimento
			lol =serial.setavanti(2000-right_motor_speed, 2000-left_motor_speed)
			
			time.sleep(0.1)  # Attendi per un breve periodo prima di ripetere il ciclo
			
		
if __name__ == '__main__':
	sn = PIDController(100, 20, 0.1)
	bno = BNO055()
	while True:
		bno.begin()
		sn.controlpid(30.0)
