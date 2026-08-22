#!/usr/bin/env python3
"""Banner ASCII animado en SVG (SMIL, sin JS) para el README de GitHub."""
import pyfiglet

FS   = 13.0    # font-size
CW   = 8.10    # avance estimado (rango seguro 7.8-8.45)
LH   = 16.6    # alto de linea
PADX = 34.0
PADT = 26.0
GAP  = 10.0
DUR  = 7.0

FONT = "monospace"


def art(word):
    rows = pyfiglet.figlet_format(word, font="doom").split("\n")
    while rows and not rows[0].strip():
        rows.pop(0)
    while rows and not rows[-1].strip():
        rows.pop()
    n = max(len(r.rstrip()) for r in rows)
    return [r.rstrip().ljust(n) for r in rows], n   # padded => misma x para todas


blocks = [art("SOFTWARE"), art("ENGINEERING")]
maxlen = max(n for _, n in blocks)

W = maxlen * CW + PADX * 2
n_lines = sum(len(rows) for rows, _ in blocks)
H = PADT + n_lines * LH + GAP + 44

esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

out, y = [], PADT + FS
for i, (rows, n) in enumerate(blocks):
    if i:
        y += GAP
    x = (W - n * CW) / 2
    spans = "".join(
        f'<tspan x="{x:.1f}" dy="{0 if j == 0 else LH}" '
        f'xml:space="preserve">{esc(r)}</tspan>'
        for j, r in enumerate(rows)
    )
    out.append(f'<text y="{y:.1f}">{spans}</text>')
    y += len(rows) * LH

art_top, art_bot = PADT, y
sub_y = art_bot + 26
k_in, k_hold = 0.30, 0.86
spl = "0.2 0 0.1 1;0 0 1 1;0.6 0 0.2 1"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}"
     viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Software Engineering">
  <defs>
    <clipPath id="wipe">
      <rect x="0" y="0" height="{H:.0f}" width="0">
        <animate attributeName="width" values="0;{W:.0f};{W:.0f};0"
                 keyTimes="0;{k_in};{k_hold};1" dur="{DUR}s"
                 repeatCount="indefinite" calcMode="spline" keySplines="{spl}"/>
      </rect>
    </clipPath>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="#0A0A0A"/>
  <rect x="0.5" y="0.5" width="{W-1:.0f}" height="{H-1:.0f}" rx="10"
        fill="none" stroke="#1A1A1A"/>

  <g clip-path="url(#wipe)" font-family="{FONT}" font-size="{FS}" fill="#ffffff">
    {chr(10) + "    " + (chr(10) + "    ").join(out)}
  </g>

  <rect x="0" y="{art_top:.0f}" width="{W:.0f}" height="24" fill="url(#scan)">
    <animate attributeName="y" values="{art_top:.0f};{art_bot:.0f};{art_top:.0f}"
             dur="4s" repeatCount="indefinite"/>
  </rect>

  <rect x="0" y="{art_top+2:.0f}" width="2" height="{art_bot-art_top-4:.0f}" fill="#fff">
    <animate attributeName="x" values="0;{W-2:.0f};{W-2:.0f};0"
             keyTimes="0;{k_in};{k_hold};1" dur="{DUR}s"
             repeatCount="indefinite" calcMode="spline" keySplines="{spl}"/>
    <animate attributeName="opacity" values="1;1;0;1;1"
             keyTimes="0;0.45;0.5;0.95;1" dur="1s" repeatCount="indefinite"/>
  </rect>

  <text font-family="{FONT}" font-size="10" fill="#7d7d7d" letter-spacing="5" x="{W/2:.0f}" y="{sub_y:.0f}" text-anchor="middle" opacity="0">
    SECURITY  ·  SYSTEMS  ·  MOBILE
    <animate attributeName="opacity" values="0;0;0.95;0.95;0"
             keyTimes="0;{k_in};{k_in+0.05};{k_hold};1"
             dur="{DUR}s" repeatCount="indefinite"/>
  </text>
</svg>
'''

open("ascii-banner.svg", "w", encoding="utf-8").write(svg)
print(f"W={W:.0f} H={H:.0f} cols={maxlen} lines={n_lines}")
