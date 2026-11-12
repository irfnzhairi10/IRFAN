# v3: v2 + social end tag (current version). Frames are waiting for approval. NO MP4 yet.

- New **S9 (43.0–47.0 s)**: QAVE mark, "Jangan lupa", 4 icons (FOLLOW · LIKE · COMMENT · SHARE) popping in one by one, then the pill **@qave.official**. Hold ≈2.2 s.
- **No music and no SFX** in S9: the music bed ends at 43.0 s (measured: the last 0.1 s is already near silent), and no sound clip is placed after 43 s.
- S8 now clears (blur-out 42.72–43.0) after holding the CTA ≈2.2 s.
- Total duration **47 s** (target 43 s + 4 s you asked for). Root `data-duration="47"`.
- The handle uses Manrope (lowercase), because Cinzel is caps-only and turned it into "@QAVE.OFFICIAL". Please confirm the spelling **@qave.official**.
- Frames: `previews/v3/` (25 frames, 7 sheets). v1 and v2 are kept.

---

# v2: HYBRID (footage + animation), current version. Frames are waiting for approval. NO MP4 yet.

Approved by the user: footage alternates with animation (about 50/50) and the footage gets a warm-gold grade.
`index.html` = v2. v1 (animation only) is kept at `versions/v1-animation-only/` and in git commit d88ff50; its frames are in `previews/v1/`.

| Time | Visual | VO |
|---|---|---|
| 0–4.1 | **FOOTAGE F1**: box + bag of gold-capped jars from the car, then "Tuan-tuan, BARANG SAYA SAMPAI." | Tuan-tuan, barang saya sampai |
| 4.1–8.1 | ANIMATION S2: READY → SECARA RASMI seal | ready… secara ofisial |
| 8.1–12.1 | **FOOTAGE F2**: STAY TUNED + small calendar landing on ? ? | stay tune, tunggu tarikh |
| 12.1–18.0 | ANIMATION S4 3D: SAFFRON → SUPER NEGIN | barang saffron… super negin |
| 18.0–21.4 | **FOOTAGE F3**: 10 / PEMBELIAN PERTAMA / 10 places fill | 10 pembelian pertama |
| 21.4–26.0 | ANIMATION S5: gift box + HADIAH MENANTI ANDA + GIFT tag | ada hadiah… gift |
| 26.0–31.0 | **FOOTAGE F4**: Tuan-tuan ingat, BUKAN SEKADAR MENJUAL SAFFRON → TETAPI KITA PASTIKAN | Tuan-tuan ingat… tetapi kita pastikan |
| 31.0–37.0 | ANIMATION S6: gold plant KUALITI · AUTENTIK · VALUE · EKSKLUSIF | kualiti… eksklusif |
| 37.0–39.05 | **FOOTAGE F5**: Jangan lupa, STAY TUNED | Jangan lupa, stay tune |
| 39.2–43.0 | ANIMATION S8: logo + CTA | (music) |

- **Footage** is a copy of your .mov converted to H.264 at 30 fps (`assets/video/`); the original is untouched. Each clip uses `data-media-start` equal to its start time, so lip-sync matches the VO. The video is muted because the sound comes from `vo-clean.wav`.
- **Grade:** HyperFrames `media-treatment` preset `warm-daylight`, intensity 0.8, on all 5 clips.
- **Text on footage** sits at the top (168–700 px) over a dark scrim, so the face and hands stay clear.
- **Transition:** a gold-ring iris (`clip-path` circle + SVG ring) on every footage ↔ animation change. The last iris closes onto the centre of the logo.
- **SFX re-timed** to the iris cues (`audio-src/cues.json`) and audio regenerated.
- **Checks:** `hyperframes check` ok = true, 0 errors. 22 v2 frames reviewed. Fixed during review: the hook text covered the cap at 3.5 s (text made smaller and moved up), and black corners showed in the iris (radius increased).
- **Pending until the MP4:** lip-sync and motion checked on video, video decoding, final mix.

---

# v1: animation only (preserved)

Status: **frames v1 are ready for review. NO MP4 has been rendered yet.** The MP4 preview is rendered only after you approve the frames in writing.

## Output
- HyperFrames 0.9.38 (installed locally in `node_modules`), 1080×1920 portrait 9:16, 30 fps, **43.0 s**
- Root: `index.html` · scenes: `compositions/s1…s8` · assets: `assets/` · cue sheet: `audio-src/cues.json`

## Visual direction: "Gilded Noir Botanical" (black card with gold foil)
Taken directly from the QAVE brand marks: gold foil stamped onto black textured card.
- **Colour roles:** black paper `#0B0A08` with 7% grain = background · gold foil `#C9A05A→#F6E1A6` = all text and line work · saffron red `#D8431E` = ONLY the saffron threads, the number **10**, the `??` and the CTA.
- **Type:** Cinzel 700 (display, echoes the QAVE wordmark) · Cormorant Garamond italic (spoken lines such as "Tuan-tuan,") · Manrope 700 (small labels).
- **Motion:** lines drawn like a foil stamp, one shine pass when a title lands, words appear on the words spoken in the VO, and transitions caused by an object on screen (zoom into the box, a seal whip, the calendar becoming the world, a 3D dive, the ring becoming the logo).
- **3D:** S4 is real Three.js geometry: 3 lathe stigmas with a frilled tip, a warm key light and a cool rim light. The camera dollies in and the threads fan out on "SUPER NEGIN". The rest is 2D SVG/HTML.

