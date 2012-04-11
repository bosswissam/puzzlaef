from django import forms
from puzzlaef.puzzle.models import PuzzlePiece
#from puzzlaef.main.models import UserProfile

class UserProfileForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(), max_length = 30)
    last_name = forms.CharField(required=False, widget=forms.TextInput(), max_length = 30)
    location = forms.CharField(required=False, widget=forms.TextInput(), max_length = 100)
    

#    class Meta:
#        model = UserProfile

class PuzzlePieceForm(forms.ModelForm):
    class Meta:
        model = PuzzlePiece
        exclude = ['helper']