from django.template.loader import render_to_string

class PictureThumb:
	
	def __init__(self, thumbLoc, pictureLoc, title):
		self.thumbLoc = thumbLoc
		self.pictureLoc = pictureLoc
		self.title = title
		
	def getAsString(self):
		return render_to_string("puzzle/pictureThumb.html", {'picture':self})