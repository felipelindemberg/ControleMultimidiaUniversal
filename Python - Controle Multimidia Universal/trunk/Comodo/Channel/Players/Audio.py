#!/usr/bin/env python
# coding: utf-8

try:
    import sys
    import os
    import pygame
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)


class Audio:
    """Classe Audio é uma classe para manipular arquivos de Audio
    
    :version: 224
    :author: Felipe Miranda
    """

    def __init__(self, path, volume):
        """Construtor da classe
        :Param path: Caminho do arquivo
        :Type path: String
        :Param volume: Volume inicial
        :Type volume: Inteiro
        """
        self.volumeAtual = (volume / 100.)
        self.pathAtual = path
        pygame.mixer.init()
        pygame.mixer.get_init()
        pygame.mixer.get_num_channels()

    def audio(self, path):
        """Método que reproduz o áudio
        :Param path: Caminho do arquivo
        :Type path: String
        """
        if (self.pathAtual != path):
            if (pygame.mixer.music.get_busy()):
                pygame.mixer.music.stop()

            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volumeAtual)
            pygame.mixer.music.play()
            self.pathAtual = path

        else:
            if (not pygame.mixer.music.get_busy()):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.volumeAtual)
                pygame.mixer.music.play()

    def setVolume(self, volume):
        """Método modificador do player do audio
        :Param volume: Volume
        :Type volume: Inteiro
        """
        self.volumeAtual = (volume / 100.)
        pygame.mixer.music.set_volume(self.volumeAtual)
