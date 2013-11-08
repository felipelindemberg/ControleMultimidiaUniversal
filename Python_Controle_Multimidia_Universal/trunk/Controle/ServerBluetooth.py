# coding: utf-8
#!/usr/bin/python

import bluetooth


class ServerBluetooth:
    """Classe ServerBluetooth é uma classe que será utilizada pelo controle para que o mesmo possa ser capaz de receber sinais bluetooth
    """
    name = None
    uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"
    server_sock = None
    client_sock = None
    client_info = None

    def __init__(self, nameOfServer):
        """Construtor da classe
        :Param nameOfServer: Nome do servidor
        :Type nameOfServer: String
        """
        self.name = nameOfServer

    def waitRequisition(self):
        """Método que aguarda a requisição do cliente bluetooth
        """
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", 3))

        self.server_sock.listen(1)
        bluetooth.advertise_service(self.server_sock, self.name, self.uuid)

        print ("Waiting for connection on RFCOMM")
        self.client_sock, self.client_info = self.server_sock.accept()
        print (self.client_info, ": connection accepted")

    def receiveInformation(self):
        """Método que recebe a informação do cliente
        :Return: Informação requisitada pelo cliente
        :RType: String
        """
        try:
            information = self.client_sock.recv(1024)

            print(information)
            return information
        except IOError:
            pass
        self.client_sock.close()

    def getClientSocket(self):
        """Método que acessa o socket do cliente
        :Return: Socket do cliente
        :Rtype: Python Socket
        """
        return self.client_sock

    def getClientInfo(self):
        """Método que acessa a informação do cliente
        :Return: A informação do cliente
        :Rtype: Python Endereço
        """
        return self.client_info
        # print (self.client_info, ": disconnected")
