from django import forms
from .models import Marker

# class NoteForm(forms.Form):
#   name = forms.CharField(label='Название', required=False, max_length=50, min_length=1, error_messages={
#     'max_length': 'Превышен лимит по кол-ву символов в названии',
#     'min_length': 'Введите хотя бы 1 символ'
#   })
#   description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
#   image = forms.CharField(label='Изображение', required=False)
  

class NoteForm(forms.ModelForm):
  class Meta:
    model = Marker
    fields = ['title', 'description', 'latitude', 'longitude']
    widgets = {
      'latitude': forms.HiddenInput(),
      'longitude': forms.HiddenInput(),
    }
    labels = {
      'title': 'Название',
      'description': 'Описание',
    }
    error_messages = {
      'title' : {
        'max_length': 'Превышен лимит по кол-ву символов в названии',
        'min_length': 'Введите хотя бы 1 символ'
      }
    }