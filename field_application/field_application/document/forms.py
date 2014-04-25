from django import forms
from field_application.document.models import Document 

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