## Script = your recording (wording unchanged)
The VO is the audio from your `.mov`, **in full order with nothing cut** (0–39.05 s): highpass, light denoise, compression, loudness normalised to −16.3 LUFS, peak −1.5 dBFS. The original file is untouched in `assets/source/`. The picture from the .mov is NOT used, so the ad stays 100% motion. Automatic transcript (Whisper small, `ms`):

> "Tuan-tuan, barang saya sampai, ready kita nak mula lancarkan penjualan kita secara ofisial. Jadi, stay tune, tunggu tarikh yang kita akan keluarkan. Barang yang akan [dijual] ini barang saffron, barang rare, saffron Super Negin. 10 pembelian pertama kita akan berikan, ada hadiah-hadiah ataupun gift yang kita akan sertakan. Tuan-tuan ingat, [kita] bukan sekadar menjual saffron, tetapi kita pastikan kualiti, autentik, value dan eksklusif. Jangan lupa, stay tune."

| # | Scene | Time | On-screen text | Flow |
|---|---|---|---|---|
| S1 | Hook | 0.0–4.1 | Tuan-tuan, / BARANG SAYA SAMPAI. | Hook |
| S2 | Rasmi | 4.1–8.1 | READY / MULA LANCARKAN PENJUALAN / SECARA RASMI (seal) | Question: what's happening? |
| S3 | Tarikh | 8.1–12.1 | STAY TUNED / TARIKH PELANCARAN ?? / tunggu tarikhnya | Question: when? |
| S4 | 3D Saffron | 12.1–18.0 | 3 HELAI SEKUNTUM BUNGA · dipetik dengan tangan / SAFFRON / PREMIUM IRANIAN SAFFRON · gred tertinggi saffron Iran / SUPER NEGIN | Explanation (edu) |
| S5 | Hadiah | 18.0–26.0 | 10 / PEMBELIAN PERTAMA / 10 slots / HADIAH MENANTI ANDA / GIFT | Example: the offer |
| S6 | Nilai | 26.0–37.0 | Tuan-tuan ingat, / BUKAN SEKADAR MENJUAL SAFFRON / TETAPI KITA PASTIKAN / KUALITI · AUTENTIK · VALUE · EKSKLUSIF | Takeaway |
| S7 | Stay tuned | 37.0–39.2 | Jangan lupa, / STAY TUNED | Reminder |
| S8 | End card | 39.2–43.0 | QAVE logo / PREMIUM IRANIAN SAFFRON · SUPER NEGIN / AKAN DILANCARKAN TIDAK LAMA LAGI / 10 PEMBELIAN TERAWAL · ADA HADIAH MENANTI ANDA | CTA (held 2.4 s) |

## Audio (generated with code: `audio-src/build_audio.py`, seeded)
- Original instrumental music in D "hijaz" mode (a nod to Iran): drone → santur-like pluck motif (Karplus-Strong) → frame-drum pulse in S5 → pad only for "bukan sekadar…" → one pluck on each value word → resolves on the logo. It does not copy any song.
- The music is **ducked by up to −9 dB** using a sidechain from the real VO. Mix: VO 1.0, music 0.42, SFX 0.6.
- SFX use the same cues as the visuals (`cues.json`): pop (box lid, 10, gift, each leaf), whoosh on scene changes, impact (RASMI seal, SUPER NEGIN, logo), and one riser into the logo.

## Checks actually run
- `hyperframes check`: **ok = true**, 0 errors. Warnings kept on purpose: reel digits in S3 flash briefly (slot-machine effect, intentional); 2 contrast warnings on reel digits during the exit; WebGL "GPU stall ReadPixels" (performance only).
- Snapshot of 19 frames, looked at one by one: assets load (logos, fonts, 3D). I saw no overlap or overflow in the final frames, and every text sits inside the 168–1330 px band.
- Loudness of each audio file **was measured, not listened to**: VO −16.3 LUFS / −1.5 dBFS; music bed −25.2 LUFS / −2.7 dBFS; SFX −19.9 LUFS / −3.0 dBFS.

## Not yet verified (pending MP4)
Motion smoothness, actual audio/visual sync, the final mix balance (heard by a person), MP4 decoding, duration and resolution, and the final mix loudness.

## Please check / confirm
1. **Transcript:** "rare" (15.6 s), "ofisial" (7.2 s) and "gift" (27.2 s, which probably means "kita") are uncertain. On screen I used SECARA RASMI and did not show "rare".
2. **Facts I added for the edu angle** (not in the VO): "3 helai sekuntum bunga", "dipetik dengan tangan" and "gred tertinggi saffron Iran" (Super Negin). These are general facts about saffron. Please confirm you are happy with them, or ask me to remove them.
3. **I made NO health claims** (anxiety, pregnancy, etc.). Saffron in high doses is not recommended during pregnancy, so any claim like that needs a verified source from you.
4. "STAY TUNED" and "VALUE" are kept in English, as in the VO.
5. The gift is shown as a "GIFT" tag only. I did not invent what the gift is.

## Weakest shot / with more time
S3 (calendar) is the most "graphic-card" scene. The S1 thumbnail only shows "Tuan-tuan," and the box; you could add "BARANG DAH SAMPAI" at frame 0 if you want a stronger thumbnail.
