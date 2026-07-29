from django import forms
from .models import Post

# День 5: Форма для создания поста
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# День 12: Форма обратной связи
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ism")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Xabar")