#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 10/21/14
# Updated By: Kevin
# Note(s): This class will be used to run
# 100 Monsters, implementing other classes
#-------------------------------------------#

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties, Filename
import sys, os
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs
from player import Player
from monster import Monster


class MainGame(ShowBase):

    # These are default settings
    controlStyle = "wasd"
    fullscreen = False
    winXSize = 1024
    winYSize = 768

    def __init__(self):
        if not os.path.isfile("settings.cfg"):
            cfgFile = open("settings.cfg", "w")
            cfgFile.close()
        else:
            cfgFile = open("settings.cfg", "r+")
        
        self.getSettings(cfgFile)
        #controlStyle = self.welcomeMessage()

        ShowBase.__init__(self)
        
        # Creates the window properties
        winProps = WindowProperties()
        # Set the window's resolution
        winProps.setSize(self.winXSize, self.winYSize)
        # Sets the cursor so that it's hidden
        winProps.setCursorHidden(True)
        # Changes the window name
        winProps.setTitle("100 Monsters")
        # Sets the game so it's fullscreen
        #winProps.setFullscreen(self.fullscreen)
        # Gives the set properties to the window
        base.win.requestProperties(winProps)

        # Disables the mouse from moving the camera (can still look around) 
        base.disableMouse()

        # Sets escape as the quit button
        base.accept("escape", sys.exit)

        self.initCollision()
        self.loadLevel()
        self.node = Player(self.controlStyle)
        
        # Shows subtitles at the bottom of the screen

        self.initMonster()
        self.initMusic()

        text = TextNode('node')
        text.setText("Every day in every way I'm getting better and better.")
        textNodePath =  render2d.attachNewNode(text)
        textNodePath.setScale(0.07)
        text.setAlign(TextNode.ABoxedCenter)
        Zccara = loader.loadFont('Zccara.ttf')
        text.setFont(Zccara)
    
    # This method sets options according to the settings.cfg file in the root folder
    def getSettings(self, cfgFile):
        for line in cfgFile:
            if line[0] == "#" or len(line) == 1:
                continue
            option, value = line.split(" = ", 2)
            option = option.lower()
            value = value.lower()
            if value[-1:] == '\n':
                value = value[:-1]
            if option == "control":
                self.controlStyle = value
            elif option == "fullscreen":
                if value == "true":
                    self.fullscreen = True
                else:
                    self.fullscreen = False
            elif option == "xres":
                self.winXSize = int(value)
            elif option == "yres":
                self.winYSize = int(value)
    
    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        #for debugging purposes
        base.cTrav.showCollisions(render)

    def loadLevel(self):
        self.level = loader.loadModel("resources/levels/first_floor.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(True)

    def initMonster(self):
        jumogoro = Monster("Jumogoro", "spiderlady.egg", 10, 30, 5, 5)

    def initMusic(self):
        music = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
        music.play()


game = MainGame()
game.run()
