#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 11/15/14
# Updated By: Joseph
# Note(s): This class will be used to run
# 100 Monsters, implementing other classes
#-------------------------------------------#

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import WindowProperties, Filename
import sys, os, math, datetime, Queue
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs
from player import Player
from monster import Monster
from item import Item
from trigger import ProxTrigger
from journal import Journal

class MainGame(ShowBase):

    # These are default settings in case they are not specified in the config file
    controlStyle = "wasd"
    fullscreen = False
    winXSize = 1024
    winYSize = 768
    debug = False
    lighting = True
    brightness = .5
    
    # Global Variables
    isPaused = False
    alreadyRemoved = False
    #monsterBookOpen = False
    looking = None
    scripts = {}
    sounds = []
    gui = 0
    winProps = 0

    def __init__(self):
        #Initilize Game Base
        ShowBase.__init__(self)
        # Input
        self.getControls()
        # Task
        taskMgr.add(self.update, 'updateWorld')        
        # Physics
        self.setup()
 
    def update(self, task):
        taskMgr.add(self.PauseUpdate, 'pause-task')
        #taskMgr.add(self.TimeUpdate, 'timer')
        return task.cont
    
    def getControls(self):
        if not os.path.isfile("settings.cfg"):
            cfgFile = open("settings.cfg", "w")
            cfgFile.close()
        else:
            cfgFile = open("settings.cfg", "r+")
        self.getSettings(cfgFile)
         # accepts for various tasks
        journalFrame = DirectFrame()
        journal = Journal(journalFrame, self.winYSize, -self.winYSize)

        base.accept("escape", sys.exit)
        base.accept("p", self.togglePause)
        base.accept("j", journal.toggleJournal)
        base.accept('mouse1', self.onMouseTask)
        base.accept('mouse3', self.dropObject)

    def windowProps(self):
    # sets up the window's properties
        # Creates the window properties
        self.winProps = WindowProperties()
        # Set the window's resolution
        self.winProps.setSize(self.winXSize, self.winYSize)
        # Sets the cursor so that it's hidden
        self.winProps.setCursorHidden(True)
        # Changes the window name
        self.winProps.setTitle("100 Monsters")
        # Sets the game so it's fullscreen
        self.winProps.setFullscreen(self.fullscreen)
        # Gives the set properties to the window
        base.win.requestProperties(self.winProps)
        # Disables the mouse from moving the camera (can still look around)
        base.disableMouse()

    '''
    def displayFont(self):
        self.text = TextNode('New_Text')
        self.text.setText("There's supposed to be a file reader. Will recreate soon!")
        textNodePath = render2d.attachNewNode(self.text)
        textNodePath.setScale(0.07)
        self.text.setAlign(TextNode.ABoxedCenter)
        Zccara = loader.loadFont('resources/fonts/Zccara.ttf')
        self.text.setFont(Zccara)
        textNodePath.setPos(0, 0, -.60)
        self.text.setWordwrap(20)
        self.text.setAlign(self.text.ACenter)
    '''

    #Mouse Collision
    def setupMouseCollision(self):
        self.mPickerTraverser = CollisionTraverser()
        self.mCollisionQue = CollisionHandlerQueue()

        #Creates a Collision Ray to detect Against
        self.mPickRay = CollisionRay()
        
        self.mPickRay.setOrigin(self.camera.getPos(self.render))
        self.mPickRay.setDirection(render.getRelativeVector(camera, Vec3(0,1,0)))

        self.mPickNode = CollisionNode('pickRay')
        self.mPickNode.addSolid(self.mPickRay)
	self.mPickNode.setFromCollideMask(BitMask32.bit(0))
        self.mPickNode.setIntoCollideMask(BitMask32.allOff())
        self.mPickNP = self.camera.attachNewNode(self.mPickNode)

        self.mPickNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.mPickerTraverser.addCollider(self.mPickNP,self.mCollisionQue)

    #Mouse Task
    def onMouseTask(self):
        #render.ls()
        entry = self.mCollisionQue.getEntry(0)
        pickedObj = entry.getIntoNodePath()
        pickedObj = pickedObj.findNetTag('collectable')
        if not pickedObj.isEmpty():
            if self.player.holding:
                self.drop(self.player.hand.getChild(0))
            pickedObj.reparentTo(self.player.hand)
	    pickedObj.getChild(1).stash()
	    
            pickedObj.setPos(1,1.5,3)
            self.player.holding = True
        

    def dropObject(self):
        if self.player.hand.getNumChildren() == 0:
            return
        else:
            self.drop(self.player.hand.getChild(0))

    def drop(self, child):     
        child.reparentTo(render)
        child.setPos(self.player.getX(), self.player.getY(), self.player.getZ())
	child.unstashAll()
        self.player.holding = False
	
    #Creates and Loads the Skybox
    def loadSkybox(self):
        self.skybox = loader.loadModel("resources/levels/skybox.egg")
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
            elif option == "brightness":
                self.brightness = float(value)

    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
	base.cQue = CollisionHandlerQueue()
        #for debugging purposes
        if self.debug:
            base.cTrav.showCollisions(render)

    def loadLevel(self):
	self.loadSkybox()

	#Loads the Collision Faces
        self.level = loader.loadModel("resources/levels/firstFloorCollision.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(False)
 
	#Loads the Level
	self.floor = loader.loadModel("resources/levels/firstFloor.egg")
	self.floor.reparentTo(self.level)
        
        # Lighting
        if self.lighting:
            alight = AmbientLight('alight')
            alight.setColor(VBase4(self.brightness, self.brightness, self.brightness, 1))
            alnp = render.attachNewNode(alight)
            
            render.setShaderAuto()
            render.clearLight()
            render.setLight(alnp)

    def initObjects(self):
        self.monsters = {}
        self.jumogoro = Monster("Jumogoro", "jorogumo.egg", 0, 30, 5, 4, 4, 1.25, 0.1)
        self.jumogoro.model.setTag('jumogoro', '1')
        self.jumogoro.anim("Walk", True)
        self.monsters["jumogoro"] = self.jumogoro
        self.kappa = Monster("Kappa", "kappa.egg", 0, 10, 5, 5, 1.5, 1.25, 0.1)
        self.kappa.model.setTag('kappa', '1')
        self.kappa.anim("Idle", True)
        self.monsters["kappa"] = self.kappa
        self.cucumber = Item("Cucumber", "cucumber.egg", 10, 10, 5, 1, 1, 1, False, True, True)
        #Mouse Tag
        self.cucumber.model.setTag('collectable','1')
        self.toilet = Item("Toilet", "toilet.egg", 20, 10, 5, 2, 1.5, 1.5, False, False, True)
        self.toilet.model.setTag('interactable','1')
        #self.door_test = Item("Door_Test", "door_test.egg", 0, 0, 6.0, 1,1,1,False, False, True)
        #self.toilet.model.setTag('interactable','2')
        self.jumotrigger = ProxTrigger(self, 0, 30, 5, 10, self.player, "jumostartmove", True)
        self.jumotrigger1 = ProxTrigger(self, 30, 25, 5, 5, self.monsters["jumogoro"], "jumoturn1", False)
        self.jumotrigger2 = ProxTrigger(self, 35, 50, 5, 5, self.monsters["jumogoro"], "jumoturn1", False)
        self.jumotrigger3 = ProxTrigger(self, -30, 55, 5, 5, self.monsters["jumogoro"], "jumoturn1", False)
        self.jumotrigger4 = ProxTrigger(self, -35, 30, 5, 5, self.monsters["jumogoro"], "jumoturn1", False)

    # Initializes music
    def initMusic(self):
        music = base.loader.loadSfx("resources/music/background/CreaturesDark.mp3")
	music.setVolume(0.25)
        music.setLoop(True)
        music.play()

    # Pausing is now handled by the gui object, the task will call
    # that object's toggle pause method
    def toggleJournal(self):
        
	""" set visiblity for monster book, currently rough """
        if self.monsterBookOpen == True:
            self.monsterBookOpen = False
            Journal(False, self.winYSize, -self.winYSize)	    
        else:
            self.monsterBookOpen = True
	    self.journal(True, self.winYSize, -self.winYSize)

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
            self.player.removeTasks()
            self.alreadyRemoved = True
        elif self.isPaused == False and self.alreadyRemoved == True: #needs to be changed so that the tasks are not added every time the task is called
            self.player.addTasks()
            self.alreadyRemoved = False
            base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2) 
	    
        elif self.isPaused == True and self.alreadyRemoved == True:
            return task.cont
        elif self.isPaused == False and self.alreadyRemoved == False:
            return task.cont
        return task.cont
      
    def TimeUpdate(self, task):
	#A Horrible way to have the text go away at the begining... but it works
	secondsTime = int(task.time)
	if secondsTime == 10:
	    self.text.setText("")
	
	return task.cont

    def initScripts(self):
        path = "./resources/scripts/"
        dir = os.listdir(path)
        # First pass reads the scripts file, turning each script into a queue of commands and
        # places each of these into a dictionary keyed by script names
        for filename in dir:
            if filename.endswith(".sc"):
                state = "start"
                file = open(path + filename)
                for line in file:
                    if state == "start":
                        if line == '\n':
                            continue
                        keyword, name = line.split(" ", 2)
                        name = name[:-2]
                        scriptBody = []
                        state = "read"
                    elif state == "read":
                        cmd = line.split(" ")
                        # Just look at this next line. Is this not the coolest thing ever?
                        # (If you're wondering, it takes the last element of the tuple
                        # cmd and then strips off the last character from it so we drop the
                        # '\n' from end of the line)
                        cmd[-1] = cmd[-1][:-1]
                        if cmd[0] == "end":
                            self.scripts[name] = scriptBody
                            state = "start"
                        else:
                            scriptBody.append(cmd)
    
    # Runs a selected script (Key is the string that names the script)
    def runScript(self, key):
        script = self.scripts[key]
        for cmd in self.scripts[key]:
            cmdType = cmd[0]
            if cmdType == "walkforward":
                print cmd[1] + " walking forward"
                self.monsters[cmd[1]].walkForward()
            elif cmdType == "stop":
                print cmd[1] + " stopping"
                self.monsters[cmd[1]].walkForward()
            elif cmdType == "turn":
                if self.monsters[cmd[1]].turning:
                    break
                print cmd[1] + " turning " + cmd[2] + " degrees " + cmd[3]
                if cmd[3] == "cw":
                    self.monsters[cmd[1]].turn(int(cmd[2]), True)
                elif cmd[3] == "ccw":
                    self.monsters[cmd[1]].turn(int(cmd[2]), False)
            elif cmdType == "anim":
                print cmd[1] + " changing animation to " + cmd[2]
                if cmd[3] == "loop":
                    self.monsters[cmd[1]].anim(cmd[2], True)
                elif cmd[3] == "noloop":
                    self.monsters[cmd[1]].anim(cmd[2], True)
            elif cmdType == "print":
                print "Printing " + cmd[1] + " with " + cmd[2] + " font for " + cmd[7] + " seconds"
                path = "./resources/text/"
                dir = os.listdir(path)
                for filename in dir:
                    if filename == cmd[1]:
                        filetext = open(path + filename, "r").read()
                        self.text = TextNode('New_Text')
                        self.text.setText(filetext)
                        textNodePath = render2d.attachNewNode(self.text)
                        textNodePath.setScale(0.07)
                        self.text.setAlign(TextNode.ABoxedCenter)
                        if cmd[2] == "normal":
                            font = loader.loadFont("resources/fonts/CTS.ttf")
                        elif cmd[2] == "garbled":
                            font = loader.loadFont("resources/fonts/Zccara.ttf")
                        self.text.setFont(font)
                        textNodePath.setPos(float(cmd[3]), float(cmd[4]), float(cmd[5]))
                        self.text.setWordwrap(int(cmd[6]))
                        self.text.setAlign(self.text.ACenter)

    def setup(self):
        # Collision
        self.initCollision()
        # Level
        self.loadLevel()
        # Player
        self.player = Player(self.controlStyle)
        # Player's Flashlight
        if self.lighting:
            self.player.initLight()
        if self.debug:
            base.setFrameRateMeter(True)
        self.windowProps()
        if self.debug:
            self.player.toggleJump()
        
        # Initialize Objects and scripts
        self.initScripts()
        self.initObjects()
        self.initMusic()
        
        self.runScript("initprint")
        
        self.looking = OnscreenText(pos = (-0.6, 0.8), scale = (0.04), fg = (1.0, 1.0, 1.0, 1.0))
        # Add Mouse Collision to our world
        self.setupMouseCollision()

        # Displays text on the bottom of the screen
        # self.displayFont()


game = MainGame()
game.run()
