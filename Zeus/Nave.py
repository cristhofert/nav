# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *

import sys, os
import random
random.seed(0)

import time
import threading

from Enemigos import Enemigo, Enemigo_Final

DIRECTORIO_ZEUS = os.getcwd()+"/"

# Numeros de pixels
VELOCIDAD_BALA = 17
VELOCIDAD_NAVE = 20
CENTRO_DE_NAVE = 44
ESPACIO_ENTRE_ENEMIGOS = 20
CENTRO_INFERIOR = 450, 650
TRAYECTO_DE_BALA = 450

# Imagenes
BALA = DIRECTORIO_ZEUS+"Imagenes/_bala.bmp"
NAVE = DIRECTORIO_ZEUS+"Imagenes/spaceship.png"

# Sonidos
EXPLOSION = DIRECTORIO_ZEUS+"Sonidos/explosion.ogg"

# Otros 
IZODE = ["izquierda", "derecha"]
MAGENTA  = (255, 0, 255)

class Nave(pygame.sprite.Sprite):

	def __init__(self, sprites, zeus):

		pygame.sprite.Sprite.__init__(self)
		
		self.nave = pygame.image.load(NAVE)
		self.image = self.nave
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = CENTRO_INFERIOR
		self.sprites = sprites

		self.enemigos = [] 
		self.cantidad_enemigos = 0

		self.zeus = zeus
		self.puntaje = 0
		self.vida = 100
		self.enemigos_muertos = 0
		self.explosion = 0
		self.hat_joy = 0

		self.vol_FX = zeus.get_configuracion("vol_FX")
		nivel = zeus.get_configuracion("nivel")

		if nivel == 1:
			self.balas_disponibles = 200

		elif nivel == 2:
			self.balas_disponibles = 300

		elif nivel == 3:
			self.balas_disponibles = 450

		self.nivel = nivel

		self.generar_enemigo(3, moverse = False)


	def update(self):
		teclas = pygame.key.get_pressed()

		if self.zeus.joystick != None:
			try:

				self.hat_joy = self.zeus.joystick.get_hat(0)

				if self.hat_joy == (-1, 0) and not self.rect.x <= 10:  self.rect.x -= VELOCIDAD_NAVE
				elif self.hat_joy == (1, 0) and not self.rect.x >= 930: self.rect.x += VELOCIDAD_NAVE
				elif self.hat_joy == (0, -1) and not self.rect.y >= 650: self.rect.y += VELOCIDAD_NAVE
				elif self.hat_joy == (0, 1) and not self.rect.y <= 50: self.rect.y -= VELOCIDAD_NAVE

				elif self.hat_joy == (1, 1) and not self.rect.y <= 50: 
					self.rect.y -= VELOCIDAD_NAVE
					self.rect.x += VELOCIDAD_NAVE

				elif self.hat_joy == (-1, -1) and not self.rect.y <= 50: 
					self.rect.y += VELOCIDAD_NAVE
					self.rect.x -= VELOCIDAD_NAVE

				elif self.hat_joy == (-1, 1) and not self.rect.y <= 50: 
					self.rect.y -= VELOCIDAD_NAVE
					self.rect.x -= VELOCIDAD_NAVE

				elif self.hat_joy == (1, -1) and not self.rect.y <= 50: 
					self.rect.y += VELOCIDAD_NAVE
					self.rect.x += VELOCIDAD_NAVE
			
			except: pass
		
		if teclas[K_RIGHT] and not self.rect.x >= 930:
        		 self.rect.x += VELOCIDAD_NAVE
				
		elif teclas[K_LEFT] and not self.rect.x <= 10:
			self.rect.x -= VELOCIDAD_NAVE

		elif teclas[K_UP] and not self.rect.y <= 50:
			self.rect.y -= VELOCIDAD_NAVE

		elif teclas[K_DOWN] and not self.rect.y >= 650:
			self.rect.y += VELOCIDAD_NAVE	


		for enemigo in self.enemigos:
			if pygame.sprite.collide_rect(self, enemigo) and enemigo.estado:
				self.vida -= 0.1

		if self.explosion == 6:
			self.sprites.remove(self)
			self.kill()
			self.estado = False

			self.zeus.estado = "fin_del_juego"
			self.zeus.RunFinJuego()
			
		elif self.explosion > 0 and self.explosion < 5:
			self.image = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/Explosiones/_"+str(self.explosion)+".png")
			self.explosion += 1


		if self.vida <= 0 and not self.explosion:
			explosion = pygame.mixer.Sound(EXPLOSION)
			explosion.set_volume(self.vol_FX)
			explosion.play()
			#time.sleep(1)
			self.explosion = 1
		
	def generar_enemigo(self, cantidad, moverse = False):
		for enemigo in range(cantidad):
			enemigo = Enemigo(self, self.cantidad_enemigos, self.zeus)
			enemigo.primera_vez = random.choice(IZODE)
			lista_de_y = []
			hay_elemento = False
			for y in self.enemigos:
				lista_de_y.append(y.rect.y)
				hay_elemento = True

			if hay_elemento and not moverse:
				enemigo.rect.y = max(lista_de_y)+100+ESPACIO_ENTRE_ENEMIGOS

			elif hay_elemento and moverse:
				enemigo.moverse_hasta = moverse

			elif not hay_elemento: enemigo.rect.y = 50+ESPACIO_ENTRE_ENEMIGOS


			self.sprites.add(enemigo)
			self.enemigos.append(enemigo)
			self.cantidad_enemigos += 1

	def generar_enemigo_final(self):
		enemigo = Enemigo_Final(self, self.zeus)
		for _enemigo in self.enemigos:
			self.sprites.remove(_enemigo)
			_enemigo.kill()
			del _enemigo 

		self.enemigos = list()
		self.enemigos.append(enemigo)
		self.sprites.add(enemigo)		

	def evento(self, event):
		if event.type == JOYBUTTONDOWN:
			if event.button == 2:
				if self.balas_disponibles:
					bala = Bala(self.sprites, self.enemigos)
					bala.disparar(self)
					self.balas_disponibles -= 1		
		
		elif event.type == KEYDOWN:
			tecla = event.key	
			if tecla == K_LCTRL or tecla == K_x:
				if self.balas_disponibles:
					bala = Bala(self.sprites, self.enemigos)
					bala.disparar(self)
					self.balas_disponibles -= 1
				

	def recibir_disparo(self, tipo):
		self.vida -= 2
		if tipo == 2: self.vida -= 8
		elif tipo == 3: self.vida -= 3
		elif tipo == 4: self.vida -= 4

	def borrar_todo(self):
		self.zeus.sprites.remove(self.zeus.barra_de_estado)
		self.zeus.barra_de_estado.kill()
		del self.zeus.barra_de_estado

		for enemigo in self.enemigos:
			enemigo.explosion = 5

		self.zeus.sprites.remove(self.zeus.nave)
		self.zeus.nave.kill()

		self.zeus.nave = None


