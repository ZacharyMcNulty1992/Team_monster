#-------------------------------------------#
# ClassName:
# Created By:
# Last Updated:
# Updated By:
# Note(s):
#-------------------------------------------#

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class Jorogumo(object):
    
    def __init__(self):

        self.joro = Actor("resources/models/spiderlady.egg")
        self.joro.setScale(1.75) 
        self.joro.setHpr(-90, 0, 0)
        self.joro.reparentTo(base.render)

        posInterval1 = self.joro.posInterval(13, Point3(0, -10, 0), startPos = Point3(0, 10, 0))
        posInterval2 = self.joro.posInterval(13, Point3(0, 10, 0), startPos = Point3(0, -10, 0))
        hprInterval1 = self.joro.hprInterval(3, Point3(180, 0, 0), startHpr = Point3(0, 0, 0))
        hprInterval2 = self.joro.hprInterval(3, Point3(0, 0, 0), startHpr = Point3(180, 0, 0))

        self.joroWalk = Sequence(posInterval1, hprInterval1, posInterval2, hprInterval2, name = "joroWalk")

        #self.joroWalk.loop()
