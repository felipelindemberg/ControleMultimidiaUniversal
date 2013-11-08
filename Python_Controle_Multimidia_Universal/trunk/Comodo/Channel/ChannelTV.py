#!/usr/bin/env python
# coding: utf-8

try:
    import pygame
    from pygame.locals import *
    import sys
    import os
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from io import BytesIO
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)


class ChannelTV():
    """Classe ChannelTV é uma classe para simular/tratar/lidar com canais da TV
    
    :version: 224
    :author: Felipe Miranda
    """

    def __init__(self, channel):
        """Construtor da classe
        """
        try:
            self.channel = channel
            if (not os.path.isfile(os.path.abspath("Comodo/Channel/Files/TV/Videos/channel" + channel + ".mpg"))): 
                raise IOError("Arquivos de video inexistentes")
            self.movie = pygame.movie.Movie(BytesIO(open(os.path.abspath("Comodo/Channel/Files/TV/Videos/channel" + channel + ".mpg"), "rb").read()))
            w, h = self.movie.get_size()
            msize = (w, h)
            self.image_surface = pygame.Surface(msize)
            self.image_surface.fill([0, 0, 0])
            self.movie.set_display(self.image_surface, Rect((5, 5), msize))
            self.movie.set_volume(0)
            self.movie.play()
        except IOError as error:
            print >> sys.stderr, error
            os._exit(1)

    def getChannel(self):
        """Método acessador do canal
        :Return: Canal
        :Rtype: String
        """
        return self.channel

    def getMovie(self):
        """Método acessador do vídeo
        :Return: Vídeo
        :Rtype: Mpg Vídeo
        """
        return self.movie

    def get(self):
        """Método acessador do superfície de vídeo
        :Return: Superfície de vídeo
        :Rtype: Superfície Pygame
        """
        if (not self.movie.get_busy()):
            self.movie.rewind()
            self.movie.play()
        return self.image_surface

    def setVolume(self, value):
        """Método modificador do volume do vídeo
        :Param value: Valor
        :Type value: Inteiro
        """
        self.movie.set_volume(value / 100.)
