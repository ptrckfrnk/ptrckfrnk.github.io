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

# --- name (auto-fit), vertically centred with the tagline ---
name = "Patrick Franke Oviedo"
max_w = W - 96 - 96   # equal left/right margins
size = 134
while size > 60:
    f = ImageFont.truetype(GEO_B, size)
    if draw.textlength(name, font=f) <= max_w:
        break
    size -= 2
name_font = ImageFont.truetype(GEO_B, size)

tag_font = ImageFont.truetype(SANS, 33)
tagline = "Humanoid robotics · Physical AI · Machine learning"

gap = 14
block_h = size + gap + 33
# Centre the text block on the lower rule-of-thirds line (2/3 down) rather
# than the middle, for a more dynamic composition.
name_top = (2 * H) // 3 - block_h // 2
draw.text((96, name_top), name, font=name_font, fill=INK, anchor="la")
draw.text((100, name_top + size + gap), tagline, font=tag_font, fill=INK_SOFT, anchor="la")

img.save("og-image.png")
print("wrote og-image.png", img.size)
