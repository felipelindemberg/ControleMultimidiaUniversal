#!/usr/bin/python
# coding: utf-8

class Equipment:
    """Classe Aparelho é uma classe para simular um aparelho de multimídia
    
    :version: 224
    :author: Felipe Miranda
    """
    def __init__(self):        
        self.__volume = 0
        self.__currentVolume = 0
        self.__isMute = False
        self.__state = False
        self.__channel = 1

    def turnOn(self):
        """Método que liga o aparelho
        """
        self.__state = True
        if (self.__isMute):
            self.mute()

    def turnOff(self):
        """Método que desliga o aparelho
        """
        self.__state = False
        if (not self.__isMute):
            self.mute()

    def getState(self):
        """Método acessador do estado do aparelho
        """
        return self.__state

    def getIsMute(self):
        """Método que retorna se o equipamento está mudo
        """
        return self.__isMute

    def setVolume(self, volume):
        """Método modificador do volume do aparelho
        :Param volume: Volume desejado
        :Type volume: Inteiro
        """
        if (volume < 0 and volume > 100):
            self.__volume = self.volume
        else:
            self.__volume = volume

    def getVolume(self):
        """Método acessador do volume do aparelho
        :Return: Volume atual do aparelho
        :Rtype: Inteiro
        """
        return self.__volume

    def upVolume(self):
        """Método que aumenta o volume do aparelho
        """
        if (self.__isMute):
            self.__isMute = False
            self.__volume = self.__currentVolume
        elif (self.__volume >= 100):
            self.__volume = 100
        else:
            self.__volume += 1

    def downVolume(self):
        """Método que diminui do volume do aparelho
        """
        if (self.__isMute):
            self.__isMute = False
            self.__volume = self.__currentVolume
        elif (self.__volume <= 0):
            self.__volume = 0
        else:
            self.__volume -= 1

    def mute(self):
        """Método que modifica o volume do aparelho para o modo mudo
        """
        if (self.__isMute):
            self.__isMute = False
            self.__volume = self.__currentVolume
        else:
            self.__isMute = True
            self.__currentVolume = self.__volume
            self.__volume = 0

    def upChannel(self):
        """Método que aumenta o canal
        """
        if (not self.__state):
            self.__state = True
        if (self.__channel < 3):
            self.__channel += 1
        else:
            self.__channel = 1

    def downChannel(self):
        """Método que diminui o canal
        """
        if (not self.__state):
            self.__state = True
        if (self.__channel > 1):
            self.__channel -= 1
        else:
            self.__channel = 3

    def getChannel(self):
        """Método acessador de canal
        :Return: Canal atual
        :Rtype: Inteiro
        """
        return self.__channel

    def setChannel(self, number):
        """Método modificador de canal
        :Param number: Numero do canal
        :Type number: Inteiro
        """
        if(number <= 3 and number >= 1):
            self.__channel = number
