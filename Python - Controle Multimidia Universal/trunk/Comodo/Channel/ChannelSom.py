#!/usr/bin/env python
# coding: utf-8

try:
    import sys
    import os
    from Players.Audio import *  # @UnusedWildImport
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)


class ChannelSom:
    """Classe ChannelSom é uma classe para simular/tratar/lidar com canais de Som
    
    :version: 224
    :author: Felipe Miranda
    """

    def __init__(self):
        """Construtor da classe
        """
        self.channels = {}
        self._loadChannels()
        self.playerAudio = Audio(os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel1.mp3"), 0)

    def _loadChannels(self):
        """Método que faz o mapeamento canal/caminho do arquivo de Som
        """
        try:
            if (not os.path.isfile(os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel1.mp3")) or 
                not os.path.isfile(os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel2.mp3")) or
                not os.path.isfile(os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel3.mp3"))) : 
                raise IOError("Arquivos de audio inexistentes")

            self.channels["1"] = os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel1.mp3")
            self.channels["2"] = os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel2.mp3")
            self.channels["3"] = os.path.abspath("Comodo/Channel/Files/SOM/Audios/channel3.mp3")
        except IOError:
            
            try:
                if (not os.path.isfile(os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel1.mp3")) or 
                    not os.path.isfile(os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel2.mp3")) or
                    not os.path.isfile(os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel3.mp3"))) : 
                    raise IOError("Arquivos de audio inexistentes")
    
                self.channels["1"] = os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel1.mp3")
                self.channels["2"] = os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel2.mp3")
                self.channels["3"] = os.path.abspath("trunk/Comodo/Channel/Files/SOM/Audios/channel3.mp3")
            except IOError:
                print >> sys.stderr, error
                os._exit(1)

    def setChannel(self, channel):
        """Método modificador de canal do Som
        :Param channel: Canal do Som
        :Type channel: String
        """
        self.playerAudio.audio(self.channels.get(channel))

    def getPlayerAudio(self):
        """Método acessador de player de audio
        :Return: Reprodutor de audio
        :Rtype: Objeto Audio
        """
        return self.playerAudio
