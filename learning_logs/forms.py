from django import forms
from .models import Topic,Entry,UploadedFile

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['name', 'file', 'is_private']
        widgets = {
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }