'''
Created on Jan 30, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from puzzlaef.puzzle.models import Puzzle

class PictureThumb:
    
    def __init__(self, thumbLoc, pictureLoc, title):
        self.thumbLoc = thumbLoc
        self.pictureLoc = pictureLoc
        self.title = title
        
    def getAsString(self):
        return render_to_string("puzzle/pictureThumb.html", {'picture':self})
    
class PictureGrid():
    
    def __init__(self, pictureList):
        self.pictureList = pictureList
        
    def getGridAsString(self):
        pictureStrings = []
        for picture in self.pictureList:
            pictureStrings.append(picture.getAsString())
        return render_to_string("puzzle/pictureGrid.html", {'pictureSet':pictureStrings})
    
def make_new_puzzle(player1, player2):
	#TODO: Wissam
	puzzle = Puzzle()
	puzzle.player1 = player1
	puzzle.player2 = User.objects.get(username=player2)
	puzzle.save()
	return puzzle.id
    
def getThemes():
    list = Photo.objects.filter(isTheme=True)
    result = [PictureThumb(x.get_thumb_url(), x.get_url(), x.title) for x in list]
    return result


def set_puzzle_theme(puzzle, theme):
    puz = Puzzle.objects.get(id = puzzle)
    puz.title = theme
    puz.save()
    pass
    
def get_puzzle(puzzle_id):
    x = Puzzle.objects.get(id=puzzle_id)
    return x

def get_puzzle_pieces(puzzle_id):
    result = Puzzle.objects.filter(puzzle=puzzle_id)
    return result