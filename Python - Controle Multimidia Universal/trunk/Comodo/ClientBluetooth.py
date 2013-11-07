# encoding: utf-8
#!/usr/bin/python

import bluetooth
import os
import time
from threading import Thread # @UnusedWildImport

os.system("echo "+str(os.getpid())+">>.tmp")

address_list = ["00:14:35:00:17:DC", "11:11:11:11:11:11"]
target_address = None
sendComanndNow = False
port = 3

def sendComannd(command):
    """Método que faz a modificação do comando
    :Param command: O novo comando
    :Type command: String
    """
    try:
        nearby_devices = bluetooth.discover_devices()
        if (len(nearby_devices) > 0):
            for bdaddr in nearby_devices:
                if bdaddr in address_list:
                    print "ip encontrado"
                    target_address = bdaddr
                    break
            if target_address is not None:
                print "Dispositivo encontrado com o endereço ", target_address

                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM )
  
                sock.connect((target_address, port))
                print("conexao aceita")
                sock.send(command)
                sock.close()
                return True
        else:
            print "Nenhum dispositivo encontrado."
    except Exception as e:
        print "except",e
        return False
    return False

def bluetoothHasConnected():
    """Método que verifica se o bluetooth está conectado na máquina
    :Return: Booleano correspondente a verificação
    :Rtype: Boolean
    """ 
    return os.popen("hcitool dev").read().replace("Devices:\n","").strip() != ""
    
def sendSignalBluetooth(nameRoom):
    """Método que faz o envio do sinal bluetooth
    :Param nameRoom: Nome do cômodo
    :Type nameRoom: String
    """ 
    sendSignal = Thread(target = sendComannd, args = (nameRoom, ))
    sendSignal.start()
