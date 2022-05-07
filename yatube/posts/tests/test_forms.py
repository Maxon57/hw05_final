import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User
from .utils_tests import TestVariables as data

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=data.GROUP_POST_SLAG.value,
            description='Тестовое описание',
        )
        cls.group_new = Group.objects.create(
            title='Новая группа',
            slug='New_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='test_post_1',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text='Comment',
            post=cls.post,
            author=cls.user
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post.pk}
                                )
        cls.POST_DETAIL = reverse('posts:post_detail',
                                  kwargs={'post_id': cls.post.pk}
                                  )
        cls.ADD_COMMENT = reverse('posts:add_comment',
                                  kwargs={'post_id': cls.post.pk}
                                  )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_record_post(self):
        """Проверка создание нового поста."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'new_post',
            'author': self.user,
        }
        response = self.authorized_client.post(
            data.CREATE_POST.value,
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, data.PROFILE.value)

    def test_create_post_with_image(self):
        """Проверка создание записи поста с картинкой в бд."""
        count_posts = Post.objects.count()
        data_from = {
            'text': 'New_post',
            'group': self.group.pk,
            'image': self.uploaded
        }
        response = self.authorized_client.post(
            data.CREATE_POST.value,
            data_from,
            follow=True
        )
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertRedirects(response, data.PROFILE.value)

    def test_add_comment_authorized_client(self):
        """Проверка выгрузки комментария на страницу."""
        data_form = {
            'post': self.post.pk,
            'author': self.user.pk,
            'text': 'New Comment'
        }
        response = self.authorized_client.post(
            self.ADD_COMMENT,
            data_form,
            follow=True
        )
        self.assertContains(response, 'New Comment')

    def test_change_record_posts(self):
        """Проверка на изменение записи поста в базе даннхы."""
        form_data = {
            'text': 'modified_post',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            self.POST_EDIT,
            form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text='modified_post',
                group=self.group).exists()
        )
        self.assertRedirects(response, self.POST_DETAIL)

    def test_check_create_new_user(self):
        """Проверка создания нового пользователя."""
        NAME_USER = 'New_User'
        form_data = {
            'first_name': NAME_USER,
            'last_name': NAME_USER,
            'username': NAME_USER,
            'email': NAME_USER + '@mail.com',
            'password1': '56tertheh64',
            'password2': '56tertheh64'
        }
        response = self.guest_client.post(
            data.SIGNUP.value,
            form_data,
            follow=True
        )
        new_user = User.objects.get(username=NAME_USER)
        self.assertEqual(new_user.username, NAME_USER)
        self.assertRedirects(response, data.INDEX.value)
