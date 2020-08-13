from django import forms
from .models import InvoiceFileUpload

class DocumentForm(forms.ModelForm):
    class Meta:
        model = InvoiceFileUpload
        fields = ('document',)
