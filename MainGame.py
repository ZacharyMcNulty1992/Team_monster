#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 10/16/14
# Updated By: Rachael
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

    def __init__(self):
        
        controlStyle = self.welcomeMessage()
	print(controlStyle)

        ShowBase.__init__(self)
        
        # Creates the window properties
        winProps = WindowProperties()
        # Sets the cursor so that it's hidden
        winProps.setCursorHidden(True)
        # Changes the window name
        winProps.setTitle("100 Monsters")
        # Sets the game so it's fullscreen
        winProps.setFullscreen(True)
        # Gives the set properties to the window
        base.win.requestProperties(winProps)

        # Disables the mouse from moving the camera (can still look around) 
        base.disableMouse()

        # Sets escape as the quit button
        base.accept("escape", sys.exit)

        self.initCollision()
        self.loadLevel()
        self.initPlayer()
        
        self.showSubs()

        #used for debugging
        self.initMonster()
        self.initMusic()

    def welcomeMessage(self):
	print("\n\n\n\n\nWelcome to 100 Monsters. Below please enter a preferred style of controls for movement within the game. The two types available are using WASD or arrow keys. (Please type your answer in a string with quotes).\n\n\n\n\n")	
	controls = input("Enter Style of Controls (WASD / Arrows): ")
        controls = controls.lower()

        while (controls != "wasd" and controls != "arrows"):
            controls = input("That wasn't an option, try again. Please enter either 'WASD' or 'Arrows'")
	
	return controls

    def showSubs(self):
        
        subFile = open("subs.txt", "r")
        subline = subFile.read()

        #font = loader.loadFont("resources/fonts/Zccara.tff")

        OnscreenText(text = subline, pos = (0, -.8), scale = .06, fg = (1, 1, 1, 1), shadow = (0, 0, 0, 1), align = TextNode.ACenter, wordwrap = 50)

    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        #for debugging purposes
        base.cTrav.showCollisions(render)

    def loadLevel(self):
        self.level = loader.loadModel("resources/levels/first_floor.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(True)

    def initPlayer(self):
        self.node = Player()

    def initMonster(self):
        self.node = Monster()

    def initMusic(self):
        music = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
        music.play()
        

game = MainGame()
game.run()
