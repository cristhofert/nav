#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   nav.py por:
#   Cristofer Travieso()

import os
import sys
import time
import random
import pygame
from pygame.locals import *


BASE= os.path.dirname(__file__)
RESOLUCION = (1200, 900)
IMAGENES = os.path.join(BASE, "Imagenes")
MI_NAVE = ("mi_nave.png","mi_nave2.png")
BALA = "bala.png"
SONIDO  = os.path.join(BASE, "Sonido")

