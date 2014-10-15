##------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 10/7/14
# Updated By: Rachael
# Note(s): This class will be used to run
# 100 Monsters, implementing other classes
#------------------------------------------#

import direct.directbase.DirectStart
import sys
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs
from player import Player
from monster import Monster

class Monsters(object):

    def __init__(self):
        
        base.accept("escape", sys.exit)
        base.disableMouse()

        self.initCollision()
        self.loadLevel()
        self.initPlayer()

        #used for debugging
        self.initMonster()
        self.initMusic()

    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        #for debugging purposes
        base.cTrav.showCollisions(render)

    def loadLevel(self):
        self.level = loader.loadModel("resources/levels/DemoRoomv3.egg")
        self.level.reparentTo(render)
        self.level.setTwoSided(True)

    def initPlayer(self):
        self.node = Player()

    def initMonster(self):
        self.node = Monster()

    def initMusic(self):
        music = base.loader.loadSfx("resources/music/Loose Spirits.ogg")
        music.play()
        
Monsters()
run()
