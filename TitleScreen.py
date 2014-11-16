from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
 
class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
        self.initMusic()
        self.displayFont()
        
    def initMusic(self):
        music = base.loader.loadSfx("resources/music/LooseSpirits.ogg")
        music.setVolume(0.8)
        music.setLoop(True)
        music.play()
 
	def displayFont(self):
  		self.text = TextNode('New_Text')
        self.text.setText("There's supposed to be a file reader. Will recreate soon!")
        textNodePath = render2d.attachNewNode(self.text)
        textNodePath.setScale(0.07)
    	self.text.setAlign(TextNode.ABoxedCenter)
  		Zccara = loader.loadFont('resources/fonts/Zccara.ttf')
        self.text.setFont(Zccara)
        textNodePath.setPos(0, 0, -.60)
    	self.text.setWordwrap(20)
 		self.text.setAlign(self.text.ACenter)
app = MyApp()
app.run()