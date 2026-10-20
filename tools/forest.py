# Builds art/forest-backdrop.svg from the forest strips build.sh crops into build/forest/.
# The band is W x H CSS px, the size pet-for-claude draws a backdrop at.
import base64, math, os, random

random.seed(5)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
W, H = 1600, 200
SH = 232  # every strip's height in the source (build.sh crops them)
# Three stretches of the same forest, so the row does not repeat one picture: (id, file, source width).
STRIPS = [('tA', 'build/forest/strip-s.jpg', 250), ('tB', 'build/forest/strip-b-s.jpg', 126), ('tC', 'build/forest/strip-c-s.jpg', 72)]
TW = {id: round(sw * H / SH) for id, _, sw in STRIPS}  # tile widths at the band's height
pick = lambda prev: random.choice([id for id in ['tA', 'tA', 'tB', 'tB', 'tC'] if id != prev])
images = ''.join(f'<image id="{id}" href="data:image/jpeg;base64,{base64.b64encode(open(f, "rb").read()).decode()}" '
                 f'width="{TW[id]}" height="{H}" preserveAspectRatio="none" style="image-rendering: pixelated"/>' for id, f, _ in STRIPS)

# Far row: the strips side by side in a random order, under a blue haze. Repeated as is, never mirrored: the light
# painted into the canopy is diagonal, and mirroring turns it into V shapes.
far, seams, x, prev = [], [], 0, None
while x < W:
    prev = pick(prev); far.append(f'<use href="#{prev}" x="{x}"/>'); x += TW[prev]; seams.append(x)
# Each seam is covered by another strip, faded at both ends, so no trunk or crown ends on a straight cut.
covers = []
for sx in seams[:-1]:
    id = random.choice(['tA', 'tB']); covers.append(f'<use href="#{id}" x="{sx - TW[id] // 2}" mask="url(#soft)"/>')
# Near trees: a few strips drawn larger, standing on the same ground line, faded at the sides into the row behind.
near = []
for nx in sorted(random.sample(range(60, W - 60, 40), 6)):
    id = random.choice(['tB', 'tB', 'tA']); k = random.uniform(1.22, 1.4)
    near.append(f'<g transform="translate({nx - TW[id] * k / 2:.0f} {H - H * k:.1f}) scale({k:.2f})"><use href="#{id}" mask="url(#soft)"/></g>')
# Uneven light: warm pools where the sun breaks through, cool shade between them.
light = []
for i in range(7):
    lx = random.uniform(0, W); rx = random.uniform(80, 170)
    light.append(f'<ellipse cx="{lx:.0f}" cy="{random.uniform(40, 120):.0f}" rx="{rx:.0f}" ry="{rx * 0.7:.0f}" fill="url(#sun)" opacity="{random.uniform(0.45, 0.9):.2f}"/>')
for i in range(5):
    lx = random.uniform(0, W); rx = random.uniform(90, 180)
    light.append(f'<ellipse cx="{lx:.0f}" cy="{random.uniform(30, 110):.0f}" rx="{rx:.0f}" ry="{rx * 0.6:.0f}" fill="url(#shade)" opacity="{random.uniform(0.5, 0.9):.2f}"/>')
tiles = ''.join(far) + ''.join(covers) + f'<rect width="{W}" height="{H}" fill="url(#haze)"/>' + ''.join(near) + ''.join(light)

# Each flower and mote draws its delay and pace from a few shared classes, so one costs ~90 characters.
DELAYS = 8
phase = ''.join(f'.d{i}{{animation-delay:calc(var(--t,0s) - {i * 0.37:.2f}s)}}' for i in range(DELAYS))
pace = '.p0{animation-duration:1.1s}.p1{animation-duration:1.45s}.p2{animation-duration:1.8s}'

rays = []
for i in range(10):
    x = random.uniform(0, W); w = random.uniform(25, 110)
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
        flowers.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({k})"><use class="f d{random.randrange(DELAYS)} p{random.randrange(3)}" href="#{random.choice("abc")}"/></g>')

motes = []
for i in range(60):
    x = random.uniform(0, W); y = random.uniform(80, H - 6); s = random.choice([3, 4, 4])
    motes.append(f'<rect class="m d{random.randrange(DELAYS)}" x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}">
  <!-- Forest band from Chocobrewcoffee's pixel art (personal use, see CREDITS.md), three stretches of canopy, trunks and grass in a hazed far row, a few larger near trees, uneven light, with
       moving light, four rows of swaying pixel flowers and rising motes. Animations take the custom property t as their delay. -->
  <style>
    .r {{ fill: url(#bd-rayg); animation: bd-ray 6s ease-in-out infinite alternate; mix-blend-mode: screen; }}
    .f {{ transform-box: fill-box; transform-origin: 50% 100%; animation: bd-sway 1.5s ease-in-out infinite alternate; }}
    .m {{ fill: #fbffd8; animation: bd-mote 4.5s linear infinite; opacity: 0; }}
    {phase}{pace}
    @keyframes bd-ray {{ 0% {{ transform: translateX(-180px); opacity: 0.2; }} 50% {{ opacity: 1; }} 100% {{ transform: translateX(180px); opacity: 0.3; }} }}
    @keyframes bd-sway {{ from {{ transform: rotate(-16deg) translateX(-1px); }} to {{ transform: rotate(16deg) translateX(1px); }} }}
    @keyframes bd-mote {{ 0% {{ transform: translate(0, 0); opacity: 0; }} 15% {{ opacity: 1; }} 100% {{ transform: translate(34px, -136px); opacity: 0; }} }}
  </style>
  <defs>
    {images}
    <linearGradient id="softg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.28" stop-color="#fff"/>
      <stop offset="0.72" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="soft" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#softg)"/></mask>
    <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#a9cdd6" stop-opacity="0.24"/><stop offset="0.65" stop-color="#a9cdd6" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#a9cdd6" stop-opacity="0.04"/>
    </linearGradient>
    <radialGradient id="sun"><stop offset="0" stop-color="#fff2b0" stop-opacity="0.38"/><stop offset="1" stop-color="#fff2b0" stop-opacity="0"/></radialGradient>
    <radialGradient id="shade"><stop offset="0" stop-color="#0c2427" stop-opacity="0.42"/><stop offset="1" stop-color="#0c2427" stop-opacity="0"/></radialGradient>
    {pf('a', '#c3d3ff', '#8fa9ff')}{pf('b', '#9fb8ff', '#6c8cf0')}{pf('c', '#d9c8ff', '#a98cf2')}
    <linearGradient id="bd-rayg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f4ffd0" stop-opacity="0.7"/><stop offset="1" stop-color="#f4ffd0" stop-opacity="0"/>
    </linearGradient>
    <mask id="bd-fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" rx="8" fill="#fff"/></mask>
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
