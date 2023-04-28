from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        text_length = 15
        return self.text[:text_length]

    text = models.TextField(
        help_text='Введите текст поста',
        verbose_name='Текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='posts',
        help_text='Выберите группу',
        verbose_name='Группа публикации'
    )
    image = models.ImageField(
        help_text='Выберите картинку для поста',
        upload_to='posts/',
        blank=True,
        verbose_name='Фотография публикации'
    )


class Group(models.Model):
    def __str__(self) -> str:
        return self.title

    title = models.CharField(
        max_length=200,
        verbose_name='Название группы'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name='Ссылка группы'
    )
    description = models.TextField(
        verbose_name='Описание группы'
    )


class Comment(models.Model):
    def __str__(self) -> str:
        return self.text[:50]

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        help_text='Введите ваш комментарий',
        verbose_name='Текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария'
    )
