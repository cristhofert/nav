# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *

import os, sys

DIRECTORIO_ZEUS = os.getcwd()+"/"

NARANJA = ( 225, 112, 5 )
VERDE = ( 0, 225, 0 )
ROJO = ( 225, 0, 0 ) 
MAGENTA  = ( 255, 0, 255 )
NEGRO = ( 0, 0, 0 )
AZUL = ( 0, 0, 225 )
BLANCO = ( 225, 225, 225 )
VIOLETA = ( 170, 0, 225 )
CELESTE = ( 0, 225, 225 )
FUENTE_BARRA = DIRECTORIO_ZEUS+"Fuentes/segoepr.ttf"

BALA = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/bala_estado.png")

class Menu(pygame.sprite.OrderedUpdates):
		
	def __init__(self, zeus):

		pygame.sprite.OrderedUpdates.__init__(self)

		self.zeus = zeus

		# Jugar:
		jugar = Boton(texto="Jugar!", tamanio=(248, 58), tamanio_fuente=25, pos_texto=(80, 5), funcion=self.jugar)
		jugar.moverse_hasta = 300
		jugar.set_x(512)
		jugar.set_activado()
		
		# Instrucciones
		ayuda = Boton(texto="Instrucciones",tamanio_fuente=25, dialogo=self, funcion=zeus.set_pausa, tamanio=(248, 58))
		ayuda.moverse_hasta = 358
		ayuda.set_x(512)

		# Opciones:
		opciones = Boton(texto="Opciones", tamanio_fuente=25,dialogo=self, tamanio=(248, 58))
		opciones.moverse_hasta = 416
		opciones.set_x(512)

		# Creditos:
		creditos = Boton(texto="Creditos", tamanio_fuente=25,dialogo=self, tamanio=(248, 58))
		creditos.moverse_hasta = 474
		creditos.set_x(512)	

		# Salir:
		salir = Boton(texto="Salir", tamanio_fuente=25, dialogo=self, tamanio=(248, 58), funcion=exit)
		salir.moverse_hasta = 532
		salir.set_x(512)

		# ******* OPCIONES *******

		configuracion = self.zeus.get_configuracion("todo")

		# volumen FX:
		vol_fx = HEscala(configuracion=configuracion["vol_FX"])
		vol_fx.moverse_hasta = 300
		vol_fx.rect.x = 512
		vol_fx.set_activado()

		# volumen musica:
		vol_musica = HEscala(configuracion=configuracion["vol_musica"], texto="Volumen musica")
		vol_musica.moverse_hasta = 300
		vol_musica.rect.x = 512

		# volumen musica del menu:
		vol_musica_menu = HEscala(configuracion=configuracion["vol_musica_menu"], texto="Volumen musica del menu")
		vol_musica_menu.moverse_hasta = 300
		vol_musica_menu.rect.x = 512
		
		# Boton Volver
		volver = Boton(texto="Volver", dialogo=self, funcion=self.main_dialog, color_fondo=NARANJA, color_texto_2=VERDE, color_texto_1=BLANCO)
		volver.moverse_hasta = 300
		volver.set_x(512)	
		

		self.add(ayuda)
		self.add(creditos)
		self.add(opciones)
		self.add(salir)
		self.add(vol_fx)
		self.add(vol_musica)
		self.add(vol_musica_menu)
		self.add(volver)
		self.add(jugar)

		self.pos = 0
		self.estado = "menu"

		self.botones = [jugar, ayuda, opciones, creditos, salir]
		self.botones_opciones = [vol_fx, vol_musica, vol_musica_menu, volver]
			

	def actualizar_eventos(self, evento):

		if evento.type == KEYDOWN:
			if evento.key == K_UP:
				if self.pos > 0: self.pos -= 1
				else: self.pos = len(self.botones) -1

			elif evento.key == K_DOWN:
				if self.pos < len(self.botones) -1: self.pos += 1
				else: self.pos = 0

			if self.estado == "menu":

				for boton in self.botones:
					boton.set_activado(False)
	
				self.botones[self.pos].set_activado(True) 

			elif self.estado == "opciones":
				for boton in self.botones_opciones:
					boton.set_activado(False)
	
				self.botones_opciones[self.pos].set_activado(True) 


	def escape(self):
		if self.botones[0].texto == "Opciones": self.main_dialog()


	def main_dialog(self):
		self.estado = "menu"

		for x in self.botones_opciones:
			x.hacia = "arriba" 
			x.moverse_hasta = 300

		self.botones[0].set_texto("Jugar!")
		self.botones[0].set_pos_texto((80, 5))
		self.botones[0].set_activado()

		self.botones[1].moverse_hasta = 350
		self.botones[1].hacia = "abajo"

		self.botones[2].moverse_hasta = 416
		self.botones[2].hacia = "abajo"

		self.botones[3].moverse_hasta = 474
		self.botones[3].hacia = "abajo"

		self.botones[4].moverse_hasta = 532
		self.botones[4].hacia = "abajo"
		

	def opciones(self):
		self.estado = "opciones"
		self.pos = 0
		for x in self.botones:
			if not self.botones.index(x) == 0:
				x.hacia = "arriba" 
				x.moverse_hasta = 300
			else: 
				x.color_fondo = NEGRO
				x.color_texto_2 = NARANJA
				x.color_texto_1 = NARANJA
				x.set_texto("Opciones")
				x.set_pos_texto((70, 5))

		self.botones_opciones[0].moverse_hasta = 358
		self.botones_opciones[1].moverse_hasta = 406
		self.botones_opciones[2].moverse_hasta = 454
		self.botones_opciones[3].moverse_hasta = 502

	def jugar(self):
		self.zeus.sprites.remove(self)
		self.zeus.estado = "en_juego"
		self.zeus.RunJuego()

