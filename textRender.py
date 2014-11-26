#------------------------------------------#
# Class Name: TextRender
# Created By: Team Monster
# Last Updated: 11/26/14
# Updated By: Kevin
# Notes: This class will be in charge of
# displaying text
#------------------------------------------#

#import direct.directbase.DirectStart
import sys
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from math import fabs

class TextRender(object):

    def __init__(self, filetext, cmd):
        self.text = TextNode('New_Text')
        self.text.setText(filetext)
        textNodePath = render2d.attachNewNode(self.text)
        textNodePath.setScale(0.07)
        self.text.setAlign(TextNode.ABoxedCenter)
        if cmd[2] == "normal":
            font = loader.loadFont("resources/fonts/CTS.ttf")
        elif cmd[2] == "garbled":
            font = loader.loadFont("resources/fonts/Zccara.ttf")
        self.text.setFont(font)
        textNodePath.setPos(float(cmd[3]), float(cmd[4]), float(cmd[5]))
        self.text.setWordwrap(int(cmd[6]))
        self.text.setAlign(self.text.ACenter)
        if cmd[7] != 0:
            self.count = int(cmd[7])
            taskMgr.add(self.countdown, 'countdown-task')

    def countdown(self, task):
        if self.count != 0:
            self.count = self.count - 1
            return task.cont
        else:
            self.stop()
            return task.done

    def stop(self):
        self.text.setText("")