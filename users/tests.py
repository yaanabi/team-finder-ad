from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

User = get_user_model()


class UserTests(TestCase):
    def test_valid_phone(self):
        user = User(
            email="test@example.com",
            name="Иван",
            surname="Иванов",
            phone="+79991234567",
        )
        user.set_password("testpassword")
        user.full_clean()

    def test_invalid_phone(self):
        invalid_phones = (
            "89991234567",
            "+19991234567",
            "+7999123456",
            "+799912345678",
            "+7999abcdefg",
            "+7 999 123 45 67",
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
