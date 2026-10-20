# Frieren pet theme

A theme for the `pet-for-claude` Claude Code mod: Frieren (and Himmel) drawn sharp in the
desktop app's Code tab, over an animated forest band.

**Personal use only.** The pictures belong to their artists (see `CREDITS.md`). Keep this repository private.

## What is here

| Path | What |
| --- | --- |
| `themes/frieren-forest.theme.json` | Frieren with her staff over the forest band, light purple status text |
| `themes/frieren-himmel-3.theme.json` | One picture per state: staff while working, the pair asleep while sleeping, the pair in flowers otherwise; no band |
| `art/` | The SVGs the themes name: transparent cutouts, and the 1600 x 200 forest band |
| `sources/` | The original pictures |
| `tools/build.sh` | Rebuilds `art/` from `sources/` (macOS: Vision, CoreImage, sips) |

## Use it on another machine

1. Install the mod (`pet-for-claude`) from its own repository, then run `/reload-plugins`.
2. Clone this repository anywhere, for example `~/Documents/frieren-pet-theme`.
3. In Claude Code, ask:

   > set the pet theme from ~/Documents/frieren-pet-theme/themes/frieren-forest.theme.json, with its art and backdrop paths made absolute against ~/Documents/frieren-pet-theme

   `art` and `backdrop` in the theme files are relative to this repository's root; `set_theme` needs them absolute.

The theme sticks across sessions on that machine. To go back to the slime, ask for the slime back.

## Limits

The desktop draws one SVG of at most 131072 characters for the band: backdrop plus picture plus status line.
`frieren-staff.svg` with `forest-backdrop.svg` comes to about 120000. The sleeping picture is too big to share the band,
which is why the three-picture theme has no backdrop.
