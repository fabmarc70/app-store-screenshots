# Écrans iPad 13" (2064x2752) construits depuis les captures iPhone nettoyées (clean/) :
# mise à l'échelle sur la largeur (sans déformation), barre d'état iPad, recadrage.
from PIL import Image, ImageDraw, ImageFont
W, H = 2064, 2752
K = W / 1320                      # facteur d'échelle iPhone -> iPad
FD = "/usr/share/fonts/opentype/inter/"
def ipad(name, out):
    im = Image.open(f"clean/{name}.png").convert("RGB")
    px = im.load()
    # 1. supprime la haute barre d'état iPhone (lignes 40..150) en gardant le dégradé de l'en-tête
    top = im.crop((0, 0, 1320, 40)); rest = im.crop((0, 150, 1320, 2868))
    body = Image.new("RGB", (1320, 40 + rest.height)); body.paste(top, (0, 0)); body.paste(rest, (0, 40))
    # efface tout texte résiduel dans la bande du haut (interpolation verticale)
    bp = body.load()
    for x in range(1320):
        a, b = bp[x, 2], bp[x, 46]
        for y in range(3, 46):
            t = (y - 2) / 44; bp[x, y] = tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))
    # 2. mise à l'échelle sur la largeur iPad, puis recadrage à la hauteur iPad
    big = body.resize((W, round(body.height * K)), Image.LANCZOS).crop((0, 0, W, H))
    # 3. barre d'état iPad : heure + date à gauche, Wi-Fi + batterie à droite
    S = 3; ov = Image.new("RGBA", (W * S, 80 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); Wh = (255, 255, 255, 255)
    f = ImageFont.truetype(FD + "Inter-SemiBold.otf", 32 * S)
    d.text((48 * S, 50 * S), "9:41   lun. 25 nov.", font=f, fill=Wh, anchor="ls")
    cx, cy = 1812 * S, 52 * S                        # Wi-Fi
    d.pieslice((cx - 11 * S, cy - 11 * S, cx + 11 * S, cy + 11 * S), 225, 315, fill=Wh)
    for r in (21, 32): d.arc((cx - r * S, cy - r * S, cx + r * S, cy + r * S), 225, 315, fill=Wh, width=6 * S)
    d.text((1938 * S, 50 * S), "100 %", font=ImageFont.truetype(FD + "Inter-SemiBold.otf", 28 * S), fill=Wh, anchor="rs")
    d.rounded_rectangle((1950 * S, 27 * S, 2006 * S, 53 * S), radius=8 * S, outline=(255, 255, 255, 150), width=3 * S)
    d.rounded_rectangle((1955 * S, 32 * S, 2001 * S, 48 * S), radius=5 * S, fill=Wh)
    d.rounded_rectangle((2009 * S, 35 * S, 2014 * S, 45 * S), radius=2 * S, fill=(255, 255, 255, 150))
    ov = ov.resize((W, 80), Image.LANCZOS); big.paste(ov, (0, 0), ov)
    big.save(out)
if __name__ == "__main__":
    import os; os.makedirs("clean-ipad", exist_ok=True)
    for n in ["planning", "bulletin-analyse", "simulateur"]:
        ipad(n, f"clean-ipad/{n}.png"); print("ok", n)
