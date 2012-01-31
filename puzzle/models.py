from django.contrib.auth.models import User
from django.db import models
try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError('Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')

# Create your models here.
#class Puzzle:
#    
#    admin = models.ForeignKey(Member, help_text = 'Administrator of this event')

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = "photos/")
    uploader = models.ForeignKey(User)
    title_slug = models.SlugField(help_text=('A "slug" is a unique URL-friendly title for an object.'))


class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    player1 = models.ForeignKey(User, related_name = "palyer 1")
    player2 = models.ForeignKey(User, related_name = "player 2")
    theme_picture = Photo()

class PuzzlePiece(models.Model):
    helper = models.ForeignKey(User, null=True)
    puzzle = models.ForeignKey(Puzzle)
    photo1 = Photo()
    photo2 = Photo()