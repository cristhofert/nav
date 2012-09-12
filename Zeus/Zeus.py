#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *

from Nave import Nave, Bala
from Graficos import Barra_de_estado, Pausa, Boton, Menu

import random, os
import s
import time

import gc
gc.enable()

# Archivos y directorios
DIRECTORIO_ZEUS = os.getcwd()+"/"
DATOS = DIRECTORIO_ZEUS+"Datos"
CONFIGURACION = DATOS+"/Configuracion.txt"

# Resolucion pantalla
RESOLUCION = (1024, 768)

# Imagenes
NIVELES = [None, DIRECTORIO_ZEUS+"Imagenes/Fondos/u_1.jpg", DIRECTORIO_ZEUS+"Imagenes/Fondos/u_2.jpg", DIRECTORIO_ZEUS+"Imagenes/Fondos/u_3.jpg"]
FIN_JUEGO = DIRECTORIO_ZEUS+"Imagenes/Fondos/fin_del_juego.jpg"
WALLPAPER = DIRECTORIO_ZEUS+"Imagenes/Fondos/presentacion.png"
WALLPAPER_2 = DIRECTORIO_ZEUS+"Imagenes/Fondos/menu.png"
POS_IMG = 0, 50
ICONO = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/spaceship.png")

# Musica
MUSICA1 = DIRECTORIO_ZEUS+"Sonidos/inicio.ogg"
MUSICA2 = DIRECTORIO_ZEUS+"Sonidos/menu.ogg"
MUSICA3 = DIRECTORIO_ZEUS+"Sonidos/juego1.ogg"

# Fuentes
SEGOE_PRINT = DIRECTORIO_ZEUS+"Fuentes/segoepr.ttf"

# Colores
AZUL = (0, 0, 225)

# Otros
TIEMPO_ACTUALIZACION_DE_JOYSTICKS = 5

