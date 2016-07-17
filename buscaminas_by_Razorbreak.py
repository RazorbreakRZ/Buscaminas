#!/usr/bin/env python

#INCLUDES
import pygame
import random

pygame.init() #start game engine

#GLOBAL VARS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#IMAGES & SPRITES (RESOURCES)
#...menu...
m_bgimage = pygame.image.load("Graficos/Menu/logo.png")
#m_credits = pygame.image.load("Graficos/Menu/credits.png") #Not Used
m_newgame = pygame.image.load("Graficos/Menu/nuevo.png")
m_exit = pygame.image.load("Graficos/Menu/salir.png")
#m_records = pygame.image.load("Graficos/Menu/records.png") #Not Used
#m_config = pygame.image.load("Graficos/Menu/config.png") #Not Used
m_final = pygame.image.load("Graficos/Menu/final.png") #Final window
m_easy = pygame.image.load("Graficos/Menu/easy.png")
m_medium = pygame.image.load("Graficos/Menu/medium.png")
m_hard = pygame.image.load("Graficos/Menu/hard.png")
#...game...
blanco = pygame.image.load("Graficos/Cuadros/blanco.png")
uno = pygame.image.load("Graficos/Cuadros/uno.png")
dos = pygame.image.load("Graficos/Cuadros/dos.png")
tres = pygame.image.load("Graficos/Cuadros/tres.png")
cuatro = pygame.image.load("Graficos/Cuadros/cuatro.png")
cinco = pygame.image.load("Graficos/Cuadros/cinco.png")
seis = pygame.image.load("Graficos/Cuadros/seis.png")
siete = pygame.image.load("Graficos/Cuadros/siete.png")
ocho = pygame.image.load("Graficos/Cuadros/ocho.png")
mina = pygame.image.load("Graficos/Cuadros/mina.png")
lleno = pygame.image.load("Graficos/Cuadros/lleno.png")
bandera = pygame.image.load("Graficos/Cuadros/bandera.png")
noflag = pygame.image.load("Graficos/Cuadros/noflag.png")
fallo = pygame.image.load("Graficos/Cuadros/fallo.png")
g_win = pygame.image.load("Graficos/Cuadros/win.png")
g_gameover = pygame.image.load("Graficos/Cuadros/gameover.png")
#...Lists of resources...
m_graphics = [m_bgimage,m_newgame,m_exit]
m_difficulty = [m_easy,m_medium,m_hard]
g_numbers = [blanco,uno,dos,tres,cuatro,cinco,seis,siete,ocho,mina,lleno,bandera,noflag,fallo]


