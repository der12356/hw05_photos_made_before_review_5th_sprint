from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from posts.models import Post, Group, Comment
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
        cls.group_2 = Group.objects.create(
            title='Тостова группа',
            slug='tosts',
            description='Группа любителей тостов',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(PostsFormsTests.user)
        self.post_arg = PostsFormsTests.post.id
        self.user_arg = PostsFormsTests.user.username
        self.group_arg = PostsFormsTests.group.slug
        self.group_2_arg = PostsFormsTests.group_2.slug

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
        new_post = Post.objects.latest('id')
        self.assertEqual(new_post.author, PostsFormsTests.user)
        self.assertEqual(new_post.group, PostsFormsTests.group)

    def test_correct_post_edit_forms(self):
        """Тесты на проверку правильности формы редактирования постов"""
        posts_count = Post.objects.count()
        post = {
            'text': 'Проверочный пост',
            'group': PostsFormsTests.group_2.id,
        }
        response = self.author_client.post(
            reverse('posts:post_edit', args=[self.post_arg]),
            data=post,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=[self.post_arg]))
        self.assertEqual(Post.objects.count(), posts_count,
                         'Отредактированный пост сохранился как новый')
        self.assertTrue(
            Post.objects.filter(
                text__exact='Проверочный пост',
            ).exists(), ('Отредактированный пост не сохранился в БД')
        )
        old_group_response = self.author_client.get(
            reverse('posts:group_list', args=[self.group_arg])
        )
        self.assertEqual(
            old_group_response.context['page_obj'].paginator.count, 0,
            ('В старой группе не удалился редактируемый пост')
        )
        new_group_response = self.author_client.get(
            reverse('posts:group_list', args=[self.group_2_arg])
        )
        self.assertEqual(
            new_group_response.context['page_obj'].paginator.count, 1,
            ('В новой группе не сохранился редактируемый пост')
        )

    def test_comments_only_for_authorized(self):
        """Проверка создания комментария авторизированным пользователем
         и его сохранение в БД"""
        self.author_client.post(
            reverse('posts:post_detail', args=[self.post_arg]),
            data={'text': 'Проверочный комментарий', },
            follow=True
        )
        self.assertTrue(
            Comment.objects.filter(
                text__exact='Проверочный комментарий',
            ).exists()
        )

    def test_guests_cant_comment(self):
        """Проверка того, что гости не могут комментировать"""
        self.guest_client.post(
            reverse('posts:post_detail', args=[self.post_arg]),
            data={'text': 'Проверочный комментарий', },
            follow=True
        )
        self.assertFalse(
            Comment.objects.filter(
                text__exact='Проверочный комментарий',
            ).exists()
        )
