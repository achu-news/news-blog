#!/usr/bin/env python3
"""Generate a branded 1200x630 social card for every Jekyll post."""

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
OUTPUT = ROOT / "assets" / "og"
LOGO = ROOT / "assets" / "logo.png"


def font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


SERIF = [
    "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
    "/System/Library/Fonts/Times.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SANS = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def front_matter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    if re.search(r"[ぁ-んァ-ン一-龯]", text):
        lines, current = [], ""
        for char in text:
            candidate = current + char
            if current and draw.textlength(candidate, font=face) > width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    lines, current = [], ""
    for word in text.split():
        candidate = word if not current else f"{current} {word}"
        if current and draw.textlength(candidate, font=face) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def make_card(post: Path) -> None:
    meta = front_matter(post.read_text(encoding="utf-8"))
    title = meta.get("headline") or meta.get("title") or post.stem
    language = meta.get("lang", "ja")
    date_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", meta.get("date", post.stem))
    if date_match:
        year, month, day = date_match.groups()
        date_label = f"{year}年{int(month)}月{int(day)}日" if language == "ja" else f"{year}-{month}-{day}"
    else:
        date_label = ""

    image = Image.new("RGB", (1200, 630), "#f7f7f4")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 12), fill="#c0392b")

    logo = Image.open(LOGO).convert("RGBA").resize((86, 86), Image.Resampling.LANCZOS)
    image.paste(logo, (76, 54), logo)
    brand_face = font(SERIF, 39)
    small_face = font(SANS, 22)
    draw.text((184, 57), "世界とお金の羅針盤" if language == "ja" else "The World & Money Compass", font=brand_face, fill="#24292f")
    draw.text((186, 111), "毎朝8時、世界の動きとお金の流れを。" if language == "ja" else "Every morning — the world and your money.", font=small_face, fill="#6e7681")

    draw.rounded_rectangle((78, 190, 300, 234), radius=22, fill="#fdecea")
    draw.text((98, 198), date_label, font=small_face, fill="#a93226")

    title_face = font(SERIF, 54)
    lines = wrap(draw, title, title_face, 1040)
    if len(lines) > 4:
        title_face = font(SERIF, 46)
        lines = wrap(draw, title, title_face, 1040)
    lines = lines[:4]
    y = 278
    line_height = 76 if title_face.size >= 50 else 66
    for line in lines:
        draw.text((78, y), line, font=title_face, fill="#24292f")
        y += line_height

    draw.rectangle((78, 568, 1122, 570), fill="#e7e5e0")
    footer = "NEWS & MARKETS · AI-WRITTEN · SOURCES INCLUDED"
    draw.text((78, 584), footer, font=font(SANS, 18), fill="#8a8f98")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / f"{post.stem}.png", optimize=True)


def main() -> None:
    posts = sorted(POSTS.rglob("*.md"))
    for post in posts:
        make_card(post)
    print(f"Generated {len(posts)} OG images in {OUTPUT}")


if __name__ == "__main__":
    main()
