# Builds art/forest-backdrop.svg from build/forest/strip-s.jpg (see build.sh).
# The band is W x H CSS px, the size pet-for-claude draws a backdrop at.
import base64, math, os, random

random.seed(5)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
W, H = 1600, 200
SW, SH = 250, 232  # the strip's size (build.sh crops it)
TW = round(SW * H / SH)  # one tile at the band's height
b = base64.b64encode(open('build/forest/strip-s.jpg', 'rb').read()).decode()
# Repeated as is, not mirrored: the light painted into the canopy is diagonal, and mirroring turns it into V shapes.
# A second row of tiles, half a tile along and faded at both ends, lies over the first: its opaque middle covers each
# seam of the row beneath, so no trunk or crown ends on a straight cut.
tiles = (''.join(f'<use href="#t" x="{i*TW}"/>' for i in range(math.ceil(W / TW) + 1))
         + '<g mask="url(#bd-seam)">' + ''.join(f'<use href="#t" x="{i*TW - TW//2}"/>' for i in range(math.ceil(W / TW) + 2)) + '</g>')

# Each flower and mote draws its delay and pace from a few shared classes, so one costs ~90 characters.
DELAYS = 8
phase = ''.join(f'.d{i}{{animation-delay:calc(var(--t,0s) - {i * 0.37:.2f}s)}}' for i in range(DELAYS))
pace = '.p0{animation-duration:1.1s}.p1{animation-duration:1.45s}.p2{animation-duration:1.8s}'

rays = []
for i in range(10):
    x = random.uniform(0, W); w = random.uniform(40, 90)
    rays.append(f'<polygon class="r d{random.randrange(DELAYS)}" points="{x:.0f},-10 {x+w:.0f},-10 {x+w-136:.0f},{H+10} {x-136-w*0.4:.0f},{H+10}"/>')

def pf(id, c1, c2):
    r = lambda x, y, c: f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>'
    return (f'<g id="{id}">' + r(0, 1, '#4f8a4a') + r(0, 2, '#4f8a4a') + r(0, 3, '#3f7440') + r(1, 2, '#5e9c55') + r(-1, 3, '#5e9c55')
            + r(-1, -1, c1) + r(0, -1, c1) + r(1, -1, c1) + r(-1, 0, c2) + r(1, 0, c2) + r(0, 1, c2) + r(0, 0, '#fdf6d8') + '</g>')

flowers = []
# (count, y from, y to, size from, size to): back row to front row, in band px.
for n, ymin, ymax, kmin, kmax in [(55, 128, 140, 3, 4), (58, 142, 154, 4, 5), (56, 152, 164, 4, 6), (60, 164, 180, 5, 7)]:
    for i in range(n):
        x = i * W / n + random.uniform(-12, 12); y = random.uniform(ymin, ymax); k = random.randint(kmin, kmax)
        # The CSS animation sets `transform`, so the place and size go on a wrapping <g>.
        # Every other flower sways; the rest stand still, which halves what the desktop repaints each frame.
        sway = f' class="f d{random.randrange(DELAYS)} p{random.randrange(3)}"' if i % 2 == 0 else ''
        flowers.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({k})"><use{sway} href="#{random.choice("abc")}"/></g>')

motes = []
for i in range(60):
    x = random.uniform(0, W); y = random.uniform(80, H - 6); s = random.choice([3, 4, 4])
    motes.append(f'<rect class="m d{random.randrange(DELAYS)}" x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}">
  <!-- Forest band from Chocobrewcoffee's pixel art (personal use, see CREDITS.md), canopy, trunks and grass tiled, with
       moving light, four rows of swaying pixel flowers and rising motes. Animations take the custom property t as their delay. -->
  <style>
    .r {{ fill: url(#bd-rayg); animation: bd-ray 6s ease-in-out infinite alternate; }}
    .f {{ transform-box: fill-box; transform-origin: 50% 100%; animation: bd-sway 1.5s ease-in-out infinite alternate; }}
    .m {{ fill: #fbffd8; animation: bd-mote 4.5s linear infinite; opacity: 0; }}
    {phase}{pace}
    @keyframes bd-ray {{ 0% {{ transform: translateX(-180px); opacity: 0.2; }} 50% {{ opacity: 1; }} 100% {{ transform: translateX(180px); opacity: 0.3; }} }}
    @keyframes bd-sway {{ from {{ transform: rotate(-16deg) translateX(-1px); }} to {{ transform: rotate(16deg) translateX(1px); }} }}
    @keyframes bd-mote {{ 0% {{ transform: translate(0, 0); opacity: 0; }} 15% {{ opacity: 1; }} 100% {{ transform: translate(34px, -136px); opacity: 0; }} }}
  </style>
  <defs>
    <image id="t" href="data:image/jpeg;base64,{b}" width="{TW}" height="{H}" preserveAspectRatio="none" style="image-rendering: pixelated"/>
    {pf('a', '#c3d3ff', '#8fa9ff')}{pf('b', '#9fb8ff', '#6c8cf0')}{pf('c', '#d9c8ff', '#a98cf2')}
    <linearGradient id="bd-rayg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f4ffd0" stop-opacity="0.7"/><stop offset="1" stop-color="#f4ffd0" stop-opacity="0"/>
    </linearGradient>
    <mask id="bd-fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" rx="8" fill="#fff"/></mask>
    <linearGradient id="bd-seamg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.3" stop-color="#fff"/>
      <stop offset="0.7" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <pattern id="bd-seamp" patternUnits="userSpaceOnUse" x="{-TW//2}" y="0" width="{TW}" height="{H}"><rect width="{TW}" height="{H}" fill="url(#bd-seamg)"/></pattern>
    <mask id="bd-seam" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#bd-seamp)"/></mask>
  </defs>
  <g mask="url(#bd-fade)">
    {tiles}
    {''.join(rays)}
    {''.join(motes)}
    {''.join(flowers)}
  </g>
</svg>
'''
open('art/forest-backdrop.svg', 'w').write(svg)
print('chars', len(svg), 'flowers', len(flowers))
