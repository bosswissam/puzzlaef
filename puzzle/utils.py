'''
Created on Jan 30, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from puzzlaef.puzzle.models import Puzzle, PuzzlePiece, Photo
from puzzlaef.main.utils import ResultUser, ResultPiece
from puzzlaef.main.models import UserProfile

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
    puzzle.turn = puzzle.player2
    puzzle.save()
	
    piece = PuzzlePiece(puzzle=puzzle)
    piece.save()

    return puzzle.id
	
def fetch_user_puzzles(user):
    list1 = set(Puzzle.objects.filter(player1=user))
    list2 = set(Puzzle.objects.filter(player2=user))
    result = list(list1.union(list2))
    pieceSetsOfPuzzles = {}
    for x in result:
	   pieceSetsOfPuzzles[x.id] = list(PuzzlePiece.objects.filter(puzzle=x)) 
    final = []
    for x in result:
        print pieceSetsOfPuzzles
        if (len(pieceSetsOfPuzzles[x.id]) and pieceSetsOfPuzzles[x.id][0] and pieceSetsOfPuzzles[x.id][0].photo1 and pieceSetsOfPuzzles[x.id][0].photo2):
			photo1 = pieceSetsOfPuzzles[x.id][0].photo1
			photo2 = pieceSetsOfPuzzles[x.id][0].photo2
        else:
			photo1 = None
			photo2 = None

        final.append(ResultPiece(x.id,
								photo1, 
								photo2,
								x.player1.username,
								x.player2.username,
								UserProfile.objects.get(user=x.player1).location,
								UserProfile.objects.get(user=x.player2).location))
	return final
    
def getThemes():
    list = Photo.objects.filter(isTheme=True)
    result = [PictureThumb(x.get_thumb_url(), x.get_url(), x.title) for x in list]
    return result


def set_puzzle_theme(reuest, puzzle, theme):
    puz = Puzzle.objects.get(id = puzzle)
    puz.title = theme
    puz.save()
    pass
    
def get_puzzle(puzzle_id):
    x = Puzzle.objects.get(id=puzzle_id)
    return x

def get_puzzle_pieces(puzzle_id):
    result = PuzzlePiece.objects.filter(puzzle=puzzle_id)
    return result