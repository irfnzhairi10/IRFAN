# QAVE · VGC-FT01 Motion Ad (HyperFrames project)

- `index.html`: root composition (1080×1920, 43 s, 30 fps), scene hosts + audio
- `compositions/s1-hook … s8-outro.html`: one scene per file (GSAP, SVG, Three.js in S4)
- `assets/`: fonts, logos (+ transparent versions), local GSAP/Three, audio (VO, music, SFX), `source/` (your originals, untouched)
- `audio-src/`: `cues.json` (timing shared by visuals and audio) + `build_audio.py` (procedural music/SFX, seeded)
- `tools/`: alpha logo generation + contact sheet script
- `previews/v1/`: frame snapshots v1 (`sheets/` = numbered contact sheets, `full/` = full size)
- `REVIEW.md`: direction, checks, and items to confirm

Install: `npm install` · Check: `npx hyperframes check` · Preview: `npx hyperframes preview`
MP4 render (ONLY after frame approval): `npx hyperframes render -o renders/qave-ft01-v1-preview.mp4`
