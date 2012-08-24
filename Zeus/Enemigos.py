# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *

import sys, os
import random

random.seed()

DIRECTORIO_ZEUS = os.getcwd()+"/"
X_ENEMIGO = 600
LARGO_DE_ENEMIGO = 50
LARGO_ENEMIGO_2 = 240
VELOCIDAD_BALA = 17
DISPARADOR_1 = 10
DISPARADOR_2 = 70
DISPARADOR_1_2 =  60
DISPARADOR_2_2 = 175
ENEMIGOS_SIMPLES = ["1", "3", "4"]

VELOCIDAD_1 = 10
VELOCIDAD_2 = 16
VELOCIDAD_3 = 22

# Imagenes
ENEMIGO1 = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_1.png"
ENEMIGO1_1TIRO = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_1_1.png"
ENEMIGO2 = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_2.png"
ENEMIGO2_FALLA = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_2_2.png"
ENEMIGO3 = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_3.png"
ENEMIGO4 = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_4.png"
BALA = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_bala.png"
BALA2 = DIRECTORIO_ZEUS+"Imagenes/Enemigos/_bala_2.png"

# Sonidos
EXPLOSION = DIRECTORIO_ZEUS+"Sonidos/explosion.ogg"

# Colores
MAGENTA  = (255, 0, 255)

class Enemigo(pygame.sprite.Sprite):

	def __init__(self, nave, numero_enemigo, zeus):

		pygame.sprite.Sprite.__init__(self)

		nivel = zeus.get_configuracion("nivel")

		if nivel == 1:
			self.velocidad = VELOCIDAD_1
			self.enemigo_1 = pygame.image.load(ENEMIGO1)
			self.tipo_enemigo = "1"

		elif nivel == 2:
			self.velocidad = VELOCIDAD_2
			self.enemigo_1 = pygame.image.load(ENEMIGO3)
			self.tipo_enemigo = "3"

		elif nivel == 3:
			self.velocidad = VELOCIDAD_3
			self.enemigo_1 = pygame.image.load(ENEMIGO4)
			self.tipo_enemigo = "4"
		
	
		self.image = self.enemigo_1
		self.rect = self.image.get_rect()
		self.rect.x = X_ENEMIGO
		self.nave = nave
		
		self.primera_vez = None
		self.disparos = 0
		self.explosion = 0 
		self.enemigo_numero = numero_enemigo
		self.adelante = True
		self.estado = True
		self.moverse_hasta = 0
		self.tiempo = 0

		self.nivel = nivel

		self.zeus = zeus
		self.vol_FX = self.zeus.get_configuracion("vol_FX")

	def update(self):

		if self.nivel >= 2:
			if self.tiempo + 5 <= self.zeus.get_tiempo():
				bala = Bala(self.zeus.sprites, self, self.nave, tipo=self.tipo_enemigo)
				bala.disparar(DISPARADOR_1, pos_nave = self.nave.rect.y)

				bala = Bala(self.zeus.sprites, self, self.nave, tipo=self.tipo_enemigo)
				bala.disparar(DISPARADOR_2, pos_nave = self.nave.rect.y)
				self.tiempo = self.zeus.get_tiempo()

		if self.primera_vez == "izquierda":
			self.primera_vez = "ya hecha"
			self.adelante = False
		
		elif self.primera_vez == "derecha":
			self.primera_vez = "ya hecha"
			self.adelante = True

		elif self.primera_vez == "ya hecha":
			if self.rect.x <= 0: self.adelante = True
			elif self.rect.x >= 930: self.adelante = False

			if self.adelante: self.rect.x += self.velocidad
			elif not self.adelante: self.rect.x -= self.velocidad	

		if self.explosion == 5:
			self.nave.enemigos_muertos += 1
			self.nave.sprites.remove(self)
			self.kill()
			self.estado = False

			if self.nivel == 1: numero = 12
			elif self.nivel == 2: numero = 22
			elif self.nivel == 3: numero = 32

			if self.nave.enemigos_muertos < numero:
				self.nave.generar_enemigo(1, moverse = self.rect.y)

			elif self.nave.enemigos_muertos >= numero:
				self.nave.generar_enemigo_final()
			
		elif self.explosion > 0 and self.explosion < 5:
			self.image = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/Explosiones/_"+str(self.explosion)+".png")
			self.explosion += 1

		if self.moverse_hasta and not self.rect.y >= self.moverse_hasta:
			self.rect.y += 10			


	def recibir_disparo(self):
		self.disparos += 1
		self.nave.puntaje += self.velocidad
		if self.estado:
			bala = Bala(self.zeus.sprites, self, self.nave, tipo=self.tipo_enemigo)
			bala.disparar(DISPARADOR_1, pos_nave = self.nave.rect.y)

			bala = Bala(self.zeus.sprites, self, self.nave, tipo=self.tipo_enemigo)
			bala.disparar(DISPARADOR_2, pos_nave = self.nave.rect.y)
	
		if self.disparos == 1 and self.tipo_enemigo == "1": self.image = pygame.image.load(ENEMIGO1_1TIRO)
		elif self.disparos == 2 and self.tipo_enemigo == "1": self.explotar()
		elif self.disparos == 3 and self.tipo_enemigo == "3": self.explotar()
		elif self.disparos == 4 and self.tipo_enemigo == "4": self.explotar()

	def explotar(self):
		explosion = pygame.mixer.Sound(EXPLOSION)
		explosion.set_volume(self.vol_FX)
		explosion.play()
		pygame.time.wait(1)
		self.explosion = 1
		self.rect.y -= 20

