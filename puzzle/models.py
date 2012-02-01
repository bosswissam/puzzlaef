from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from os.path import join
from tempfile import *
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from puzzlaef.settings import *

import datetime
import django.core.files.uploadhandler
import os
import time
import zipfile

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

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.user.username), '' + time.strftime("%Y-%m-%d-") + slugify(split(filename,'.')[0])+split(filename,'.')[1])

class Photo(models.Model):
    title = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
    isTheme = models.BooleanField(default = False);
    title_slug = models.SlugField(help_text=('A "slug" is a unique URL-friendly title for an object.'))
    image = models.ImageField(upload_to=get_image_path, height_field='height', width_field='width')
    user = models.ForeignKey(User, related_name = "user")

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        self.im_resize()
        
        im = Image.open(self.image.path)
        self.image.name = slugify(self.image.name)
        im.thumbnail((250,250), Image.ANTIALIAS)

        path, fnext = os.path.split(self.image.name)
        fn, ext = os.path.splitext(fnext)
        thumb_path = join(MEDIA_ROOT, path, 'thumbnails/')
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path)
        im.save(thumb_path + fn + '-thumb' + ext, 'JPEG')
        self.thumbLoc = self.get_thumb_url()
        self.pictureLoc = self.get_url()

    def im_resize(self):
        new_image = Image.open(self.image.path)
        new_image.thumbnail((700, 500), Image.ANTIALIAS)
        os.remove(self.image.path)
        new_image.save(self.image.path)
        
    def get_thumb(self):
        path, fnext = os.path.split(self.image.name)
        fn, ext = os.path.splitext(fnext)
        thumb_path = join(path, 'thumbnails/')
        return thumb_path + fn + '-thumb' + ext

    def get_thumb_url(self):
        return join(MEDIA_URL, self.get_thumb())

    def get_url(self):
        return join(MEDIA_URL, self.image.name)
            
    def delete(self):
        os.remove(self.image.path)
        os.remove(join(MEDIA_ROOT, self.get_thumb()))
        super(Photo,self).delete()
        
    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
    def getAsString(self):
        return render_to_string("puzzle/pictureThumb.html", {'picture':self})
class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    player1 = models.ForeignKey(User, related_name = "palyer 1")
    player2 = models.ForeignKey(User, related_name = "player 2")
    turn = models.ForeignKey(User, related_name = "player turn")
    theme_picture = models.ForeignKey(Photo, related_name = "theme photo", null = True)

class PuzzlePiece(models.Model):
    helper = models.ForeignKey(User, null=True)
    puzzle = models.ForeignKey(Puzzle, related_name="puzzle")
    photo1 = models.ForeignKey(Photo, related_name ="photo 1", null = True)
    photo2 = models.ForeignKey(Photo, related_name ="photo 2", null = True)
    needs_help = models.BooleanField()