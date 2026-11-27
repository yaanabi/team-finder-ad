from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from tempfile import TemporaryDirectory

User = get_user_model()


class UserTests(TestCase):
    def test_valid_phone(self):
        valid_phones = (
            "+79991234567",
            "89991234567",
        )

        for phone in valid_phones:
            with self.subTest(phone=phone):
                user = User(
                    email="test@example.com",
                    name="Иван",
                    surname="Иванов",
                    phone=phone,
                )
                user.set_password("testpassword")
                user.full_clean()

                self.assertEqual(user.phone, "+79991234567")

    def test_invalid_phone(self):
        invalid_phones = (
            "+19991234567",
            "+7999123456",
            "+799912345678",
            "+7999abcdefg",
            "+7 999 123 45 67",
            "8999123456",
            "899912345678",
            "8999abcdefg",
            "79991234567",
            "",
        )

        for phone in invalid_phones:
            with self.subTest(phone=phone):
                user = User(
                    email="test@example.com",
                    name="Иван",
                    surname="Иванов",
                    phone=phone,
                )
                user.set_password("testpassword")

                with self.assertRaises(ValidationError) as context:
                    user.full_clean()

                self.assertIn("phone", context.exception.message_dict)

    def test_unique_phone(self):
        User.objects.create_user(
            email="first@example.com",
            password="testpassword",
            name="Иван",
            surname="Иванов",
            phone="+79991234567",
        )

        duplicate_phones = (
            "+79991234567",
            "89991234567",
        )

        for phone in duplicate_phones:
            with self.subTest(phone=phone):
                user = User(
                    email="second@example.com",
                    name="Пётр",
                    surname="Петров",
                    phone=phone,
                )
                user.set_password("testpassword")

                with self.assertRaises(ValidationError) as context:
                    user.full_clean()

                self.assertIn("phone", context.exception.message_dict)
                self.assertEqual(
                    context.exception.error_dict["phone"][0].code,
                    "unique",
                )

    def test_github_url_validation(self):
        urls = (
            ("https://github.com/user", True),
            ("http://github.com/user", True),
            ("https://gitlab.com/user", False),
            ("invalid-url", False),
        )

        for url, is_valid in urls:
            with self.subTest(url=url):
                user = User(
                    email="test@example.com",
                    name="Иван",
                    surname="Иванов",
                    phone="+79991234567",
                    github_url=url,
                )
                user.set_password("testpassword")

                if is_valid:
                    user.full_clean()
                else:
                    with self.assertRaises(ValidationError) as context:
                        user.full_clean()

                    self.assertIn(
                        "github_url",
                        context.exception.message_dict,
                    )

    def test_default_avatar_creation(self):
        with TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                user = User.objects.create_user(
                    email="test@asdasd.com",
                    password="asdasd",
                    name="Иван",
                    surname="Иванов",
                    phone="+79991234567",
                )

                user.refresh_from_db()

                self.assertTrue(user.avatar)
                self.assertTrue(user.avatar.storage.exists(user.avatar.name))
