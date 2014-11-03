#------------------------------------------#
# Class Name: Monster
# Created By: Team Monster
# Last Updated: 11/02/14
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
    walking = False
    turning = False

    def __init__(self, name, model, posX, posY, posZ, height, width, scale, speed):
        self.name = name
        self.model = Actor("resources/models/" + model)
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.height = height
        self.width = width
        self.scale = scale
        self.speed = speed
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
        mn.addSolid(CollisionSphere(0, 0, self.height/2, self.width))
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
    
    def walkForward(self):
        if not self.walking:
            taskMgr.add(self.WalkForwardUpdate, 'walkforward-task')
            self.walking = True
    
    def stop(self):
        taskMgr.remove('walkforward-task')
        self.walking = False
    
    def turn(self, angle, clockwise):
        if not self.turning:
            if clockwise:
                taskMgr.add(self.TurnUpdateCW, 'turncwupdate-task', extraArgs = [angle], appendTask = True)
            else:
                taskMgr.add(self.TurnUpdateCCW, 'turnccwupdate-task', extraArgs = [angle], appendTask = True)
            self.turning = True
    
    def WalkForwardUpdate(self, task):
        self.node.setPos(self.node, self.speed, 0, 0)
        return task.cont
        
    def TurnUpdateCW(self, angle, task):
        self.node.setH(self.node.getH() - 1)
        if self.node.getH() == angle:
            self.turning = False
            return task.done
        else:
            return task.cont
    
    def TurnUpdateCCW(self, angle, task):
        self.node.setH(self.node.getH() + 1)
        if self.node.getH() == angle:
            self.turning = False
            return task.done
        else:
            return task.cont