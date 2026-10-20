#!/bin/sh
# Rebuilds art/*.svg from sources/*.jpg. macOS only: it uses Vision (subject cutout), CoreImage and sips.
set -e
cd "$(dirname "$0")/.."
T=tools
B=build
mkdir -p $B/ref $B/staff $B/sleep $B/forest

# Himmel and Frieren sitting in flowers: crop the pair, cut them out of the background.
swift $T/crop.swift sources/frieren-himmel-ref.jpg $B/ref/crop.jpg 0 600 736 520
swift $T/cutout.swift $B/ref/crop.jpg $B/ref
python3 $T/wrap.py $B/ref art/frieren-himmel-ref.svg 400

# Frieren with her staff, and the pair asleep: cut out whole.
swift $T/cutout.swift sources/frieren-staff.jpg $B/staff
python3 $T/wrap.py $B/staff art/frieren-staff.svg 340
swift $T/cutout.swift sources/frieren-himmel-sleep.jpg $B/sleep
python3 $T/wrap.py $B/sleep art/frieren-himmel-sleep.svg 340

# Forest band: trunks and grass from the left of the picture, mirror tiled, with light, flowers and motes on top.
swift $T/crop.swift sources/forest.jpg $B/forest/strip.jpg 0 70 250 232
sips -Z 250 -s formatOptions 50 $B/forest/strip.jpg --out $B/forest/strip-s.jpg >/dev/null
swift $T/crop.swift sources/forest.jpg $B/forest/strip-b.jpg 392 70 126 232
sips -Z 232 -s formatOptions 50 $B/forest/strip-b.jpg --out $B/forest/strip-b-s.jpg >/dev/null
swift $T/crop.swift sources/forest.jpg $B/forest/strip-c.jpg 664 70 72 232
sips -Z 232 -s formatOptions 50 $B/forest/strip-c.jpg --out $B/forest/strip-c-s.jpg >/dev/null
python3 $T/forest.py
