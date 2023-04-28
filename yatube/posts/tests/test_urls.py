from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
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
        self.guest_client = Client()
        self.user = User.objects.create_user(username='VIP')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(PostsURLTests.user)
        self.group_arg = PostsURLTests.group.slug
        self.user_arg = PostsURLTests.user.username
        self.post_arg = PostsURLTests.post.id

    def test_urls_and_templates_correct_guest(self):
        """URL-адрес доступна и использует соответствующий шаблон."""
        templates_urls = {
            'posts/index.html': ('posts:index', ),
            'posts/group_list.html': ('posts:group_list', [self.group_arg]),
            'posts/profile.html': ('posts:profile', [self.user_arg]),
            'posts/post_detail.html': ('posts:post_detail', [self.post_arg]),

        }
        for template, url_full in templates_urls.items():
            with self.subTest(url_full=url_full):
                if len(url_full) == 1:  # Если аргументы url не нужны
                    url = url_full[0]
                    response = self.guest_client.get(reverse(url))
                else:  # Если аргументы url нужны
                    url = url_full[0]
                    url_args = url_full[1]
                    response = self.guest_client.get(reverse(
                        url, args=url_args))
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 f'Ошибка статуса в {url}')
                self.assertTemplateUsed(response, template,
                                        f'Ошибка шаблона в {url}')

    def test_404_url(self):
        """Страница 404 работает как надо."""
        response = self.guest_client.get('/notexist/yes/no/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND,
                         'страница 404 не работает')

    def test_create_new_post_url(self):
        """Проверка работы и шаблона страницы создания нового поста
         и не имеют ли доступ к ней гости"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         ('Пользователи не могут создать посты!'))
        self.assertTemplateUsed(response, 'posts/create_post.html',
                                ('Ошибка шаблона при создании поста'))
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         ('Гости могут создавать посты!'))

    def test_edit_post_url(self):
        """Проверка работы страницы редактирования поста и не имеют ли к ней
         доступ гости и не авторы поста"""
# Проверка при пользователе, авторе поста
        response = self.author_client.get(reverse('posts:post_edit',
                                                  args=[self.post_arg]))
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         ('Автор не может изменить свой пост!'))
        self.assertTemplateUsed(response, 'posts/create_post.html',
                                ('Ошибка шаблона при создании поста'))
# Проверка при пользователе, анонимном госте сайта
        response = self.guest_client.get(reverse('posts:post_edit',
                                                 args=[self.post_arg]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         ('Гости могут изменять посты!'))
        expected_redirect = '/auth/login/?next=/posts/1/edit/'
        self.assertRedirects(response, expected_redirect, status_code=302,
                             target_status_code=200)
# Проверка при авторизованном пользователе, но не авторе поста
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      args=[self.post_arg]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         ('Пользователи могут изменять чужие посты!'))
        expected_redirect = reverse('posts:post_detail', args=[self.post_arg])
        self.assertRedirects(response,
                             expected_redirect,
                             status_code=302,
                             target_status_code=200
                             )
