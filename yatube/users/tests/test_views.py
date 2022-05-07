from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

USERNAME = 'Test_User'
SIGNUP = reverse('users:signup')


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_signup_correct_context(self):
        """Шаблон users:signup сфомирован с правильным контекстом."""

        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                client = self.guest_client.get(SIGNUP)
                form_field = client.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
