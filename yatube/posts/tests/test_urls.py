from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User
from .utils_tests import TestVariables as data


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.new_user = User.objects.create_user(
            username=data.NEW_USERNAME.value
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=data.GROUP_POST_SLAG.value,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.POST_EDIT = reverse('posts:post_edit',
                                args=[cls.post.pk]
                                )
        cls.DETAIL_POST = reverse('posts:post_detail',
                                  args=[cls.post.pk]
                                  )

    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.new_authorized_client = Client()
        self.new_authorized_client.force_login(self.new_user)

    def test_pages_codes(self):
        """Страницы доступны любому пользователю."""
        OK = HTTPStatus.OK
        FOUND = HTTPStatus.FOUND
        NOT_FOUND = HTTPStatus.NOT_FOUND

        url_names = [
            [self.authorized_client, data.CREATE_POST.value, OK],
            [self.authorized_client, self.POST_EDIT, OK],
            [self.authorized_client, self.DETAIL_POST, OK],
            [self.authorized_client, data.FOLLOW_INDEX.value, OK],
            [self.new_authorized_client, data.FOLLOW_USER.value, FOUND],
            [self.new_authorized_client, data.UNFOLLOW_USER.value, FOUND],
            [self.authorized_client, data.FAKE_PAGE.value, NOT_FOUND],
            [self.guest_client, data.INDEX.value, OK],
            [self.guest_client, data.CREATE_POST.value, FOUND],
            [self.guest_client, self.POST_EDIT, FOUND],
            [self.guest_client, data.GROUP_POST.value, OK],
            [self.guest_client, data.PROFILE.value, OK],
            [self.guest_client, self.DETAIL_POST, OK],
            [self.guest_client, data.FOLLOW_INDEX.value, FOUND],
            [self.guest_client, data.FOLLOW_USER.value, FOUND],
            [self.guest_client, data.UNFOLLOW_USER.value, FOUND],
            [self.guest_client, data.FAKE_PAGE.value, NOT_FOUND]
        ]
        for client, url, code in url_names:
            with self.subTest(url=url):
                response = client.get(url)
                if url == self.POST_EDIT:
                    if self.post.author != self.user:
                        code = FOUND
                self.assertEqual(
                    code,
                    response.status_code
                )

    def test_redirect(self):
        """Перенаправление пользователя."""
        templates_url_names = [
            [
                self.guest_client,
                data.CREATE_POST.value,
                data.AUTH.value + '?next=' + data.CREATE_POST.value
            ],
            [
                self.guest_client,
                self.POST_EDIT,
                data.AUTH.value + '?next=' + self.POST_EDIT
            ],
            [
                self.guest_client,
                data.FOLLOW_INDEX.value,
                data.AUTH.value + '?next=' + data.FOLLOW_INDEX.value
            ],
            [
                self.guest_client,
                data.FOLLOW_USER.value,
                data.AUTH.value + '?next=' + data.FOLLOW_USER.value
            ],
            [
                self.guest_client,
                data.UNFOLLOW_USER.value,
                data.AUTH.value + '?next=' + data.UNFOLLOW_USER.value
            ],
            [
                self.new_authorized_client,
                data.FOLLOW_USER.value,
                data.NEW_PROFILE.value
            ],
            [
                self.new_authorized_client,
                data.UNFOLLOW_USER.value,
                data.NEW_PROFILE.value
            ],
        ]
        for client, url, url_redirect in templates_url_names:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertRedirects(
                    response,
                    url_redirect
                )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = data.templates_url_names.value
        templates_url_names[self.DETAIL_POST] = 'posts/post_detail.html'
        templates_url_names[self.POST_EDIT] = 'posts/create_post.html'
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
