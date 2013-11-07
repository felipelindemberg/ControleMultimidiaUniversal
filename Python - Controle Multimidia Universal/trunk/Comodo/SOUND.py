#!/usr/bin/python
# coding: utf-8


try:
    from Equipment import *
    from Channel.ChannelSom import *
    import pygame

    lib_path = os.path.abspath('Comodo/Channel/')
    sys.path.append(lib_path)
    from ChannelSom import *

    lib_path = os.path.abspath('Util/')
    sys.path.append(lib_path)
    try:
        from Pygame import loadSprite
    except ImportError:
        print("erro ao importar")

except ImportError, error:
    lib_path = os.path.abspath('trunk/Comodo/Channel/')
    sys.path.append(lib_path)
    #print >> sys.stderr, "Erro ao importar o modulo 2", error,lib_path
    try:
        from ChannelSom import *
    except ImportError, error:
        print >> sys.stderr, "Erro ao importar o modulo", error
        os._exit(1)


class SOUND(Equipment, pygame.sprite.Sprite):
    """A classe SOUND é uma classe que vai representar um aparelho de Som do mundo real
    
    :version: 224
    :author: Felipe Miranda
    """

    def __init__(self):
        """Construtor da classe
        """
        Equipment.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.sprites = {}
        self.channelSom = ChannelSom()
        
        self.screen = None
        self.rect = None
        self.image = None
        

    def load(self, screen):
        """Método que faz o carregamento das imagens do aparelho Som
        :Param screen: Tela
        :Type screen: Screen Pygame
        """
        self.screen = screen

        self.sprites["som_off"] = loadSprite("Comodo/images/som/off.png", False)
        self.sprites["som_on"] = loadSprite("Comodo/images/som/on.png", False)

        for sprite in self.sprites.values():
            sprite.set_colorkey((0, 255, 0))

    def update(self):
        """Método que faz a atualização da imagem do aparelho Som
        """
        if (self.getState()):
            self.image = self.sprites.get("som_on")
            self.channelSom.setChannel(str(self.getChannel()))
        else:
            self.image = self.sprites.get("som_off")

        self.channelSom.getPlayerAudio().setVolume(self.getVolume())

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(360, 90)
