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
from textRender import TextRender

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
    numSoundChannels = 8

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
        #base.accept('mouse1', self.onMouseTask)
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
        self.skybox.setScale(300.0,200.0,75.0)
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
        self.items = {}
        self.triggers = {}
        self.monster_book = Item("Monster_Book", "monster_book", -66, -17, .25, 1, 1, 1, False, False, False)
        #self.door_test = Item("Door_Test", "door_test.egg", 0, 0, 6.0, 1,1,1,False, False, True)
        #self.toilet.model.setTag('interactable','2')

    # Initializes music and sound
    def initSound(self):
        self.music = base.loader.loadSfx("resources/music/background/CreaturesDark.ogg")
        self.music.setVolume(0.25)
        self.music.setLoop(True)
        self.music.play()
        # This initializes the sound system with a number of channels.
        # Each channel is a dict containing sound effects, which
        # can be manipulated with the scripting language.
        self.soundSystem = []
        for i in range(0, self.numSoundChannels):
            channel = {}
            self.soundSystem.append(channel)

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
                if cmd[1] not in self.monsters:
                    print cmd[1] + " does not currently exist."
                else:
                    print cmd[1] + " walking forward"
                    self.monsters[cmd[1]].walkForward()
            elif cmdType == "stop":
                if cmd[1] not in self.monsters:
                    print cmd[1] + " does not currently exist."
                else:
                    print cmd[1] + " stopping"
                    self.monsters[cmd[1]].walkForward()
            elif cmdType == "turn":
                if cmd[1] not in self.monsters:
                    print cmd[1] + " does not currently exist."
                else:
                    if self.monsters[cmd[1]].turning:
                        break
                    print cmd[1] + " turning " + cmd[2] + " degrees " + cmd[3]
                    if cmd[3] == "cw":
                        self.monsters[cmd[1]].turn(int(cmd[2]), True)
                    elif cmd[3] == "ccw":
                        self.monsters[cmd[1]].turn(int(cmd[2]), False)
            elif cmdType == "anim":
                if cmd[1] not in self.monsters:
                    print cmd[1] + " does not currently exist."
                else:
                    print cmd[1] + " changing animation to " + cmd[2]
                    if cmd[3] == "loop":
                        self.monsters[cmd[1]].anim(cmd[2], True)
                    elif cmd[3] == "noloop":
                        self.monsters[cmd[1]].anim(cmd[2], True)
            elif cmdType == "despawn":
                if cmd[1] in self.monsters:
                    print "Despawning " + cmd[1]
                    self.monsters[cmd[1]].model.delete()
                    del self.monsters[cmd[1]]
                else:
                    print cmd[1] + " does not currently exist."
            elif cmdType == "spawnmonster":
                print "Spawning monster " + cmd[1] + " with model filename " + cmd[2] + " at x = " + cmd[3] + " y = " + cmd[4] + " z = " + cmd[5] + " with height " + cmd[6] + " and width " + cmd[7] + " and scale " + cmd[8] + " and speed " + cmd[9]
                monster = Monster(cmd[1], cmd[2], float(cmd[3]), float(cmd[4]), float(cmd[5]), float(cmd[6]), float(cmd[7]), float(cmd[8]), float(cmd[9]))
                monster.model.setTag(cmd[1], '1')
                self.monsters[cmd[1]] = monster
            elif cmdType == "spawnitem":
                print "Spawning item " + cmd[1] + " with model filename " + cmd[2] + " x = " + cmd[3] + " y = " + cmd[4] + " z = " + cmd[5] + " height of " + cmd[6] + " width of " + cmd[7] + " scale of " + cmd[8] + " defiesGravity set to " + cmd[9] + " isCollectable set to " + cmd[10] + " isInteractable set to " + cmd[11]
                if cmd[9] == "true":
                    gravity = True
                else:
                    gravity = False
                if cmd[10] == "true":
                    collect = True
                else:
                    collect = False
                if cmd[11] == "true":
                    interact = True
                else:
                    interact = False
                item = Item(cmd[1], cmd[2], float(cmd[3]), float(cmd[4]), float(cmd[5]), float(cmd[6]), float(cmd[7]), float(cmd[8]), gravity, collect, interact)
                if collect:
                    item.model.setTag('collectable', '1')
                elif interact:
                    item.model.setTag('interactable', '1')
                else:
                    item.model.setTag(cmd[1], '1')
            elif cmdType == "spawnproxtrigger":
                print "Spawning trigger for script " + cmd[1] + " at x = " + cmd[2] + " y = " + cmd[3] + " z = " + cmd[4] + " with range " + cmd[5] + " with target " + cmd[6] + " of type " + cmd[7] + " running " + cmd[8] + " with a refresh delay of " + cmd[9]
                runOnce = False
                if cmd[8] == "runonce":
                    runOnce = True
                if cmd[7] == "monster":
                    target = self.monsters[cmd[6]]
                if cmd[7] == "item":
                    target = self.items[cmd[6]]
                if cmd[7] == "player":
                    target = self.player
                trigger = ProxTrigger(self, float(cmd[2]), float(cmd[3]), float(cmd[4]), float(cmd[5]), target, cmd[1], runOnce, int(cmd[9]))
                self.triggers[cmd[1]] = trigger
            elif cmdType == "print":
                print "Printing " + cmd[1] + " with " + cmd[2] + " font for " + cmd[7] + " tics"
                path = "./resources/text/"
                dir = os.listdir(path)
                # This parses the text file supplied and then maps it to a textNode, which is then displayed
                # for an amount of time
                for filename in dir:
                    if filename == cmd[1]:
                        textRender = TextRender(open(path + filename, "r").read(), cmd)
                        
            elif cmdType == "playsound":
                print "Playing sound " + cmd[1] + " set to volume " + cmd[2] + " on channel " + cmd[3] + " on " + cmd[4]
                channel = self.soundSystem[int(cmd[3])]
                # If the channel already has this sound, stop it if it's playing and then play it
                if cmd[1] in channel:
                    channel[cmd[1]].stop()
                    channel[cmd[1]].setVolume(float(cmd[2]))
                    if cmd[4] == "loop":
                        channel[cmd[1]].setLoop(True)
                    elif cmd[4] == "noloop":
                        channel[cmd[1]].setLoop(False)
                    channel[cmd[1]].play()
                # Otherwise, create a new sound object and plop it in the channel
                else:
                    sound = base.loader.loadSfx("resources/music/soundEffects/" + cmd[1])
                    sound.setVolume(float(cmd[2]))
                    if cmd[4] == "loop":
                        sound.setLoop(True)
                    elif cmd[4] == "noloop":
                        sound.setLoop(False)
                    sound.play()
                    channel[cmd[1]] = sound
            elif cmdType == "changemusic":
                print "Changing music to " + cmd[1] + " set to volume " + cmd[2]
                self.music.stop()
                self.music = base.loader.loadSfx("resources/music/background/" + cmd[1])
                self.music.setVolume(float(cmd[2]))
                self.music.setLoop(True)
                self.music.play()

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
        self.initSound()
        
        self.runScript("init")
        
        self.looking = OnscreenText(pos = (-0.6, 0.8), scale = (0.04), fg = (1.0, 1.0, 1.0, 1.0))
        # Add Mouse Collision to our world
        self.setupMouseCollision()

        # Displays text on the bottom of the screen
        # self.displayFont()


game = MainGame()
game.run()
