# coding: utf-8
#!/usr/bin/python
import os
import sys

lib_path = os.path.abspath('Util/')


sys.path.append(lib_path)
try:
    import Network as util
except ImportError:
    print("erro ao importar")

from ServerBluetooth import *
import threading

os.system("echo " + str(os.getpid()) + ">>.tmp")


class threadBluetooth(threading.Thread):
    """Classe threadBluetooth é uma classe que vai permitir que operações bloqueantes sejam processadas paralelamente as outras classes

    :version 164
    :author Lucas Salvino
    """
    serverBlue = ServerBluetooth("Controle")
    room = None

    def __init__ (self, ipResidence):
        """Construtor da classe    
        :Param ipResidence: Endereço ip de residência
        :Type ipResidence: String
        """
        threading.Thread.__init__(self)
        self.ipResidence = ipResidence

    def run(self):
        """Método que roda as funções bloqueantes da classe Servidor Bluetooth
        """
        while True:
            self.serverBlue.waitRequisition()
            self.room = self.serverBlue.receiveInformation()
            print("passei")
            params = {"nameRoom": self.room}
            util.httpPostRequest(self.ipResidence, 5432, "setRoomOfControl", params)

    def getRoom(self):
        """Método que acessa o cômodo
        :Return: Cômodo
        :Rtype: String
        """
        return self.room