#-------------------
#CLASSES & FUNCTIONS
class Minesweeper:
	""" La clase "MineSweeper" inicializa un nuevo juego, cargando la configuracion pasada """
	def __init__(self,N,M,minas,ancho,alto,margen,OX,OY,DX,DY,screen,graficos):
		self.screen = screen #control de ventana
		self.g_numbers = graficos[:]
		self.N = N
		self.M = M
		self.WIDTH = ancho
		self.HEIGHT = alto
		if ancho != 40 and alto != 40: self.__resizer(ancho,alto)
		self.MARGIN = margen
		self.MINAS = minas
		self.OX = OX
		self.OY = OY
		self.DX = DX
		self.DY = DY
		self.game_status = -1 # None = -1, Started = 0, Win = 1, Lose = 2
		self.to_win = N*M - (self.MINAS) # casillas por desbloquear
		self.game = [] #matriz de casillas desbloqueadas
		self.numbers = [] #matriz de minas (minas)
		self.list_minas = [] #lista posiciones minas
		
		#Inicializar reglas de juego
		for row in range(N):
				self.game.append([])
				self.numbers.append([])
				for column in range(M):
					self.game[row].append(0) #False = 0, True = 1, Flag = 2, Fail = 3
					self.numbers[row].append(0)
		
		mines = self.MINAS #colocacion aleatoria de las self.MINAS minas
		while mines > 0:
			x = random.randrange(0,N)
			y = random.randrange(0,M)
			if self.numbers[x][y] == 0:
				self.numbers[x][y] = 9
				mines -= 1
				self.list_minas.append(x)
				self.list_minas.append(y)
				#print("Mine coordinates:",x,y)
		
		for row in range(self.N):
			for column in range(self.M):
				if self.numbers[row][column] != 9:
					self.numbers[row][column] = self.__rellenarCasilla(row,column)
	
	def __resizer(self,X,Y):
		for i in range(len(self.g_numbers)):
			self.g_numbers[i] = pygame.transform.scale(self.g_numbers[i],(X,Y))
	
	def __rellenarCasilla(self,px,py):
		minas=0
		n = px - 1
		m = py - 1
		if n >= 0 and m >= 0 and self.numbers[n][m] == 9: minas += 1
		n = px - 1
		if n >= 0 and self.numbers[n][py] == 9: minas += 1
		n = px - 1
		m = py + 1
		if n >= 0 and m < M and self.numbers[n][m] == 9: minas += 1
		m = py - 1
		if m >= 0 and self.numbers[px][m] == 9: minas += 1
		m = py + 1
		if m < M and self.numbers[px][m] == 9: minas += 1
		n = px + 1
		m = py - 1
		if n < N and m >= 0 and self.numbers[n][m] == 9: minas += 1
		n = px + 1
		if n < N and self.numbers[n][py] == 9: minas += 1
		n = px + 1
		m = py + 1
		if n < N and m < M and self.numbers[n][m] == 9: minas += 1
		return minas


	def __liberarCasilla(self,px,py):
		if self.game[px][py] == 0 and self.numbers[px][py] != 9:
			self.game[px][py] = 1
			self.to_win -= 1
			if self.numbers[px][py] == 0:
				n = px - 1
				m = py - 1
				if n >= 0 and m >= 0: self.__liberarCasilla(n,m)
				n = px - 1
				if n >= 0: self.__liberarCasilla(n,py)
				n = px - 1
				m = py + 1
				if n >= 0 and m < M: self.__liberarCasilla(n,m)
				m = py - 1
				if m >= 0: self.__liberarCasilla(px,m)
				m = py + 1
				if m < self.M: self.__liberarCasilla(px,m)
				n = px + 1
				m = py - 1
				if n < self.N and m >= 0: self.__liberarCasilla(n,m)
				n = px + 1
				if n < self.N: self.__liberarCasilla(n,py)
				n = px + 1
				m = py + 1
				if n < self.N and m < self.M: self.__liberarCasilla(n,m)


	def __descubrirMinas(self,row,column):
		self.game[row][column] = 3
		for i in range(0,2*(self.MINAS),2):
			if self.list_minas[i] != row or self.list_minas[i+1] != column:
				if self.game[self.list_minas[i]][self.list_minas[i+1]] == 0:
					self.game[self.list_minas[i]][self.list_minas[i+1]] = 1

	def start(self,win,gameover):
		clock = pygame.time.Clock()
		FPS = 20 # frames por segundo (juego)
		font_size = 50
		font = pygame.font.Font("Graficos/Fuentes/Led.ttf", font_size) # estilo de letra de las puntuaciones
		timer = 0 #temporizador de juego
		start_time = 0 #comienzo de partida
		exit = False
		while not exit:
			#TEST FINAL
			if self.to_win == 0 and self.game_status != 1: 
				self.game_status = 1
				print "YOU WIN!! in %.2f seconds" % (float(pygame.time.get_ticks()-start_time)/1000)
			#CAPTURE EVENTS
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					button = pygame.mouse.get_pressed()
					if pos[0] > self.OX and pos[0] < self.DX-self.MARGIN and pos[1] > self.OY and pos[1] < self.DY-self.MARGIN and self.game_status <= 0:
						if self.game_status == -1: 
							start_time = pygame.time.get_ticks()
							self.game_status = 0
						column = (pos[0] - self.OX) // (self.WIDTH+self.MARGIN) #X
						row = (pos[1] - self.OY) // (self.HEIGHT+self.MARGIN) #Y
						if button == (True,False,False) and self.game[row][column] == 0: #Button1 Mouse
							if self.numbers[row][column] == 0: self.__liberarCasilla(row,column)
							elif self.numbers[row][column] == 9:
								self.__descubrirMinas(row,column)
								self.game_status = 2
								print "GAME OVER!! at %.2f sencods" % (float(pygame.time.get_ticks()-start_time)/1000)
							else: 
								self.game[row][column] = 1
								self.to_win -= 1
						elif button == (False,False,True): #Button2 Mouse
							if self.game[row][column] == 0: self.game[row][column] = 2
							elif self.game[row][column] == 2: self.game[row][column] = 0
						#print("Valor casilla:",game[row][column])
	
			#UPDATE SCORES
			if self.game_status == 0: timer = float(pygame.time.get_ticks()-start_time)/1000  #Temporizador segundos
			text_time = font.render(str("%.2f" % timer),True,RED)
			text_score = font.render(str(self.to_win),True,RED)
	
			#RENDERING GAME
			self.screen.fill(BLACK)
			self.screen.blit(text_time,(5,8))
			self.screen.blit(text_score,(self.DX-1.5*font_size,8))
			for row in range(self.N):
				for column in range(self.M):
					if self.game_status <= 1:
						if self.game[row][column] == 0:
							self.screen.blit(self.g_numbers[10],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
						elif self.game[row][column] == 1:
							self.screen.blit(self.g_numbers[self.numbers[row][column]],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
						elif self.game[row][column] == 2:
							self.screen.blit(self.g_numbers[11],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
					elif self.game_status == 2:
						if self.game[row][column] == 0:
							self.screen.blit(self.g_numbers[10],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
						elif self.game[row][column] == 1:
							self.screen.blit(self.g_numbers[self.numbers[row][column]],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
						elif self.game[row][column] == 2:
							if self.numbers[row][column] == 9:
								self.screen.blit(self.g_numbers[11],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
							else:
								self.screen.blit(self.g_numbers[12],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
						elif self.game[row][column] == 3:
							self.screen.blit(self.g_numbers[13],(self.OX+(self.MARGIN+self.WIDTH)*column+self.MARGIN,self.OY+(self.MARGIN+self.HEIGHT)*row+self.MARGIN))
			if self.game_status == 1: self.screen.blit(win,(DX/2 - 128,DY/2 - 26))
			elif self.game_status == 2: self.screen.blit(gameover,(DX/2 - 86,DY/2 - 58))
			#RELOAD SCREEN
			clock.tick(FPS)
			pygame.display.flip()
#FIN CLASE "MINESWEEPER"
#-----------------------

#-----------------------
#-----------------------
#MAIN - WINDOW MANAGER
resolution = (640,340+64*(len(m_graphics)))
screen = pygame.display.set_mode(resolution)
caption = "Buscaminas by Razorbreak"
pygame.display.set_caption(caption)
pygame.display.set_icon(pygame.image.load("Graficos/Buscaminas.ico"))
clock = pygame.time.Clock()
FPS = 20 # Frames Por Segundo (solo menu)

#DEFAULT GAME CONFIGURATION
M = 9       # ancho del panel (en cuadros)
N = 9       # alto del panel (en cuadros)
MINAS = 10  # numero de minas
WIDTH = 40  # ancho cuadros
HEIGHT = 40 # alto cuadros
MARGIN = 1  # bordes cuadros
OX = 0      # origen X del panel de juego
OY = 50     # origen Y del panel de juego
caption = "Buscaminas - Easy %dx%d - %d minas" % (M,N,MINAS) # nombre de la ventana

#INITIAL MENU
exit = False
difficulty = 0 # Easy = 0, Medium = 1, Hard = 2
while not exit:
	#FETCH EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True #Finish game
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			button = pygame.mouse.get_pressed()
			if button == (True,False,False):
				#Click sobre Opcion "Nuevo Juego"
				if m_graphics[1].get_rect(center=(320,372)).collidepoint(pos):
					DX = OX + M * (WIDTH+MARGIN) + MARGIN  # destino X panel de juego
					DY = OY + N * (HEIGHT+MARGIN) + MARGIN # destino Y panel de juego
					screen = pygame.display.set_mode((DX,DY))
					newgame = Minesweeper(N,M,MINAS,WIDTH,HEIGHT,MARGIN,OX,OY,DX,DY,screen,g_numbers)
					pygame.display.set_caption(caption)
					newgame.start(g_win,g_gameover)
					screen = pygame.display.set_mode(resolution)
					pygame.display.set_caption("Buscaminas by Razorbreak")
				#Click sobre "Dificultad"
				elif m_difficulty[difficulty].get_rect(center=(320,436)).collidepoint(pos):
					difficulty += 1
					if difficulty >= len(m_difficulty): difficulty -= 3
					if difficulty == 0:
						N = 9
						M = 9
						MINAS = 10
						WIDTH = 40
						HEIGHT = 40
						caption = "Buscaminas - Easy %dx%d - %d minas" % (M,N,MINAS)
					elif difficulty == 1:
						N = 16
						M = 16
						MINAS = 32
						WIDTH = 30
						HEIGHT = 30
						caption = "Buscaminas - Medium %dx%d - %d minas" % (M,N,MINAS)
					elif difficulty == 2:
						N = 16
						M = 30
						MINAS = 72
						WIDTH = 25
						HEIGHT = 25
						caption = "Buscaminas -  Hard %dx%d - %d minas" % (M,N,MINAS)
				#Click sobre Opcion "Salir"
				elif m_graphics[2].get_rect(center=(320,500)).collidepoint(pos):
					exit = True #Finish game
			
	#RENDERING MENU
	if not exit:
		screen.fill(WHITE)
		screen.blit(m_graphics[0],(0,0))
		screen.blit(m_graphics[1],(192,340)) #New Game
		screen.blit(m_difficulty[difficulty],(192,404)) #Difficulty
		screen.blit(m_graphics[2],(192,468)) #Exit
		clock.tick(FPS)
		pygame.display.flip()
	else:
		screen.fill(BLACK)
		screen.blit(m_final,(0,resolution[1]/2-154))
		pygame.display.flip()

pygame.quit() #Close game engine

#--------------------------
#--Created by Razorbreak---
#--------------------------
#--------------------------
