from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from puzzlaef.puzzle.models import Puzzle, PuzzlePiece, Photo, Comment, CONSTRAINT_CHOICES
from puzzlaef.main.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

import random

class PictureThumb(Photo):
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

class PuzzleRenderer:
	def __init__(self, puzzle, request = None):
		self.request = request
		self.puzzle = puzzle
		self.pieces = PuzzlePiece.objects.filter(puzzle=puzzle).order_by('-time_modified')
		self.left_pieces = []
		self.right_pieces = []
	
	def insert_left_piece(self, piece):
		self.left_pieces.append(piece)
	
	def insert_right_piece(self, piece):
		self.right_pieces.append(piece)
		
	def get_rendered_to_string(self):
		right_pieces_name = "right-pieces-normal"
		left_pieces_name = "left-pieces-normal"
		upload_button_script = None
		if self.request: #This is one of the puzzles of this user
			upload_button_script = render_to_string("puzzle/uploadButton.html", 
												{"style":"margin: 10px auto 0;", 
												"id":"plus-button{0}".format(self.puzzle.id), "label":"Add Picture", 
												"action":"upload/makeMove", 
												"params": '{'+' "puzzle": "{0}" '.format(str(self.puzzle.id)) +'}',
												"onCompleteCallback":"onComplete: refreshPuzzle,"})
			if self.request.user == self.puzzle.turn:
				turn_piece = render_to_string("puzzle/yourTurnPiece.html", 
											context_instance=RequestContext(self.request, { "uploadButtonScript": upload_button_script, "puzzle_id": self.puzzle.id}))
				if self.request.user == self.puzzle.player1:
					self.insert_left_piece(turn_piece)
					right_pieces_name = "right-pieces-shifted"
					previous_is_left = False
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "one", previous_is_left
				else:
					self.insert_right_piece(turn_piece)
					left_pieces_name = "left-pieces-shifted"
					previous_is_left = True
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "two", previous_is_left, self.request.user, self.puzzle.player1
			else:
				turn_piece = render_to_string("puzzle/theirTurnPiece.html", {})
				if not self.request.user == self.puzzle.player1:
					self.insert_left_piece(turn_piece)
					right_pieces_name = "right-pieces-shifted"
					previous_is_left = False
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "three", previous_is_left
				else:
					self.insert_right_piece(turn_piece)
					left_pieces_name = "left-pieces-shifted"
					previous_is_left = True
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "four", previous_is_left
		else:
			if not self.puzzle.player1 == self.puzzle.turn:
				right_pieces_name = "right-pieces-shifted"
				previous_is_left = True
				print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "five", previous_is_left
			else:
				left_pieces_name = "left-pieces-shifted"
				previous_is_left = False
				print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "six", previous_is_left
		
		for piece in self.pieces:
				if previous_is_left:
					new_piece = render_to_string("puzzle/normalPiece.html", {"piece":piece, 'constraintClass':'left-constraint'})
					self.insert_left_piece(new_piece)
					previous_is_left = False
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "seven", previous_is_left
				else:
					new_piece = render_to_string("puzzle/normalPiece.html", {"piece":piece, 'constraintClass':'right-constraint'})
					self.insert_right_piece(new_piece)
					previous_is_left = True
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "eight", previous_is_left
					
		return render_to_string("puzzle/puzzle.html",  {"rightPiecesName": right_pieces_name,
														"leftPiecesName": left_pieces_name,
														"rightPieces": self.right_pieces,
														"leftPieces": self.left_pieces,
														"puzzle": self.puzzle,
														"request": self.request })
	
class PuzzlePrinter:
	def get_user_puzzle_as_string(self, puzzle, request):
		renderer = PuzzleRenderer(puzzle, request)
		return renderer.get_rendered_to_string()

	def get_foreign_puzzle_as_string(self, puzzle):
		renderer = PuzzleRenderer(puzzle)
		return renderer.get_rendered_to_string()
    	
def make_new_puzzle(player, photo):
	puzzle = Puzzle()
	puzzle.player1 = player
	puzzle.save()
	
	piece = PuzzlePiece(puzzle=puzzle, owner=player, photo=photo)
	piece.save()
	
	return puzzle.id

def add_new_comment (commenter, piece, comment):
	piece = get_puzzle_piece(piece);
	
	new_comment = Comment(piece=piece, text=comment, commenter=commenter)
	new_comment.save()

def join_puzzle(player, puzzle_id):
	puzzle = get_puzzle(puzzle_id)
	puzzle.player2 = player
	puzzle.turn = player
	puzzle.save()
	
	return puzzle
	
def generate_constraint(player = None, puzzle_id = None):
	index = random.randint(0, len(CONSTRAINT_CHOICES)-1)
	return CONSTRAINT_CHOICES[index]
	
def make_move_with_photo(player, puzzle_id, photo):
	puzzle = get_puzzle(puzzle_id)
	
	if(player == puzzle.turn):
		piece = PuzzlePiece(puzzle=puzzle, owner=player, photo=photo, constraint=generate_constraint())
		piece.save()
	
		if player == puzzle.player1:
			puzzle.turn = puzzle.player2
		else:
			puzzle.turn = puzzle.player1
		puzzle.save()
		
		return True
	else:
		return False
	
def fetch_all_open_puzzle_pieces(user):
	return PuzzlePiece.objects.filter(Q(puzzle__player2__isnull = True), ~Q(puzzle__player1 = user))

def fetch_latest_nonuser_puzzles(user):
	return Puzzle.objects.exclude(Q(player1 = user) | Q(player2 = user)).order_by('-time_modified')[0:2]

def fetch_latest_user_puzzles(user):
	try:
		return Puzzle.objects.filter(Q(player2__isnull = False), Q(player1 = user) | Q(player2 = user)).order_by('-time_modified')[0:2]
	except IndexError:
		return None

def fetch_all_latest_user_puzzles(user):
	return Puzzle.objects.filter(Q(player2__isnull = False), Q(player1 = user) | Q(player2 = user)).order_by('time_modified')
	
def fetch_user_puzzles(user):	
	return user.Puzzle_set().filter(player2__isnull=False).order_by('time_modified')
    
def getThemes():
    list = Photo.objects.filter(isTheme=True)
    return list

def set_puzzle_theme(reuest, puzzle, theme):
    puz = Puzzle.objects.get(id = puzzle)
    puz.title = theme
    puz.save()
    pass
    
def get_puzzle(puzzle_id):
    return Puzzle.objects.get(id=puzzle_id)

def get_puzzle_piece(piece_id):
    return PuzzlePiece.objects.get(id=piece_id)

def get_next_puzzle_piece(piece_id):
	currentPiece = PuzzlePiece.objects.get(id=piece_id)
	try:
		return currentPiece.get_previous_by_time_modified()
	except ObjectDoesNotExist:
		return None

def get_prev_puzzle_piece(piece_id):
	currentPiece = PuzzlePiece.objects.get(id=piece_id)
	try:
		return currentPiece.get_next_by_time_modified()
	except ObjectDoesNotExist:
		return None

def get_piece_comments(piece_id):
	piece = PuzzlePiece.objects.get(id=piece_id)
	return Comment.objects.filter(piece=piece).order_by('time_made')

def get_user_profile(user):
	return UserProfile.objects.get(user=user)

def get_puzzle_pieces(puzzle_id):
    return PuzzlePiece.objects.filter(puzzle=puzzle_id)