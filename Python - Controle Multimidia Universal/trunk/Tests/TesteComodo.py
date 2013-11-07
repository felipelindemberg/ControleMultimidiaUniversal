'''
Created on 07/10/2013

@author: felipelindemberg
'''

import unittest
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
try:
    from Comodo.Room import *  # @UnusedWildImport
except ImportError:
    from trunk.Comodo.Room import *  # @UnusedWildImport


class TesteComodo(unittest.TestCase):
    def setUp(self):
        self.room = Room("Sala")
        self.room2 = Room("Quarto")

    def tearDown(self):
        self.room = None
        self.room2 = None

    def testInitRoom(self):
        self.assertEqual(self.room.getName(), "Sala", "O nome deve ser Sala")
        self.assertEqual(len(self.room.getEquipments()), 2, "O numero inicial de equipamentos deve ser 2")
        self.assertEqual(sorted(self.room.getEquipments()), sorted(["tv", "som"]), "O room deve iniciar com tv e som")

        self.assertEqual(self.room2.getName(), "Quarto", "O nome deve ser Quarto")
        self.assertEqual(len(self.room2.getEquipments()), 2, "O numero inicial de equipamentos deve ser 2")
        self.assertEqual(sorted(self.room2.getEquipments()), sorted(["tv", "som"]), "O room deve iniciar com tv e som")

    def testAddEquipment(self):
        self.assertEqual(len(self.room.getEquipments()), 2, "O numero inicial de equipamentos deve ser 2")
        self.assertEqual(sorted(self.room.getEquipments()), sorted(["tv", "som"]), "O room deve iniciar com tv e som")

        self.assertTrue(self.room.addEquipment("dvd", None), "Deve retornar True pois dvd nao existe no room")
        self.assertEqual(len(self.room.getEquipments()), 3, "O numero de equipamentos deve ser 3")
        self.assertEqual(sorted(self.room.getEquipments()), sorted(["tv", "som", "dvd"]), "O room deve possui dvd, tv e som")

        self.assertFalse(self.room.addEquipment("dvd", None), "Deve retornar False pois dvd ja existe no room")
        self.assertEqual(len(self.room.getEquipments()), 3, "O numero de equipamentos deve ser 3 pois nao mudou apos tentar add o DVD")
        self.assertEqual(sorted(self.room.getEquipments()), sorted(["tv", "som", "dvd"]), "O room deve possui apenas dvd, tv e som")

    def testNumberPeople(self):
        self.assertEqual(self.room.getNumberOfPeoples(), 0, "O numero inicial de pessoas num room deve ser 0")
        self.assertTrue(self.room.setNumberOfPeoples(0), "O numero de pessoas deve ser maior que 0 e menor que 10")

        self.assertFalse(self.room.setNumberOfPeoples(12), "O numero de pessoas deve ser maior que 0 e menor que 10")
        self.assertEqual(self.room.getNumberOfPeoples(), 9, "O numero de pessoas continua 0, nao foi alterado")

        self.assertTrue(self.room.setNumberOfPeoples(4), "O numero de pessoas e valido")
        self.assertEqual(self.room.getNumberOfPeoples(), 4, "O numero de pessoas foi alterado para 4")
