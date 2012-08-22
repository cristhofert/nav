#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   nav.py por:
#   Cristofer Travieso(cristhofert97@gmail.com)

import os
import sys
import pygame
import random
import variables
from pygame.locals import *


#---------------------clases de sprites------------------------------

#------------------------------------------------------------------------------
class Bala(pygame.sprite.Sprite):
    def __init__(self, center, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           variables.BALA))
        self.rect = self.image.get_rect()
        self.rect.center = center
        if posicion:
            self.rect.centerx += 40
        else:
            self.rect.centerx -= 40

    def update(self,data=None,grupo=None,balas=None,nivel=0):
        self.rect.centery -= 10
        if self.rect.centery < 0:
            self.kill()


class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           "bala2.png"))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self,data=None,grupo=None,balas=None,nivel=0):
        self.rect.centery += 10
        if self.rect.centery > variables.RESOLUCION[1]:
            self.kill()


#----------------------------------------------
class Buum(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(variables.IMAGENES,
                           "buum.png"))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.cronometro = 5
        #self.sonido = #pygame.mixer.Sound(SONIDO,"BUUM.MP3")
        #serlf.sonodo.play()


    def update(self,data=None,grupo=None,balas=None,nivel=0):
        if self.cronometro == 0:
            data += 1
            self.kill()
        else:
            self.cronometro -= 1


class Buum_fin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           "buum_final.png"))
        self.rect = self.image.get_rect()
        self.rect.move_ip(0,0)
        self.cronometro = 2

    def update(self,data=None,grupo=None,balas=None,nivel=0):
        if self.cronometro == 0:
            sys.exit()
        else:self.cronometro -= 1


#----------
class Continuar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.escala = (110,60)
        self.imagen = pygame.image.load(os.path.join(variables.IMAGENES,\
                        "continuar.png"))
        self.imagen2 = pygame.image.load(os.path.join(variables.IMAGENES,\
                         "continuar2.png"))
        self.image = self.imagen.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (variables.RESOLUCION[0]/2,0)


    def Actualizar(self,puntero,pausa):
        self.Bajar()

        if pygame.sprite.collide_rect(puntero,self):
            self.image = self.imagen2.copy()
            if pygame.mouse.get_pressed()[0]:pausa()
        else:
            self.image = self.imagen.copy()


    def Bajar(self):
        if self.rect.centery < variables.RESOLUCION[1]/2:
            self.rect.centery += 10


    def Subir(self):
        if self.rect.centery > 0:
            self.rect.centery -= 10

    def Reniciate(self):
        self.rect.centery = 0
        self.kill()

class Mi_nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagen1 = pygame.image.load(os.path.join(variables.IMAGENES,\
                         variables.MI_NAVE[0]))
        self.imagen2 = pygame.image.load(os.path.join(variables.IMAGENES,\
                         variables.MI_NAVE[1]))
        self.image = self.imagen1
        self.rect = self.image.get_rect()
        self.rect.center = (variables.RESOLUCION[0]/2,variables.RESOLUCION[1]-150)
        self.cronometro = 6
        self.vidas = 1

    def update(self,data=None,grupo=None,balas=None,nivel=0):
        if self.cronometro == 0:
            self.image = self.imagen1
            self.cronometro = 6
        elif self.cronometro == 3:
            self.image = self.imagen2
            self.cronometro -= 1
        else:self.cronometro -= 1

        self.Controles()


    def Controles(self):
        tecla = pygame.key.get_pressed()
        if tecla[K_LEFT] or tecla[K_a]:
            self.rect.centerx -= 10
        elif tecla[K_RIGHT] or tecla[K_d]:
            self.rect.centerx += 10
        elif tecla[K_UP] or tecla[K_w]:
            self.rect.centery -= 10
        elif tecla[K_DOWN] or tecla[K_s]:
            self.rect.centery += 10

        if self.rect.left <= 0:
            self.rect.centerx += 10
        if self.rect.right >= variables.RESOLUCION[0]:
            self.rect.centerx -= 10
        if self.rect.top <= 0:
            self.rect.centery += 10
        if self.rect.bottom >= variables.RESOLUCION[1]:
            self.rect.centery -= 10


#------------------------------Nave_enemiga------------------------------------------------
class Nave_enemiga(pygame.sprite.Sprite):
    def __init__(self, nivel):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           "nave_enemiga.png"))
        self.rect = self.image.get_rect()
        self.centrox = variables.RESOLUCION[0]/2  #random.randint(100,variables.RESOLUCION[0]-100)
        self.rect.center = (self.centrox,0)
        self.cronometro = 10
        self.cronometro_tiro = 75*nivel
        self.verdadero = True
        self.velocidad_x = 10

    def update(self,data=None,grupo=None,balas=None,nivel=0):
        self.rect.centery += 5
        self.mover(self.centrox, 200)
        self.rect.centerx += self.velocidad_x
        #self.mover_x()
        if self.rect.top > variables.RESOLUCION[1]:
            self.kill()
        elif self.rect.x > variables.RESOLUCION[0]:
            self.kill()
        elif self.rect.left < 0:
            self.kill()

        if self.cronometro_tiro == 0:
            balae = BalaEnemiga(self.rect.center)
            grupo.add(balae)
            balas.add(balae)
            self.cronometro_tiro = 75*nivel
        else:
            self.cronometro_tiro -= 1


    def mover(self,x,ancho):
        self.max = x + ancho
        self.min = x - ancho
        if self.rect.centerx < self.min:
            self.velocidad_x = 10
        elif self.rect.centerx > self.max:
            self.velocidad_x = -10


#-------------------------dialogo_pausa---------------------------------------------

class Pausa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagen = pygame.image.load(os.path.join(variables.IMAGENES,\
                        "pausa.png"))
        self.image = self.imagen.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (variables.RESOLUCION[0]/2,0)


    def Actualizar(self):
        self.Bajar()

    def Bajar(self):
    	if self.rect.centery < variables.RESOLUCION[1]/2-100:
            self.rect.centery += 10

    def Subir(self):
        if self.rect.centery > 0:
            self.rect.centery -= 10

    def Reniciate(self):
        self.rect.centery = 0
        self.kill()


#--------------
class Puntero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           "puntero.png"))
        self.rect = self.image.get_rect()


    def Actualizar(self):
        self.rect.center = pygame.mouse.get_pos()

    def Reniciate(self):
        self.rect.centery = 0
        self.kill()


#-----------------
class Salir(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.escala = (110,60)
        self.imagen = pygame.image.load(os.path.join(variables.IMAGENES,\
                        "salir.png"))
        self.imagen2 = pygame.image.load(os.path.join(variables.IMAGENES,\
                         "salir2.png"))
        self.image = self.imagen.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (variables.RESOLUCION[0]/2,0)


    def Actualizar(self,puntero):
        self.Bajar()

        if pygame.sprite.collide_rect(puntero,self):
            self.image = self.imagen2.copy()
            if pygame.mouse.get_pressed()[0]:sys.exit()
        else:
            self.image = self.imagen.copy()

    def Bajar(self):
        if self.rect.centery < variables.RESOLUCION[1]/2+100:
            self.rect.centery += 10

    def Subir(self):
        if self.rect.centery > 0:
            self.rect.centery -= 10

    def Reniciate(self):
        self.rect.centery = 0
        self.kill()
#-----------------
'''class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(variables.IMAGENES,\
                           "meteorito.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint( 0, 1200)

    def update(self, data, grupo, balas, nivel):
        self.rect.centery += 5
        if self.rect.top > variables.RESOLUCION[1]:
            self.kill()'''