class Enemigo_Final(pygame.sprite.Sprite):

	def __init__(self, nave, zeus):

		pygame.sprite.Sprite.__init__(self)
		
		self.enemigo_2 = pygame.image.load(ENEMIGO2)
		self.image = self.enemigo_2
		self.rect = self.image.get_rect()
		self.rect.x = 300
		self.nave = nave
		
		self.explosion = 0 
		self.moverse_hasta = 200
		self.estado = False
		self.disparos = 0

		self.zeus = zeus
		self.vol_FX = self.zeus.get_configuracion("vol_FX")

	def update(self):

		if self.explosion == 6:
			self.nave.enemigos_muertos += 1
			self.nave.sprites.remove(self)
			self.kill()
			self.estado = False

		elif self.explosion > 0 and self.explosion < 6:
			self.image = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/Explosiones/_"+str(self.explosion)+"_2.png")
			self.explosion += 1

		if self.moverse_hasta and not self.rect.y >= self.moverse_hasta:
			self.rect.y += 5

		elif self.moverse_hasta and self.rect.y >= self.moverse_hasta:
			self.estado = True			


	def recibir_disparo(self):
		self.disparos += 1
		self.nave.puntaje += 15
		if self.estado:
			bala = Bala(self.zeus.sprites, self, self.nave, tipo=2)
			bala.disparar(DISPARADOR_1_2)

			bala = Bala(self.zeus.sprites, self, self.nave, tipo=2)
			bala.disparar(DISPARADOR_2_2)
	
		if self.disparos == 1: self.image = pygame.image.load(ENEMIGO2_FALLA)
		elif self.disparos == 15:
			explosion = pygame.mixer.Sound(EXPLOSION)
			explosion.set_volume(self.vol_FX)
			explosion.play()
			pygame.time.wait(1)
			self.explosion = 1
			self.rect.x += 20
			self.rect.y += 20

class Bala(pygame.sprite.Sprite):

	def __init__(self, sprites, enemigo, nave, tipo=1):

		pygame.sprite.Sprite.__init__(self)
		
		if tipo == 2:
			self.image = pygame.image.load(BALA2)

		else:
			self.image = pygame.image.load(BALA)

		self.image.set_colorkey(MAGENTA)

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = enemigo.rect.x, enemigo.rect.y

		self.disparo = False
		self.sprites = sprites
		self.enemigo = enemigo
		self.nave = nave
		self.tipo = tipo
		self.posicion_de_nave = None
	
	def update(self):
		if self.disparo: self.rect.y += VELOCIDAD_BALA
		if self.posicion_de_nave and self.rect.y >= self.posicion_de_nave: 
			self.sprites.remove(self)
			self.kill()

		if self.enemigo.estado and pygame.sprite.collide_rect(self.nave, self):
			self.nave.recibir_disparo(self.tipo)
			self.sprites.remove(self)
			self.kill()

	def disparar(self, disparador, pos_nave = None):
		self.posicion_de_nave = pos_nave
	
		self.sprites.add(self)
		self.disparo = True
		if self.tipo == 1: self.rect.x, self.rect.y = self.enemigo.rect.x+disparador, self.enemigo.rect.y + LARGO_DE_ENEMIGO
		elif self.tipo == 2: self.rect.x, self.rect.y = self.enemigo.rect.x+disparador, self.enemigo.rect.y + LARGO_ENEMIGO_2
