from graphics import *
import time
window = GraphWin('interface', 4000, 200)
input = ''
keys = {}
blackKeys = {1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40, 42, 45, 47, 49, 52, 54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85}
lights = {}

class Key(Rectangle):

	def __init__(self, pnt1, pnt2, light, color = "white", note = "B", text = "", keyNum = 0):
		super().__init__(pnt1, pnt2)
		self.KeyLight = light
		self.note = note
		self.keyNum = keyNum
		self.setFill(color)
		self.text = text
		
	def setNote(self, note):
		self.note = note

	def getNote(self):
		return self.note

	def getLight(self):
		return self.KeyLight

	def setLightColor(self, color):
		self.getLight().setColor(color)
	
	def draw(self,window):
		super().draw(window)
		self.getLight().draw(window)

class Light(Circle):
	
	def __init__(self, pnt, radi, color = "black"):
		super().__init__(pnt, radi)
		self.setColor(color)
	
	def setColor(self, color):
		try:
			self.setFill(color)
			self.color = color
		except:
			return -1
		
def setLightColor(num,color):
	global keys
	keys[num-21].setLightColor(color)

def GenKeys():
	global window, keys
	notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
	for i in range(87):
		tempi = i%12
		message = Text(Point((27 + i*14), 110), notes[tempi])
		message.setSize(7)
		light = Light(Point((27 + i*14), 50), 3)
		if(i in blackKeys):
			keys[i] = Key(Point((20 + i*14), 100), Point((34 + i*14), 60), light, "black", notes[tempi])
		else:
			keys[i] = Key(Point((20 + i*14), 100), Point((34 + i*14), 60), light, "white", notes[tempi])
		message.draw(window)
		keys[i].draw(window)
	
	window.checkKey()


def gameLoop():
	global window, keys
	for i in range(87):
		setLightColor(i+21,"green")
		time.sleep(0.125)
		setLightColor(i+21,"black")

def main():
	global window
	GenKeys()
	setLightColor(21, "red")
	gameLoop()
main()
