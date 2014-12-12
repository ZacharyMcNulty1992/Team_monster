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

    def __init__(self, game, posX, posY, posZ, range, target, script, runOnce, refreshDelay):
        self.game = game
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.range = range
        self.script = script
        self.runOnce = runOnce
        self.refreshDelayMax = refreshDelay
        self.refreshDelay = 0
        taskMgr.add(self.proxCheck, 'proxCheck-task', extraArgs = [target], appendTask = True)
        if not runOnce:
            taskMgr.add(self.delayCountdown, 'delayCountdown-task')
    
    def proxCheck(self, target, task):
        if self.refreshDelay == 0:
            if fabs(target.getX() - self.posX) <= self.range and fabs(target.getY() - self.posY) <= self.range and fabs(target.getZ() - self.posZ) <= self.range:
                self.activate()
                if self.runOnce:
                    return task.done
                self.refreshDelay = self.refreshDelayMax
        return task.cont

    def delayCountdown(self, task):
        if self.refreshDelay > 0:
            self.refreshDelay = self.refreshDelay - 1
        else:
            self.refreshDelay = 0
        return task.cont

    def activate(self):
        self.game.runScript(self.script)