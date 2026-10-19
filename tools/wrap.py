# usage: python3 wrap.py <dir with color.jpg + mask.png> <out.svg> <max side px>
import base64, subprocess, sys, os
d, out, side = sys.argv[1], sys.argv[2], sys.argv[3]
subprocess.run(['sips', '-Z', side, '-s', 'formatOptions', '82', f'{d}/color.jpg', '--out', f'{d}/color-s.jpg'], check=True, capture_output=True)
subprocess.run(['sips', '-Z', side, f'{d}/mask.png', '--out', f'{d}/mask-s.png'], check=True, capture_output=True)
W, H = [int(subprocess.check_output(['sips', '-g', k, f'{d}/color-s.jpg']).split()[-1]) for k in ('pixelWidth', 'pixelHeight')]
c = base64.b64encode(open(f'{d}/color-s.jpg', 'rb').read()).decode()
m = base64.b64encode(open(f'{d}/mask-s.png', 'rb').read()).decode()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
  <style>
    .petal {{ transform-box: fill-box; transform-origin: 50% 50%; animation: fall 7s linear infinite; animation-delay: var(--t, 0s); opacity: 0; }}
    .petal.p2 {{ animation-delay: calc(var(--t, 0s) + 2.3s); }}
    .petal.p3 {{ animation-delay: calc(var(--t, 0s) + 4.6s); }}
    @keyframes fall {{
      0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0; }}
      12% {{ opacity: 0.95; }}
      85% {{ opacity: 0.85; }}
      100% {{ transform: translate(-50px, {H - 30}px) rotate(280deg); opacity: 0; }}
    }}
  </style>
  <defs>
    <mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <image href="data:image/png;base64,{m}" width="{W}" height="{H}"/>
    </mask>
  </defs>
  <image href="data:image/jpeg;base64,{c}" width="{W}" height="{H}" mask="url(#cut)"/>
  <g fill="#c9d6ff" stroke="#7d93e6" stroke-width="1.2">
    <ellipse class="petal" cx="{W * 0.5:.0f}" cy="10" rx="6" ry="3.6"/>
    <ellipse class="petal p2" cx="{W * 0.85:.0f}" cy="6" rx="5" ry="3"/>
    <ellipse class="petal p3" cx="{W * 0.2:.0f}" cy="12" rx="5.5" ry="3.3"/>
  </g>
</svg>
'''
open(out, 'w').write(svg)
print(out, W, H, len(svg))
