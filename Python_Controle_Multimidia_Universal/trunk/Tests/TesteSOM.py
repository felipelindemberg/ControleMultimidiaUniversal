import unittest
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
try:
    from Comodo.SOUND import *  # @UnusedWildImport
except ImportError:
    from trunk.Comodo.SOUND import *  # @UnusedWildImport


class TesteSOM(unittest.TestCase):
    def setUp(self):
        self.sound1 = SOUND()

    def tearDown(self):
        self.sound1 = None

    def testPower(self):
        self.assertFalse(self.sound1.getState(), "O estado deve ser False")
        self.sound1.turnOn()
        self.assertTrue(self.sound1.getState(), "O estado deve ser True")
        self.sound1.turnOff()
        self.assertFalse(self.sound1.getState(), "O estado deve ser False")

    def testVolume(self):
        self.assertEqual(self.sound1.getVolume(), 0, "O volume deve iniciar em 0")
        self.sound1.upVolume()
        self.assertEqual(self.sound1.getVolume(), 1, "O volume deve ser 1")
        for _ in range(10):
            self.sound1.upVolume()
        self.assertEqual(self.sound1.getVolume(), 11, "O volume deve ser 11")
        # down volume
        self.sound1.downVolume()
        self.assertEqual(self.sound1.getVolume(), 10, "O volume deve ser 10")
        for _ in range(5):
            self.sound1.downVolume()
        self.assertEqual(self.sound1.getVolume(), 5, "O volume deve ser 5")

    def testChannel(self):
        self.assertEqual(1, self.sound1.getChannel(), "O canal inicial deve ser 1")
        self.sound1.upChannel()
        self.assertEqual(2, self.sound1.getChannel(), "O canal deve ser 2")
        for _ in range(3):
            self.sound1.upChannel()
        self.assertEqual(2, self.sound1.getChannel(), "O canal deve ser 2")
        # down canal
        self.sound1.downChannel()
        self.assertEqual(1, self.sound1.getChannel(), "O canal deve ser 1")
        for _ in range(3):
            self.sound1.downChannel()
        self.assertEqual(1, self.sound1.getChannel(), "O canal deve ser 1")
