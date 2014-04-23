from django import forms
from models import Document 

class DocumentForm(forms.ModelForm):
    docfile=forms.FileField( label='Select a file')
    class Meta:
        model=Document
