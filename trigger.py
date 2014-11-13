#------------------------------------------#
# Class Name: Trigger
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

class ProxTrigger(object):

    def __init__(self, game, posX, posY, posZ, range, target, script, runOnce):
        self.game = game
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.range = range
        self.script = script
        self.runOnce = runOnce
        taskMgr.add(self.proxCheck, 'proxCheck-task', extraArgs = [target], appendTask = True)
    
    def proxCheck(self, target, task):
        if fabs(target.getX() - self.posX) <= self.range and fabs(target.getY() - self.posY) <= self.range and fabs(target.getZ() - self.posZ) <= self.range:
            self.activate()
            if self.runOnce:
                return task.done
        return task.cont

    def activate(self):
        self.game.runScript(self.script)