#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   nav.py por:
#   Cristofer Travieso

import os
import sys
import time
import random
import pygame
from pygame.locals import *

import variables
import sprites_file

os.system("clear")


#tarea proxima:balas enemigas funcionen
#self.NIVELes
#ect

class Nav():
    def __init__(self):
        self.ventana= None
        self.fondo= None
        self.reloj = None
        self.estado= None
        self.personaje= None
        self.sprites= None
        self.balas = None
        self.n = 0
        self.cronometro = 0
        self.bala1 = []
        self.bala2 = []
        self.mi_nave = None
        self.mis_naves = None
        self.cantidad_buum = 0
        self.pausa = False
        self.grupo_pausa = None
        self.naves_muertas = 0
        self.fuente = None
        self.NIVEL = 1
        self.limite = 25

        self.precargar()
        self.cargar()
        self.ejecutar()


    def precargar(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode(variables.RESOLUCION , pygame.FULLSCREEN, 0)


    def cargar(self):
        self.ventana = pygame.display.get_surface()
        self.fondo = pygame.transform.scale(pygame.image.load(os.path.join(variables.IMAGENES, "fondo.png")),variables.RESOLUCION)
        self.reloj = pygame.time.Clock()
        self.mis_naves = pygame.sprite.Group()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.mi_nave = sprites_file.Mi_nave()
        self.sprites.add(self.mi_nave)
        self.mis_naves.add(self.mi_nave)
        self.naves_enemigas = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.balas_enemigas = pygame.sprite.Group()
        self.fuente = pygame.font.Font(None,48)
        #self.lluvia = 100
        #self.meteoritos = pygame.sprite.Group()


        #pygame.mixer.music.load(os.path.join(SONIDO, "Zeropage-Trance_Etude_2.mp3")) MP3 no sopórtado por pygame
        #pygame.mixer.music.play(-1,0)

        self.dialogo_Continuar = sprites_file.Continuar()
        self.dialogo_salir = sprites_file.Salir()
        self.dialogo_pausa = sprites_file.Pausa()
        self.dialogo_puntero = sprites_file.Puntero()

        pygame.mouse.set_visible(False)

        self.estado = True
        self.cronometro = 5*self.NIVEL


    def ejecutar(self):
        self.ventana.blit(self.fondo, (0,0))
        pygame.display.update()
        while self.estado:
            self.reloj.tick(35)
            self.sprites.clear(self.ventana, self.fondo)

            if not self.pausa:
                self.sprites.update(self.cantidad_buum,self.sprites,self.balas_enemigas,self.NIVEL)
            else:
                self.dialogo_puntero.Actualizar()
                self.dialogo_Continuar.Actualizar(self.dialogo_puntero,self.Pausa)
                self.dialogo_salir.Actualizar(self.dialogo_puntero)
                self.dialogo_pausa.Actualizar()

            self.handle_event()
            pygame.event.clear()
            self.sprites.draw(self.ventana)
            pygame.display.update()

            if not self.pausa:
                self.Genera_enemigos()

                self.coliciones_mi_nave()
                self.coliciones_bala()
                self.coliciones_bala_enemigas_meteorito()

            if self.naves_muertas > self.limite:

                self.NIVEL += 1
                self.limite = self.limite * 2
                texto = self.fuente.render("Nivel  "+str(self.NIVEL),0,(255,230,245))
                self.ventana.blit(texto,(variables.RESOLUCION[0]/2,variables.RESOLUCION[1]/2))

            #self.Lluvia()

            pygame.display.update()


    def Mostrar_Esconder(self):
        objetos=[self.dialogo_Continuar,self.dialogo_salir,self.dialogo_pausa,self.dialogo_puntero]
        for objeto in objetos:
            if objeto in self.sprites.sprites():
                objeto.Reniciate()
            else:self.sprites.add(objeto)
        '''if self.dialogo_pausa == None:
            self.dialogo_Continuar = sprites_file.Continuar()
            self.dialogo_salir = sprites_file.Salir()
            self.dialogo_pausa = sprites_file.Pausa()
            self.dialogo_puntero = sprites_file.Puntero()
        else:
            self.dialogo_Continuar = None
            self.dialogo_salir = None
            self.dialogo_pausa = None
            self.dialogo_puntero = None'''


    def coliciones_mi_nave(self):
            #colicion entre mi nave y enemigaspñ
            colicionados1 = pygame.sprite.groupcollide(self.mis_naves,self.naves_enemigas,False,False)
            try:
                for enemiga in colicionados1[self.mi_nave]:
                    self.fin()
            except:pass


    def coliciones_bala(self):
        #colicion entre balas y enemigas
        colicionados2 = pygame.sprite.groupcollide(self.balas,self.naves_enemigas,False,False)
        for bala in colicionados2.keys():
            for obstaculo in colicionados2[bala]:
                self.sprites.add(sprites_file.Buum(obstaculo.rect.center))
                obstaculo.kill()
                bala.kill()
                self.naves_muertas += 1


    def coliciones_bala_enemigas_meteorito(self):
        if pygame.sprite.spritecollideany(self.mi_nave,self.balas_enemigas):
            self.fin()
        #if pygame.sprite.spritecollideany(self.mi_nave,self.meteoritos):
        #    self.fin()



    def Genera_enemigos(self):
        if self.cronometro == 0:
            self.enemiga = sprites_file.Nave_enemiga(self.NIVEL)
            self.naves_enemigas.add(self.enemiga)
            self.sprites.add(self.enemiga)
            self.cronometro = 25*self.NIVEL
        else:self.cronometro -= 1


    def handle_event(self):
        for event in pygame.event.get(pygame.KEYDOWN):
            tecla= event.key
            if not self.pausa:
                if tecla == pygame.K_SPACE:
                    self.bala1.append(sprites_file.Bala(self.mi_nave.rect.center,True))
                    self.sprites.add(self.bala1[-1])
                    self.balas.add(self.bala1[-1])

                    self.bala2.append(sprites_file.Bala(self.mi_nave.rect.center,False))
                    self.sprites.add(self.bala2[-1])
                    self.balas.add(self.bala2[-1])

            if tecla == pygame.K_ESCAPE:
                self.Pausa()
            elif tecla == pygame.K_r:
                Galaxian()


    def Pausa(self):
        print "pause"

        self.Mostrar_Esconder()
        if self.pausa:self.pausa = False
        else:self.pausa = True

    def fin(self):
        print"fin"
        buum_fin = sprites_file.Buum_fin()
        self.sprites.add(buum_fin)


    def salir():
        print "Saliendo..."
        self.estado = False
        sys.exit()


    #def Lluvia(self):
    #    if self.lluvia == 0:
    #        a = sprites_file.Meteorito()
    #        self.sprites.add(a)
    #        self.meteoritos.add(a)
    #        self.lluvia = random.randint( 100, 130)
    #    else:self.lluvia -= 1

#pygame.mouse.get_pressed(): retorna (button1,button2,button3)
#pygame.mouse.get_pressed()[0]:retorna bool por click izquierdo
#

if __name__=="__main__":
    Nav()
