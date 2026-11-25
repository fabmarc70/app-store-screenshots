# Nettoie la barre d'état (9:41, batterie pleine) et remplace salaires / noms réels par du fictif.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
NAMES = ["planning","bulletin-analyse","simulateur","rentabilite","vacations",
         "gain-reel","radar","missions","carriere","scanner"]
FD = "/usr/share/fonts/opentype/inter/"
# Remplacements de texte : zone à effacer (x0,y0,x1,y1), texte, police, taille,
# position d'ancrage (x, ligne de base), ancre PIL, couleur.
REPL = {
    "planning": [
        (("disc", 125, 1681, 66, 1628, 1671), "ATL", "Inter-Bold.otf", 39, (125, 1665), "ms", (232, 236, 245)),
        (("disc", 720, 1681, 66, 1628, 1671), "ORYS", "Inter-Bold.otf", 39, (720, 1665), "ms", (232, 236, 245)),
        ((258, 1970, 365, 2018), "ATL", "Inter-SemiBold.otf", 55, (262, 2015), "ls", (255, 255, 255)),
        ((1096, 2390, 1236, 2434), "2390€", "Inter-Bold.otf", 48, (1100, 2430), "ls", (255, 255, 255)),
    ],
    "carriere": [
        ((120, 975, 362, 1040), "2180 €", "Inter-Bold.otf", 76, (125, 1035), "ls", (255, 255, 255)),
    ],
    "simulateur": [
        ((92, 1332, 640, 1394), "27100 Montval, France", "Inter-Regular.otf", 50, (95, 1378), "ls", (255, 255, 255)),
    ],
    "vacations": [
        ((140, 757, 470, 803), "27100 Montval", "Inter-SemiBold.otf", 44, (145, 795), "ls", (183, 195, 217)),
        ((1012, 757, 1228, 803), "Brévan 27", "Inter-SemiBold.otf", 44, (1218, 795), "rs", (183, 195, 217)),
        ((140, 1281, 470, 1327), "27100 Montval", "Inter-SemiBold.otf", 44, (145, 1319), "ls", (183, 195, 217)),
        ((1012, 1281, 1228, 1327), "Brévan 27", "Inter-SemiBold.otf", 44, (1218, 1319), "rs", (183, 195, 217)),
        ((140, 2273, 470, 2319), "27100 Montval", "Inter-SemiBold.otf", 44, (145, 2311), "ls", (183, 195, 217)),
        ((1012, 2273, 1228, 2319), "Brévan 27", "Inter-SemiBold.otf", 44, (1218, 2311), "rs", (183, 195, 217)),
    ],
    "missions": [
        ((290, 2092, 710, 2142), "Sécurité.pro", "Inter-Regular.otf", 44, (295, 2133), "ls", (172, 182, 202)),
    ],
}
def erase_disc(im, cx, cy, r, y0, y1):
    """Efface une bande dans un badge rond avec la couleur médiane du fond."""
    px = im.load(); dark = []
    for y in range(y0, y1):
        for x in range(cx - r, cx + r):
            if (x - cx) ** 2 + (y - cy) ** 2 < r * r and sum(px[x, y]) < 150:
                dark.append(px[x, y])
    dark.sort(key=sum); c = dark[len(dark) // 2]
    for y in range(y0, y1):
        for x in range(cx - r, cx + r):
            if (x - cx) ** 2 + (y - cy) ** 2 < r * r:
                px[x, y] = c
def map_label(im):
    """Remplace le libellé « Chaumont » de la carte, sans toucher au trajet ni à l'épingle."""
    x0, y0, x1, y1 = 1030, 1010, 1168, 1048; px = im.load(); pad = 4
    keep = lambda c: (c[2] > 140 and c[0] < 90) or (c[0] > 220 and 120 < c[1] < 200 and c[2] < 80)
    for y in range(y0, y1):
        a, b = px[x0 - pad, y], px[x1 + pad, y]
        for x in range(x0, x1):
            if keep(px[x, y]): continue
            t = (x - x0 + pad) / (x1 - x0 + 2 * pad)
            px[x, y] = tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))
    big = Image.new("RGBA", (im.width * 2, im.height * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    d.text((1078 * 2, 1040 * 2), "Montval", font=ImageFont.truetype(FD + "Inter-Medium.otf", 60), fill=(60, 64, 67, 255),
           anchor="ls", stroke_width=5, stroke_fill=(255, 255, 255, 235))
    ov = big.resize(im.size, Image.LANCZOS); im.paste(ov, (0, 0), ov)
def erase_box(im, box, pad=5):
    if box[0] == "disc":
        return erase_disc(im, *box[1:])
    x0, y0, x1, y1 = box; px = im.load()
    for y in range(y0, y1):
        a, b = px[x0 - pad, y], px[x1 + pad, y]
        for x in range(x0, x1):
            t = (x - x0 + pad) / (x1 - x0 + 2 * pad)
            px[x, y] = tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))
def draw_text(im, text, font, size, pos, anchor, color):
    S = 4; ov = Image.new("RGBA", (im.width * S // 4, im.height * S // 4), (0, 0, 0, 0))
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    big = Image.new("RGBA", (im.width * 2, im.height * 2), (0, 0, 0, 0))
    ImageDraw.Draw(big).text((pos[0] * 2, pos[1] * 2), text, font=ImageFont.truetype(FD + font, size * 2),
                             fill=color + (255,), anchor=anchor)
    ov = big.resize(im.size, Image.LANCZOS)
    im.paste(ov, (0, 0), ov)
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
    if n == "simulateur":
        map_label(im)
    for box, text, font, size, pos, anchor, color in REPL.get(n, []):
        erase_box(im, box); draw_text(im, text, font, size, pos, anchor, color)
    im.save(f"clean/{n}.png")
print("ok")
