#-------------------------------------------#
# Class Name: Journal
# Created By: Team Monster
# Last Updated: 12/4/14
# Updated By: Joseph
# Note(s): This class is used to create and
# and manipulate the journal gui
#-------------------------------------------#

from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectButton import DirectButton
from pandac.PandaModules import TransparencyAttrib
from direct.task import Task

class Journal:

    # Pause variables
    isPaused = False
    alreadyRemoved = False

    # Variables which keep track of whether the journal is open
    # and where in the list of pages the user is currently viewing
    monsterBookOpen = False
    pages = []
    currentPage = 0

    # Will be used to manipulate the game's window properties
    # most notably the visibilty of the mouse
    gameWinProps = 0

    # Used for the frame and so the object knows
    # the size of the game window
    gui = 0
    winYSize = 0
    winXSize = 0

    # Buttons
    closeJournalButton = 0
    nextPage = 0
    prevPage = 0

    # Constructs the gui object with a simple frame and adds
    # all of the page images to the list of pages
    def __init__(self, winY, winX, wProps):
        self.gui = DirectFrame()
        self.winXSize = winX
        self.winYSize = winY
        self.gameWinProps = wProps
        for i in range (1, 4):
            self.pages.append('resources/GUI_Assets/Monster_Book/PNG_Files/pg' + str(i) + '.png')
        self.currentPage = self.pages[0]
        

    # Used to open the monster book if it isn't already open
    # will also make the cursor visable and give the user back control of it
    def openJournal(self):
        if self.monsterBookOpen == False:
            self.togglePause()
            self.createJournalButtons()
            self.monsterBookOpen = True
            self.gui['frameColor'] = (0, 0, 0, 1)
            self.gui['frameSize'] = (1, -1, self.winYSize, -self.winYSize)
            self.gui['image'] = self.currentPage
            self.gui['image_scale'] = (1.8, 1, 1)

    # Close the journal, hide the cursor and destroy all buttons
    def closeJournal(self):
        self.togglePause()
        self.monsterBookOpen = False
        self.gui['image_scale'] = (0, 0, 0)
        self.gui['frameColor'] = (0, 0, 0, 0)
        self.gui['text'] = ""
        self.closeJournalButton.destroy()
        self.nextPage.destroy()
        self.prevPage.destroy()

    # Creates all the buttons within the journal frame
    def createJournalButtons(self):
        self.closeJournalButton = DirectButton(image=('resources/GUI_Assets/Monster_Book/PNG_Files/close.png',
                                                'resources/GUI_Assets/Monster_Book/PNG_Files/closeOver.png',
                                                'resources/GUI_Assets/Monster_Book/PNG_Files/closeOver.png',
                                                'resources/GUI_Assets/Monster_Book/PNG_Files/closeOver.png'),
                                         pos=(1.45, 1, 0.85),
                                         image_scale=(0.2, 0.1, 0.1),
                                         relief=None,
                                         command=self.closeJournal)
        self.closeJournalButton.setTransparency(TransparencyAttrib.MAlpha)
        self.closeJournalButton.reparentTo(self.gui)
        self.nextPage = DirectButton(image=('resources/GUI_Assets/Monster_Book/PNG_Files/ArrowRight.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowRightOver.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowRightOver.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowRightOver.png'),
                                     pos=(1.5, 1, -0.93),
                                     image_scale=(0.1, 0.1, 0.1),
                                     relief=None,
                                     command=self.gotoNextPage)
        self.nextPage.setTransparency(TransparencyAttrib.MAlpha)
        self.nextPage.reparentTo(self.gui)
        self.prevPage = DirectButton(image=('resources/GUI_Assets/Monster_Book/PNG_Files/ArrowLeft.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowLeftOver.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowLeftOver.png',
                                            'resources/GUI_Assets/Monster_Book/PNG_Files/ArrowLeftOver.png'),
                                     pos=(-1.5, 1, -0.93),
                                     image_scale=(0.1, 0.1, 0.1),
                                     relief=None,
                                     command=self.gotoPrevPage)
        self.prevPage.setTransparency(TransparencyAttrib.MAlpha)
        self.prevPage.reparentTo(self.gui)

    # Button command: Will go to the next page in the book if
    # not already at the end of the list
    def gotoNextPage(self):
        if self.currentPage is self.pages[2]:
            self.currentPage = self.pages[2]
            self.gui['image'] = self.currentPage
            self.closeJournal()
            self.openJournal()
        else:
            self.currentPage = self.pages[self.pages.index(self.currentPage) + 1]
            self.gui['image'] = self.currentPage
            self.closeJournal()
            self.openJournal()

    # Button command: Will go back to the previous page if
    # not already on the first page
    def gotoPrevPage(self):
        if self.currentPage is self.pages[0]:
            self.currentPage = self.pages[0]
            self.gui['image'] = self.currentPage
            self.closeJournal()
            self.openJournal()
        else:
            self.currentPage = self.pages[self.pages.index(self.currentPage) - 1]
            self.gui['image'] = self.currentPage
            self.closeJournal()
            self.openJournal()

    # used to toggle the pausing so the player can use
    # the same button to pause and unpause
    def togglePause(self):
        if self.isPaused == True:
            self.gameWinProps.setCursorHidden(True)
            base.win.requestProperties(self.gameWinProps)
            self.isPaused = False
        elif self.isPaused == False:
            self.gameWinProps.setCursorHidden(False)
            base.win.requestProperties(self.gameWinProps)
            self.isPaused = True

