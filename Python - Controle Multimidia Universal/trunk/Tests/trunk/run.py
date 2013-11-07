#!/usr/bin/env python
# coding: utf-8

try:
    import os
    import sys
    import pygtk
    pygtk.require("2.0")
    import gobject
    import gtk
    import json
    import time
    import cherrypy
    import bluetooth
    import threading
except ImportError, error:
    print >> sys.stderr, "Erro ao importar o modulo", error
    os._exit(1)

gtk.gdk.threads_init()

import threading

lib_path = os.path.abspath('Util/')
sys.path.append(lib_path)
try:
    import Network as util
except ImportError, e:
    try:
        import trunk.Util.Network as util
    except ImportError, err:
        print("A residência não importou o modulo", err)


class Application:
    def __init__(self):
        # Create a window
        
        self.threadComodo = None
        self.threadControle = None
        self.process = None
        self.ipResidence = None
        self.clickedResidence = False
        self.rooms = []
        self.namesRooms = []

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Controle multimidia universal")
        self.window.set_resizable(False)
        self.window.set_size_request(382, 220)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_position("center")

        self.window.set_icon_from_file('logo128.png')
        
        self.fixed = gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()
        self.window.show()

        # Label "Coverter"
        self.label = gtk.Label("Nome do cômodo")
        self.fixed.put(self.label, 0, 85)
        self.label.show()

        # Entrada
        self.entry = gtk.Entry()
        self.entry.set_max_length(10)
        self.entry.set_size_request(200, 40)
        self.entry.select_region(0, len(self.entry.get_text()))
        self.entry.connect("key_release_event", self.verifyNameRoom)
        self.fixed.put(self.entry, 0, 110)
        self.entry.show()
        self.entry.grab_focus()

        # Botão Iniciar residencia
        self.residenceButton = gtk.Button("Iniciar residência")
        self.residenceButton.set_size_request(200, 40)
        self.residenceButton.connect("clicked", self.openResidence)
        # self.button.connect("clicked", self.go)
        self.fixed.put(self.residenceButton, 0, 35)
        self.residenceButton.show()

        # Botão Iniciar controle
        self.controlButton = gtk.Button("Iniciar controle")
        self.controlButton.set_size_request(150, 40)
        self.controlButton.connect("clicked", self.openControl)
        self.fixed.put(self.controlButton, 210, 35)
        self.controlButton.show()

        # Botão Iniciar comodo
        self.roomButton = gtk.Button("Iniciar cômodo")
        self.roomButton.set_size_request(150, 40)
        self.roomButton.connect("clicked", self.openRoom)
        self.roomButton.set_sensitive(False)
        self.fixed.put(self.roomButton, 210, 110)
        self.roomButton.show()

        # Label "Saida"
        self.label = gtk.Label("")
        self.fixed.put(self.label, 0, 145)
        self.label.show()

        menubar = gtk.MenuBar()

        menu_help = gtk.Menu()

        item_tutorial = gtk.MenuItem("Tutorial")
        menu_help.append(item_tutorial)

        item_tutorial.connect_object("activate", self.openTutorial, None)

        item_about = gtk.MenuItem("Sobre")
        menu_help.append(item_about)

        item_about.connect_object("activate", self.openAbout, None)

        item_help = gtk.MenuItem("Ajuda")
        item_help.set_submenu(menu_help)

        menubar.append(item_help)

        self.fixed.put(menubar, 0, 0)
        menubar.show_all()

        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(360, 30)
        self.fixed.put(self.pbar, 0 , 165)

        self.timer = gobject.timeout_add (100, self.progress_timeout, self.pbar)

        self.window.show()

    def getRooms(self):
        if (self.ipResidence == None):
            self.ipResidence = util.getResidenceIp()
        if (self.ipResidence != "Residence is offline"):
            tmp = util.httpGetRequest(self.ipResidence, 5432,"getRooms")
            self.rooms = json.loads(tmp).keys()
        else:
            self.ipResidence = None

    def roomExist(self, nameRoom):
        self.getRooms()
        return nameRoom in self.rooms

    def openTutorial(self, data=None):
        os.system("evince %s" % os.path.abspath("Tutorial/tutorial.pdf"))

    def openAbout(self, data=None):
        about = gtk.AboutDialog()
        about.set_program_name("Controle Remoto Universal")
        about.set_version("1.0")
        about.set_copyright("10/2013\n\nFelipe Lindemberg\nFelipe Medeiros\nMarcos Antônio\nLucas Salvino")
        about.set_comments("Embedded - Laboratório de Sistemas Embarcados e Computação Pervasiva")
        about.run()
        about.destroy()

    def progress_timeout(self, pbobj):
        pbobj.pulse()
        return True

    def verifyNameRoom(self, widget, key):
        if (len(self.entry.get_text()) > 0):
            self.roomButton.set_sensitive(True)
            if (key.keyval == 65293):
                self.openRoom(widget)
        else:
            self.roomButton.set_sensitive(False)

    def startThreadResidence(self):
        self.pbar.show()
        self.residenceButton.set_sensitive(False)
        self.pbar.set_text("Iniciando residência")
        status = util.getResidenceIp()
        self.pbar.hide()
        self.clickedResidence = True
        if (status == "Residence is offline"):
            self.residenceButton.set_label("Residência iniciada")
            os.system("python " + os.path.abspath("Residencia/server.py"))
        else:
            self.residenceButton.set_label("Residência iniciada na rede")

    def startThreadRoom(self, nameRoom):
        self.pbar.show()
        if (not self.clickedResidence):
            self.residenceButton.set_sensitive(False)

        self.entry.set_sensitive(False)
        self.roomButton.set_sensitive(False)
        self.roomButton.set_label("Iniciando cômodo")
        self.pbar.set_text("Iniciando cômodo")

        if ((not self.entry.get_text() in self.namesRooms) and (not self.roomExist(self.entry.get_text()))):
            if (not self.clickedResidence):
                self.residenceButton.set_sensitive(True)
            self.entry.set_sensitive(True)
            self.roomButton.set_sensitive(True)
            self.pbar.hide()
            self.roomButton.set_label("Iniciar cômodo")
            self.namesRooms.append(nameRoom)
            os.system("python " + os.path.abspath("Comodo/main.py") + " " + nameRoom)
            self.namesRooms.remove(nameRoom)
        else:
            self.pbar.hide()
            self.roomButton.set_label("Cômodo existente")
            time.sleep(2)
            self.roomButton.set_label("Iniciar cômodo")
            if (not self.clickedResidence):
                self.residenceButton.set_sensitive(True)
            self.entry.set_sensitive(True)
            self.roomButton.set_sensitive(True)

    def startThreadControl(self):
        self.controlButton.set_sensitive(False)
        os.system("python " + os.path.abspath("Controle/control.py"))
        self.controlButton.set_sensitive(True)

    def openResidence(self, widget):
        threading.Thread(target=self.startThreadResidence).start()

    def openControl(self, widget):
        threading.Thread(target=self.startThreadControl).start()

    def openRoom(self, widget):
        threading.Thread(target=self.startThreadRoom, args=(self.entry.get_text(),)).start()

    def main(self):
        gtk.main()

    def destroy(self, widget, data=None):
        global timer
        self.timer = 0
        os.system("echo " + str(os.getpid()) + ">>.tmp")
        self.closeAllThreads()
        gtk.main_quit()
        sys.exit()
        gtk.main_quit()

    def closeAllThreads(self):
        fTmp = open(os.path.abspath(".tmp"))
        text = fTmp.readlines()
        if(len(text) > 0):
            for line in text:
                if (line.strip().isdigit()):
                    os.system("kill -9 " + line.replace("\n", "").strip())
        fTmp.close()
        os.system("rm .tmp")

if __name__ == "__main__":
    # Create an instance of our GTK application
    app = Application()
    gtk.gdk.threads_enter()
    app.main()
    gtk.gdk.threads_leave()
