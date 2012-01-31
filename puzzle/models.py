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

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.user.username), '' + time.strftime("%Y-%m-%d-") + filename)

class Photo(models.Model):
    title = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
    isTheme = models.BooleanField();
    title_slug = models.SlugField(help_text=('A "slug" is a unique URL-friendly title for an object.'))
    image = models.ImageField(upload_to=get_image_path, height_field='height', width_field='width')
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        if(self.resize=='resize'):
            self.im_resize()
        
        im = Image.open(self.image.path)
        im.thumbnail((250,250), Image.ANTIALIAS)

        path, fnext = os.path.split(self.image.name)
        fn, ext = os.path.splitext(fnext)
        thumb_path = join(MEDIA_ROOT, path, 'thumbnails/')
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path)
        im.save(thumb_path + fn + '-thumb' + ext, 'JPEG')

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
    
class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    player1 = models.ForeignKey(User, related_name = "palyer 1")
    player2 = models.ForeignKey(User, related_name = "player 2")
    turn = models.ForeignKey(User, related_name = "player turn")
    theme_picture = Photo()

class PuzzlePiece(models.Model):
    helper = models.ForeignKey(User, null=True)
    puzzle = models.ForeignKey(Puzzle)
    photo1 = Photo()
    photo2 = Photo()
    needs_help = models.BooleanField()