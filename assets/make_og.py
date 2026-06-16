#!/usr/bin/env python3
"""Render the 1200x630 OpenGraph card for ptrckfrnk.github.io."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
PAPER   = (250, 246, 239)
PAPER2  = (243, 237, 225)
LINE    = (221, 213, 198)
INK     = (28, 26, 23)
INK_SOFT= (83, 78, 70)
INK_FNT = (139, 132, 120)
CLARET  = (154, 47, 47)

GEO_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SANS  = "/System/Library/Fonts/Supplemental/Arial.ttf"
MONO  = "/System/Library/Fonts/Menlo.ttc"

img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# --- subtle claret glow, top-right ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 520, -360, W + 360, 520], fill=(154, 47, 47, 34))
glow = glow.filter(ImageFilter.GaussianBlur(180))
img.paste(Image.new("RGB", (W, H), CLARET), (0, 0), glow)

# --- thin frame ---
draw.rounded_rectangle([24, 24, W - 24, H - 24], radius=12, outline=LINE, width=2)

# --- pf mark ---
mx, my, ms = 96, 74, 118
draw.rounded_rectangle([mx, my, mx + ms, my + ms], radius=26, fill=PAPER2, outline=LINE, width=2)
pf_font = ImageFont.truetype(GEO_B, 62)
draw.text((mx + ms / 2, my + ms / 2), "pf", font=pf_font, fill=CLARET, anchor="mm")

def spaced(draw, xy, text, font, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += draw.textlength(ch, font=font) + spacing

# --- eyebrow ---
eye_font = ImageFont.truetype(MONO, 23)
spaced(draw, (98, 300), "PHYSICAL AI · ROBOTICS · TU MÜNCHEN", eye_font, CLARET, 5)

# --- name (auto-fit to frame width) ---
name = "Patrick Franke"
max_w = (W - 24) - 96 - 30   # right frame inset minus left margin
size = 132
while size > 60:
    f = ImageFont.truetype(GEO_B, size)
    if draw.textlength(name, font=f) <= max_w:
        break
    size -= 2
name_font = ImageFont.truetype(GEO_B, size)
draw.text((92, 342), name, font=name_font, fill=INK, anchor="la")

# --- tagline ---
tag_font = ImageFont.truetype(SANS, 31)
draw.text((98, 498), "Humanoid robotics · vision-language-action · world models",
          font=tag_font, fill=INK_SOFT, anchor="la")

# --- url ---
url_font = ImageFont.truetype(MONO, 22)
draw.text((98, 556), "ptrckfrnk.github.io", font=url_font, fill=INK_FNT, anchor="la")

img.save("og-image.png")
print("wrote og-image.png", img.size)
