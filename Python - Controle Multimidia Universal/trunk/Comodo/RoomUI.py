# coding: utf-8
# testlink

try:
    import sys
    import os
    import pygame
    from pygame.locals import *  # @UnusedWildImport
    from ClientBluetooth import *  # @UnusedWildImport
    from Equipment_Info import *
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)


lib_path = os.path.abspath('Util/')
sys.path.append(lib_path)
try:
    from Pygame import loadSprite
except ImportError:
    print("erro ao importar")


os.system("echo " + str(os.getpid()) + ">>.tmp")


class RoomUI:
    """A classe RoomUI é uma classe de interface gráfica de cômodo
    """

    hand_strings = (
      "     XX                 ",
      "    X..X                ",
      "    X..X                ",
      "    X..X                ",
      "    X..X                ",
      "    X.."+"X"*3+"              ",
      "    X..X.."+"X"*3+"           ",
      "    X..X..X..XX         ",
      "    X..X..X..X.X        ",
      "X"*3+" X..X..X..X..X       ",
      "X..XX........X..X       ",
      "X...X...........X       ",
      " X..X...........X       ",
      "  X.X...........X       ",
      "  X.............X       ",
      "   X............X       ",
      "   X...........X        ",
      "    X..........X        ",
      "    X..........X        ",
      "     X........X         ",
      "     X........X         ",
      "     "+"X"*10+"         ",
      "                        ",
      "                        ",
    )

    arrow_strings = (
      "X                       ",
      "XX                      ",
      "X.X                     ",
      "X..X                    ",
      "X...X                   ",
      "X....X                  ",
      "X.....X                 ",
      "X......X                ",
      "X.......X               ",
      "X........X              ",
      "X.........X             ",
      "X..........X            ",
      "X......"+"X"*6+"           ",
      "X...X..X                ",
      "X..XX..X                ",
      "X.X  X..X               ",
      "XX   X..X               ",
      "X     X..X              ",
      "      X..X              ",
      "       X..X             ",
      "       X..X             ",
      "        XX              ",
      "                        ",
      "                        ",
    )

    def __init__(self, serverFacade, room):
        """Construtor da classe faz a inicialização dos atributos
        :Param serverFacade: Servidor de faixada
        :Type serverFacade: Servidor Residência
        :Param room: Cômodo
        :Type room: Objeto Comodo
        """
        pygame.init()

        self.time_loading = 0
        self.bluetoothConnected = False
        self.bluetoothButtonClicked = False
        self.controlStatusPosition = False
        self.SOUND = None
        self.buttonAddPeopleRect = None
        self.bluetoothSprite = None
        self.buttonSubtPeopleSprite = None
        self.bluetoothRect = None
        self.TV = None
        self.controlStatusSprite = None
        self.buttonSubtPeoplePosition = None
        self.bluetoothRectPosition = None
        self.buttonAddPeopleSprite = None
        self.controlInfoRect = None
        self.buttonSubtPeopleRect = None
        self.buttonAddPeoplePosition = None

        screen_width = 640
        screen_height = 480
        screen_flag = 0
        screen_depht = 32

        self.sprites = {}
        self.channels = {}
        self.cursors = {}

        self.screen = pygame.display.set_mode((screen_width, screen_height), screen_flag, screen_depht)
        self.clock = pygame.time.Clock()

        self.serverFacade = serverFacade
        self.room = room
        
        icon=pygame.Surface((32,32))
        rawicon=pygame.image.load("logo128.png")
        for i in range(0,128):
            for j in range(0,128):
                icon.set_at((i,j), rawicon.get_at((i,j)))
        pygame.display.set_icon(icon)#set wind


        pygame.display.set_caption("Cômodo " + self.room.getName())

        self.__loadSprites()
        self.__loadCursors()
        self.__loadEquipments()

        self.__createBluetoothSprite()
        self.__createAddPeopleButton()
        self.__createSubtPeopleButton()
        self.__createControlInfo()

        self.image_surface = pygame.Surface((233.6, 131.4))

        self.image_surface.fill(Color("black"))


    def __loadSprites(self):
        """Metodo que faz o carregamento das imagens
        """
        self.sprites["people"] = loadSprite("Comodo/images/people.png")
        self.sprites["background"] = loadSprite("Comodo/images/background.jpg", False)
        self.sprites["bluetooth_off"] = loadSprite("Comodo/images/bluetooth_off.png")
        self.sprites["bluetooth_on"] = loadSprite("Comodo/images/bluetooth_on.png")
        self.sprites["bluetooth_down"] = loadSprite("Comodo/images/bluetooth_down.png")
        self.sprites["add_normal"] = loadSprite("Comodo/images/add_normal.png")
        self.sprites["add_down"] = loadSprite("Comodo/images/add_down.png")
        self.sprites["subt_normal"] = loadSprite("Comodo/images/subt_normal.png")
        self.sprites["subt_down"] = loadSprite("Comodo/images/subt_down.png")
        self.sprites["control_off"] = loadSprite("Comodo/images/control_off.png")
        self.sprites["control_on"] = loadSprite("Comodo/images/control_on.png")
        self.sprites["panel"] = loadSprite("Comodo/images/panel.png")

    def __loadCursors(self):
        """Método que faz o carregamento dos cursores
        """
        self.cursors["hand"] = pygame.cursors.compile(self.hand_strings, ".", "X")
        self.cursors["arrow"] = pygame.cursors.compile(self.arrow_strings, ".", "X")

    def __loadEquipments(self):
        """Método que faz o carregamento dos equipamentos
        """
        self.room.getTv().load(self.screen)
        self.room.getSound().load(self.screen)

        self.TV = pygame.sprite.RenderPlain(self.room.getTv())
        self.SOUND = pygame.sprite.RenderPlain(self.room.getSound())

    def __createBluetoothSprite(self):
        """Método que cria a imagem do dispositivo bluetooth
        """
        self.bluetoothSprite = self.sprites.get("bluetooth_off")
        self.bluetoothRect = self.bluetoothSprite.get_rect()
        self.bluetoothRectPosition = (475, 389)
        self.bluetoothRect = self.bluetoothRect.move(self.bluetoothRectPosition)

    def __createAddPeopleButton(self):
        """Método que cria o botão de adicionar pessoas
        """
        self.buttonAddPeopleSprite = self.sprites.get("add_normal")
        self.buttonAddPeopleRect = self.buttonAddPeopleSprite.get_rect()
        self.buttonAddPeoplePosition = (165, 389)
        self.buttonAddPeopleRect = self.buttonAddPeopleRect.move(self.buttonAddPeoplePosition)

    def __createSubtPeopleButton(self):
        """Método que cria o botão de decrementar pessoas
        """
        self.buttonSubtPeopleSprite = self.sprites.get("subt_normal")
        self.buttonSubtPeopleRect = self.buttonSubtPeopleSprite.get_rect()
        self.buttonSubtPeoplePosition = (237, 389)
        self.buttonSubtPeopleRect = self.buttonSubtPeopleRect.move(self.buttonSubtPeoplePosition)

    def __createControlInfo(self):
        """Método que cria a imagem do controle
        """
        self.controlStatusSprite = self.sprites.get("control_off")
        self.controlInfoRect = self.buttonSubtPeopleSprite.get_rect()
        self.controlStatusPosition = (548, 389)
        self.controlInfoRect = self.controlInfoRect.move(self.controlStatusPosition)

    def run(self):
        """Método de atualização da interface
        """
        while (not self.serverFacade.getConnected()):
            self.clock.tick(60)
            self.screen.blit(self.sprites["background"], (0, 0))
            self.__loadingScreen()
            pygame.display.flip()
            self.__pygameEvents()
        while True:
            self.clock.tick(60)
            self.__pygameEvents()
            self.screen.blit(self.sprites["background"], (0, 0))
            self.screen.blit(self.sprites["panel"], ((640 - self.sprites["panel"].get_width()) / 2, 10))
            printText(self.screen, self.room.getName(), "Arial", 35, 205, 15, Color("black"), "center")
            self.__drawTV()
            self.__drawSound()
            self.__drawNumberPeople()
            self.__drawDeviceBluetooth()
            self.__drawButtonBluetooth()
            self.__drawButtonAddPeople()
            self.__drawButtonSubtPeople()
            self.__drawControlStatus()
            pygame.display.flip()

    def __pygameEvents(self):
        """Método que roda os eventos do Pygame
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.serverFacade.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (self.buttonAddPeopleRect.collidepoint(x, y)):
                    self.buttonAddPeopleSprite = self.sprites.get("add_down")
                    self.room.setNumberOfPeoples(self.room.getNumberOfPeoples() + 1)

                elif (self.buttonSubtPeopleRect.collidepoint(x, y)):
                    self.buttonSubtPeopleSprite = self.sprites.get("subt_down")
                    self.room.setNumberOfPeoples(self.room.getNumberOfPeoples() - 1)

                elif (self.bluetoothRect.collidepoint(x, y)):
                    if (self.bluetoothConnected):
                        self.bluetoothButtonClicked = True
                        self.bluetoothSprite = self.sprites.get("bluetooth_down")
                        if (self.bluetoothConnected):
                            sendSignalBluetooth(self.room.getName())
            if event.type == pygame.MOUSEBUTTONUP:
                self.bluetoothButtonClicked = False
                self.buttonAddPeopleSprite = self.sprites.get("add_normal")
                self.buttonSubtPeopleSprite = self.sprites.get("subt_normal")

        x, y = pygame.mouse.get_pos()
        
        if (self.bluetoothRect.collidepoint(x, y) or self.buttonAddPeopleRect.collidepoint(x, y) or
            self.buttonSubtPeopleRect.collidepoint(x, y)):
            pygame.mouse.set_cursor((24, 24), (5, 0), self.cursors.get("hand")[0], self.cursors.get("hand")[1])
        else:
            pygame.mouse.set_cursor((24, 24), (5, 0), self.cursors.get("arrow")[0], self.cursors.get("arrow")[1])

    def __loadingScreen(self):
        """Método que faz o carregamento da tela de conexão com Residência
        """
        if (self.time_loading < 10):
            printText(self.screen , "Conectando", "Arial", 60, 150, 40, Color("white"))
            self.time_loading += 1
        elif (self.time_loading >= 10 and self.time_loading < 40):
            printText(self.screen , "Conectando.", "Arial", 60, 150, 40, Color("white"))
            self.time_loading += 1
        elif (self.time_loading >= 40 and self.time_loading < 70):
            printText(self.screen , "Conectando..", "Arial", 60, 150, 40, Color("white"))
            self.time_loading += 1
        elif (self.time_loading >= 70 and self.time_loading < 100):
            printText(self.screen , "Conectando...", "Arial", 60, 150, 40, Color("white"))
            self.time_loading += 1
        else:
            printText(self.screen , "Conectando", "Arial", 60, 150, 40, Color("white"))
            self.time_loading = 0

    def __drawTV(self):
        """Método que desenha a TV na interface
        """
        self.room.getTv().update()
        self.TV.draw(self.screen)
        showInfo(self.screen, self.room.getSound(), "SOM", (500, 285))

    def __drawSound(self):
        """Método que desenha a Som na interface
        """
        self.room.getSound().update()
        self.SOUND.draw(self.screen)
        showInfo(self.screen, self.room.getTv(), "TV", (159, 285))

    def __drawNumberPeople(self):
        """Método que desenha o número de pessoas presentes no cômodo
        """
        self.screen.blit(self.sprites["people"], (23, 390))
        printText(self.screen , str(self.room.getNumberOfPeoples()), "Arial", 40, 110, 400, Color("black"))

    def __drawDeviceBluetooth(self):
        """Método que desenha o dispositivo bluetooth do cômodo
        """
        self.screen.blit(self.bluetoothSprite, (self.bluetoothRectPosition))

    def __drawButtonBluetooth(self):
        """Método que desenha o botão bluetooth do cômodo
        """
        self.bluetoothConnected = bluetoothHasConnected()
        if (not self.bluetoothButtonClicked):
            self.bluetoothSprite = self.sprites.get("bluetooth_on" if self.bluetoothConnected else "bluetooth_off")

    def __drawButtonAddPeople(self):
        """Método que desenha o botão de adicionar pessoas
        """
        self.screen.blit(self.buttonAddPeopleSprite, (self.buttonAddPeoplePosition))

    def __drawButtonSubtPeople(self):
        """Método que desenha o botão de decrementar pessoas
        """
        self.screen.blit(self.buttonSubtPeopleSprite, (self.buttonSubtPeoplePosition))

    def __drawControlStatus(self):
        """Método que desenha o status do controle
        """
        if (self.room.getControlIsFound()):
            self.controlStatusSprite = self.sprites.get("control_on")
        else:
            self.controlStatusSprite = self.sprites.get("control_off")

        self.screen.blit(self.controlStatusSprite, (self.controlStatusPosition))
