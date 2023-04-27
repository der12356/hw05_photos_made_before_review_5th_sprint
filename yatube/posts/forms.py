from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст вашего поста',
            'group': 'Группа где будет отдыхать ваш пост',
            'image': 'Загрузите фото-заголовок вашего поста'
        }
