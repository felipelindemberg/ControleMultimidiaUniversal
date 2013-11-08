#!/bin/bash

RED="\033[0;31m"
GREEN="\033[1;32m"
ENDCOLOR="\033[0m"

echo -e  $GREEN"Instalador de dependências do Controle Multimida Universal\n"$ENDCOLOR

TESTCONNECTION=`wget --tries=3 --timeout=15 www.google.com -O /tmp/testinternet &>/dev/null 2>&1`
if [ $? != 0 ]
then
	echo -e $RED"É necessário conexão com a internet para continuar"$ENDCOLOR
    exit 1
else
	echo -e $GREEN"Conexão com a internet verificada"$ENDCOLOR
fi

if [ -e /usr/bin/zenity ]
then
	echo -e $GREEN"\nZenity verificado"$ENDCOLOR
else
    /usr/bin/notify-send "Instalando Zenity."
	echo -e $RED"\nZenity não instalado. Instalando Zenity\n==============================\n"$ENDCOLOR
	sudo apt-get -y install zenity
    /usr/bin/notify-send "Zenity instalado."
fi

if [ -e /usr/bin/notify-send ]
then
	echo -e  $GREEN"\nNotify-osd verificado"$ENDCOLOR
else
    /usr/bin/notify-send "Instalando Notify-osd."
	echo -e  $RED"\nnotify-osd não instalado. Instalando notify-osd\n==============================\n"$ENDCOLOR
	sudo apt-get -y install notify-osd libnotify-bin
    /usr/bin/notify-send "Notify-osd instalado."
fi

while ! zenity --password | sudo -S echo ''; do
    if $(zenity --question --text="Senha inválida, deseja cancelar a instalação?"); then
      echo "Instalação cancelada"
      exit 1
    fi
done

echo "$appEntry" | sudo -S tee ${launcher}

/usr/bin/notify-send "Instalando dependências."

dpkg -s python2.7 >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython2.7 verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Python 2.7."
    echo -e  $RED"\npython2.7 não instalado. Instalando python2.7\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python2.7
    /usr/bin/notify-send "Python 2.7 instalado."
}

dpkg -s python-bluez >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-bluez verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Bluez."
    echo -e  $RED"\npython-bluez não instalado. Instalando python-bluez\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python-bluez
    /usr/bin/notify-send "Bluez instalado."
}

dpkg -s python-pygame >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-pygame verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Pygame."
    echo -e  $RED"\npython-pygame não instalado. Instalando python-pygame\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python-pygame
    /usr/bin/notify-send "Pygame instalado."
}

dpkg -s python-gtk2 >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-gtk2 verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Pygtk 2."
    echo -e  $RED"\npython-gtk2 não instalado. Instalando python-gtk2\n==============================\n"$ENDCOLOR
    /usr/bin/notify-send "Pygtk 2 instalado."
}

dpkg -s python-cherrypy3 >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-cherrypy3 verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Cherrypy 3."
    echo -e  $RED"\npython-cherrypy3 não instalado. Instalando python-cherrypy3\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python-cherrypy3
    /usr/bin/notify-send "Cherrypy 3 instalado."
}

dpkg -s timidity >/dev/null 2>&1 && {
    echo -e  $GREEN"\ntimidity verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Timidity."
    echo -e  $RED"\ntimidity não instalado. Instalando timidity\n==============================\n"$ENDCOLOR
    sudo apt-get -y install timidity
    /usr/bin/notify-send "Timidity instalado."
}

dpkg -s python-pip >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-pip verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando PIP."
    echo -e  $RED"\npython-pip não instalado. Instalando python-pip\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python-pip
    /usr/bin/notify-send "PIP instalado."
}

pip freeze | grep pep8 > ".tmp"

if [ "$?" == 0 ]
then
    echo -e  $GREEN"\npep8 verificado"$ENDCOLOR
else
    /usr/bin/notify-send "Instalando PEP8."
    echo -e  $RED"\npep8 não instalado. Instalando pep8\n==============================\n"$ENDCOLOR
    sudo pip install pep8
    /usr/bin/notify-send "PEP8 instalado."
fi

pip freeze | grep pylint > ".tmp"

if [ "$?" == 0 ]
then
    echo -e  $GREEN"\npylint verificado"$ENDCOLOR
else
    /usr/bin/notify-send "Instalando Pylint."
    echo -e  $RED"\npylint não instalado. Instalando pylint\n==============================\n"$ENDCOLOR
    sudo pip install pylint
    /usr/bin/notify-send "Pylint instalado."
fi

rm .tmp

dpkg -s python-xmlrunner >/dev/null 2>&1 && {
    echo -e  $GREEN"\npython-xmlrunner verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando XMLRunner."
    echo -e  $RED"\npython-xmlrunner não instalado. Instalando python-xmlrunner\n==============================\n"$ENDCOLOR
    sudo apt-get -y install python-xmlrunner
    /usr/bin/notify-send "XMLRunner instalado."
}

dpkg -s pulseaudio >/dev/null 2>&1 && {
    echo -e  $GREEN"\npulseaudio verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando PulseAudio."
    echo -e  $RED"\npulseaudio não instalado. Instalando pulseaudio\n==============================\n"$ENDCOLOR
    sudo apt-get install pulseaudio
    /usr/bin/notify-send "PulseAudio instalado."
}

dpkg -s evince >/dev/null 2>&1 && {
    echo -e  $GREEN"\nevince verificado"$ENDCOLOR
} || {
    /usr/bin/notify-send "Instalando Evince."
    echo -e  $RED"\nevince não instalado. Instalando evince\n==============================\n"$ENDCOLOR
    sudo apt-get install evince
    /usr/bin/notify-send "Evince instalado."
}

sudo -K

echo -e  $GREEN"\nDependências instaladas.\n"$ENDCOLOR

/usr/bin/notify-send "Dependências instaladas."
exit 0
