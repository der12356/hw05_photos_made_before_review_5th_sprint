from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_test = PostModelTest.post.__str__()
        post_result = 'Тестовый пост'
        self.assertEqual(post_test, post_result, 'str поста не верный!')
        group_test = PostModelTest.group.__str__()
        group_result = 'Тестовая группа'
        self.assertEqual(group_test, group_result, 'str группы не верный!')

    def test_post_model_have_correct_group(self):
        """Проверяем, что у поста корректно выставлена группа."""
        post_test = PostModelTest.post.group
        post_result = PostModelTest.group
        self.assertEqual(post_test, post_result, ('Посты сохранились не в '
                                                  'той группе!'))
