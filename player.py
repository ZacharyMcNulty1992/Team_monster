#------------------------------------------#
# Class Name: Player
# Created By: Team Monster
# Last Updated: 10/29/14
# Updated By: Kevin
# Notes: This class will be in charge of
# the player/camera "object"
#------------------------------------------#

from direct.showbase.ShowBase import ShowBase
import sys
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs


class Player(object):
    """
        Player is the main actor in the fps game
    """
    speed = .995
    run = False
    FORWARD = Vec3(0,1,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-10,0,0)
    RIGHT = Vec3(10,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    readyToJump = False
    canJump = False
    jump = 0
    cameraHeight = 5
    Light = False
    firstLightPass = False
    onscreen = False
    hasBeenRemoved = True
    coordsAdded = False
    Movement = False
    mouseOver = None
    clickable = False
    holding = False
    runSpeedApplied = False

    def __init__(self, controlStyle):
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls(controlStyle)
        if base.debug:
            self.initCoords()
        self.attachHand()
        #self.initCoords()
        # init mouse update task
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.jumpUpdate, 'jump-task')
        taskMgr.add(self.respawnUpdate, 'respawn-task')
        taskMgr.add(self.sprintUpdate, 'sprint-task')
        if base.debug:
            taskMgr.add(self.CoordsTask, 'Coords-task')

    def attachHand(self):
        self.hand = NodePath("Hand")
        self.hand.reparentTo(self.node)

    def initCoords(self):
        global playerX
        global playerY
        global playerZ
        playerX  = OnscreenText(pos = (0.8, 0.8), scale = (0.07), fg = (1.0, 1.0, 1.0, 1.0))
        playerY  = OnscreenText(pos = (0.8, 0.7), scale = (0.07), fg = (1.0, 1.0, 1.0, 1.0))
        playerZ = OnscreenText(pos = (0.8, 0.6), scale = (0.07), fg = (1.0, 1.0, 1.0, 1.0))

    def CoordsTask(self, task):
        if self.Movement == True:
            playerX.setText("")
            playerY.setText("")
            playerZ.setText("")
            return task.cont
        elif self.Movement == False:
            playerX.setText("X = " + str(self.node.getX()))
            playerY.setText("Y = " + str(self.node.getY()))
            playerZ.setText("Z = "+ str(self.node.getZ()))
            return task.cont
        return task.cont

    def initLight(self):
        self.slight = Spotlight('player light')
        self.slight.setScene(render)
        self.slight.setColor(VBase4(0.7, 0.7, 0.5, 1))
        self.slight.setAttenuation(Point3(0, 0, 0.00005))
        self.slight.getLens().setFov(90,70)
        self.slight.getLens().setNearFar(1, 5)
        self.slight.setShadowCaster(True, 1024, 1024)
        self.dlnp = self.node.attachNewNode(self.slight)
        self.dlnp.reparentTo(self.node)
        render.setLight(self.dlnp)
        self.node.setLight(self.dlnp)
        taskMgr.add(self.LightTask, 'light-task')
        
    def loadModel(self):
        """ make the nodepath for player """
        self.node = NodePath("resources/models/player1v2.egg")
        self.node.reparentTo(render)
        self.node.setPos(0,0,.5)
        self.node.setScale(1)

    def setUpCamera(self):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov(90)
        base.cam.node().setLens(pl)
        base.camera.setPos(0,0,self.cameraHeight)
        base.camera.reparentTo(self.node)

    def createCollisions(self):
        """ create a collision solid and ray for the player """
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node, base.drive.node())
        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

    # Attaches events to key presses and if the key is lifted
    def attachControls(self, controlStyle):
        
        # These are the tenative jump commands, will be taken out, being used for debugging
        base.accept("space", self.__setattr__, ["readyToJump",True])
        base.accept("space-up", self.__setattr__, ["readyToJump",False])
        #base.accept("f", self.toggleFlashLight)
        base.accept("`", self.keyRespawn)
        base.accept("shift", self.__setattr__, ["run", True])
        base.accept("shift-up", self.__setattr__, ["run", False])
        
        if (controlStyle == "wasd"):
            # WASD Controls
            # Move backwards / stop
            #base.accept("s", self.__setattr__, ["walk",self.STOP])
            base.accept("s", self.__setattr__, ["walk",self.BACK])
            base.accept("s-up", self.__setattr__, ["walk",self.STOP])

            # Move forward
            base.accept( "w" , self.__setattr__,["walk",self.FORWARD])
            base.accept( "w-up" , self.__setattr__,["walk",self.STOP] )

            # Move left
            base.accept( "a" , self.__setattr__,["strafe",self.LEFT])
            base.accept( "a-up" , self.__setattr__,["strafe",self.STOP] )

            # Move right
            base.accept( "d" , self.__setattr__,["strafe",self.RIGHT] )
            base.accept( "d-up" , self.__setattr__,["strafe",self.STOP] )
        else:
            # Arrow Controls
            # Move backwards / stop
            #base.accept("arrow_down", self.__setattr__, ["walk",self.STOP])
            base.accept("arrow_down", self.__setattr__, ["walk",self.BACK])
            base.accept("arrow_down-up", self.__setattr__, ["walk",self.STOP])

            # Move forward
            base.accept( "arrow_up" , self.__setattr__,["walk",self.FORWARD])
            base.accept( "arrow_up-up" , self.__setattr__,["walk",self.STOP] )

            # Move left
            base.accept( "arrow_left" , self.__setattr__,["strafe",self.LEFT])
            base.accept( "arrow_left-up" , self.__setattr__,["strafe",self.STOP] )

            # Move right
            base.accept( "arrow_right" , self.__setattr__,["strafe",self.RIGHT] )
            base.accept( "arrow_right-up" , self.__setattr__,["strafe",self.STOP] )

    def mouseUpdate(self,task):
        """ this task updates the mouse """
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
            self.dlnp.setHpr(0, (base.camera.getP() - (y - base.win.getYSize()/2)*0.1), 0)
            self.node.setH(self.node.getH() -  (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        if base.camera.getP() >= 90:
            base.camera.setP(90)
        if base.camera.getP() <= -90:
            base.camera.setP(-90)

        #This takes the camera and see if the player has hit anything
        self.hitSomething()
        return task.cont

    def moveUpdate(self,task):
        """ this task makes the player move """
        #move where the keys set it

        self.node.setPos(self.node,self.walk*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,self.strafe*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,(self.walk+self.strafe*globalClock.getDt())*self.speed)

        if self.walk == self.STOP:
            self.Movement = False
        else:
            self.Movement = True

        return task.cont

    def sprintUpdate(self,task):
        """used for adding speed when the shift button is pressed"""
        if self.run == True and self.runSpeedApplied == False:
            self.speed += .9
            self.runSpeedApplied = True
        elif self.run == False and self.runSpeedApplied == True:
            self.speed = .995
            self.runSpeedApplied = False
        elif self.run == True and self.runSpeedApplied == True:
            return task.cont
        return task.cont

    def toggleJump(self):
        if self.canJump:
            self.canJump = False
        else:
            self.canJump = True

    def togglePause(self):
        if self.isPaused:
            self.isPaused = False
        else:
            self.isPaused = True

    def jumpUpdate(self,task):
        """ this task simulates gravity and makes the player jump """
        # get the highest Z from the down casting ray

        highestZ = -500 # do not make this a positive value it will spawn the camera outside of the map
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "COLLISION":
                highestZ = z

        # gravity effects and jumps
        self.node.setZ(self.node.getZ()+self.jump*globalClock.getDt())
        self.jump -= 20*globalClock.getDt() #change the numerical value here to affect falling speed and height the higher the number the lower the player can jump
        if highestZ > self.node.getZ()-.3: #dont change this value if changed to .2 then you cant jump if changed to .4 you constantly jump or bounce
            self.jump = 0
            self.node.setZ(highestZ+.3) #dont change this value if changed to .2 then you cant jump if changed to .4 you constantly jump or bounce
        if not self.canJump:
            return task.cont
        if self.readyToJump:
                self.jump = 5 # This is the value for jump power.
        return task.cont

    def respawnUpdate(self, task):
        """ Will place player back at spawn if Z is below -10 """
        if self.node.getZ() <= -7:
            self.node.setPos(0,0,self.cameraHeight)
            base.camera.setPos(0,0,self.cameraHeight)
        return task.cont
      
    #By Pressing the '`' key the player will move back to the origin
    def keyRespawn(self):
        self.node.setPos(0,0,self.cameraHeight)
        base.camera.setPos(0,0,self.cameraHeight)

    def removeTasks(self):
        """used for pausing it removes the tasks that keep track of moving and looking around"""
        taskMgr.remove('mouse-task')
        taskMgr.remove('move-task')

    def addTasks(self):
        """used fro resuming play, it adds the tasks back to the task Manager"""
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')

    def toggleFlashLight(self):
        """used to toggle the flashlight when/if we need to do that"""
        if self.Light == False:
            self.Light = True
            self.firstLightPass = True
        elif self.Light == True:
            self.Light = False
            self.firstLightPass = False

    def LightTask(self, task):
        self.dlnp.setPos(0, 0, self.cameraHeight -1)
        if self.Light == True and self.firstLightPass == True:
            self.node.setLight(dlnp)
            self.firstLightPass = False
            return task.cont
        elif self.Light == False and self.firstLightPass == True:
            self.node.clearLight(dlnp)
            self.firstLightPass = False
            return task.cont
        elif self.Light == True and self.firstLightPass == False:
            return task.cont
        elif self.Light == False and self.firstLightPass == False:
            return task.cont
        return task.cont

    #This method will test what the camera is looking at.
    def hitSomething(self):
        #This method will continueously check for if you
        #are around anything interavtable (including clicking)
        global mouseOver
        if(base.mouseWatcherNode.hasMouse() == False):
            return
        mpos = base.mouseWatcherNode.getMouse()
        
        base.mPickRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        base.mPickerTraverser.traverse(base.render)
        
        if(base.mCollisionQue.getNumEntries() > 0):
            base.mCollisionQue.sortEntries()
            obj =  base.mCollisionQue.getEntry(0).getIntoNodePath()
            obj = obj.findNetTag('collectable')
            if not obj.isEmpty(): 
                self.mouseOver = "Left Click to PICK UP"
                base.looking.setText(str(self.getMouseOver()))
            else:
                self.mouseOver = ""
                base.looking.setText(str(self.getMouseOver()))
            obj = obj.findNetTag('interactable')
            if not obj.isEmpty():
                print "interactable"
            
    

    def getX(self):
        return self.node.getX()
        
    def getY(self):
        return self.node.getY()
        
    def getZ(self):
        return self.node.getZ()
        
    def getMouseOver(self):
        return self.mouseOver


