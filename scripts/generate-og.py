from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = Path(__file__).resolve().parents[1] / "assets" / "og-pkfit.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

bg = (8, 8, 8)
ink = (245, 245, 245)
muted = (145, 145, 145)
gold = (201, 168, 76)
line = (42, 42, 42)

image = Image.new("RGB", (W, H), bg)
draw = ImageDraw.Draw(image)
regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
black = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

font_wordmark = ImageFont.truetype(bold, 27)
font_kicker = ImageFont.truetype(bold, 19)
font_head = ImageFont.truetype(black, 76)
font_offer = ImageFont.truetype(bold, 28)
font_small = ImageFont.truetype(regular, 20)

# restrained grid
a = 0
for x in range(0, W, 40):
    draw.line((x, 0, x, H), fill=(14, 14, 14), width=1)
for y in range(0, H, 40):
    draw.line((0, y, W, y), fill=(14, 14, 14), width=1)

# frame and signal line
draw.rounded_rectangle((50, 46, W - 50, H - 46), radius=18, outline=line, width=2)
draw.rectangle((50, 46, 58, H - 46), fill=gold)

draw.text((92, 82), "PKFIT", font=font_wordmark, fill=ink)
draw.text((92, 130), "TRAINING STRUCTURE", font=font_kicker, fill=gold)

draw.text((88, 196), "THE STANDARD", font=font_head, fill=ink)
draw.text((88, 280), "HAS TWO LANES.", font=font_head, fill=muted)

# offer rail
rail_y = 440
draw.line((92, rail_y - 24, W - 92, rail_y - 24), fill=line, width=2)
draw.text((92, rail_y), "LITE", font=font_offer, fill=ink)
draw.text((178, rail_y + 3), "$20 ONCE · SELF-GUIDED", font=font_small, fill=muted)
draw.text((650, rail_y), "STANDARD", font=font_offer, fill=ink)
draw.text((830, rail_y + 3), "$250/MO · COACHING", font=font_small, fill=muted)

draw.text((92, 533), "OPERATEFITNESS.APP", font=font_kicker, fill=gold)
draw.text((W - 420, 533), "STRUCTURE OUTLIVES MOTIVATION.", font=font_small, fill=muted)

image.save(OUT, "PNG", optimize=True)
print(f"generated={OUT} size={image.size[0]}x{image.size[1]}")