class Zeus():

	def __init__(self):
		self.nave = None
		self.fondo = None
		self.menu = None
		self.ventana = None
		self.reloj = None
		self.estado = None
		self.pausa = False
		self.joystick = None
		self.actualizacion_de_joysticks_tiempo = 0
		self.tiempo = 0
		self.sprites = pygame.sprite.OrderedUpdates()

	def Run(self):

		pygame.mouse.set_visible(False)
		self.fondo = self.fondo
		self.ventana.blit(self.fondo, (0,0))
		pygame.display.update()

		self.tiempo = 0
		while self.estado == "presentacion":
			self.reloj.tick(32)

			self.actualizar()

	def RunMenu(self):
		pygame.mixer.music.fadeout(1200)
		time.sleep(1.2)

		self.menu = Menu(self)
		self.sprites.add(self.menu)

		self.set_musica("menu")

		self.fondo = self.get_fondo("menu")
		self.ventana.blit(self.fondo, (0,0))
		pygame.display.update()
		
		self.tiempo = 0
		while self.estado == "menu":
			self.reloj.tick(32)

			self.actualizar()

	def RunJuego(self):
                pygame.mixer.music.fadeout(1200)
		time.sleep(1.2)

		self.set_musica("juego")

		self.nave = Nave(self.sprites, self)		
		self.barra_de_estado = Barra_de_estado(self.nave)

		self.sprites.add(self.nave)
		self.sprites.add(self.barra_de_estado)		

		self.sprites.clear(self.ventana, self.fondo)
		self.sprites.draw(self.ventana)

		self.fondo = self.get_fondo("en_juego")
		self.ventana.blit(self.fondo, (0,0))	
		self.estado = "en_juego"

		pygame.mouse.set_visible(False)
		pygame.display.update()

		self.tiempo = 0
		self.pos_fondo = 0
	
		while self.estado == "en_juego":
			self.reloj.tick(32)
			self.actualizar()

	def RunFinJuego(self):
		self.nave.borrar_todo()

		self.sprites.clear(self.ventana, self.fondo)
		self.sprites.draw(self.ventana)

		self.fondo = self.get_fondo("fin_del_juego")
		self.ventana.blit(self.fondo, (0,0))	

		pygame.display.update()

		self.tiempo = 0
	
		while self.estado == "fin_del_juego":

			self.reloj.tick(10)

			self.actualizar()	


	def setup(self):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		
		self.actualizar_joysticks()
		self.segoepr = pygame.font.Font(SEGOE_PRINT, 30)
		
		pygame.display.set_mode(RESOLUCION, 0,0)
		pygame.display.set_caption(".: Zeus :.")
		pygame.display.set_icon(ICONO)
		#pygame.display.toggle_fullscreen()
				
		self.set_musica("inicio")

		self.ventana = pygame.display.get_surface()
		self.reloj = pygame.time.Clock()
		self.estado = "presentacion"
		self.fondo = self.get_fondo("inicio")
		self.sprites.draw(self.ventana)

		pygame.display.update()

	def get_fondo(self, tipo="inicio"):
		fondo = pygame.surface.Surface(RESOLUCION,  flags=HWSURFACE)

		if tipo == "inicio":
			imagen = pygame.image.load(WALLPAPER)
			fondo.blit(imagen, POS_IMG)
			fondo.blit(self.segoepr.render(".: Presiona espacio para continuar :.", 1, AZUL), (350, 700))

		elif tipo == "en_juego":
			imagen = pygame.image.load(NIVELES[self.get_configuracion("nivel")])
			fondo.blit(imagen, (0,0))

		elif tipo == "menu":
			imagen = pygame.image.load(WALLPAPER_2)
			fondo.blit(imagen, POS_IMG)

		elif tipo == "fin_del_juego":
			imagen = pygame.image.load(FIN_JUEGO)
			fondo.blit(imagen, POS_IMG)
		
		else: print "Ese fondo no existe, igual se retorna una superficie en negro"

		return fondo

	def set_musica(self, tipo="incio y menu"):
		if tipo == "inicio":
			pygame.mixer.music.load(MUSICA1)
			pygame.mixer.music.play(-1, 0.0)
		
		elif tipo == "menu":
			pygame.mixer.music.load(MUSICA2)
			pygame.mixer.music.play(-1, 0.0)			

		elif tipo == "juego":
			pygame.mixer.music.load(MUSICA3)
			pygame.mixer.music.play(-1, 0.0)

	def handle_event(self):
		for event in pygame.event.get():

   			if event.type == QUIT:
      				exit()

   			elif event.type == KEYDOWN:
				if event.key == K_q: exit()
		
				elif event.key == K_ESCAPE and self.estado == "en_juego":
					self.set_pausa()

				if self.estado == "presentacion" and event.key == K_SPACE:
					self.estado = "menu"
					self.RunMenu()				


			elif event.type == JOYBUTTONDOWN:
				if event.button == 8 and self.estado == "en_juego":
					self.set_pausa()

				if self.estado == "presentacion" and event.button == 0:
					self.estado = "menu"
					self.RunMenu()
			

			try: self.nave.evento(event)
			except: pass
			try: self.dialogo_pausa.actualizar_eventos(event)
			except: pass
			try: self.menu.actualizar_eventos(event)
			except: pass

				

		pygame.event.clear()

	def get_configuracion(self, tipo):
		# abrir archivo:
		config = open(CONFIGURACION, "r")		
		configuracion = {"vol_FX": 0.7, "vol_musica": 0.5, "vol_musica_menu": 1.0, "nivel": 1}
		
		for cfg in config.readlines():
			variable = cfg.split(" = ")
			nombre = variable[0]
			info = variable[1]
			
			if nombre == "vol_fx":
				configuracion["vol_FX"] = float(info)
			
			elif nombre == "vol_musica":
				configuracion["vol_musica"] = float(info)

			elif nombre == "vol_musica_menu":
				configuracion["vol_musica_menu"] = float(info)

			elif nombre == "nivel":
				configuracion["nivel"] = int(info)

		if tipo == "vol_FX": configuracion = configuracion["vol_FX"]
		elif tipo == "vol_musica": configuracion = configuracion["vol_musica"]
		elif tipo == "vol_musica_menu": configuracion = configuracion["vol_musica_menu"]
		elif tipo == "nivel":  configuracion = configuracion["nivel"]

		return configuracion

	def get_tiempo(self):
		return int(self.tiempo)

	def set_pausa(self):
		if not self.pausa:
			self.pausa = True
			self.dialogo_pausa = Pausa(self)

			self.sprites.add(self.dialogo_pausa)

		elif self.pausa:
			self.dialogo_pausa.escape()

	def actualizar(self):

		self.tiempo += 0.032

		self.actualizar_graficos()
		
		if self.actualizacion_de_joysticks_tiempo + TIEMPO_ACTUALIZACION_DE_JOYSTICKS <= self.get_tiempo():
			self.actualizar_joysticks()
			self.actualizacion_de_joysticks_tiempo = self.get_tiempo()

	def actualizar_graficos(self, sprites=True):
		cambios=[]

		if self.estado == "en_juego":
			self.pos_fondo += 1
			self.fondo = self.get_fondo(tipo = "en_juego")

		self.sprites.clear(self.ventana, self.fondo)
		if not self.pausa:
			self.sprites.update()
			
		elif self.pausa:
			self.dialogo_pausa.update()
		cambios.extend ( self.sprites.draw(self.ventana) )
		self.handle_event()
		if sprites: pygame.display.update(cambios)		
		elif not sprites: pygame.display.update()

	def actualizar_joysticks(self):
		if pygame.joystick.get_init(): pygame.joystick.quit()
		elif not pygame.joystick.get_init(): self.joystick = None
		pygame.joystick.init()

		if pygame.joystick.get_count():
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
		
		if self.joystick != None: "Joystick conectado"
		elif self.joystick == None: "Joystick desconectado"	
	
if __name__ == "__main__":
	zeus = Zeus()
	zeus.setup()
	zeus.Run()
