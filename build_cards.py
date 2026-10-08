"""Render the four project cards: a hand-drawn scene per add-on (art.py) with a crisp title, description and version chip.

Run:  python build_cards.py        (after build_assets.py has created assets/; needs Microsoft Edge)
Cards are 1200 x 420 and rendered at 1.5x, so they stay sharp when GitHub shows them at 440 px wide.
"""
import sys

from art import SCENES
from build_assets import COMMON, ICONS, render

CARD = """<!doctype html><meta charset=utf-8><style>@@COMMON@@
body{background:#120c0d}
.art{position:absolute;inset:0}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,9,8,.92) 0,rgba(13,9,8,.8) 38%,rgba(13,9,8,.4) 54%,rgba(13,9,8,0) 68%)}
.frame{position:absolute;inset:10px;border:5px solid var(--ink);box-shadow:inset 0 0 0 3px var(--brown),0 0 0 2px rgba(0,0,0,.4)}
.bar{position:absolute;left:10px;top:10px;bottom:10px;width:20px;background:@@ACCENT@@;border-right:5px solid var(--ink)}
.ico{position:absolute;left:68px;top:42px;width:84px;height:84px;stroke:@@ACCENT@@;fill:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;
 filter:drop-shadow(3px 3px 0 #0d0908)}
h2{position:absolute;left:170px;top:22px;font-family:'Bebas Neue',Impact,sans-serif;font-weight:400;font-size:124px;line-height:1;
 color:#f4eddb;letter-spacing:.03em;text-shadow:5px 5px 0 #0d0908,-1px -1px 0 #0d0908,1px -1px 0 #0d0908,-1px 1px 0 #0d0908}
p{position:absolute;left:68px;top:170px;width:560px;font-family:'Courier Prime','Courier New',monospace;font-weight:700;font-size:37px;line-height:1.3;
 color:#f1ead8;text-shadow:2px 2px 0 #0d0908,0 0 10px rgba(0,0,0,.9)}
.chip{position:absolute;left:68px;bottom:38px;font-family:'Courier Prime','Courier New',monospace;font-weight:700;font-size:27px;color:#0d0908;
 background:@@ACCENT@@;padding:4px 16px;border:4px solid #0d0908;box-shadow:4px 4px 0 rgba(0,0,0,.6)}
</style><body><div class=art>@@SCENE@@</div><div class=shade></div><div class=frame></div><div class=bar></div>
<svg class=ico viewBox="0 0 64 64">@@ICON@@</svg><h2>@@TITLE@@</h2><p>@@TEXT@@</p><div class=chip>@@CHIP@@</div></body>"""

CARDS = [
    ("terrain-blend", "TERRAIN BLEND", "Blend any number of PBR textures with vertex groups.", "Blender 5.0-5.2  v1.1.0", "#6fae5c", "terrain"),
    ("retopo-kit", "RETOPO KIT", "One-click quad retopology for props, vehicles and characters.", "Blender 5.0-5.2  v1.0.0", "#e0cf45", "retopo"),
    ("fivem-toolkit", "FIVEM TOOLKIT", "Check, fix and export props, interiors and peds for FiveM.", "Blender 5.0-5.2  v0.1.1", "#d9534a", "fivem"),
    ("ue5-bridge", "UE5 BRIDGE", "Clean FBX export for Unreal Engine 5, with root motion.", "Blender 5.0-5.2  v0.2.0", "#d8cfbd", "ue5"),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for slug, title, text, chip, accent, icon in CARDS:
        if only and slug not in only:
            continue
        html = (CARD.replace("@@TITLE@@", title).replace("@@TEXT@@", text).replace("@@CHIP@@", chip)
                .replace("@@ACCENT@@", accent).replace("@@ICON@@", ICONS[icon]).replace("@@SCENE@@", SCENES[slug]()))
        render(html, f"card-{slug}", 1200, 420)
