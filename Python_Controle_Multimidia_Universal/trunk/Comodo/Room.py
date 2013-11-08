# coding: utf-8

from TV import *  # @UnusedWildImport
from SOUND import *  # @UnusedWildImport

class Room:
    """Classe Room é uma classe que vai simular um cômodo de uma residência

    :version 153
    :author Felipe Lindemberg
    """
    
    def __init__(self, name):
        """Construtor da classe
        :Param name: Nome do cômodo a ser criado
        :Type name: String 
        """
        self.__rooms = {}
        self.__port = None
        self.__name = name
        self.__numberOfPeoples = 0
        self.__equipments = {}
        self.addEquipment("tv", TV())
        self.addEquipment("som", SOUND())
        self.__control = False
    
    def setPort(self, port):
        """Método modificador da porta do cômodo
        :Param port: Porta do cômodo
        :Type port: String
        """
        self.__port = port
    
    def getPort(self):
        """Método acessador da porta do cômodo
        :Return: Porta do cômodo
        :Rtype: String
        """
        return self.__port
    
    def addEquipment(self, nameEquipment, equipment):
        """Método que faz a adição de equipamentos no cômodo
        :Param nameEquipment: Nome do equipamento
        :Type nameEquipment: String
        :Param equipment: Equipamento
        :Type equipment: Objeto Aparelho
        :Return: Booleano correspondente a adição do equipamento
        :Rtype: Boolean
        """
        nameEquipment = nameEquipment.lower()
        if(nameEquipment not in self.__equipments.keys()):
            self.__equipments[nameEquipment] = equipment
            return True
        return False
    
    def getEquipment(self, nameEquipment):
        """Método acessador do equipamento presente no cômodo
        :Param nameEquipment: Nome do equipamento
        :Type nameEquipment: String
        :Return: O equipamento
        :Rtype: Objeto Aparelho
        """
        nameEquipment = nameEquipment.lower()
        if(nameEquipment in self.__equipments.keys()):
            return self.__equipments[nameEquipment]
        return False
    
    def controlIsFound(self, isFound):
        """Método modificador da presença do controle no cômodo
        :Param isFound: Booleano correspondente a presença
        :Type isFound: Boolean
        """
        self.__control = isFound
        numTemp = self.getNumberOfPeoples()
        if(isFound):
            self.setNumberOfPeoples(numTemp + 1)
        else:
            self.setNumberOfPeoples(numTemp - 1)
    
    def getControlIsFound(self):
        """Método acessador da presença do controle no cômodo
        :Return: Booleano correspondente a presença
        :Rtype: Boolean
        """
        return self.__control
    
    def getEquipments(self):
        """Método acessador dos equipamentos presentes no cômodo
        :Return: Equipamentos do cômodo
        :Rtype: Lista
        """
        return self.__equipments.keys()
    
    def getName(self):
        """Método acessador do nome do cômodo
        :Return: O nome do cômodo
        :Rtype: String
        """
        return self.__name

    def getSound(self):
        """Método acessador de Som
        :Return: O equipamento Som
        :Rtype: Objeto Som
        """
        return self.getEquipment("Som")
        #return self.som
    
    def getTv(self):
        """Método acessador de TV
        :Return: O equipamento TV
        :Rtype: Objeto TV
        """
        return self.getEquipment("TV")
    
    def getNumberOfPeoples(self):
        """Método acessador do número de pessoas presentes no cômodo
        :Return: Número de pessoas presentes no cômodo
        :TypeReturn: Inteiro
        """
        return self.__numberOfPeoples
    
    def setNumberOfPeoples(self, number):
        """Método modificador do número de pessoas presentes no cômodo
        :Param number: Número de pessoas
        :Type number: Inteiro
        :Return: Booleano referente a modificação
        :Rtype: Boolean
        """
        number = int(number)
        if (((number >= 0 and not self.__control ) or (number >= 1 and self.__control)) and number < 10):
            self.__numberOfPeoples = number
            return True
        elif (number >= 10):
            self.__numberOfPeoples = 9
            return False
        elif (number < 0 and self.__control):
            self.__numberOfPeoples = 0
            return False
        return False

    def getCommands(self):
        """Método acessador dos comandos enviados aos aparelhos
        :Return: Comandos
        :Rtype: Lista
        """
        return self.__rooms.keys()

    def powerOffEquipments(self):
        """Método que faz o desligamento dos aparelhos do cômodo
        """
        self.getTv().turnOff()
        self.getSound().turnOff()