class Barra_de_estado(pygame.sprite.Sprite):

	def __init__(self, nave):
		
		pygame.sprite.Sprite.__init__(self)
		
		self.superficie = pygame.surface.Surface((1024, 45), flags=HWSURFACE)
		self.fondo = nave.zeus.get_fondo("en_juego")
		
		self.superficie.blit(self.fondo, (0,0))
	
		self.image = self.superficie
		self.rect = self.superficie.get_rect()

		self.nave = nave
	
		self.fuente = pygame.font.Font(FUENTE_BARRA, 20)

	def update(self):
		self.superficie.blit(self.fondo, (0,0))

		balas = self.fuente.render(str(self.nave.balas_disponibles), 1, NARANJA)

		barra = Barra_de_progreso()
		barra.set_porcentaje(self.nave.vida)
		
		puntaje = self.nave.puntaje

		cuadro = Cuadro_informacion()
		cuadro.actualizar(["Puntos: "+str(puntaje), "Muertes: "+str(self.nave.enemigos_muertos)])
	
		self.superficie.blit(barra, (20,20))
		self.superficie.blit(BALA, (392, 15))
		self.superficie.blit(balas, (432, 15))
		self.superficie.blit(cuadro, (700, 10))

class Barra_de_progreso(pygame.surface.Surface):

	def __init__(self):
		
		pygame.surface.Surface.__init__(self, (150, 20), flags=HWSURFACE)	
		self.fill(NARANJA)
		self.fuente = pygame.font.Font(FUENTE_BARRA, 12)

		self.set_porcentaje(0)
				
	def set_porcentaje(self, porcentaje):
		if porcentaje >= 0:
			pixels = porcentaje * 150 / 100

			self.fill(ROJO)
			borde1 = pygame.draw.rect(self, NEGRO, (0, 0, 150, 20), 3)

			barra = pygame.surface.Surface((pixels, 20), flags=HWSURFACE)
			barra.fill(VERDE)
			borde = pygame.draw.rect(barra, NEGRO, (0, 0, pixels, 20), 3)
			
			texto = self.fuente.render("Energia "+str(porcentaje)+"%", 1, AZUL)		

			self.blit(barra, (0,0))
			self.blit(texto, (30, 0))


class Cuadro_informacion(pygame.surface.Surface):

	def __init__(self):
		pygame.surface.Surface.__init__(self, (220, 35), flags=HWSURFACE)	
		self.fuente = pygame.font.Font(FUENTE_BARRA, 14)
		self.set_colorkey(NEGRO)
		self.fill(NEGRO)

	def actualizar(self, info = ["Puntos: 0", "Muertes: 0"]):
		cuadro = pygame.draw.rect(self, NARANJA, (0, 0, 220, 35), 1)
		linea = pygame.draw.line(self, NARANJA, (110, 0), (110, 35))

		texto1 = self.fuente.render(info[0], 1, BLANCO)
		texto2 = self.fuente.render(info[1], 1, BLANCO) 	
	
		self.blit(texto1, (5, 5))
		self.blit(texto2, (120,  5))

