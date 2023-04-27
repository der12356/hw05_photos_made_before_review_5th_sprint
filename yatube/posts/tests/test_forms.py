from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from posts.models import Post, Group
from posts.forms import PostForm

User = get_user_model()


class PostsFormsTests(TestCase):
    """Тесты на проверку работы форм создания и редактирования постов"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(PostsFormsTests.user)
        self.post_arg = PostsFormsTests.post.id
        self.user_arg = PostsFormsTests.user.username

    def test_correct_post_creation_forms(self):
        """Тесты на проверку правильности формы создания постов"""
        posts_count = Post.objects.count()
        post = {
            'text': 'Проверочный пост',
            'group': PostsFormsTests.group.id,
        }
        response = self.author_client.post(
            reverse('posts:post_create'),
            data=post,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                                               args=[self.user_arg]))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text__exact='Проверочный пост',
            ).exists()
        )

    def test_correct_post_edit_forms(self):
        """Тесты на проверку правильности формы редактирования постов"""
        posts_count = Post.objects.count()
        post = {
            'text': 'Проверочный пост',
            'group': PostsFormsTests.group.id,
        }
        response = self.author_client.post(
            reverse('posts:post_edit', args=[self.post_arg]),
            data=post,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=[self.post_arg]))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text__exact='Проверочный пост',
            ).exists()
        )
