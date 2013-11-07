# encoding: utf-8

import httplib
import urllib
import socket
from twisted.internet.error import ConnectBindError
from httplib import BadStatusLine

from socket import AF_INET, SOCK_STREAM


def httpGetRequest(ip, port, metodo):
    """Método que faz a requisição Http Get
    :Param ip: Endereço ip
    :Type ip: String
    :Param port: Porta
    :Type port: String
    :Param method: Método a ser executado
    :Type method: String
    :Return: Booleano correspondente a requisição
    :Rtype: Boolean
    """
    try:
        conn = httplib.HTTPConnection(ip, port)
        conn.request("GET", "/" + metodo)
        r1 = conn.getresponse()
        return r1.read()
    except Exception:
        return False


def httpPostRequest(ip, port, metodo, params):
    """Método que faz a requisição Http Post
    :Param ip: Endereço ip
    :Type ip: String
    :Param port: Porta
    :Type port: String
    :Param method: Método a ser executado
    :Type method: String
    :Param params: Os parâmetros do método
    :Type params: Dicionário
    :Return: Booleano correspondente a requisição
    :Rtype: Boolean
    """
    try:
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        params = urllib.urlencode(params)
        conn = httplib.HTTPConnection(ip, port)
        conn.request("POST", "/" + metodo, params, headers)
        r1 = conn.getresponse()
        return r1.read()
    except Exception:
        return False


def get_local_ip_address(target):
    """Método acessador do endereço ip local
    :Param target: Máquina alvo
    :Type target: String
    :Return: Endereço ip correspondente a máquina alvo
    :Rtype: String
    """
    ipaddr = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except ConnectBindError:
        print("Not Ip")
    except BadStatusLine:
        print "Sem conexão"
        print "Modo local ativado"
        return "localhost"
    return ipaddr


def __isResidence(addr):
    """Método que vai fazer a verificação se um determinado servidor é ou não o servidor residência
    :Param addr: endereço Ip
    :Type addr: String
    :Return: Booleano correspondente a verificação
    :Rtype: Boolean
    """
    try:
        s = socket.socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.01)
        print addr
        if ((not s.connect_ex((addr, 5432))) and (httpGetRequest(addr, 5432, "index") == "Welcome to Control multimedia Universal!")):
            s.close()
            return True
        else:
            s.close()
            return False
    except BadStatusLine:
        print "Endereco invalido"


def getResidenceIp():
    """Método acessador do endereço Ip de residência
    :Return: Endereço Ip
    :Rtype: String
    """
    addr = ""
    if (__isResidence("127.0.0.1")):
        return "127.0.0.1"
    for ip1 in xrange(3):
        for ip2 in xrange(0, 256):
            addr = "192.168." + str(ip1) + "." + str(ip2)
            if __isResidence(addr):
                return addr
    return "Residence is offline"
