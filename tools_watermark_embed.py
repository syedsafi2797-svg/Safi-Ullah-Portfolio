"""Watermark every embedded image in the case-study HTML files.
Bakes a diagonal repeated 'safiullahportfolio.vercel.app' mark into the image
data itself, so extraction (DevTools, URL, base64) always yields the branded image.
Run: python watermark_embed.py
"""
import os, re, io, base64, sys
from PIL import Image, ImageDraw, ImageFont

CS = r'C:\Users\dell\Documents\portfolio-upgrade\case-studies'
TEXT = 'safiullahportfolio.vercel.app'
FONT = r'C:\Windows\Fonts\arialbd.ttf'
GOLD = (212, 168, 67, 88)          # #D4A843 at ~35% alpha
ANGLE = -30

def load_font(px):
    for f in (FONT, r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, px)
            except Exception:
                pass
    return ImageFont.load_default()

def watermark(raw, mime):
    img = Image.open(io.BytesIO(raw)).convert('RGBA')
    w, h = img.size
    fs = max(16, int(min(w, h) * 0.045))
    font = load_font(fs)
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    bbox = d.textbbox((0, 0), TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    dx, dy = tw + fs * 3, th + fs * 4          # tile spacing
    for y in range(-h - th, h + th, dy):
        for x in range(-w - tw, w + tw, dx):
            d.text((x - bbox[0], y - bbox[1]), TEXT, font=font, fill=GOLD)
    layer = layer.rotate(ANGLE, expand=False, resample=Image.BICUBIC)
    out = Image.alpha_composite(img, layer)
    buf = io.BytesIO()
    if mime == 'image/png':
        out.convert('RGBA').save(buf, 'PNG', optimize=True)
        mime_out = 'image/png'
    else:
        out.convert('RGB').save(buf, 'JPEG', quality=80, optimize=True, progressive=True)
        mime_out = 'image/jpeg'
    return buf.getvalue(), mime_out

total = 0
for hf in sorted(f for f in os.listdir(CS) if f.endswith('.html')):
    p = os.path.join(CS, hf)
    html = open(p, encoding='utf-8', errors='replace').read()

    def repl(m):
        global total
        mime, b64 = m.group(1), m.group(2)
        try:
            raw = base64.b64decode(b64, validate=True)
        except Exception:
            return m.group(0)
        new_raw, mime_out = watermark(raw, mime)
        total += 1
        return f'data:{mime_out};base64,' + base64.b64encode(new_raw).decode()

    html2 = re.sub(r'data:(image/(?:jpeg|png));base64,([A-Za-z0-9+/=]+)', repl, html)
    if html2 != html:
        open(p, 'w', encoding='utf-8', newline='').write(html2)
        print(f'watermarked: {hf}')

print(f'\n{total} images watermarked')
