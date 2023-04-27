from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    class Meta:
        ordering = ['-pub_date']

    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='posts',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        help_text='Выберите картинку для поста',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите ваш комментарий'
    )
    created = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self) -> str:
        return self.text[:50]
