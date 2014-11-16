#------------------------------------------#
# Class Name: Journal
# Created By: Team Monster
# Last Updated by: Rachael
# Notes: This is the monster book object
#------------------------------------------#

#from direct.gui.DirectFrame import DirectFrame
#from direct.showbase import DirectObject

class Journal(object):
 
    #global self.journal
    #journal = base.DirectFrame()   
    journalPages = [2, 3, 9, 11]
    currentPos = 0
    bookOpen = False

    def __init__(self, journalFrame,  winYSize1, winYSize2):
	
	self.winYSize1 = winYSize1
	self.winYSize2 = winYSize2
	self.journal = journalFrame

	#base.accept('j', self.toggleJournal)

    def toggleJournal(self):
        
	if self.bookOpen == False:
	    self.bookOpen = True
	    self.journal['frameSize'] = (1, 1, 1, 1)
	    currentPage = 'resources/pages/' + str(self.journalPages[self.currentPos]) + '.png'
	    self.journal['image'] = currentPage.translate(None, ' ')
	else:
 	    self.bookOpen = False
	    self.journal['image_scale'] = (0, 0, 0)
	    self.journal['frameColor'] = (0, 0, 0, 0)
	    self.journal['text'] = ""
        self.currentPos = 0

   #def movePos(self):