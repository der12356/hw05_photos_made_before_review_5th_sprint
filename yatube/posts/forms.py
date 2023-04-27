from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст вашего поста',
            'group': 'Группа где будет отдыхать ваш пост',
            'image': 'Загрузите фото-заголовок вашего поста'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        help_texts = {
            'text': 'Текст вашего комментария',
        }
