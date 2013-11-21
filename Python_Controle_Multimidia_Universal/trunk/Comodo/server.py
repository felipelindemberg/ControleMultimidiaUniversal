# coding: utf-8

import os
import sys
import cherrypy
import json

lib_path = os.path.abspath('Util/')
sys.path.append(lib_path)
try:
    import Network as util
except ImportError:
    print("erro ao importar")

class ServerRoom:
    """Classe ServerRoom é uma classe para fazer a comunicação Comodo/Residencia 

    :version 165
    :author Felipe Medeiros
    """
    connected = False
    
    def __init__(self, room):
        """Construtor da classe
        :Param room: Cômodo
        :Type room: Objeto Comodo
        """
        self.room = room
        self.ipResidence = None

    def getConnected(self):
        """Método acessador da conexão
        :Return: Booleano correspondente ao status da conexão
        :Rtype: Boolean
        """
        return self.connected
    
    @cherrypy.tools.allow(methods=['POST'])
    def controlIsFound(self, isFound):
        """Método modificador da presença do controle no cômodo
        :Param isFound: String do boolean correspondente a presença
        :Type isFound: String
        :Return: Mensagem de status da modificação
        :Rtype: String
        """
        print("------------------- passando")
        self.room.controlIsFound(eval(isFound))
        return "OK"
    controlIsFound.exposed = True
    
    def Connect(self):
        """Método que faz a conexão com Residência
        """
        myIp = util.get_local_ip_address("1.1.1.1")
        print "mayyyyyyyyyyyyyyyyyyyyyyy0",util.get_local_ip_address("1.1.1.1")
        while True:
            port = self.room.getPort()
            if(port != None):
                print ("----------------------------My IP", myIp)
                params = {"nameRoom": self.room.getName(), "ip": myIp, "port": port}
                self.ipResidence = util.getResidenceIp()
                if (self.ipResidence == "Residence is offline"):
                    print "Residence is offline"
                    os._exit(1)
                print "sdssssssssssssss----------_",myIp,params,self.ipResidence
                sucessToCreatComod = util.httpPostRequest(self.ipResidence, 5432, "addRoom", params)
                if(sucessToCreatComod == False):
                    print "Problemas na conexao, tente novamente!"
                    os._exit(1)
                elif (sucessToCreatComod == "Comodo já existe"):
                    print "Nome de room existente, altere-o"
                    os._exit(1)
                break
        self.connected = True 

    def index(self):
        """Método que exibe o nome do cômodo
        :Return: Identificação do cômodo
        :Rtype: String
        """
        return "Cômodo -", self.room.getName()
    index.exposed = True

    @cherrypy.tools.allow(methods=['POST'])
    def controlEquipment(self, equipment, command):
        """Método que controla o equipamento
        :Param equipment: Equipamento
        :Type equipment: String
        :Param command: O comando
        :Type command: String
        :Return: Mensagem referente a execução do comando
        """
        command = command.upper()
        equipment = equipment.upper()
        if ((equipment == "TV") or (equipment == "SOM")):
            equipment = (self.room.getTv() if equipment == "TV" else self.room.getSound()) 
            if (command == "POWER"):
                if (equipment.getState()):
                    equipment.turnOff()
                else:
                    equipment.turnOn()

            if (command == "UPCHANNEL"):
                equipment.upChannel()
            elif (command == "DOWNCHANNEL"):
                equipment.downChannel()
            if (equipment.getState()):
                if (command == "UPVOLUME"):
                    equipment.upVolume()
                elif (command == "DOWNVOLUME"):
                    equipment.downVolume()
                elif (command == "MUTE"):
                    equipment.mute()
            else:
                return ("Aparelho não esta ligado")
        elif (equipment == "ALL"):
            if (command == "POWEROFF"):
                self.room.powerOffEquipments()
            elif (command == "MUTE"):
                self.room.getTv().mute()
                self.room.getSound().mute()

        return "ok"
    controlEquipment.exposed = True

    @cherrypy.tools.allow(methods=['POST'])
    def setNewConfiguration(self, configuration):
        """Método modificador da configuração do aparelho
        :Param configuration: Nova configuração
        :Type configuration: String
        """
        configuration = eval(configuration)
        tvConfiguration = configuration.get("tv")
        soundConfiguration = configuration.get("sound")

        if (tvConfiguration.get("status")):
            self.room.getTv().turnOn()
        else:
            self.room.getTv().turnOff()

        if (soundConfiguration.get("status")):
            self.room.getSound().turnOn()
        else:
            self.room.getSound().turnOff()

        self.room.getTv().setVolume(tvConfiguration.get("volume"))
        self.room.getTv().setChannel(tvConfiguration.get("channel"))

        
        self.room.getSound().setVolume(soundConfiguration.get("volume"))
        self.room.getSound().setChannel(soundConfiguration.get("channel"))


    setNewConfiguration.exposed = True

    @cherrypy.tools.allow(methods=['POST'])
    def setNumberOfPeoples(self, number):
        """Método modificador do número de pessoas presentes no cômodo
        :Param number: Número de pessoas
        :Type number: Inteiro
        :Return: Mensagem de modificação
        :Rtype: String
        """
        self.room.setNumberOfPeoples(number)
        return "Add"
    setNumberOfPeoples.exposed = True
    
    @cherrypy.tools.allow(methods=['POST'])
    def sleep(self, time):
        """Método modificador do número de pessoas presentes no cômodo
        :Param number: Número de pessoas
        :Type number: Inteiro
        :Return: Mensagem de modificação
        :Rtype: String
        """
        self.room.sleep(int(time))
        return "Add"
    sleep.exposed = True
    
    @cherrypy.tools.allow(methods=['POST'])
    def cancelSleep(self):
        """Método modificador do número de pessoas presentes no cômodo
        :Param number: Número de pessoas
        :Type number: Inteiro
        :Return: Mensagem de modificação
        :Rtype: String
        """
        self.room.cancelSleep()
        return "cancel"
    cancelSleep.exposed = True
    
    def getNumberOfPeoples(self):
        """Método acessador do número de pessoas presentes no cômodo
        :Return: Numero de pessoas
        :Rtype: String
        """
        return str(self.room.getNumberOfPeoples())
    getNumberOfPeoples.exposed = True
    
    def exit(self):
        """Método que encerra a conexão com Residência
        """
        params = {"nameRoom": self.room.getName()}
        try:
            print util.httpPostRequest(self.ipResidence, 5432, "removeRoom", params)
        except AttributeError:
            print "Parametros insuficientes"
        cherrypy.engine.exit()
        os._exit(0)
    exit.exposed = True
    
    def getRoomConfiguration(self):
        """Método acessador dos comandos enviados aos aparelhos
        :Return: Comandos enviados
        :Rtype: Json
        """
        dados = {"tv": {"status":self.room.getTv().getState(), "channel": self.room.getTv().getChannel(), "volume" : self.room.getTv().getVolume() }, "sound":{"status":self.room.getSound().getState(), "channel": self.room.getSound().getChannel(), "volume" : self.room.getSound().getVolume() }}
        retorno = json.dumps(dados)
        return retorno
    getRoomConfiguration.exposed = True

    def default(self):  # isso eh tipo uma excecao
        return "Dados Incorretos"
    default.exposed = True  # deixa o metodo visivel no server
