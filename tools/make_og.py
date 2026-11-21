"""Генерация OG-изображения 1200×630 для сайта.

Запуск:  .venv/bin/python tools/make_og.py
Нужен Pillow:  .venv/bin/pip install pillow
"""

from __future__ import annotations

import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
AVATAR = ROOT / "docs" / "assets" / "avatar.png"
OUTPUT = ROOT / "docs" / "assets" / "og-image.png"

FONT_URL = "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf"
FONT_CACHE = Path("/tmp/opencode/fonts/Manrope.ttf")

WIDTH, HEIGHT = 1200, 630


def load_font(size: int, weight: int = 700) -> ImageFont.FreeTypeFont:
    if not FONT_CACHE.exists():
        FONT_CACHE.parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(FONT_URL, FONT_CACHE)
        except Exception:
            pass

    if FONT_CACHE.exists():
        font = ImageFont.truetype(str(FONT_CACHE), size)
        try:
            font.set_variation_by_axes([weight])
        except Exception:
            pass
        return font

    fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    return ImageFont.truetype(fallback, size)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def make_gradient() -> Image.Image:
    stops = [(0.0, (67, 56, 202)), (0.52, (109, 40, 217)), (1.0, (3, 105, 161))]
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            t = (x / WIDTH * 0.72) + (y / HEIGHT * 0.28)
            for i in range(len(stops) - 1):
                start, color_a = stops[i]
                end, color_b = stops[i + 1]
                if start <= t <= end:
                    local = (t - start) / (end - start)
                    color = tuple(lerp(color_a[j], color_b[j], local) for j in range(3))
                    break
            else:
                color = stops[-1][1]
            pixels[x, y] = color
    return img


def add_circle(base: Image.Image, xy: tuple[int, int, int, int], alpha: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse(xy, fill=(255, 255, 255, alpha))
    base.alpha_composite(layer)


def add_math(base: Image.Image) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    serif = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 92)
    serif_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 54)
    for text, pos, font in [
        ("∑", (40, 20), serif),
        ("π", (1090, 30), serif),
        ("√x", (60, 500), serif_small),
        ("x²", (1040, 500), serif_small),
        ("sin²α + cos²α = 1", (420, 18), ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 30)),
        ("a² + b² = c²", (860, 565), ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 26)),
    ]:
        draw.text(pos, text, font=font, fill=(255, 255, 255, 28))
    base.alpha_composite(layer)


def rounded_chip(
    base: Image.Image,
    x: int,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    color: tuple[int, int, int, int] = (255, 255, 255, 255),
    padding_x: int = 22,
    padding_y: int = 12,
) -> int:
    draw = ImageDraw.Draw(base)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0] + padding_x * 2
    height = bbox[3] - bbox[1] + padding_y * 2

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (x, y, x + width, y + height), radius=height // 2, fill=fill
    )
    base.alpha_composite(layer)
    draw.text((x + padding_x, y + padding_y - bbox[1] + 1), text, font=font, fill=color)
    return width


def add_avatar(base: Image.Image) -> None:
    size = 330
    left = WIDTH - size - 110
    top = (HEIGHT - size) // 2 - 8

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse(
        (left - 18, top + 18, left + size + 18, top + size + 38),
        fill=(15, 10, 50, 150),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    base.alpha_composite(shadow)

    ring = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse(
        (left - 14, top - 14, left + size + 14, top + size + 14),
        fill=(255, 255, 255, 255),
    )
    ring_draw.ellipse((left, top, left + size, top + size), fill=(255, 255, 255, 255))
    base.alpha_composite(ring)

    avatar = Image.open(AVATAR).convert("RGBA")
    avatar = avatar.resize((size, size), Image.LANCZOS)
    base.paste(avatar, (left, top), avatar)


def add_sparkles(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base)
    for cx, cy, r, alpha in [
        (790, 120, 7, 230),
        (760, 500, 5, 180),
        (1085, 300, 6, 200),
        (95, 330, 4, 160),
    ]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(251, 191, 36, alpha))


def main() -> None:
    base = make_gradient().convert("RGBA")
    add_circle(base, (-180, -220, 420, 380), 18)
    add_circle(base, (820, -260, 1460, 380), 14)
    add_circle(base, (-260, 420, 360, 980), 12)
    add_math(base)

    add_avatar(base)

    draw = ImageDraw.Draw(base)
    left = 84

    badge_font = load_font(21, 800)
    rounded_chip(
        base,
        left,
        92,
        "РЕПЕТИТОР ПО МАТЕМАТИКЕ",
        badge_font,
        fill=(255, 255, 255, 38),
        padding_x=20,
        padding_y=11,
    )

    title_font = load_font(78, 800)
    draw.text((left, 156), "Терехова", font=title_font, fill=(255, 255, 255, 255))

    name_font = load_font(46, 700)
    draw.text((left, 250), "Елена Викторовна", font=name_font, fill=(255, 255, 255, 255))

    accent_font = load_font(27, 700)
    draw.text(
        (left, 330),
        "Математика, которая становится понятной",
        font=accent_font,
        fill=(232, 228, 255, 255),
    )

    chip_font = load_font(22, 700)
    x = left
    for text in ["ОГЭ", "ЕГЭ база и профиль", "1–11 класс"]:
        width = rounded_chip(
            base,
            x,
            430,
            text,
            chip_font,
            fill=(255, 255, 255, 40),
            padding_x=20,
            padding_y=12,
        )
        x += width + 14

    footer_font = load_font(20, 600)
    draw.text(
        (left, 545),
        "alena-teacher.github.io/services",
        font=footer_font,
        fill=(255, 255, 255, 150),
    )

    add_sparkles(base)

    base.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(f"Saved {OUTPUT} ({os.path.getsize(OUTPUT) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
