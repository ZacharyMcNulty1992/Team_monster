#------------------------------------------#
# Class Name: Item
# Created By: Team Monster
# Last Updated: 11/1/14
# Updated By: Kevin
# Notes: This class will be in charge of
# items and their behavior
#------------------------------------------#

#import direct.directbase.DirectStart
import sys
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs

class Item(object):

    def __init__(self, name, model, posX, posY, posZ, height, width, scale, defiesGravity, isCollectable, isInteractable):
        self.name = name
        self.model = Actor("resources/models/" + model)
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.height = height
        self.width = width
        self.scale = scale
	self.isCollectable = isCollectable
        self.loadItem()
        self.itemCollision()
        if not defiesGravity:
            taskMgr.add(self.GravityUpdate, 'gravity-task')

    def loadItem(self):
        self.node = NodePath("")
        self.node.reparentTo(base.render)
        self.model.reparentTo(self.node)
        self.node.setPos(self.posX, self.posY, self.posZ)
        self.node.setScale(self.scale)

    def itemCollision(self):
        #itn for item node
        itn = CollisionNode('Item')
	#itn.set_from_collide_mask(0)
        itn.addSolid(CollisionSphere(0, 0, self.height/2, self.width))
        Solid = self.node.attachNewNode(itn)
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
        Solid = self.node.attachNewNode(itn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(Solid, self.nodeGroundHandler)
        Solid = self.node.attachNewNode(itn)
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
