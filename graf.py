import pygame
from pygame.locals import *

AZUL = (0,0,255)
AZUL2 = (127,127,255)
AZUL3 = (200,200,255)
ROJO = (255,0,0)
AMARILLO = (255,255,0)
VERDE = (0,255,0)
MORADO = (255,0,255)
NARANJA = (255,127,0)
CAFE = (127,64,127)
NEGRO = (0,0,0)
BLANCO = (255,255,255)


class Pantalla:
        def __init__(self,Width=640,Height=480):
                if not pygame.display.get_init():
                        pygame.init()
                self.Width = Width
                self.Height = Height
                self.Screen = pygame.display.set_mode((self.Width,self.Height))
        def actualizar(self):
                pygame.display.update()
                pygame.display.flip()
	def endloop(self):
		for evento in pygame.event.get():
	                if evento.type == pygame.QUIT:
	                     self.cerrar()
        def cerrar(self):
                pygame.display.quit()

	def elipse(self,centro,dhor,dver,color=ROJO,width=0):
		P1 = int(round(-dhor/2.0+centro[0])), int(round(-dver/2.0+centro[1]))
		P2 = int(round(dhor/2.0+centro[0])), int(round(dver/2.0+centro[1]))
		pygame.draw.ellipse(self.Screen, color, P1+P2,width)
		
	def linea(self,origen,destino,color=NEGRO):
		pygame.draw.aaline(self.Screen,color,origen,destino)
	
	def punto(self,x,y,color=AZUL):
		pygame.draw.circle(self.Screen,color,(x,y),0)
	def fondo(self,color=BLANCO):
		self.Screen.fill(color)

