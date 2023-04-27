from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostsViewFuncsTests(TestCase):
    """Тесты на проверку работы шаблонов вью функций"""
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

    def setUp(self):
        self.user = User.objects.create_user(username='VIP')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(PostsViewFuncsTests.user)
        self.group_arg = PostsViewFuncsTests.group.slug
        self.user_arg = PostsViewFuncsTests.user.username
        self.post_arg = PostsViewFuncsTests.post.id

    def test_pages_uses_correct_template(self):
        """Вью функция использует нужный шаблон"""
        test_dict = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list',
                                             args=[self.group_arg]),
            'posts/profile.html': reverse('posts:profile',
                                          args=[self.user_arg]),
            'posts/post_detail.html': reverse('posts:post_detail',
                                              args=[self.post_arg]),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, reverse_name in test_dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_correct_template(self):
        """Вью функция редактирования поста использует нужный шаблон"""
        response = self.author_client.get(reverse('posts:post_edit',
                                                  args=[self.post_arg]))
        self.assertTemplateUsed(response, 'posts/create_post.html')


class PaginatorViewsTest(TestCase):
    """Тесты на проверку работоспособности пажинатора"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        test_posts_texts = [
            'Текст1', 'Текст2', 'Текст3', 'Текст4', 'Текст5', 'Текст6',
            'Текст7', 'Текст8', 'Текст9', 'Текст10', 'Текст11', 'Текст12',
            'Текст13',
        ]
        for text in test_posts_texts:
            cls.post = Post.objects.create(
                author=cls.user,
                text=text,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        self.group_arg = PaginatorViewsTest.group.slug
        self.user_arg = PaginatorViewsTest.user.username

    def test_paginator_first_page_10_posts_index(self):
        """"Проверка паджинатора на главной странице"""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_second_page_3_posts_index(self):
        """"Проверка паджинатора на второй странице Index'а"""
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_paginator_first_page_10_posts_group(self):
        """"Проверка паджинатора на первой странице групп"""
        response = self.guest_client.get(reverse('posts:group_list',
                                                 args=[self.group_arg]))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_second_page_3_posts_group(self):
        """"Проверка паджинатора на второй странице групп"""
        response = self.guest_client.get(reverse('posts:group_list',
                                                 args=[self.group_arg])
                                         + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_paginator_first_page_10_posts_profile(self):
        """"Проверка паджинатора на первой странице профиля"""
        response = self.guest_client.get(reverse('posts:profile',
                                                 args=[self.user_arg]))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_second_page_3_posts_profile(self):
        """"Проверка паджинатора на второй странице профиля"""
        response = self.guest_client.get(reverse('posts:profile',
                                                 args=[self.user_arg])
                                         + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)


class ContextViewTest(TestCase):
    """Проверка правильности контекста и дополнительная проверка
     правильности создания постов"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.user_two = User.objects.create_user(username='SomeoneElse')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )  # Создание 1-го поста для аргумента вью функций
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст1',
            group=cls.group
        )  # Создание постов с группой и автором
        test_posts = [
            'Текст2', 'Текст3', 'Текст4', 'Текст5',
        ]
        for text in test_posts:
            cls.post_group = Post.objects.create(
                author=cls.user,
                text=text,
                group=cls.group
            )  # Создание постов с другим автором и без группы
        test_posts_no_group = [
            'ТекстБезГруппы1', 'ТекстБезГруппы2', 'ТекстБезГруппы3',
        ]
        for text in test_posts_no_group:
            cls.post_no_group = Post.objects.create(
                author=cls.user_two,
                text=text,
            )

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(ContextViewTest.user)
        self.group_arg = ContextViewTest.group.slug
        self.user_arg = ContextViewTest.user.username
        self.post_arg = ContextViewTest.post.id

    def test_context_index_view(self):
        """"Проверка контекста на главной странице"""
        response = self.author_client.get(reverse('posts:index'))
        object = response.context['page_obj']
        self.assertEqual(object.paginator.count, 8)

    def test_context_group_view(self):
        """"Проверка контекста на странице группы"""
        response = self.author_client.get(reverse('posts:group_list',
                                                  args=[self.group_arg]))
        object = response.context['page_obj']
        for post in object:
            with self.subTest(post=post):
                self.assertEqual(post.group, ContextViewTest.group)

    def test_context_profile_view(self):
        """"Проверка контекста на странице профиля"""
        response = self.author_client.get(reverse('posts:profile',
                                                  args=[self.user_arg]))
        object = response.context['page_obj']
        for post in object:
            with self.subTest(post=post):
                self.assertEqual(post.author, ContextViewTest.user)

    def test_context_post_detail_view(self):
        """Проверка контекста страницы с деталями о посте"""
        response = self.author_client.get(reverse('posts:post_detail',
                                                  args=[self.post_arg]))
        post = response.context['post']
        self.assertEqual(post.text, 'Текст1')

    def test_context_create_post_view(self):
        """Проверка контекста (формы) страницы создания поста"""
        response = self.author_client.get(reverse('posts:post_create'))
        form_fields_expected = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields_expected.items():
            with self.subTest(value=value):
                field = response.context.get('form').fields.get(value)
                self.assertIsInstance(field, expected)

    def test_context_edit_post_view_form(self):
        """Проверка формы страницы изменения поста"""
        response = self.author_client.get(reverse('posts:post_edit',
                                                  args=[self.post_arg]))
        form_fields_expected = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields_expected.items():
            with self.subTest(value=value):
                field = response.context.get('form').fields.get(value)
                self.assertIsInstance(field, expected)