class Bala(pygame.sprite.Sprite):

	def __init__(self, sprites, enemigos):

		pygame.sprite.Sprite.__init__(self)

		self.imagen_original = pygame.image.load(BALA)
		
		self.image = self.imagen_original.copy()
		self.image.set_colorkey(MAGENTA)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = CENTRO_INFERIOR

		self.disparo = False
		self.sprites = sprites
		self.enemigos = enemigos
		self.y_de_disparo = CENTRO_INFERIOR[1] 
		self.angulo = 0
	
	def update(self):
		if self.disparo: self.rect.y -= VELOCIDAD_BALA
		if self.rect.y <= self.y_de_disparo - TRAYECTO_DE_BALA: 
			self.sprites.remove(self)
			self.kill()


		for enemigo in self.enemigos:
			if pygame.sprite.collide_rect(enemigo, self) and enemigo.estado:
				enemigo.recibir_disparo()
				self.sprites.remove(self)
				self.kill()
				break

		self.angulo += 1
		self.image = pygame.transform.rotate(self.imagen_original, self.angulo)


	def disparar(self, nave):
		self.sprites.add(self)
		self.disparo = True
		self.y_de_disparo = nave.rect.y
		self.rect.x, self.rect.y = nave.rect.x+CENTRO_DE_NAVE, nave.rect.y
		
		self.nave = nave
