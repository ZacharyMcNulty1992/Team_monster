#------------------------------------------#
# Class Name: Player
# Created By: Team Monster
# Last Updated: 10/21/14
# Updated By: Kevin
# Notes: This class will be in charge of
# the monster and its ai
#------------------------------------------#

#import direct.directbase.DirectStart
import sys
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs

class Monster(object):
    #copied from player class may need to change
    speed = .75
    FORWARD = Vec3(0,1,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-9,0,0)
    RIGHT = Vec3(9,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP

    def __init__(self, name, model, posX, posY, posZ, collisionSize, scale):
        self.name = name
        self.model = Actor("resources/models/" + model)
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.collisionSize = collisionSize
        self.scale = scale
        self.loadMonster()
        self.monsterCollision()
        taskMgr.add(self.GravityUpdate, 'gravity-task')

    def loadMonster(self): #need to test to see what model to load for what type of monster
        self.node = NodePath("")
        self.node.reparentTo(base.render)
        self.model.reparentTo(self.node)
        self.node.setPos(self.posX, self.posY, self.posZ)
        self.node.setScale(self.scale)

    def monsterCollision(self):
        #mn for monster node
        mn = CollisionNode('Monster')
        mn.addSolid(CollisionSphere(0, 0, 0, self.collisionSize))
        Solid = self.node.attachNewNode(mn)
        #base.cTrav.addCollider(Solid, base.pusher)
        base.pusher.addCollider(Solid, self.node, base.drive.node())

        #ray for monster
        ray = CollisionRay()
        ray.setOrigin(0, 0, -2)
        ray.setDirection(0, 0, -1)
        mn = CollisionNode('monsterRay')
        mn.addSolid(ray)
        mn.setFromCollideMask(BitMask32.bit(0))
        mn.setIntoCollideMask(BitMask32.allOff())
        Solid = self.node.attachNewNode(mn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(Solid, self.nodeGroundHandler)
        Solid = self.node.attachNewNode(mn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(Solid, self.nodeGroundHandler)

    def GravityUpdate(self, task):
        highZ = -500 # do not make this a positive value it will spawn the camera outside of the map
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highZ and entry.getIntoNode().getName() == "Floor":
                highZ = z
            # gravity effects and jumps
        self.node.setZ(self.node.getZ()*globalClock.getDt())
        return task.cont
    
    def anim(self, anim, loop):
        if loop:
            self.model.loop(anim)
        else:
            self.model.play(anim)
    