class Pausa(pygame.sprite.OrderedUpdates):
		
	def __init__(self, zeus):

		pygame.sprite.OrderedUpdates.__init__(self)

		self.zeus = zeus

		# Pausa:
		pausa = Boton(texto="Pausa", color_fondo=NEGRO, color_texto_1=NARANJA, tamanio_fuente=25, pos_texto=(80, 5))
		pausa.moverse_hasta = 240
		pausa.set_x(384)
		pausa.set_activado(False)
		
		# Boton Volver
		volver = Boton(texto="Volver", dialogo=self, funcion=zeus.set_pausa)
		volver.moverse_hasta = 300
		volver.set_x(384)
		volver.set_activado()	

		# Opciones:
		opciones = Boton(texto="Opciones", dialogo=self)
		opciones.moverse_hasta = 348
		opciones.set_x(384)

		# Menu Principal:
		menu = Boton(texto="Menu Principal", dialogo=self, funcion=self.ir_menu)
		menu.moverse_hasta = 396
		menu.set_x(384)	
		
		self.add(menu)
		self.add(opciones)
		self.add(volver)
		self.add(pausa)

		self.pos = 1

		self.botones = [pausa, volver, opciones, menu]
		self.botones_opciones = []

	def ir_menu(self):
		self.zeus.nave.borrar_todo()
		self.destruir()
		self.zeus.estado = "menu"
		self.zeus.RunMenu()	

	def actualizar_eventos(self, evento):

		if evento.type == KEYDOWN:
			if evento.key == K_UP:
				if self.pos > 1: self.pos -= 1
				else: self.pos = 3

			elif evento.key == K_DOWN:
				if self.pos < 3: self.pos += 1
				else: self.pos = 1

			for boton in self.botones:
				boton.set_activado(False)
	
			self.botones[self.pos].set_activado(True) 

		if self.zeus.joystick: 
			h = self.joystick.get_hat(0)

			if h[0] == -1: 
				if self.pos > 1: self.pos -= 1
				else: self.pos = 3
			
			elif h[0] == 1:
				if self.pos < 3: self.pos += 1
				else: self.pos = 1

	def escape(self):
		if self.botones[0].texto == "Opciones": self.main_dialog()
		else:
			for boton in self.botones:
				boton.hacia = "arriba"
				boton.moverse_hasta = 10

	def destruir(self):
		self.zeus.sprites.remove(self)
		self.zeus.pausa = False

	def main_dialog(self):
		for x in self.botones_opciones:
			x.hacia = "arriba" 
			x.moverse_hasta = 240

		self.botones[0].set_texto("Pausa")
		self.botones[0].set_pos_texto((80, 5))

		self.botones[1].moverse_hasta = 300
		self.botones[1].hacia = "abajo"

		self.botones[2].moverse_hasta = 348
		self.botones[2].hacia = "abajo"

		self.botones[3].moverse_hasta = 396
		self.botones[3].hacia = "abajo"
		

	def opciones(self):
		for x in self.botones:
			if not self.botones.index(x) == 0:
				x.hacia = "arriba" 
				x.moverse_hasta = 240
			else: 
				x.set_texto("Opciones")
				x.set_pos_texto((70, 5))


