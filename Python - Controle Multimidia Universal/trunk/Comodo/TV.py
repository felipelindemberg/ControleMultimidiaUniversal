#!/usr/bin/python
# coding: utf-8

from Equipment import *
import pygame
from Channel.ChannelTV import *
from pygame.locals import *

lib_path = os.path.abspath('Util/')
sys.path.append(lib_path)
try:
    from Pygame import *
except ImportError:
    print("erro ao importar")


class TV(Equipment, pygame.sprite.Sprite):
    """A classe TV é uma classe que vai representar um aparelho de TV do mundo real
    :version: 224
    :author: Felipe Miranda
    """

    def __init__(self):
        """Construtor da classe
        """
        Equipment.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.sprites = {}
        self.channelList = {}
        self.currentVolume = 0

    def load(self, screen):
        """Método que faz o carregamento das imagens do aparelho TV
        :Param screen: Tela
        :Type screen: Screen Pygame
        """
        self.screen = screen

        # self.movie = ChannelTV(str(self.getChannel()))
        
        self.channelList = {"1":ChannelTV("1"), "2":ChannelTV("2"), "3":ChannelTV("3")}
        self.currentChannelPlay = self.channelList.get("1")

        self.sprites["tv_off"] = loadSprite("Comodo/images/tv/off.png", False)
        self.sprites["tv_on"] = loadSprite("Comodo/images/tv/on.png", False)

        

    def update(self):
        """Método que faz a atualização da imagem do aparelho TV
        """
        if (self.getState()):
            self.image = self.sprites.get("tv_on")
            self.image.blit(self.currentChannelPlay.get(), (12, 18))
            self.__drawTvDisplay()

            if (self.currentVolume != self.getVolume()):
                self.currentChannelPlay.setVolume(self.getVolume())
                self.currentVolume = self.getVolume()
            
            if  (self.currentChannelPlay.getChannel() != str(self.getChannel())):
                self.currentChannelPlay = (self.channelList.get(str(self.getChannel())))
        else:
            self.image = self.sprites.get("tv_off")
            if (not self.getIsMute()):
                self.mute()

        # Adiciona mais um canal
        
        
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(20, 80)
        
         #Se o canal nao estiver ativo ele sera pausado

    def __drawTvDisplay(self):
        """Método que desenha o display que contém as informações da TV
        """
        pygame.draw.rect(self.image, (255, 255, 255), Rect((183, 32), (50, 20)))
        printText(self.image, "CH " + str(self.getChannel()), "Arial", 15, 188, 33, (0, 50, 255))
        pygame.draw.rect(self.image, (140, 220, 130), Rect((38, 130), (self.getVolume() * 1.8, 10)))
        printText(self.image, "+", "Arial", 20, 223, 123, (140, 220, 130))
        printText(self.image, "-", "Arial", 20, 23, 120, (140, 220, 130))
