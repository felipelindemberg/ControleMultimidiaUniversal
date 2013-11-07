# coding: utf-8
import pygame
from pygame.locals import *

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

def showInfo(screen, equipment, equipmentName, position):
    """Método que exibe as informações de estado do aparelho
    :Param screen: Tela de apresentação
    :Type screen: Screen Pygame
    :Param equipment: Equipamento
    :Type equipment: Obejto Aparelho
    :Param equipmentName: Nome do equipamento
    :Type equipmentName: String
    :Param position: A posição em que as informações estará
    :Type position: Tuple
    """
    # pygame.draw.rect(screen, (255, 255, 255), Rect((23, 260), (250, 50)))
    pygame.draw.rect(screen, (255, 255, 255), Rect((position[0] - 135, position[1] - 25), (250, 50)))
    printText(screen, equipmentName, "Arial", 40, position[0] - 125, position[1] - 25, (0, 0, 0))
    printText(screen, "Volume: " + str(equipment.getVolume()), "Arial", 20, position[0] - 7, position[1] - 23, (0, 0, 0))
    printText(screen, "Canal: " + (str(equipment.getChannel()) if equipment.getState() else "0"), "Arial", 20, position[0] + 7, position[1], (0, 0, 0))
