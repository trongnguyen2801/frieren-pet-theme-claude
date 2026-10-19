# Builds art/forest-backdrop.svg from build/forest/strip-s.jpg (see build.sh).
import base64, math, random, os
random.seed(5)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
W, H = 1600, 100
TW = round(250 * H / 160)
b = base64.b64encode(open('build/forest/strip-s.jpg', 'rb').read()).decode()
tiles = ''.join(f'<use href="#bd-tile" xlink:href="#bd-tile" x="{i*TW}"/>' if i % 2 == 0 else
                f'<use href="#bd-tile" xlink:href="#bd-tile" transform="translate({(i+1)*TW} 0) scale(-1 1)"/>'
                for i in range(math.ceil(W / TW) + 1))
rays = []
for i in range(9):
    x = random.uniform(0, W); w = random.uniform(20, 46); d = random.uniform(0, 7)
    rays.append(f'<polygon class="bd-ray" style="animation-delay:calc(var(--t,0s) - {d:.1f}s)" points="{x:.0f},-10 {x+w:.0f},-10 {x+w-70:.0f},110 {x-70-w*0.4:.0f},110"/>')
# Pixel flowers, one unit = 1px before scale: stem below, five-petal head with a pale centre.
def pf(id, c1, c2):
    r = lambda x, y, c: f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>'
    return (f'<g id="{id}">' + r(0, 1, '#4f8a4a') + r(0, 2, '#4f8a4a') + r(0, 3, '#3f7440') + r(1, 2, '#5e9c55') + r(-1, 3, '#5e9c55')
            + r(-1, -1, c1) + r(0, -1, c1) + r(1, -1, c1) + r(-1, 0, c2) + r(1, 0, c2) + r(0, 1, c2) + r(0, 0, '#fdf6d8') + '</g>')
flowers = []
for row, (n, ymin, ymax, kmin, kmax) in enumerate([(56, 74, 80, 2, 2), (60, 82, 88, 2, 3), (58, 86, 92, 2, 3), (62, 90, 97, 3, 4)]):
    for i in range(n):
        x = i * W / n + random.uniform(-9, 9); y = random.uniform(ymin, ymax); k = random.choice(range(kmin, kmax + 1))
        v = random.choice(['bd-fa', 'bd-fb', 'bd-fc'])
        d = random.uniform(0, 3); dur = random.uniform(1.1, 2.0)
        # The CSS animation sets `transform`, so the place and size go on a wrapping <g>.
        flowers.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({k})"><use class="bd-flower" '
                       f'style="animation-delay:calc(var(--t,0s) - {d:.2f}s);animation-duration:{dur:.2f}s" href="#{v}" xlink:href="#{v}"/></g>')
motes = []
for i in range(22):
    x = random.uniform(0, W); y = random.uniform(40, 95); d = random.uniform(0, 5); s = random.choice([2, 2, 3])
    motes.append(f'<rect class="bd-mote" style="animation-delay:calc(var(--t,0s) - {d:.1f}s)" x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}">
  <!-- Forest band from Chocobrewcoffee's pixel art (personal use, see CREDITS.txt), trunks and grass mirror tiled, with
       moving light, four rows of swaying pixel flowers and rising motes. Animations take the custom property t as their delay. -->
  <style>
    .bd-ray {{ fill: url(#bd-rayg); animation: bd-ray 6s ease-in-out infinite alternate; mix-blend-mode: screen; }}
    .bd-flower {{ transform-box: fill-box; transform-origin: 50% 100%; animation: bd-sway 1.5s ease-in-out infinite alternate; }}
    .bd-mote {{ fill: #fbffd8; animation: bd-mote 4.5s linear infinite; opacity: 0; }}
    @keyframes bd-ray {{ 0% {{ transform: translateX(-110px); opacity: 0.2; }} 50% {{ opacity: 1; }} 100% {{ transform: translateX(110px); opacity: 0.3; }} }}
    @keyframes bd-sway {{ from {{ transform: rotate(-16deg) translateX(-1px); }} to {{ transform: rotate(16deg) translateX(1px); }} }}
    @keyframes bd-mote {{ 0% {{ transform: translate(0, 0); opacity: 0; }} 15% {{ opacity: 1; }} 100% {{ transform: translate(22px, -70px); opacity: 0; }} }}
  </style>
  <defs>
    <image id="bd-tile" href="data:image/jpeg;base64,{b}" width="{TW}" height="{H}" preserveAspectRatio="none" style="image-rendering: pixelated"/>
    {pf('bd-fa', '#c3d3ff', '#8fa9ff')}{pf('bd-fb', '#9fb8ff', '#6c8cf0')}{pf('bd-fc', '#d9c8ff', '#a98cf2')}
    <linearGradient id="bd-rayg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f4ffd0" stop-opacity="0.7"/><stop offset="1" stop-color="#f4ffd0" stop-opacity="0"/>
    </linearGradient>
    <mask id="bd-fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" rx="12" fill="#fff"/></mask>
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
print('chars', len(svg))
