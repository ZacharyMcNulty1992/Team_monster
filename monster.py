#------------------------------------------#
# Class Name: Player
# Created By: Team Monster
# Last Updated: 10/7/14
# Updated By: Zach
# Notes: This class will be in charge of
# the monster and its ai
#------------------------------------------#

import direct.directbase.DirectStart
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

    def __init__(self):
        self.loadMonster()
        self.monsterCollision()

    def loadMonster(self): #need to test to see what model to load for what type of monster
        self.node = NodePath("resources/models/panda-model.egg")
        self.node.reparentTo(render)
        self.node.setPos(30, -9, 20)
        self.node.setScale(.5)


    def monsterCollision(self):
        #mn for monster node
        mn = CollisionNode('Monster')
        mn.addSolid(CollisionSphere(0,0,0,5))
        Solid = self.node.attachNewNode(mn)
        base.cTrav.addCollider(Solid, base.pusher)
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