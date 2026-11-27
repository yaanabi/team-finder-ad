from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_github_url(value):
    try:
        parsed = urlparse(value)

        if (
            parsed.hostname == "github.com"
            and parsed.scheme in ("http", "https")
            and parsed.username is None
            and parsed.password is None
        ):
            return
    except ValueError:
        pass

    raise ValidationError("Укажите ссылку на сайт github.com.")
