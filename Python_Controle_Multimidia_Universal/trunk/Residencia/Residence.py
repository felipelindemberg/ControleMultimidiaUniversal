# encoding: utf-8

import time
import sys
import os
import json

lib_path = os.path.abspath('Util/')
sys.path.append(lib_path)
try:
    import Network as util
except ImportError, e:
    try:
        import trunk.Util.Network as util
    except ImportError, err:
        print("A residência não importou o modulo",err)

class Residence:
    """A Classe Residencia é uma classe que vai intermediar a comunicação controle e cômodo

    :version 164
    :author Felipe Lindemberg
    """
        
    def __init__(self):
        """Construtor da classe
        """
        self.rooms = {}
        self.roomOfControl = None
        
    def addRoom(self, nameRoom, ip, port):
        """Método que adiciona cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Param ip: Endereço ip do cômodo
        :Type ip: String
        :Param port: Porta para comunicação
        :Type port: String
        :Return: Booleano referente a adição
        :Rtype: Boolean
        """
        canAdd = True
        nameRoom = nameRoom.lower()
        for roomTemp in self.rooms.items():
            nameRoomTemp = roomTemp[0]
            ipRoomTemp = roomTemp[1][0]
            portRoomTemp = roomTemp[1][1]
            if((nameRoom == nameRoomTemp) or
               (ipRoomTemp == ip and portRoomTemp == int(port))):
                canAdd = False

        if(canAdd):
            self.rooms[nameRoom] = (ip, int(port))
            #if(self.roomOfControl == None):
            #    self.roomOfControl = nameRoom
            #    self.notificaComodoControle(self.roomOfControl, "True")
            return True
        else:
            return False
    
    def disconnectControl(self, nameRoom):
        """Método que desconecta o controle do cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        """
        self.roomOfControl = None
        self.notificaComodoControle(nameRoom.lower(), "False")
        
    
    def removeRoom(self, nameRoom):
        """Método que remove cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: Booleano referente a remorção
        :Rtype: Boolean
        """
        nameRoom = nameRoom.lower()
        if(nameRoom in self.rooms.keys()):
            self.rooms.pop(nameRoom)
            return True
        else:
            return False
    
    def setRoomOfControl(self, nameRoom):
        """Método que modifica o cômodo a ser controlado
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: String referente a modificação
        :Rtype: String
        """
        oldRoomOfControl = self.roomOfControl
        nameRoom = nameRoom.lower()
        if((nameRoom != self.roomOfControl) and (nameRoom in self.rooms.keys())):
            self.roomOfControl = nameRoom
            self.notificaComodoControle(self.roomOfControl, "True")

            if(oldRoomOfControl != None):
                self.notificaComodoControle(oldRoomOfControl, "False")
                infoRoom = self.__searchRoom(oldRoomOfControl.lower())
                if(infoRoom != False):
                    ip = infoRoom[0]
                    port = infoRoom[1]

                    print("---------------ip e port", ip, port)
                    method = "getRoomConfiguration"
                    roomConfiguration = util.httpGetRequest(ip, port, method)
                    print("------------------------------ satatsus" ,roomConfiguration)
                    if(roomConfiguration != False): #trocar pára diferente
                        roomConfiguration = json.loads(roomConfiguration)
                        self.powerEquipmentsNewRoom(roomConfiguration, nameRoom)

                        print ("devo ligar todos os equipamentos")
                        print("+++++++++++++++++++++++", type(roomConfiguration), roomConfiguration)
                        params = {"equipment": "all", "command":"poweroff"}
                        method = "controlEquipment"
                        util.httpPostRequest(ip, port, method, params)
                    #print ("desligar os comodos do quarto antigo caso não tenha pessoas", ip, port)
            return "Local alterado"
        return "Comodo nao existe"

    def powerEquipmentsNewRoom(self, roomConfiguration, nameRoom):
        """Método que liga os equipamentos do novo cômodo
        :Param data: Dicionário contendo os aparelhos e os comandos
        :Type data: Dicionário
        :Param nameRoom: Nome do novo cômodo
        :Type nameRoom: String
        """
        infoRoom = self.__searchRoom(nameRoom.lower())
        ip = infoRoom[0]
        port = infoRoom[1]

        params = {"configuration": str(roomConfiguration)}
        method = "setNewConfiguration"
        util.httpPostRequest(ip, port, method, params)

    def getRoomOfControl(self):
        """Método acessador do cômodo que esta sendo controlado
        :Return: Cômodo que esta sendo controlado
        :Rtype: Objeto Cômodo
        """
        return self.roomOfControl

    def __searchRoom(self, nameRoom):
        """Método que procura o cômodo desejado
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: O cômodo procurado 
        :Rtype: Objeto Cômodo
        """
        if(nameRoom in self.rooms.keys()):
            return self.rooms[nameRoom]
        return False

    def notificaComodoControle(self, nameRoom, status):
        """Método que notifica ao cômodo se o controle se encontra ou não dentro dele
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Param status: String do boolean correspondente a sua presença
        :Type status: String
        """
        infoRoom = self.__searchRoom(nameRoom.lower())
        print("Passandoo 1")
        if(infoRoom != False):
            ip = infoRoom[0]
            port = infoRoom[1]
            print("Passandoo 2")

            params = {"isFound" : status}
            method = "controlIsFound"
            
            print("Passandoo 3")
            util.httpPostRequest(ip, port, method, params)

    def powerOffEquipmentsRoom(self):
        """Método que desliga todos os equipamentos do cômodo
        """
        for roomTemp in self.rooms.items():
            print("---------------------------------", roomTemp)
            nameRoomTemp = roomTemp[0]
            ipRoomTemp = roomTemp[1][0]
            portRoomTemp = roomTemp[1][1]
            method = "getNumberOfPeoples"
            result = util.httpGetRequest(ipRoomTemp, portRoomTemp, method)

            if(result == False):
                self.removeRoom(nameRoomTemp)
            elif(result == "0"):
                params = {"equipment": "all", "command": "poweroff"}
                method = "controlEquipment"
                util.httpPostRequest(ipRoomTemp, portRoomTemp, method, params)

        time.sleep(15)
        self.powerOffEquipmentsRoom()

    def sendCommand(self, nameRoom, equipment, command):
        """Método que envia os comandos para o cômodo
        :Param nameRoom: O nome do cômodo
        :Type nameRoom: String
        :Param equipment: O equipamento
        :Type equipment: String
        :Param command: O comando a ser executado
        :Type command: String
        :Return: A requisição Http Post do Cômodo
        :Rtype: Requisição Http Post
        """
        nameRoom = nameRoom.lower()
        infoRoom = self.__searchRoom(nameRoom)
        if(infoRoom != False):
            ip = infoRoom[0]
            port = infoRoom[1]
            params = {"equipment": equipment, "command": command}
            method = "controlEquipment"
            return util.httpPostRequest(ip, port, method, params)
        else:
            return "Comodo nao existe"

    def getRooms(self):
        """Método acessador de cômodos
        :Return: Cômodos mapeados pelos seus nomes
        :Rtype: Dicionário
        """
        return self.rooms
