#!/usr/bin/env python
# coding: utf-8

import pygame
import os
import sys
from pygame.locals import Color

def printText(surface, txtText, Textfont, Textsize, Textx, Texty, Textcolor, option="normal"):
    """Método que imprime textos
    :Param surface: Superfície de exibição
    :Type surface: Superfície Pygame
    :Param txtText: Texto
    :Type txtText: String
    :Param Textfont: Estilo
    :Type Textfont: String
    :Param Textsize: Tamanho
    :Type Textsize: Inteiro
    :Param Textx: Posição eixo X
    :Type Textx: Inteiro
    :Param Texty: Posição eixo y
    :Type Texty: Inteiro
    :Param Textcolor: Cor
    :Type Textcolor: Triple
    :Param option: Opção
    :Type option: String
    """
    myfont = pygame.font.SysFont(Textfont, Textsize)
    label = myfont.render(txtText, 1, Textcolor)
    if option == "normal":
        surface.blit(label, (Textx, Texty))
    else:
        surface.blit(label, ((640 - label.get_width()) / 2, Texty))


def loadSprite(path, alpha = True):
    path = os.path.abspath(path)
    try:
        if (not os.path.isfile(path)):
            raise IOError("Arquivo %s inexistente" %path)
        if (alpha):
            sprite = pygame.image.load(path).convert_alpha()
        else:
            sprite = pygame.image.load(path).convert()
            sprite.set_colorkey(Color("green"))
        return sprite
    except IOError, error:
        print >> sys.stderr, error
        os._exit(1)
