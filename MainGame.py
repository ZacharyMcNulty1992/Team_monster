#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 10/26/14
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

    # These are default settings in case they are not specified in the config file
    controlStyle = "wasd"
    fullscreen = False
    winXSize = 1024
    winYSize = 768
    debug = False

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
        winProps.setFullscreen(self.fullscreen)
        # Gives the set properties to the window
        base.win.requestProperties(winProps)

        # Disables the mouse from moving the camera (can still look around) 
        base.disableMouse()

        # Sets escape as the quit button
        base.accept("escape", sys.exit)

        self.initCollision()
        self.loadLevel()
        self.node = Player(self.controlStyle)
        if self.debug:
            self.node.toggleJump()
        
        # Shows subtitles at the bottom of the screen

        self.initMonster()
        self.initMusic()

        text = TextNode('node')
        text.setText("There's supposed to be a file reader. Will recreate soon!")
        textNodePath =  render2d.attachNewNode(text)
        textNodePath.setScale(0.07)
        text.setAlign(TextNode.ABoxedCenter)
        Zccara = loader.loadFont('resources/fonts/Zccara.ttf')
        text.setFont(Zccara)
        textNodePath.setPos(0, 0, -.60)
        text.setWordwrap(20)
        text.setAlign(text.ACenter)
       
    
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
            elif option == "debugmode":
                if value == "true":
                    self.debug = True
                else:
                    self.debug = False

    # Shows subtitles at the bottom of the screen
    def showSubs(self):
        subFile = open("subs.txt", "r")
        subline = subFile.read()
        #font = loader.loadFont("resources/fonts/Zccara.tff")
        OnscreenText(text = subline, pos = (0, -.8), scale = .06, fg = (1, 1, 1, 1), shadow = (0, 0, 0, 1),
        align = TextNode.ACenter, wordwrap = 50)

    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        #for debugging purposes
        if self.debug:
            base.cTrav.showCollisions(render)

    def loadLevel(self):
        self.level = loader.loadModel("resources/levels/first_floor.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(True)

    def initMonster(self):
        path = "resources/models/"
        jumogoro = Monster("Jumogoro", "spiderlady.egg", 0, 30, 5, 5, 0.85)
        jumogoro.anim("Walk", True)
        kappa = Monster("Kappa", "kappa.egg", 0, 10, 5, 3, 0.80)
        kappa.anim("Idle", True)

    def initMusic(self):
        music = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
        music.play()


game = MainGame()
game.run()
