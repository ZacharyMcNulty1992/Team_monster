from direct.showbase.ShowBase import ShowBase
import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, PandaNode
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject


class Titlescreen(ShowBase):
  
  startPressed = False
  screen = 0
  b = 0



    #This sets the size of the screen
  def __init__(self, xSize, ySize):
      self.screen = DirectFrame(frameSize=(xSize/2, xSize/2, ySize/2, ySize/2),	frameColor=(0, 0, 0, 1))
  
  
  
    #This plays the music
  def __init__(self):
      self.mySound = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
      self.mySound.play()

      OnscreenImage(image = "logo.png", pos = (0.0, -70.0, 0.45), scale = (1.1, 0.9, 0.3))

      start = DirectButton(text = ("Start!", "Start!", "Hover", "disabled"), scale = 0.09, pos = (0,0,-.1))
      quit = DirectButton(text = ("Quit", "Quit", "Hover", "disabled"), scale = 0.09, pos = (0,0,-.3))

#This Creates the play button
#  def __init__(self):
#    self.maps = loader.loadModel('resources/Buttons/EGG_Play_Files/button_maps.egg')
#    self.play = DirectButton(geom = (self.maps.find('Play.png/button_ready'),
#    self.maps.find('Play_Click.png/button_click'),
#    self.maps.find('Play_Hover.png/button_rollover'),
#    self.maps.find('Play_Click.png/button_disabled')))
#This Creates the quit button
#def __init__(self):
#     self.maps = loader.loadModel('resources/Buttons/EGG_Quit_Files/button_maps.egg')
#     self.quit = DirectButton(geom = (maps.find('Quit.png/button_ready'),
#     maps.find('Quit_Click.png/button_click'),
#     maps.find('Quit_Hover.png/button_rollover'),
#     maps.find('Quit_Click.png/button_disabled')))

t = Titlescreen()
run()