class Boton(pygame.sprite.Sprite):

	def __init__(self, 
		     texto="", 
		     tamanio = (248, 48),
		     tamanio_fuente=20, 
                     color_fondo=NARANJA, 
                     dialogo=None, 
                     funcion=None,
		     color_texto_1=NEGRO,
		     color_texto_2=BLANCO,
		     pos_texto=(60, 10)):
		
		pygame.sprite.Sprite.__init__(self)

		self.fuente = pygame.font.Font(FUENTE_BARRA, tamanio_fuente)
		self.activado = False
		self.texto = texto
		self.color_fondo = color_fondo
		self.color_texto_1 = color_texto_1
		self.color_texto_2 = color_texto_2
		self.pos_texto = pos_texto
		self.superficie = pygame.surface.Surface(tamanio, flags=HWSURFACE)

		self.moverse_hasta = 0
		self.hacia = "abajo"

		self.image = self.get_surface(texto)
		self.rect = self.image.get_rect()

		self.rect.x, self.rect.y = 300, 0

		if self.color_fondo == MAGENTA: self.superficie.set_colorkey(MAGENTA)

		self.dialogo = dialogo
		self.funcion = funcion

	def set_texto(self, texto): self.texto = texto
	def set_pos_texto(self, pos): self.pos_texto = pos

	def get_surface(self, texto):
		self.superficie.fill(self.color_fondo)

		if self.activado:
			self.superficie.fill(self.color_texto_1)
			texto_boton = self.fuente.render(texto, 1, self.color_fondo)
			imagen = pygame.image.load(DIRECTORIO_ZEUS+"Imagenes/navecita.png")

			self.superficie.blit(imagen, (0,0))
		
		elif not self.activado:
			texto_boton = self.fuente.render(texto, 1, self.color_texto_1)


		self.superficie.blit(texto_boton, self.pos_texto)
			

		return self.superficie

	def set_x(self, x):
		self.rect.x = x		

	def set_activado(self, tf=True):
		self.activado = tf
		self.image = self.get_surface(self.texto)
	
	def update(self):
		self.image = self.get_surface(self.texto)

		if self.moverse_hasta and not self.rect.y >= self.moverse_hasta and not self.hacia == "arriba":
			self.rect.y += 10

		elif self.moverse_hasta and not self.rect.y <= self.moverse_hasta and not self.hacia == "abajo":
			self.rect.y -= 10
	
		if self.texto == "Menu Principal" and self.dialogo and self.hacia == "arriba" and self.rect.y == 10: self.dialogo.destruir()

		teclas = pygame.key.get_pressed()

		if teclas[K_RETURN] and self.activado and self.funcion: self.funcion()
		if teclas[K_RETURN] and self.activado and self.dialogo and self.texto == "Opciones": self.dialogo.opciones()
		
		if self.dialogo and self.dialogo.zeus.joystick:
			if self.dialogo.zeus.joystick.get_button(2) and self.activado and self.funcion: self.funcion() 
			elif self.dialogo.zeus.joystick.get_button(2) and self.activado and self.dialogo and self.texto == "Opciones": self.dialogo.opciones()

class HEscala(pygame.sprite.Sprite):
	
	def __init__(self,
		     texto = "Volumen FX",
		     pos_texto = (60, 30),
		     configuracion = 0,
		     color_fondo_barra=NEGRO, 
                     color_fondo=NARANJA, 
		     color_control=VERDE):
		
		pygame.sprite.Sprite.__init__(self)

		self.fuente = pygame.font.Font(FUENTE_BARRA, 9)

		self.color_fondo = color_fondo
		self.color_control = color_control
		self.color_fondo_barra = color_fondo_barra
		self.texto = texto
		self.pos_texto = pos_texto

		self.superficie = pygame.surface.Surface((248, 48), flags=HWSURFACE)

		self.moverse_hasta = 300
		self.hacia = "abajo"
		self.pos = configuracion

		self.activado = False

		self.image = self.get_surface(texto)
		self.rect = self.image.get_rect()

		self.rect.x, self.rect.y = 512, 0

		if self.color_fondo == MAGENTA: self.superficie.set_colorkey(MAGENTA)



	def get_surface(self, texto):
		self.superficie.fill(self.color_fondo)
		color = BLANCO

		if self.activado: color = self.color_control
			
		sup = pygame.surface.Surface((150, 20), flags=HWSURFACE)

		sup.fill(self.color_fondo_barra)
		borde1 = pygame.draw.rect(sup, NEGRO, (0, 0, 150, 20), 3)

		barra = pygame.surface.Surface((20, 20), flags=HWSURFACE)
		barra.fill(color)
		borde = pygame.draw.rect(barra, NEGRO, (0, 0, 20, 20), 3)		

		sup.blit(barra, (self.pos, 0))

		tipo = self.fuente.render(texto, 1, BLANCO)

		self.superficie.blit(sup, (49, 5))
		self.superficie.blit(tipo, self.pos_texto)

		return self.superficie

	def set_x(self, x):
		self.rect.x = x		

	def get_pos(self, maximo):
		pos = self.pos * 150 / maximo
		return pos

	def set_activado(self, tf=True):
		self.activado = tf		
		self.image = self.get_surface(self.texto)
	
	def update(self):
		self.image = self.get_surface(self.texto)

		if self.moverse_hasta and not self.rect.y >= self.moverse_hasta and not self.hacia == "arriba":
			self.rect.y += 10

		elif self.moverse_hasta and not self.rect.y <= self.moverse_hasta and not self.hacia == "abajo":
			self.rect.y -= 10

		print self.pos
	

		if self.activado:
			teclas = pygame.key.get_pressed()	
	
			if teclas[K_LEFT] and not self.pos <= 0: self.pos -= 3
			elif teclas[K_RIGHT] and not self.pos >= 150: self.pos += 3	
