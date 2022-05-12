from http import HTTPStatus

from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post, User
from .utils_tests import TestVariables as data


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.new_user = User.objects.create_user(
            username=data.NEW_USERNAME.value
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
            image=data.uploaded.value
        )
        cls.DETAIL_POST = reverse('posts:post_detail',
                                  args=[cls.post.pk]
                                  )
        cls.POST_EDIT = reverse('posts:post_edit',
                                args=[cls.post.pk]
                                )
        cls.ADD_COMMENT = reverse('posts:add_comment',
                                  args=[cls.post.pk]
                                  )

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = data.templates_url_names.value
        templates_url_names[self.DETAIL_POST] = 'posts/post_detail.html'
        templates_url_names[self.POST_EDIT] = 'posts/create_post.html'
        for url, template in templates_url_names.items():
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
                author=self.new_user,
                user=self.user
            ).exists()
        )
        self.assertRedirects(response, data.NEW_PROFILE.value)

    def test_authorized_client_unfollow_user(self):
        """Авторизированный клиент может отписаться
         от пользователя."""
        Follow.objects.create(
            author=self.new_user,
            user=self.user
        )
        response = self.authorized_client.get(data.UNFOLLOW_USER.value)
        self.assertFalse(
            Follow.objects.filter(
                author=self.new_user,
                user=self.user
            ).exists()
        )
        self.assertRedirects(response, data.NEW_PROFILE.value)

    def test_records_subscribed_authors(self):
        """Проверка выгрузки записей авторов,
        на которых подписан пользователь.
        """
        response = self.authorized_client.get(data.FOLLOW_INDEX.value)
        self.assertNotIn(self.post, response.context['page_obj'])
