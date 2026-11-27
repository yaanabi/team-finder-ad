from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


def create_avatar(name):
    image = Image.new("RGB", (256, 256), color="lightblue")

    font_path = (
        settings.BASE_DIR /
        "static" /
        "fonts" / "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
    )
    font = ImageFont.truetype(str(font_path), size=121)
    letter = name.strip()[:1].upper()

    ImageDraw.Draw(image).text(
        (128, 128),
        letter,
        font=font,
        fill="SteelBlue",
        anchor="mm",
    )

    with BytesIO() as buffer:
        image.save(buffer, format="PNG")
        return ContentFile(
            buffer.getvalue(),
            name=f"avatar_{uuid4().hex}.png",
        )