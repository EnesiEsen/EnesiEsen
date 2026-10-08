"""Render the profile images (banner, avatar, project cards, toolbox) from HTML with headless Edge.

Run:  python build_assets.py            (needs Microsoft Edge, which ships with Windows 11)

The look follows the "Walter" drawing: charcoal ink lines, a dark maroon-brown room, muted jacket browns, a green
pharmacy cross and a red-and-yellow book cover. The drawing itself is assets/walter-source.webp.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
SRC = ASSETS / "_src"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WALTER = (ASSETS / "walter-source.webp").as_uri()

COMMON = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap');
:root{--bg:#17100f;--bg2:#2a1f1d;--paper:#e2d9c6;--paper2:#b8b0a0;--brown:#6a5240;--green:#3f9a5b;--red:#c0392f;--yellow:#e0cf45;--ink:#0d0908}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg)}
body{position:relative;font-family:'Special Elite','Courier Prime',monospace;color:var(--paper)}
.grain::after{content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:overlay;opacity:.5;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.vignette::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:5;
 background:radial-gradient(ellipse at 60% 45%,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%)}
.cross{display:inline-block;width:.8em;height:.8em;position:relative;vertical-align:-.05em}
.cross::before,.cross::after{content:"";position:absolute;background:var(--green);border:2px solid var(--ink)}
.cross::before{left:33%;top:0;width:34%;height:100%}.cross::after{top:33%;left:0;height:34%;width:100%}
"""

BANNER = """<!doctype html><meta charset=utf-8><style>@@COMMON@@
body{background:linear-gradient(100deg,#120b0a 0%,#1e1513 52%,#2c211d 100%)}
.art{position:absolute;right:0;top:0;width:900px;height:100%;
 background:url('@@WALTER@@') 62% 20%/1010px auto no-repeat;filter:contrast(1.06) saturate(.92) brightness(.95);
 -webkit-mask-image:linear-gradient(to right,transparent 0,#000 46%);mask-image:linear-gradient(to right,transparent 0,#000 46%)}
.txt{position:absolute;left:84px;top:0;height:100%;display:flex;flex-direction:column;justify-content:center;z-index:6}
.tag{font-size:26px;color:var(--green);letter-spacing:.08em;margin-bottom:6px}
h1{font-family:'Bebas Neue',Impact,sans-serif;font-weight:400;font-size:190px;line-height:.86;color:var(--paper);
 text-shadow:7px 7px 0 var(--ink),9px 9px 0 rgba(192,57,47,.55);letter-spacing:.02em}
.sub{margin-top:22px;font-size:32px;color:var(--paper2)}
.sub b{color:var(--yellow);font-weight:400}
.tr{margin-top:6px;font-size:23px;color:#8c8374}
.rule{position:absolute;left:84px;right:84px;bottom:42px;height:3px;background:repeating-linear-gradient(90deg,var(--brown) 0 18px,transparent 18px 28px);z-index:6}
</style><body class="grain vignette"><div class=art></div>
<div class=txt><div class=tag><span class=cross></span>&nbsp; PROFILE / 2026</div>
<h1>Enes Esen</h1>
<div class=sub>I build tools for <b>games</b>, <b>servers</b> &amp; <b>production assets</b>.</div>
<div class=tr>Oyun, sunucu ve üretim malzemeleri için araçlar yapıyorum.</div></div><div class=rule></div></body>"""

AVATAR = """<!doctype html><meta charset=utf-8><style>@@COMMON@@
.face{position:absolute;inset:0;background:url('@@WALTER@@') -150px -20px/1230px auto no-repeat;filter:contrast(1.08) saturate(.95)}
body::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 46%,rgba(0,0,0,0) 52%,rgba(8,4,3,.7) 100%)}
</style><body><div class=face></div></body>"""

TOOLBOX = """<!doctype html><meta charset=utf-8><style>@@COMMON@@
body{background:linear-gradient(100deg,#150e0d,#271c19)}
.frame{position:absolute;inset:10px;border:4px solid var(--ink);box-shadow:inset 0 0 0 2px var(--brown),8px 8px 0 rgba(0,0,0,.55)}
h2{position:absolute;left:44px;top:26px;font-family:'Bebas Neue',Impact,sans-serif;font-weight:400;font-size:62px;color:var(--paper);text-shadow:4px 4px 0 var(--ink);letter-spacing:.04em}
.row{position:absolute;left:44px;right:44px;display:flex;gap:16px;flex-wrap:wrap}
.r1{top:112px}.r2{top:196px}
.c{font-size:27px;padding:8px 20px;border:3px solid var(--ink);background:var(--bg2);color:var(--paper);box-shadow:5px 5px 0 rgba(0,0,0,.5)}
.c i{display:inline-block;width:14px;height:14px;margin-right:12px;border:2px solid var(--ink);vertical-align:0}
.note{position:absolute;left:44px;bottom:22px;font-size:20px;color:#8c8374}
</style><body class=grain><div class=frame></div><h2>Toolbox</h2>
<div class="row r1"><span class=c><i style="background:#e87d0d"></i>Blender 5.x</span><span class=c><i style="background:#3f7fbf"></i>Python</span><span class=c><i style="background:#3f9a5b"></i>Geometry Nodes</span><span class=c><i style="background:#c0392f"></i>Sollumz</span></div>
<div class="row r2"><span class=c><i style="background:#e0cf45"></i>FiveM</span><span class=c><i style="background:#8c8374"></i>Minecraft / KubeJS</span><span class=c><i style="background:#6a5240"></i>Unreal Engine 5 (next)</span></div>
<div class=note>// Unreal Engine 5 is next: the bridge add-on is ready, the engine is not installed yet</div></body>"""

ICONS = {
    "terrain": '<path d="M4 50 L22 22 L32 36 L42 18 L60 50 Z"/><path d="M4 58 H60"/>',
    "scatter": '<path d="M8 58 Q10 42 4 32 M20 58 Q20 36 26 22 M32 58 Q36 40 46 32 M44 58 Q48 48 58 44"/>'
               '<circle cx="14" cy="14" r="4"/><circle cx="40" cy="12" r="3"/><circle cx="54" cy="22" r="4"/>',
    "retopo": '<path d="M8 8 H56 V56 H8 Z M8 32 H56 M32 8 V56 M20 8 V32 M44 32 V56"/>',
    "fivem": '<path d="M32 6 L56 18 V46 L32 58 L8 46 V18 Z M8 18 L32 30 L56 18 M32 30 V58"/>',
    "ue5": '<circle cx="32" cy="12" r="7"/><path d="M32 19 V40 M32 26 L16 34 M32 26 L48 34 M32 40 L20 58 M32 40 L44 58"/>',
}
def render(html, name, width, height, scale=1.5):
    page = SRC / f"{name}.html"
    page.write_text(html.replace("@@COMMON@@", COMMON).replace("@@WALTER@@", WALTER), encoding="utf-8")
    out = ASSETS / f"{name}.png"
    out.unlink(missing_ok=True)
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
           "--virtual-time-budget=9000", f"--window-size={width},{height}", f"--screenshot={out}", page.as_uri()]
    subprocess.run(cmd, check=False, capture_output=True, timeout=120)
    if not out.exists():
        sys.exit(f"render failed: {name}")
    print(out)


if __name__ == "__main__":
    render(BANNER, "banner", 1600, 520)
    render(AVATAR, "avatar", 800, 800)
    render(TOOLBOX, "toolbox", 1200, 300)
