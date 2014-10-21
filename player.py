#------------------------------------------#
# Class Name: Player
# Created By: Team Monster
# Last Updated: 10/7/14
# Updated By: Rachael
# Notes: This class will be in charge of
# the player/camera "object"
#------------------------------------------#

#import direct.directbase.DirectStart
import sys
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs

class Player(object):
    """
        Player is the main actor in the fps game
    """
    speed = .75
    FORWARD = Vec3(0,1,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-10,0,0)
    RIGHT = Vec3(10,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    readyToJump = False
    jump = 0

    def __init__(self, controlStyle):
	
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls(controlStyle)
        # init mouse update task
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.jumpUpdate, 'jump-task')

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
        base.camera.setPos(0,0,3)
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
        
        if (controlStyle == "wasd"):
            # WASD Controls
            # Move backwards / stop
            base.accept("s", self.__setattr__, ["walk",self.STOP])
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
            base.accept("arrow_down", self.__setattr__, ["walk",self.STOP])
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
            self.node.setH(self.node.getH() -  (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        if base.camera.getP() >= 90:
            base.camera.setP(90)
        if base.camera.getP() <= -90:
            base.camera.setP(-90)
        return task.cont

    def moveUpdate(self,task):
        """ this task makes the player move """
        #move where the keys set it
        self.node.setPos(self.node,self.walk*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,self.strafe*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,(self.walk+self.strafe*globalClock.getDt())*self.speed)
        return task.cont

    def jumpUpdate(self,task):
        """ this task simulates gravity and makes the player jump """
        # get the highest Z from the down casting ray

        highestZ = -500 # do not make this a positive value it will spawn the camera outside of the map
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Floor":
                highestZ = z

        # gravity effects and jumps
        self.node.setZ(self.node.getZ()+self.jump*globalClock.getDt())
        self.jump -= 20*globalClock.getDt() #change the numerical value here to affect falling speed and height the higher the number the lower the player can jump
        if highestZ > self.node.getZ()-.3: #dont change this value if changed to .2 then you cant jump if changed to .4 you constantly jump or bounce
            self.jump = 0
            self.node.setZ(highestZ+.3) #dont change this value if changed to .2 then you cant jump if changed to .4 you constantly jump or bounce
        if self.readyToJump:
                self.jump = 5 # This is the value for jump power.
        return task.cont

