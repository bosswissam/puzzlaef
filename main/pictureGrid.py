from django.template.loader import render_to_string
from puzzlaef.main.pictureThumb import *

class PictureGrid():

	def __init__(self, pictureList):
		self.pictureList = pictureList
		
	def getGridAsString(self):
		pictureStrings = []
		for picture in self.pictureList:
			pictureStrings.append(picture.getAsString())
		return render_to_string("puzzle/pictureGrid.html", {'pictureSet':pictureStrings})