from http import HTTPStatus

from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post
from .utils_tests import TestVariables as data

User = get_user_model()


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
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
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug=data.GROUP_POST_SLAG.value
        )
        cls.post = Post.objects.create(
            text='Тестовый пост 1',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded
        )
        cls.new_post = Post.objects.create(
            text='New_Post',
            author=cls.new_user,
        )

        cls.DETAIL_POST = reverse('posts:post_detail',
                                  kwargs={'post_id': cls.post.pk}
                                  )
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post.pk}
                                )
        cls.ADD_COMMENT = reverse('posts:add_comment',
                                  kwargs={'post_id': cls.post.pk}
                                  )
        cls.templates_page_names = {
            data.INDEX.value: 'posts/index.html',
            data.GROUP_POST.value: 'posts/group_list.html',
            data.PROFILE.value: 'posts/profile.html',
            cls.DETAIL_POST: 'posts/post_detail.html',
            data.CREATE_POST.value: 'posts/create_post.html',
            cls.POST_EDIT: 'posts/create_post.html'
        }

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.templates_page_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_and_group_posts_and_profile_correct_context(self):
        """
        Шаблоны posts:index, posts:group_posts и posts:profile
        сформирован с правильным контекстом.
        """
        urls = [
            data.INDEX.value,
            data.GROUP_POST.value,
            data.PROFILE.value,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                first_object = response.context['page_obj'][0]
                if url == data.GROUP_POST.value:
                    self.assertEqual(first_object.text, 'Тестовый пост 1')
                    self.assertEqual(
                        first_object.author.username,
                        data.USERNAME.value
                    )
                    self.assertEqual(first_object.image, self.post.image)
                    self.assertEqual(
                        first_object.group.slug,
                        data.GROUP_POST_SLAG.value
                    )
                self.assertEqual(first_object.text, 'Тестовый пост 1')
                self.assertEqual(
                    first_object.author.username,
                    data.USERNAME.value
                )
                self.assertEqual(first_object.image, self.post.image)

    def test_post_detail_correct_context(self):
        """Шаблон posts:post_detail сформированы с правильным контекстом."""
        response = self.guest_client.get(self.DETAIL_POST)
        detail_post = response.context['detail_post']
        self.assertEqual(detail_post.text, 'Тестовый пост 1')
        self.assertEqual(detail_post.author.username, data.USERNAME.value)
        self.assertEqual(detail_post.image, self.post.image)

    def test_post_create_correct_context(self):
        """
        Шаблон posts:post_create и posts:post_edit
        сформированы с правильным контекстом.
        """
        urls = [data.CREATE_POST.value, self.POST_EDIT]

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                for url in urls:
                    client = self.authorized_client.get(url)
                    form_field = client.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_check_created_post_with_group(self):
        """
        Правильность вывода созданного поста с группой на страницах.
        Правильность вывода поста в нужной группе
        """
        urls = [
            data.INDEX.value,
            data.GROUP_POST.value,
            data.PROFILE.value
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                context = response.context['page_obj'][0]
                self.assertIn(self.group.title, context.group.title)

        response = self.guest_client.get(data.GROUP_POST.value)
        context = response.context['page_obj'][0]
        self.assertEqual(context.group, self.group)

    def test_add_comment_guest_client(self):
        """Проверка создания комментария
         авторизированным пользователям.
         """
        response = self.guest_client.get(self.ADD_COMMENT)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug=data.GROUP_POST_SLAG.value
        )
        cls.posts = []
        for post in range(1, 14):
            cls.posts.append(Post.objects.create(
                text=f'text_{post}',
                author=cls.user,
                group=cls.group
            ))

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_index_profile_pages_contains_ten_records(self):
        """
        Определяет posts:index, posts:profile и posts:group_posts
        правильность вывода постов на странице.
        """
        pages_paginator = [
            [data.INDEX.value, self.posts],
            [data.GROUP_POST.value, self.posts],
            [data.PROFILE.value, self.posts]
        ]
        for url, posts in pages_paginator:
            with self.subTest(url=url):
                response_one_page = self.guest_client.get(url)
                response_two_page = self.guest_client.get(url + '?page=2')
                self.assertEqual(
                    len(response_one_page.context['page_obj']), 10
                )
                self.assertEqual(
                    len(response_two_page.context['page_obj']), 3
                )


class CacheViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        post_note = 'Создаем пост'
        Post.objects.create(
            text=post_note,
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()

    def test_cache_index_pages(self):
        """Проверяем работу кэша главной страницы."""
        first_response = self.client.get(data.INDEX.value)
        Post.objects.create(
            text='New post',
            author=self.user
        )
        response_after_post_add = self.client.get(data.INDEX.value)
        self.assertEqual(
            len(first_response.content),
            len(response_after_post_add.content)
        )


class FollowUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.new_user = User.objects.create_user(
            username=data.NEW_USERNAME.value
        )
        cls.post = Post.objects.create(
            text='Тестовый пост 1',
            author=cls.new_user,
        )

    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_authorized_client_follow_user(self):
        """Авторизированный клиент может подписываться
         на пользователя."""
        response = self.authorized_client.get(data.FOLLOW_USER.value)
        self.assertTrue(
            Follow.objects.filter(
                author=self.user,
                user=self.new_user
            ).exists()
        )
        self.assertRedirects(response, data.NEW_PROFILE.value)

    def test_authorized_client_unfollow_user(self):
        """Авторизированный клиент может отписаться
         от пользователя."""
        Follow.objects.create(
            author=self.user,
            user=self.new_user
        )
        response = self.authorized_client.get(data.UNFOLLOW_USER.value)
        self.assertFalse(
            Follow.objects.filter(
                author=self.user,
                user=self.new_user
            ).exists()
        )
        self.assertRedirects(response, data.NEW_PROFILE.value)

    def test_records_subscribed_authors(self):
        """Проверка выгрузки записей авторов,
        на которых подписан пользователь.
        """
        response = self.authorized_client.get(data.FOLLOW_INDEX.value)
        self.assertNotIn(self.post, response.context['page_obj'])
