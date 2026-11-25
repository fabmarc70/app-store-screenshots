# Nettoie la barre d'état (9:41, batterie pleine) et floute le salaire.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
NAMES = ["planning","bulletin-analyse","simulateur","rentabilite","vacations",
         "gain-reel","radar","missions","carriere","scanner"]
BLUR = {  # zones salaire (x0,y0,x1,y1) en pixels source 1320x2868
    "carriere": [(105, 955, 400, 1060)],
    "planning": [(1030, 2368, 1250, 2452)],
}
def erase_band(im, y0=58, y1=138, x0=150, x1=1230):
    px = im.load()
    for x in range(x0, x1):
        a, b = px[x, y0 - 4], px[x, y1 + 4]
        for y in range(y0, y1):
            t = (y - y0 + 4) / (y1 - y0 + 8)
            px[x, y] = tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))
def draw_bar(im):
    S = 4  # supersampling
    ov = Image.new("RGBA", (1320 * S, 200 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov); W = (255, 255, 255, 255)
    f = ImageFont.truetype(FONT, 62 * S)
    d.text((250 * S, 97 * S), "9:41", font=f, fill=W, anchor="mm")
    # réseau : 4 barres pleines
    for i in range(4):
        h = (16 + i * 9) * S; x = (937 + i * 18) * S
        d.rounded_rectangle((x, 118 * S - h, x + 12 * S, 118 * S), radius=4 * S, fill=W)
    # wifi : 3 arcs + point
    cx, cy = 1052 * S, 117 * S
    for r in (14, 30, 46):
        if r == 14:
            d.pieslice((cx - 16 * S, cy - 16 * S, cx + 16 * S, cy + 16 * S), 225, 315, fill=W)
        else:
            d.arc((cx - r * S, cy - r * S, cx + r * S, cy + r * S), 225, 315, fill=W, width=9 * S)
    # batterie pleine
    d.rounded_rectangle((1106 * S, 76 * S, 1190 * S, 118 * S), radius=13 * S, outline=(255,255,255,150), width=4 * S)
    d.rounded_rectangle((1112 * S, 82 * S, 1184 * S, 112 * S), radius=9 * S, fill=W)
    d.rounded_rectangle((1194 * S, 89 * S, 1201 * S, 105 * S), radius=3 * S, fill=(255,255,255,150))
    ov = ov.resize((1320, 200), Image.LANCZOS)
    im.paste(ov, (0, 0), ov)
for n in NAMES:
    im = Image.open(f"src/{n}.png").convert("RGB")
    erase_band(im); draw_bar(im)
    for box in BLUR.get(n, []):
        blurred = im.filter(ImageFilter.GaussianBlur(40))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(box, radius=30, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(10))
        im = Image.composite(blurred, im, mask)
    im.save(f"clean/{n}.png")
print("ok")
