from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

AUTHOR = reverse('about:author')
TECH = reverse('about:tech')
FAKE_PAGE = '/fake_page/'


class AboutURLTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_pages_code(self):
        """Страницы доступны любому пользователю."""

        CODE_SUCCESS = 200
        CODE_NOT_FOUND = 404

        url_names = [
            [self.guest_client, AUTHOR, CODE_SUCCESS],
            [self.guest_client, TECH, CODE_SUCCESS],
            [self.guest_client, FAKE_PAGE, CODE_NOT_FOUND]
        ]

        for client, url, code in url_names:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(code, response.status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            AUTHOR: 'about/author.html',
            TECH: 'about/tech.html'
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
