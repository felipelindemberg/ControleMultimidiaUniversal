import unittest
import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
try:
    from Residencia.Residence import *  # @UnusedWildImport
except ImportError:
    from trunk.Residencia.Residence import *  # @UnusedWildImport

class TesteResidencia(unittest.TestCase):
    def setUp(self):
        self.residence = Residence()

    def tearDown(self):
        self.residence = None

    def testInitResidence(self):
        self.assertEqual(0, len(self.residence.getRooms()), "A residence deve inciar com 0 comodos")
        self.assertEqual(None, self.residence.getRoomOfControl(), "Ao iniciar a residence considera-se que o controle nao esta em comodo")

    def testAddRooms(self):
        result = self.residence.addRoom("Quarto", "192.168.1.2", 4545)
        self.assertTrue(result, "O resultado da adicao deve ser True pois o comodo nao existe no sistema")
        #self.assertEqual(["quarto"].sort(), self.residence.getRooms().sort(), "Comodos da residence invalidos")
        result = self.residence.addRoom("Sala", "192.168.1.0", 4545)
        self.assertTrue(result, "O resultado da adicao deve ser True pois o comodo nao existe no sistema")
        #self.assertEqual(["quarto", "sala"].sort(), self.residence.getRooms().sort(), "Comodos da residence invalidos")

    def testAddExistentRoom(self):
        result = self.residence.addRoom("Quarto", "192.168.1.2", 4545)
        self.assertTrue(result, "O resultado da adicao deve ser True pois o comodo nao existe no sistema")
        #self.assertEqual(["quarto"].sort(), self.residence.getRooms().sort(), "A residence deve inciar com 0 comodos")
        result = self.residence.addRoom("Quarto", "192.168.1.0", 4545)
        self.assertFalse(result, "O resultado da adicao deve ser False pois o comodo ja existe no sistema")
        #self.assertEqual(["quarto"].sort(), self.residence.getRooms().sort(), "Comodos da residence invalidos")

    def testRemoveRoom(self):
        result = self.residence.addRoom("Quarto", "192.168.1.2", 4545)
        self.assertTrue(result, "O resultado da adicao deve ser True pois o comodo nao existe no sistema")
        result = self.residence.addRoom("Sala", "192.168.1.0", 4545)
        self.assertTrue(result, "O resultado da adicao deve ser True pois o comodo nao existe no sistema")

        #self.assertEqual(2, len(self.residence.getRooms()), "A residence deve possuir 2 comodos")

        self.assertFalse(self.residence.removeRoom("banheiro"), "O resultado deve ser False pois banheiro nao existe no sistema")

        self.assertTrue(self.residence.removeRoom("sala"), "O resultado deve ser True pois sala existe no sistema")
        #self.assertEqual(1, len(self.residence.getRooms()), "A residence deve possuir 1 comodo")

        self.assertFalse(self.residence.removeRoom("sala"), "O resultado deve ser False pois sala nao existe no sistema")
        #self.assertEqual(1, len(self.residence.getRooms()), "A residence deve possuir 1 comodo")
