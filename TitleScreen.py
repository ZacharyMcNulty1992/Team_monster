from direct.showbase.ShowBase import ShowBase
from direct.directbase import DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode
from direct.gui.DirectFrame import DirectFrame


 
class TitleScreen:

	startPressed = False
 	screen = 0
 	b = 0
 	
    #This sets the size of the screen
def __init__(self, xSize, ySize):
    self.screen = DirectFrame(frameSize=(xSize/2, xSize/2, ySize/2, ySize/2),	frameColor=(0, 0, 0, 1))
    #This plays the music
    self.initMusic()
    #This Creates a button
    self.b = DirectButton(text=("Click me"), scale=.1)
    b['command'] = self.buttonClicked
    
	# Font Header
    self.text = TextNode('New_Text')
    self.text.setText("100 Monsters")
    textNodePath = render2d.attachNewNode(self.text)
    textNodePath.setScale(0.07)
    self.text.setAlign(TextNode.ABoxedCenter)
    Zccara = loader.loadFont('resources/fonts/CTS.ttf')
    self.text.setFont(Zccara)
    textNodePath.setPos(0, 0, .60)
    self.text.setWordwrap(20)
    self.text.setAlign(self.text.ACenter)
