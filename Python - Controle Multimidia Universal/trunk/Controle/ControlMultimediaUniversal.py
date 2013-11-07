# coding: utf-8
#!/usr/bin/python
import pygame
from pygame.locals import *  # @UnusedWildImport @IgnorePep8
import os
import sys
from ServerBluetooth import *
from ThreadBluetooth import *
lib_path = os.path.abspath('Util/')

sys.path.append(lib_path)
try:
    import Network as util
    from Pygame import loadSprite
except ImportError:
    print("erro ao importar")

# variaveis do sistema

class ControlMultimediaUniversal:
    """A Classe ControlMultimediaUniversal é uma classe que faz o controle dos equipamentos presentes no cômodo em que o mesmo se encontra

    :version 164
    :author Lucas Salvino
    """

    def __init__(self):
        """Construtor da classe
        """
        pygame.init()
        # carrega imagens

        self.__ip_residence = util.getResidenceIp()

        if (self.__ip_residence != "Residence is offline"):
            self.font = None
            self.__pressed = False
            self.__buttonTVTurnedOn = True
            self.__buttonSoundTurnedOn = False
            self.__port = 5432
            self.__sprites = {}

            self.__screen = pygame.display.set_mode((290, 590))

            pygame.display.set_caption('Controle')

            self.__background = pygame.Surface(self.__screen.get_size()).convert()
            self.__room = None
            self.__background.fill((0, 0, 0))
            self.__loadSprites()

            self.__thread = threadBluetooth(self.__ip_residence)
            # __thread.setDaemon(True)
            self.__thread.start()
        else:
            self.__screen = pygame.display.set_mode((600, 300))
            self.__background = pygame.Surface(self.__screen.get_size()).convert()
            self.__room = None
            self.__background.fill((0, 0, 0))  
            pygame.display.set_caption('Residência não encontrada')
            self.__background = pygame.Surface(self.__screen.get_size()).convert()
            pygame.font.get_fonts()
            self.font = pygame.font.Font(os.path.abspath("Controle/font/ALPNSCND.TTF"), 45, bold = False)
            countToQuit = 0
            label = self.font.render("RESIDENCIA", 1, (255, 0, 0))
            label2 = self.font.render("OFFLINE", 1, (255, 0, 0))

            clock = pygame.time.Clock()
            while True:
                if countToQuit == 5:
                    pygame.quit()
                    os._exit(0)
                for event in pygame.event.get():
                    if event == None:
                        break
                    if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        os._exit(0)

                self.__screen.blit(self.__background, (0, 0))
                self.__screen.blit(label, (0, 80))
                self.__screen.blit(label2, (50, 130))

                pygame.display.flip()
                clock.tick(1)
                countToQuit += 1

    # funcionalidades do controle-> COLOCAR FUNCOES AKI<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # checa __room
    def __loadSprites(self):
        """Método que faz o carregamento das imagens
        """
        self.__sprites["button_mute"] = loadSprite("Controle/images/mudo.png")
        self.__sprites["button_mute_animation"] = loadSprite("Controle/images/mudo_branco.png")
        self.__sprites["background_control"] = loadSprite("Controle/images/background.png")
        self.__sprites["display1"] = loadSprite("Controle/images/visor.png")
        self.__sprites["display"] = pygame.transform.scale(self.__sprites.get("display1"), (290, 160))
        self.__sprites["button_sound"] = loadSprite("Controle/images/som.png")
        self.__sprites["button_sound_animation"] = loadSprite("Controle/images/som_branco.png")
        self.__sprites["button_tv"] = loadSprite("Controle/images/TV.png")
        self.__sprites["button_tv_animation"] = loadSprite("Controle/images/TV_branco.png")
        self.__sprites["button_channelDown"] = loadSprite("Controle/images/mudar_canal1.png")
        self.__sprites["button_channelDown_animation"] = loadSprite("Controle/images/mudar_canal1_brancos.png")
        self.__sprites["button_channelUp"] = loadSprite("Controle/images/mudar_canal2.png")
        self.__sprites["button_channelUp_animation"] = loadSprite("Controle/images/mudar_canal2_branco.png")
        self.__sprites["button_volumeDown"] = loadSprite("Controle/images/diminuir_volume.png")
        self.__sprites["button_volumeDown_animation"] = loadSprite("Controle/images/diminuir_volume_branco.png")
        self.__sprites["button_volumeUp"] = loadSprite("Controle/images/aumentar_volume.png")
        self.__sprites["button_volumeUp_animation"] = loadSprite("Controle/images/aumentar_volume_branco.png")
        self.__sprites["button_turnOff"] = loadSprite("Controle/images/image.png")
        self.__sprites["button_turnOff_animation"] = loadSprite("Controle/images/image_branco.png")

    def __printText(self, txtText, Textx, Texty, Textcolor):
        """Método que imprime textos
        """
        pygame.font.get_fonts()
        # cor = (255,255,255)

        # myfont = pygame.font.SysFont(Textfont, Textsize)
        #self.font = pygame.font.Font(os.path.abspath("Controle/font/ALPNSCND.TTF"), 45, bold = False)
        # __room = font.render(txtText, False, cor)
        self.font = pygame.font.Font(os.path.abspath("Controle/font/ALPNSCND.TTF"), 45, bold = False)
        label = self.font.render(txtText, 1, Textcolor)

        self.__screen.blit(label, (Textx, Texty))

    def __sendCommand(self, command):
        """Método que envia comandos
        :Param command: Comando
        :Type command: String
        :Return: Requisição Http Post em Residência
        :Rtype: Requisição Http Post
        """
        # o command tem que ser uma string
        # TV
        if (self.__room != None and self.__room != ""):
            params = None
            if self.__buttonTVTurnedOn == True:
                params = {"nameRoom": self.__room, "equipment":"tv", "command": command}
                print (params)
            # SOM
            if self.__buttonSoundTurnedOn == True:
                params = {"nameRoom": self.__room, "equipment":"som", "command": command}
                print (params)
            self.__pressed = True

            return util.httpPostRequest(self.__ip_residence, self.__port, "sendCommand", params)

    def getIp(self):
        return self.__ip_residence

    def drawScreen(self, position):
        """Método que exibe uma tela com o nome do cômodo em que o controle se encontra
        """
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__sprites.get("background_control"), (-10, -12))

        self.__room = self.__thread.getRoom()
        if self.__room != None:
            self.__printText(self.__room,  -position, 200, Color("red"))
        else:
            if position > -300:
                self.__printText("",  70, 200, Color("red"))
            if position > -150:
                self.__printText(".",  70, 200, Color("red"))
            if position > 0:
                self.__printText("..",  70, 200, Color("red"))
            if position > 150:
                self.__printText("...",  70, 200, Color("red"))

        self.__screen.blit(self.__sprites.get("display"), (-1, 138))

        if self.__buttonSoundTurnedOn:
            self.__screen.blit(self.__sprites.get("button_sound_animation"), (190, 70))
        else:
            self.__screen.blit(self.__sprites.get("button_sound"), (190, 70))

        if self.__buttonTVTurnedOn:
            self.__screen.blit(self.__sprites.get("button_tv_animation"), (30, 70))
        else:
            self.__screen.blit(self.__sprites.get("button_tv"), (30, 70))
        # captura de eventos dos botoes

    def __unpressButton(self, eventReceiver):
        """Método que despressiona o botão
        :Param event: Evento Pygame a ser capturado
        :Type event: Evento Pygame
        """
        if (eventReceiver.type == MOUSEBUTTONUP and eventReceiver.button == 1) and self.__pressed:
            self.__pressed = False

    def __isPressedButton(self, eventReceiver):
        """Método que verifica se o botão foi pressionado
        :Param event: Evento Pygame a ser checado
        :Type event: Evento Pygame
        """
        return(eventReceiver.type == MOUSEBUTTONDOWN and eventReceiver.button == 1) and not self.__pressed

    def __capturePositionMouseX(self, minor, major):
        """Método que captura a posição do cursor no eixo X do plano cartesiano 
        :Param minor: Menor limite de X
        :Type minor: Inteiro
        :Param major: Maior limite de X
        :Type major: Inteiro
        :Return: Inteiro referente a posição
        :Return: Inteiro
        """
        return major > pygame.mouse.get_pos()[0] > minor

    def __capturePositionMouseY(self, minor, major):
        """Método que captura a posição do cursor no eixo Y do plano cartesiano 
        :Param minor: Menor limite de Y
        :Type minor: Inteiro
        :Param major: Maior limite de Y
        :Type major: Inteiro
        :Return: Inteiro referente a posição
        :Rtype: Inteiro
        """
        return major > pygame.mouse.get_pos()[1] > minor

    def turnOffCaptureEvent(self, eventReceiver):
        """Método que desliga o aparelho"
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(45, 135):
            self.__sendCommand("power")

        self.__unpressButton(eventReceiver)

    def optionTVCaptureEvent(self, eventReceiver):
        """Método que seleciona a opção TV
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(30, 120) and self.__capturePositionMouseY(70, 160):
            self.__pressed = True
            print "controll"
            if self.__buttonSoundTurnedOn:
                self.__buttonSoundTurnedOn = False
                self.__buttonTVTurnedOn = True

            elif not self.__buttonTVTurnedOn:
                self.__buttonTVTurnedOn = True

        self.__unpressButton(eventReceiver)

    def optionSoundCaptureEvent(self, eventReceiver):
        """Método que seleciona a opção Som
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(190, 280) and self.__capturePositionMouseY(70, 160):
            self.__pressed = True
            if self.__buttonTVTurnedOn:
                self.__buttonTVTurnedOn = False
                self.__buttonSoundTurnedOn = True

            elif not self.__buttonSoundTurnedOn:
                self.__buttonSoundTurnedOn = True
        self.__unpressButton(eventReceiver)

    def upVolumeCaptureEvent(self, eventReceiver):
        """Método que aumenta o volume
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(192, 275) and self.__capturePositionMouseY(400, 490):
            self.__sendCommand("upvolume")

    def downVolumeCaptureEvent(self, eventReceiver):
        """Método que diminui o volume
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(35, 118) and self.__capturePositionMouseY(400, 490):
            self.__sendCommand("downvolume")

        self.__unpressButton(eventReceiver)

    def upChannelCaptureEvent(self, eventReceiver):
        """Método que aumenta o canal
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(325, 408):
            self.__sendCommand("upChannel")

        self.__unpressButton(eventReceiver)

    def downChannelCaptureEvent(self, eventReceiver):
        """Método que diminui o canal
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(482, 565):
            self.__sendCommand("downChannel")

        self.__unpressButton(eventReceiver)

    def muteCaptureEvent(self, eventReceiver):
        """Método que coloca o aparelho na opção "mudo"
        :Param event: Evento do Pygame a ser checado
        :Type event: Evento Pygame
        """
        if self.__isPressedButton(eventReceiver) and self.__capturePositionMouseX(115, 160) and self.__capturePositionMouseY(410, 480):
            self.__sendCommand("mute")

        self.__unpressButton(eventReceiver)
    # animacoes dos botões

    def turnOffAnimation(self):
        """Método que simula o cursor em cima do botão desligar
        """
        if self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(45, 135):
            self.__screen.blit(self.__sprites.get("button_turnOff_animation"), (110, 45))
        else:
            self.__screen.blit(self.__sprites.get("button_turnOff"), (110, 45))

    def optionTVAnimation(self):
        """Método que simula o cursor em cima do botão TV
        """
        if self.__capturePositionMouseX(30, 120) and self.__capturePositionMouseY(70, 160):
            self.__screen.blit(self.__sprites.get("button_tv_animation"), (30, 70))

    def optionSoundAnimation(self):
        """Método que simula o cursor em cima do botão Som
        """
        if self.__capturePositionMouseX(190, 280) and self.__capturePositionMouseY(70, 160):
            self.__screen.blit(self.__sprites.get("button_sound_animation"), (190, 70))

    def upVolumeAnimation(self):
        """Método que simula o cursor em cima do botão aumentar volume
        """
        if self.__capturePositionMouseX(195, 275) and self.__capturePositionMouseY(400, 490):
            self.__screen.blit(self.__sprites.get("button_volumeUp_animation"), (185, 400))
        else:
            self.__screen.blit(self.__sprites.get("button_volumeUp"), (185, 400))

    def downVolumeAnimation(self):
        """Método que simula o cursor em cima do botão diminuir volume
        """
        if self.__capturePositionMouseX(35, 115) and self.__capturePositionMouseY(400, 490):
            self.__screen.blit(self.__sprites.get("button_volumeDown_animation"), (35, 400))
        else:
            self.__screen.blit(self.__sprites.get("button_volumeDown"), (35, 400))

    def changeChannelUPAnimation(self):
        """Método que simula o cursor em cima do botão aumentar canal
        """
        if self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(335, 400):
            self.__screen.blit(self.__sprites.get("button_channelUp_animation"), (110, 325))
        else:
            self.__screen.blit(self.__sprites.get("button_channelUp"), (110, 325))

    def changeChannelDownAnimation(self):
        """Método que simula o cursor em cima do botão diminuir canal
        """
        if  self.__capturePositionMouseX(110, 200) and self.__capturePositionMouseY(485, 565):
            self.__screen.blit(self.__sprites.get("button_channelDown_animation"), (110, 475))
        else:
            self.__screen.blit(self.__sprites.get("button_channelDown"), (110, 475))

    def muteAnimation(self):
        """Método que simula o cursor em cima do botão mute
        """
        if  self.__capturePositionMouseX(120, 185) and self.__capturePositionMouseY(410, 480):
            self.__screen.blit(self.__sprites.get("button_mute_animation"), (110, 400))
        else:
            self.__screen.blit(self.__sprites.get("button_mute"), (110, 400))

    def disconnectControl(self):
        """Método que desconecta o controle do cômodo que está sendo controlado
        """
        params = {"nameRoom": self.__room}
        util.httpPostRequest(self.__ip_residence, self.__port, "disconnectControl", params)
