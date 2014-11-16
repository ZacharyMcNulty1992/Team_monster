#-------------------------------------------#
# Class Name: 100Monsters
# Created By: Team Monster
# Last Updated: 11/15/14
# Updated By: Joseph
# Note(s): This class will be used to create,
# maintain, and manipulate all guis
#-------------------------------------------#

from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectButton
from direct.task import Task

class GUI:

    # Pause variables
    isPaused = False
    alreadyRemoved = False

    # Menus are closed when the object is created
    monsterBookOpen = False
    pauseMenuOpen = False

    # Will be used to manipulate the game's window properties
    # most notably the visibilty of the mouse
    gameWinProps = 0

    # Used for the frame and so the object knows
    # the size of the game window
    gui = 0
    winYSize = 0
    winXSize = 0

    # Constructs the gui object with a simply frame
    def __init__(self, winY, winX, wProps):
        self.gui = DirectFrame()
        self.winXSize = winX
        self.winYSize = winY
        self.gameWinProps = wProps

    # Used to open and close the monster book, will play a
    # sound when the method is called, as well as pause the camera
    # and make the mouse visible
    def toggleMonsterBook(self, openSound, closeSound):
        """ set visiblity for monster book, currently rough """
        if self.monsterBookOpen == True:
            self.togglePause()
            self.monsterBookOpen = False
            closeSound.play()
            self.gui['image_scale'] = (0, 0, 0)
            self.gui['frameColor'] = (0, 0, 0, 0)
            self.gui['text'] = ""
        else:
            self.togglePause()
            self.monsterBookOpen = True
            openSound.play()
            self.gui['frameColor'] = (0, 0, 0, 1)
            self.gui['frameSize'] = (1, -1, self.winYSize, -self.winYSize)
            self.gui['image'] = 'resources/GUI_Assets/Monster_Book/PNG_Files/Book.png'
            self.gui['image_scale'] = (1.9, 1, 1)
            self.gui['text'] = "Monster Book"
            self.gui['text_fg'] = (20, 0, 0, 1)
            self.gui['text_pos'] = (-1, 0.6)
            self.gui['text_scale'] = (0.2, 0.2)

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

