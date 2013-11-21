# encoding: utf-8
try:
    import os
    import sys
    import json
    import cherrypy
    import threading as t  # @UnusedWildImport
    from Residence import *  # @UnusedWildImport
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)

os.system("echo "+str(os.getpid())+">>.tmp")

class ServerPrincipal:
    """A Classe ServerPrincipal é uma classe que vai fazer o papel de servidor de Residência

    :version 157
    :author Felipe Lindemberg
    """
    
    def __init__(self, residence):
        """Construtor da classe
        :Param residence: Residência
        :Type residence: Objeto Residencia
        """
        self.residence = residence
    
    def index(self):
        """Método que exibe as boas vindas
        :Return: A mensagem de boas vindas
        :Rtype: String
        """
        return "Welcome to Control multimedia Universal!"
    index.exposed = True
    
    
    def default(self):  # isso eh tipo uma excecao
        return "Invalid Data"
    default.exposed = True  # deixa o metodo visivel no server
    
    @cherrypy.tools.allow(methods=['POST'])
    def addRoom(self, nameRoom, ip, port):
        """Método que adiciona o cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Param ip: Endereço ip
        :Type ip: String
        :Param port: Porta para comunicação
        :Type port: String
        :Return: Mensagem string indicando a adição do cômodo
        :Rtype: String
        """
        if(self.residence.addRoom(nameRoom, ip, port)):
            return "Comodo adicionado"
        else:
            return "Comodo já existe"
    addRoom.exposed = True
        
    @cherrypy.tools.allow(methods=['POST'])
    def disconnectControl(self, nameRoom):
        """Método que desconecta o controle do cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: Mensagem string indicando a desconexão
        :Rtype: String
        """
        self.residence.disconnectControl(nameRoom)
        return "OK"
    disconnectControl.exposed = True    
        
    @cherrypy.tools.allow(methods=['POST'])
    def removeRoom(self, nameRoom):
        """Método que remove o cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: Mensagem string indicando a remorção do cômodo
        :Rtype: String
        """  
        if (self.residence.removeRoom(nameRoom)):
            return "Comodo removido"
        else:
            return "Comodo nao existe"
    removeRoom.exposed = True
    
    @cherrypy.tools.allow(methods=['POST'])
    def sendCommand(self, nameRoom, equipment, command):
        """Método que envia o comando para o cômodo
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Param equipment: Equipamento
        :Type equipment: String
        :Param command: Comando
        :Type command: String
        :Return: A requisição Http Post do Comodo
        :Rtype: Requisição Http Post
        """
        return self.residence.sendCommand(nameRoom, equipment, command)
    sendCommand.exposed = True
    
    @cherrypy.tools.allow(methods=['POST'])
    def setRoomOfControl(self, nameRoom):
        """Método modificador do cômodo a ser controlado
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: String referente a modicação do cômodo a ser controlado
        :Rtype: String
        """
        return self.residence.setRoomOfControl(nameRoom)
    setRoomOfControl.exposed = True
    
    def getRoomOfControl(self):
        """Método acessador do cômodo que esta sendo controlado
        :Return: O cômodo que esta sendo controlado
        :Rtype: Objeto Comodo
        """
        return self.residence.getRoomOfControl()
    getRoomOfControl.exposed = True
    
    
    @cherrypy.tools.allow(methods=['POST'])
    def sleep(self, nameRoom, time):
        """Método modificador do cômodo a ser controlado
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: String referente a modicação do cômodo a ser controlado
        :Rtype: String
        """
        return self.residence.sleep(nameRoom, time)
    sleep.exposed = True
    
    @cherrypy.tools.allow(methods=['POST'])
    def cancelSleep(self, nameRoom):
        """Método modificador do cômodo a ser controlado
        :Param nameRoom: Nome do cômodo
        :Type nameRoom: String
        :Return: String referente a modicação do cômodo a ser controlado
        :Rtype: String
        """
        return self.residence.cancelSleep(nameRoom)
    cancelSleep.exposed = True
    
    def getRooms(self):
        """Método acessador de cômodos
        :Return: Os cômodos adicionados
        :Rtype: Json
        """
        retorno = json.dumps(self.residence.getRooms())
        return retorno
    getRooms.exposed = True

residenceClass = Residence()

class MyThread(t.Thread):
    """Classe My Thread é uma classe que extende a classe Thread e vai fazer a execução de trechos de códigos bloqueantes

    :version 157
    :author Felipe Lindemberg
    """
    
    def run(self):
        """Construtor da classe
        """
        residenceClass.powerOffEquipmentsRoom()
                
mt = MyThread()
mt.start()

cherrypy.config.update(os.path.abspath("Residencia/config.cfg"))
cherrypy.quickstart(ServerPrincipal(residenceClass))
