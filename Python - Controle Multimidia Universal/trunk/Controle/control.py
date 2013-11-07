# coding: utf-8
#!/usr/bin/python
import pygame  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
from ControlMultimediaUniversal import *  # @UnusedWildImport


# carrega as imagens e inicia o control
control = ControlMultimediaUniversal()

# loop principal do pygame
counter = 0
position = -300

residenceFounded = True

if control.getIp() == "Residence is offline":
    residenceFounded = False

while residenceFounded:
    for event in pygame.event.get():
        if event == None:
            break
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            control.disconnectControl()
            pygame.quit()
            os._exit(0)
        control.turnOffCaptureEvent(event)
        control.optionTVCaptureEvent(event)
        control.optionSoundCaptureEvent(event)
        control.upVolumeCaptureEvent(event)
        control.downVolumeCaptureEvent(event)
        control.upChannelCaptureEvent(event)
        control.downChannelCaptureEvent(event)
        control.muteCaptureEvent(event)

    # carrega botões na tela

    control.drawScreen(position)
    # botao desligar
    control.turnOffAnimation()
    # botao mudar opcao tv
    control.optionTVAnimation()
    # botao mudar opcao som
    control.optionSoundAnimation()
    # aumentar volume
    control.upVolumeAnimation()
    # diminuir volume
    control.downVolumeAnimation()
    # botao mudar canal cima
    control.changeChannelUPAnimation()
     # botao mudar canal baixo
    control.changeChannelDownAnimation()
    
    control.muteAnimation()
    
    # Checa o comodo que o control se encontra
    counter += 1
    if counter % 10 == 0:
        position += 1
    if position == 300:
        position = -300
        counter = 0

        # Obs:A maioria dessa variaveis referentes ao comodo devem estar no servidor e nao no control

    pygame.display.flip()
