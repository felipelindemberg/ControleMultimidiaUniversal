#!/usr/bin/env python
# coding: utf-8

try:
    import sys
    import os
    import random
    import threading as t  # @UnusedWildImport
    import cherrypy  # @UnusedWildImport
    from Room import *  # @UnusedWildImport
    from RoomUI import *  # @UnusedWildImport
    from server import *  # @UnusedWildImport
except ImportError as error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)


class CherrypyConfig(t.Thread):
    """A classe CherrypyConfig é uma classe que foi delegada para sortear uma porta automática para o servidor de cômodo
    
    :version 224
    :author Felipe Miranda
    """

    def run(self):
        """Método que faz o sorteio da porta do servidor de cômodo
        """
        port = random.randint(3000, 8099)
        try:
            print "procurando",port
            room.setPort(port)
            print "porta encontradaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            cherrypy.config.update(os.path.abspath("Comodo/config.cfg"))
            cherrypy.config.update({'server.socket_port': port})
            cherrypy.quickstart(server)
        except:
            self.run()


class Server(t.Thread):
    """A classe Server é uma classe que vai fazer a conexão de cômodo com residência
    
    :version 224
    :author Felipe Miranda
    """

    def run(self):
        """Método que faz a conexão do servidor de cômodo com servidor de residência
        """
        print ("Conectando com o servidor")
        server.Connect()


def main(nameOfRoom):
    """Método que faz a criação automática de todos os componentes de cômodo
    :Param nameOfRoom: Nome do cômodo
    :Type nameOfRoom: String
    """

    global room
    room = Room(nameOfRoom)

    global server
    server = ServerRoom(room)

    roomUI = RoomUI(server, room)
    thServer = Server()
    thServer.start()

    mt = CherrypyConfig()
    mt.start()

    roomUI.run()

if __name__ == '__main__':
    if (sys.version_info < (2, 7)):
        print >> sys.stderr, "Versão de python não suportada, requer a 2.7"
        os._exit(1)
    if (sys.platform != "linux2"):
        print >> sys.stderr, "SO não suportado"
        os._exit(1)
    if (len(sys.argv) != 2):
        print >> sys.stderr, "Nome do cômodo inválido"
        os._exit(1)
    main(sys.argv[1])
