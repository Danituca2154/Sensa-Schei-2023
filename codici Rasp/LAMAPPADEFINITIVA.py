import pygame
from nuovi30cmprova import Movimenti, queue
import RPi.GPIO as GPIO
import nuove_camere 
from nuove_camere import videocamere 
from led import Led
from multiprocessing import Process, Queue, Value, Array
import time
from time import sleep
from servo import Servo
import subprocess
from colorama import Fore, Back, Style
from SENS_DIST import VL6180X
subprocess.call('sudo pigpiod', shell=True)
sleep(0.1)


RES = WIDTH, HEIGHT = 762, 762
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE
mov = Movimenti()
led = Led()
servo = Servo()
servo.init()
mov.init()
start = 0
Pin_errore = 12
cam = videocamere()


class Cell:
	def __init__(self, x, y):
		self.x, self.y = x, y
		self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
		self.visited = False
		self.thickness = 4
		self.colore = {'rosso': {'rosso_s' : Value('b', False), 'rosso_d' : Value('b', False)},
						 'giallo': {'giallo_s' : Value('b', False), 'giallo_d' : Value('b', False)},
						 'verde': {'verde_s': Value('b', False), 'verde_d': Value('b', False)}}
		self.lettere = { 'h': {'h_s' : Value('b', False), 'h_d' : Value('b', False)},
						 's': {'s_s' : Value('b', False), 's_d' : Value('b', False)},
						 'u': {'u_s': Value('b', False), 'u_d': Value('b', False)}}
		self.coo_v = Array('i', 2) 
		self.placca = {'blu': False, 'argento': False, 'nero': False, 'objective': False, 'dislivello': False}
		self.condizioni_esterne = {'salita': False, 'ostacolo': False}
		self.priority = None
		self.neighbours = []

	def draw(self):
		x, y = self.x * TILE, self.y * TILE
		if self.visited:
			pygame.draw.rect(sc, pygame.Color('antiquewhite'), (x, y, TILE, TILE))

		if self.walls['top']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
		if self.walls['right']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
		if self.walls['bottom']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
		if self.walls['left']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)
		if self.condizioni_esterne['salita']:
			pygame.draw.rect(sc, pygame.Color('white'), (x, y, TILE, TILE))

		# PLACCHE
		if self.placca['objective']:
			pygame.draw.rect(sc, pygame.Color('purple'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['nero']:
			pygame.draw.rect(sc, pygame.Color('black'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['argento']:
			pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['blu']:
			pygame.draw.rect(sc, pygame.Color('blue'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['dislivello']:
			pygame.draw.rect(sc, pygame.Color('tan'), (x + 2, y + 2, TILE - 1, TILE - 1))

		# COLORI
		if bool(self.colore['rosso']['rosso_s'].value):
			pygame.draw.rect(sc, pygame.Color('red'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['rosso']['rosso_d'].value):
			pygame.draw.rect(sc, pygame.Color('red'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['giallo']['giallo_s'].value):
			pygame.draw.rect(sc, pygame.Color('yellow'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['giallo']['giallo_d'].value):
			#print(self.coo_v, grid_cells.index(self))
			pygame.draw.rect(sc, pygame.Color('yellow'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['verde']['verde_s'].value):
			pygame.draw.rect(sc, pygame.Color('green'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['verde']['verde_d'].value):
			pygame.draw.rect(sc, pygame.Color('green'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))

		# LETTERE
		if bool(self.lettere['h']['h_s'].value):
			text = font.render("H", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['h']['h_d'].value):
			text = font.render("H", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['s']['s_s'].value):
			text = font.render("S", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['s']['s_d'].value):
			text = font.render("S", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['u']['u_s'].value):
			text = font.render("U", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['u']['u_d'].value):
			text = font.render("U", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)

	def new_cell(self, muoviamoci, posizione):
		index = grid_cells.index(self)
		movimento = muoviamoci[0] 
		next_cell = current_cell
		mossa = 0
		if movimento == 'avanti':
			if posizione == 90:
				next_cell = grid_cells[index - 1]
			elif posizione == 270:
				next_cell = grid_cells[index + 1]
			elif posizione == 0:
				next_cell = grid_cells[index - cols]
			elif posizione == 180:
				next_cell = grid_cells[index + cols]
			with open('valore.txt', 'w') as file:
				file.write(str(grid_cells.index(next_cell)))
			while True:		
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.cm30()
				mov.dritta()
				break
		elif movimento == 'gira a destra':
			if posizione == 90:
				posizione = 0
			elif posizione == 270:
				posizione = 180
			elif posizione == 0:
				posizione = 270
			elif posizione == 180:
				posizione = 90
			queue.put('posizione')
			queue.put(posizione)
			while True:
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.destra()
				if muoviamoci[1]!='gira a destra' and mov.laser.read(5)<120:  # no len perchè dopo destra sempre altro
					mov.riposizionamento()
				else:
					mov.dritta()
				break
		elif movimento == 'gira a sinistra':
			if posizione == 90:
				posizione = 180
			elif posizione == 270:
				posizione = 0
			elif posizione == 0:
				posizione = 90
			elif posizione == 180:
				posizione = 270
			queue.put('posizione')
			queue.put(posizione)
			while True:		
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.sinistra()
				if mov.laser.read(5)<130:
					mov.riposizionamento()
				else:
					mov.dritta()
				break
		
		return next_cell, posizione, mossa	
			
	def check_cell(self, x, y):
		find_index = lambda x, y: x + y * cols
		if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
			return False
		return grid_cells[find_index(x, y)]

	def create_dict(self):
		shortest_cell_path = []
		visitable_cell = []
		for cell in grid_cells:
			if not cell.visited and not all(cell.walls.values()):
				visitable_cell.append(cell)
		if len(visitable_cell) == 0:
			target = grid_cells[int((cols*rows)/2)]
			visitable_cell.append(target)

		#print('DICT', grid_cells.index(self))
		for target in visitable_cell:
			#print('TARGET', grid_cells.index(target))
			fwdPath = []
			unvisited = {n: float('inf') for n in grid_cells}  # valore infinito positivo
			unvisited[self] = 0  # costo cela iniziale 0
			visited = {}
			revPath = {}
			while unvisited:  # go until unvisited is empty
				currCell = min(unvisited, key=unvisited.get)  # prendi la cella col minimo costo dal dictionary
				# print(grid_cells.index(currCell))
				visited[currCell] = unvisited[currCell]  # add the cell to the dictionary
				if currCell == target:
					break
				for wall in currCell.walls:
					if not currCell.walls[wall]:  # se non c'è il muro
						if wall == 'top':
							childCell = currCell.check_cell(currCell.x, currCell.y - 1)
						elif wall == 'right':
							childCell = currCell.check_cell(currCell.x + 1, currCell.y)
						elif wall == 'bottom':
							childCell = currCell.check_cell(currCell.x, currCell.y + 1)
						elif wall == 'left':
							childCell = currCell.check_cell(currCell.x - 1, currCell.y)
						if childCell in visited:  # se è già presente vai alla prossima (per i vicoli cieci)
							continue
						tempDist = unvisited[currCell] + 1  # assume il numero più corto per raggiungere la casella
						if tempDist < unvisited[childCell]:
							unvisited[childCell] = tempDist  # costo della cella non è più infinito
							if childCell.placca['nero']:
								unvisited[childCell] += 500
							elif childCell.placca['blu']:
								unvisited[childCell] += 3
							revPath[childCell] = currCell
				unvisited.pop(currCell)
			cell = target  # target
			fwdPath.append(cell)
			#print(revPath)
			while cell != self:
				fwdPath.append(revPath[cell])
				cell = revPath[cell]
			fwdPath.reverse()
			if len(shortest_cell_path) == 0 or len(fwdPath) < len(shortest_cell_path):
				shortest_cell_path = fwdPath
		mostra_sentiero = True
		#for cell in shortest_cell_path:
			#print(grid_cells.index(cell))
		cell_before = shortest_cell_path[0]
		posizione_dij = posizione
		muoviamoci = []
		while mostra_sentiero:
			for cell in shortest_cell_path:
				draw_base()
				pygame.draw.rect(sc, pygame.Color('purple'), (cell.x * TILE, cell.y * TILE, TILE, TILE - 1))
				posizione_dij, muoviamoci = define_posizione(cell_before, cell, posizione_dij, muoviamoci)
				draw_robot(posizione, x_robot, y_robot)
				pygame.display.flip()
				cell_before = cell
				clock.tick(10)
			mostra_sentiero = False
		return shortest_cell_path, muoviamoci # might just need the last cell
		
	def destroy_wall(self, posizione, muri):  # could be done with conditions for each wall
		#cell_destra = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120]
		cell_destra = [18, 37, 56, 75, 94, 113, 132, 151, 170, 189] # da cambiare se cambiano rows or cols
		index = grid_cells.index(self)
		for muro in muri:  # muri = ['avanti', ...]
			if muro == 'avanti':
				if posizione == 0 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 270 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 180 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 90 and index % 11 != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
			elif muro == 'destra':
				if posizione == 0 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 270 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 180 and index % 11 != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 90 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
			elif muro == 'sinistra':
				if posizione == 0 and index % 11 != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 270 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 180 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 90 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
			elif muro == 'dietro':
				if posizione == 0 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 270 and index % 11 != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 180 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 90 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False

	def define_coo(self, posizione, verso, vittima):
		x, y = self.x * TILE, self.y * TILE
		if vittima == 'lettera':
			if (posizione == 0 and verso == 'sinistra') or (posizione == 180 and verso == 'destra'):
				x = x + TILE/7 + 3
				y = y + TILE/2
			elif (posizione == 0 and verso == 'destra') or (posizione == 180 and verso == 'sinistra'):
				x = x + TILE - TILE/7
				y = y + TILE/2
			elif (posizione == 90 and verso == 'sinistra') or (posizione == 270 and verso == 'destra'):
				x = x + TILE/2
				y = y + TILE - TILE/7
			elif (posizione == 90 and verso == 'destra') or (posizione == 270 and verso == 'sinistra'):
				x = x + TILE/2
				y = y + TILE/7 + 3
		elif vittima == 'colore':
			if (posizione == 0 and verso == 'sinistra') or (posizione == 180 and verso == 'destra'):
				x = x + 3
				y = y + TILE/2 - TILE/20
			elif (posizione == 0 and verso == 'destra') or (posizione == 180 and verso == 'sinistra'):
				x = x + TILE - TILE/10 - 1
				y = y + TILE/2 - TILE/20  # 45
			elif (posizione == 90 and verso == 'sinistra') or (posizione == 270 and verso == 'destra'):
				x = x + TILE/2 - TILE/20  # 45
				y = y + TILE - TILE/10 - 1
			elif (posizione == 90 and verso == 'destra') or (posizione == 270 and verso == 'sinistra'):
				x = x + TILE/2 - TILE/20
				y = y + 3
		return int(x), int(y)   #might need int
		
	def vittima(self, vittima_s, vittima_d, posizione, before_cell):
		#print(bool(grid_cells[5].colore['giallo']['giallo_d'].value))
		#print('UAUAU', grid_cells.index(before_cell))
		trovato = False		
		if vittima_s >= 7 and vittima_s <= 9 and self.coo_v[0] == 0 and before_cell.ultima_vittima(vittima_s):
			trovato = True
			self.coo_v[0] = self.define_coo(posizione, 'sinistra', 'lettera')[0]
			self.coo_v[1] = self.define_coo(posizione, 'sinistra', 'lettera')[1]
			#mov.ser.setfermo(0)	
			if vittima_s == 7:
				self.lettere['u']['u_s'].value = not self.lettere['u']['u_s'].value
				servo.U_sinistra()
			elif vittima_s == 8:
				self.lettere['h']['h_s'].value = not self.lettere['h']['h_s'].value
				servo.H_sinistra()
			elif vittima_s == 9:
				self.lettere['s']['s_s'].value = not self.lettere['s']['s_s'].value
				servo.S_sinistra()
			#GPIO.output(Pin_errore, GPIO.HIGH)
		elif vittima_d >= 10 and vittima_d <= 12 and self.coo_v[0] == 0 and before_cell.ultima_vittima(vittima_d):
			trovato = True
			self.coo_v[0] = self.define_coo(posizione, 'destra', 'lettera')[0]
			self.coo_v[1] = self.define_coo(posizione, 'destra', 'lettera')[1]
			#mov.ser.setfermo(0)
			if vittima_d == 10:
				self.lettere['u']['u_d'].value = not self.lettere['u']['u_d'].value
				servo.U_destra()
			elif vittima_d == 11:
				self.lettere['h']['h_d'].value = not self.lettere['h']['h_d'].value
				servo.H_destra()
			elif vittima_d == 12:
				self.lettere['s']['s_d'].value = not self.lettere['s']['s_d'].value
				servo.S_destra()
			#GPIO.output(Pin_errore, GPIO.HIGH)
		elif vittima_s >= 1 and vittima_s <= 3 and self.coo_v[0]== 0 and before_cell.ultima_vittima(vittima_s):
			self.coo_v[0] = self.define_coo(posizione, 'sinistra', 'colore')[0]
			self.coo_v[1] = self.define_coo(posizione, 'sinistra', 'colore')[1] 
			#mov.ser.setfermo(0)
			if vittima_s == 1:
				self.colore['giallo']['giallo_s'].value = not self.colore['giallo']['giallo_s'].value
				servo.giallo_sinistra()
			elif vittima_s == 2:
				self.colore['rosso']['rosso_s'].value = not self.colore['rosso']['rosso_s'].value
				servo.rosso_sinistra()
			elif vittima_s == 3:
				self.colore['verde']['verde_s'].value = not self.colore['verde']['verde_s'].value
				servo.verde_sinistra()
			#GPIO.output(Pin_errore, GPIO.HIGH)
		elif vittima_d >= 4 and vittima_d <= 6 and self.coo_v[0]== 0 and before_cell.ultima_vittima(vittima_d):
			self.coo_v[0] = self.define_coo(posizione, 'destra', 'colore')[0]
			self.coo_v[1] = self.define_coo(posizione, 'destra', 'colore')[1]
			mov.ser.setfermo(0)
			sleep(2)
			if vittima_d == 4:
				self.colore['giallo']['giallo_d'].value = not self.colore['giallo']['giallo_d'].value
				servo.giallo_destra()
			elif vittima_d == 5:
				self.colore['rosso']['rosso_d'].value = not self.colore['rosso']['rosso_d'].value
				servo.rosso_destra()
			elif vittima_d == 6:
				self.colore['verde']['verde_d'].value = not self.colore['verde']['verde_d'].value
				servo.verde_destra()
			#GPIO.output(Pin_errore, GPIO.HIGH)
		return trovato
		
	def ultima_vittima(self, v):
		#print('ultima_vittima', grid_cells.index(self))
		if (v == 1 or v == 4) and (bool(self.colore['giallo']['giallo_s'].value) or bool(self.colore['giallo']['giallo_d'].value)):
			return False 
		elif (v == 2 or v == 5) and (bool(self.colore['rosso']['rosso_s'].value) or bool(self.colore['rosso']['rosso_d'].value)):
			#print('kek')
			return False
		elif (v == 3 or v == 6) and (bool(self.colore['verde']['verde_s'].value) or bool(self.colore['verde']['verde_d'].value)):
			return False
		elif (v == 7 or v == 10) and (bool(self.lettere['u']['u_s'].value) or bool(self.lettere['u']['u_d'].value)):
			return False
		elif (v == 8 or v == 11) and (bool(self.lettere['h']['h_s'].value) or bool(self.lettere['h']['h_d'].value)):
			return False
		elif (v == 9 or v == 12) and (bool(self.lettere['s']['s_s'].value) or bool(self.lettere['s']['s_d'].value)):
			return False 
		else:
			return True
			
def camere(queue):
	last_c = centre
	last_p = 0
	last_b = centre
	current_cell = grid_cells[centre]
	while True:
		if queue.empty():
			current_cell = grid_cells[last_c]
			posizione = last_p
			before_cell = grid_cells[last_b]
		else:
			identificate = queue.get()
			i = queue.get()
			#print(identificate, i)
			if identificate == 'cella':
				before_cell = current_cell
				last_b = grid_cells.index(before_cell)
				current_cell = grid_cells[i]
				last_c = i
				posizione = last_p
			elif identificate == 'posizione':
				posizione = i
				last_p = i
				current_cell = grid_cells[last_c]
				before_cell = grid_cells[last_b]
			
		img, img1 = cam.telecamere()
		lettera = cam.get_letter(img, 'sinistra')
		lettera1 = cam.get_letter(img1, 'destra')
		print(lettera, lettera1)
		trovato = current_cell.vittima(lettera, lettera1, posizione, before_cell)
		if not trovato:
			color = cam.get_color(img, 'sinistra')
			color1 = cam.get_color(img1, 'destra')
			trovato = current_cell.vittima(color, color1, posizione, before_cell)
		#print('camere', grid_cells.index(current_cell), posizione)

def define_posizione(cell_before, cell, posizione_dij, muoviamoci):
	index_before = grid_cells.index(cell_before)
	index_cell = grid_cells.index(cell)
	i = index_cell - index_before
	#print(index_cell, index_before, posizione_dij)
	if posizione_dij == 0:
		if i == - rows:
			muoviamoci.append('avanti')
		elif i == 1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 270
		elif i == - 1:
			muoviamoci.append('gira a sinistra')
			muoviamoci.append('avanti')
			posizione_dij = 90
		elif i == rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 180
	elif posizione_dij == 90:   # <--
		if i == - 1:
			muoviamoci.append('avanti')
		elif i == - rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 0
		elif i == rows:
			muoviamoci.append('gira a sinistra')
			muoviamoci.append('avanti')
			posizione_dij = 180
		elif i == 1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 270
	elif posizione_dij == 270:  # -->
		if i == 1:
			muoviamoci.append('avanti')
		elif i == rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 180
		elif i == - rows:
			muoviamoci.append('gira a sinistra')
			muoviamoci.append('avanti')
			posizione_dij = 0
		elif i == -1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 90
	elif posizione_dij == 180:
		if i == rows:
			muoviamoci.append('avanti')
		elif i == - 1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			
			posizione_dij = 90
		elif i == 1:
			muoviamoci.append('gira a sinistra')
			muoviamoci.append('avanti')
			posizione_dij = 270
		elif i == -rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			muoviamoci.append('avanti')
			posizione_dij = 0
	return posizione_dij, muoviamoci

		
def draw_robot(posizione, x, y):
	x = int(x * TILE + 11) # da cambiare se cambiano rows or cols
	y = int(y * TILE + 11) # da cambiare se cambiano rows or cols
	if posizione == 0:
		sc.blit(robot_img, (x, y))
	elif posizione == 90:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 90)  # rotate
		sc.blit(robot_img_sinistra, (x, y))
	elif posizione == 180:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 180)  # rotate
		sc.blit(robot_img_sinistra, (x, y))
	elif posizione == 270:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 270)  # rotate
		sc.blit(robot_img_sinistra, (x, y))


def draw_base():
	sc.fill(pygame.Color('darkslategray'))
	[cell.draw() for cell in grid_cells]

pygame.init()
sc = pygame.display.set_mode(RES)  # window
clock = pygame.time.Clock()
robot_img = pygame.image.load(
	"/home/sensaschei2/Desktop/codici macc nuova/robot.png").convert()  # ottenere l'immagine
# resize
width = robot_img.get_rect().width
height = robot_img.get_rect().height
robot_img = pygame.transform.scale(robot_img, (TILE - 20, TILE - 20))  # da cambiare se cambiano rows or cols

player_speed = 0.06
posizione = 0
font = pygame.font.Font('freesansbold.ttf', 17)

global grid_cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
global centre
centre = int(cols * rows/2)
current_cell = grid_cells[centre]

target = current_cell 
next_cell = current_cell
x_robot, y_robot = current_cell.x, current_cell.y
objective = current_cell
muoviamoci = []
check = []
togli_muro = True
before_cell = current_cell

				
if __name__ == '__main__':
	#queue = Queue()
	'''
	queue.put('cella')
	queue.put(grid_cells.index(current_cell)) 
	queue.put('posizione')
	queue.put(posizione)      
	#p_cam = Process(target=camere, args=(queue, ))      
	p_cam.start()
	'''
	while True:
		led.led_cam_ON()
		x_robot, y_robot = current_cell.x, current_cell.y
		#print('AAAAAAA', grid_cells.index(current_cell))
		current_cell.visited = True
		draw_base()
		draw_robot(posizione, x_robot, y_robot)	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		if len(muoviamoci) != 0:
			next_cell, posizione, condizione = current_cell.new_cell(muoviamoci, posizione)
			if next_cell != current_cell:
				before_cell = current_cell
			print('CONDIZIONE', condizione)
			img, img1 = cam.telecamere()
			lettera = cam.get_letter(img, 'sinistra')
			lettera1 = cam.get_letter(img1, 'destra')
			print('lettere', lettera, lettera1)
			trovato = next_cell.vittima(lettera, lettera1, posizione, before_cell)
			if not trovato:
				color = cam.get_color(img, 'sinistra')
				color1 = cam.get_color(img1, 'destra')
				print('colori', color, color1)
				trovato = next_cell.vittima(color, color1, posizione, before_cell)
			if condizione == 'nero':
				next_cell.visited = True
				next_cell.placca['nero'] = True
				objective = current_cell
				next_cell = current_cell  # rimango sulla stessa cell
			elif condizione == 'blu':
				next_cell.visited = True
				next_cell.placca['blu'] = True
			elif condizione == 'argento':
				next_cell.visited = True
				next_cell.placca['argento'] = True
			elif condizione == 'discesa' or condizione == 'salita':
				next_cell.visited = True
				next_cell.placca['dislivello'] = True
				i = grid_cells.index(next_cell)  # number in grid of dislivello
				if posizione == 0:
					next_cell = grid_cells[i - rows]
					next_cell.destroy_wall(posizione, ['dietro'])
				elif posizione == 90:
					next_cell = grid_cells[i - 1]
					next_cell.destroy_wall(posizione, ['destra'])
				elif posizione == 180:
					next_cell = grid_cells[i + rows]
					next_cell.destroy_wall(posizione, ['avanti'])
				elif posizione == 270:
					next_cell = grid_cells[i + 1]
					next_cell.destroy_wall(posizione, ['sinistra'])
				objective = next_cell							
			muoviamoci.pop(0)
			togli_muro = True
		else: 
			if togli_muro:
				for i in range (0, 3):
					check = mov.check_sens()
				print(check)
				togli_muro = False
				#print('qua')	
			for muro in check:
				current_cell.destroy_wall(posizione, [muro])
		if objective == current_cell:
			objective.placca['objective'] = False
			path, muoviamoci = current_cell.create_dict()
			#print(muoviamoci)
			objective = path[-1]
			objective.placca['objective'] = True
		current_cell = next_cell
		pygame.display.flip()
		clock.tick(60)
