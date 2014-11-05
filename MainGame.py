#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 11/02/14
# Updated By: Kevin
# Note(s): This class will be used to run
# 100 Monsters, implementing other classes
#-------------------------------------------#

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties, Filename
import sys, os, math, datetime
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs
from player import Player
from monster import Monster
from item import Item


class MainGame(ShowBase):

    # These are default settings in case they are not specified in the config file
    controlStyle = "wasd"
    fullscreen = False
    winXSize = 1024
    winYSize = 768
    debug = False
    lighting = True
    isPaused = False
    alreadyRemoved = False

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

        # Sets p as the quit button and escape for pause
        base.accept("p", sys.exit)
        base.accept("escape", self.togglePause)

        taskMgr.add(self.PauseUpdate, 'pause-task')

        self.initCollision()
	
        self.player = Player(self.controlStyle)
        if self.debug:
            self.player.toggleJump()
	
	self.loadSkybox()
	self.loadLevel()
        self.initObjects()
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
        
        #Lighting Test
        if self.lighting:
            alight = AmbientLight('alight')
            alight.setColor(VBase4(0.25, 0.25, 0.25, .75))
            alnp = render.attachNewNode(alight)
            render.setLight(alnp)
            render.setShaderAuto()
            self.player.initLight()
        

    #Creates and Loads the Skybox
    def loadSkybox(self):
        self.skybox = loader.loadModel("resources/models/skybox.egg")
	self.skybox.setScale(1000.0,1000.0,1000.0)
        self.skybox.setPos(2,2,2)
        self.skybox.reparentTo(base.cam)
        self.skybox.setEffect(CompassEffect.make(self.render, CompassEffect.PRot))
        
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
            elif option == "lighting":
                if value == "true":
                    self.lighting = True
                else:
                    self.lighting = False

    # Shows subtitles at the bottom of the screen
    def showSubs(self):
        subFile = open("subs.txt", "r")
        subline = subFile.read()
        font = loader.loadFont("resources/fonts/Zccara.tff")
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

    def initObjects(self):
        self.jumogoro = Monster("Jumogoro", "spiderlady.egg", 0, 30, 5, 4, 4, 1.25, 0.1)
        self.jumogoro.anim("Walk", True)
        self.kappa = Monster("Kappa", "kappa.egg", 0, 10, 5, 5, 1.5, 1.25, 0.1)
        self.kappa.anim("Idle", True)
        self.cucumber = Item("Cucumber", "cucumber.egg", 10, 10, 5, 1, 1, 1, False)
        self.toilet = Item("Toilet", "toilet.egg", 20, 10, 5, 2, 1.5, 1.5, False)
        taskMgr.add(self.MonsterUpdate, 'MonsterUpdate-task')
        
    def MonsterUpdate(self, task):
        if self.jumogoro.node.getPos().getX() == 0:
            self.jumogoro.walkForward()
        if (round(self.jumogoro.node.getPos().getX()) == 20 and round(self.jumogoro.node.getPos().getY()) == 30):
            self.jumogoro.turn(90, False)
        if (round(self.jumogoro.node.getPos().getX()) == 27 and round(self.jumogoro.node.getPos().getY()) == 50):
            self.jumogoro.turn(180, False)
        if round(self.jumogoro.node.getPos().getX()) == -50:
            self.jumogoro.stop()
        return task.cont

    def initMusic(self):
        music = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
        music.setLoop(True)
        music.play()

    def togglePause(self):
        #used to toggle the pausing so the player can use the same button to pause and unpause
        if self.isPaused == True:
            self.isPaused = False
        elif self.isPaused == False:
            self.isPaused = True

    def PauseUpdate(self, task):
        #pausing task this will remove all tasks it needs to and then when the player
        #decides to unpause the task will add the tasks it removed back to the task manager

        if self.isPaused == True and self.alreadyRemoved == False:
            self.node.removeTasks()
            self.alreadyRemoved = True
        elif self.isPaused == False and self.alreadyRemoved == True: #needs to be changed so that the tasks are not added every time the task is called
            self.node.addTasks()
            self.alreadyRemoved = False
        elif self.isPaused == True and self.alreadyRemoved == True:
            return task.cont
        elif self.isPaused == False and self.alreadyRemoved == False:
            return task.cont

        return task.cont

game = MainGame()
game.run()
