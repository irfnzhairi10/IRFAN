# QAVE – Prompt Klip, Watak & Jadual Suntingan

Gaya global (tampal dalam SETIAP prompt):
`stylized realistic 3D cartoon, Pixar-like proportions, cinematic, premium, emotional storytelling, shallow depth of field, volumetric light, warm golden colour grade, 24fps, vertical 9:16`

Negative prompt (setiap jana):
`inconsistent face, changing outfit, extra fingers, distorted hands, garbled text, Arabic letters, any text or logo, real portrait of Ibn Sina, watermark, flicker, low resolution`

---
## A. GAMBAR RUJUKAN WATAK (jana dahulu, guna dalam Midjourney / Flux / Ideogram / Gemini)

**AMIR – depan**
`Character sheet, front view, full body. Malay man, 28 years old, short black tousled hair, tired brown eyes with faint eye bags, light stubble, loose grey t-shirt, dark trousers. Stylized realistic 3D cartoon, Pixar-like, soft skin shading, neutral grey background, even studio lighting.`
**AMIR – sisi:** sama, tukar kepada `side profile view`.

**HAKIM – depan**
`Character sheet, front view, full body. Malay man, 29 years old, neat short black hair, warm friendly face, slightly round jaw, teal button-up shirt with sleeves rolled, dark trousers. Stylized realistic 3D cartoon, Pixar-like, soft skin shading, neutral grey background, even studio lighting.`
**HAKIM – sisi:** sama, tukar kepada `side profile view`.

**IBN SINA (ilustrasi sejarah)**
`Illustrated medieval Islamic scholar seen from behind, white turban, brown robe, writing with a reed pen at a wooden desk, face not visible, stylised historical illustration.`

---
## B. PROMPT KLIP (image-to-video; masukkan gambar rujukan + audio berkaitan)

| Klip | Audio | Prompt |
|---|---|---|
| **K1** | Amir 1 (10.4s) | `[AMIR reference] sits on the edge of a bed in a dim bedroom at night, shoulders slumped, phone dangling in his hand with a dimmed screen. Warm bedside lamp plus cold blue window light. Slow push-in on his tired face. He speaks softly, natural lip movement, subtle sad blinking.` |
| **K2** | Hakim 2.1 (≈8s) | `[HAKIM reference] walks in and sits beside [AMIR], placing a gentle hand on his shoulder. Warm lamp light, two-shot then close-up on Hakim, caring smile, speaking naturally.` |
| **K3** | Amir 2 (2.5s) | `Close-up on [AMIR], curious, slightly raised eyebrow, speaking. Same bedroom, warm lamp light.` |
| **K4** | Hakim 2.3 (6.8s) | `Close-up on [HAKIM], warm and knowing expression, speaking, subtle hand gesture. Same bedroom lighting.` |
| **K5** | Hakim 3.1 (16.7s, suara latar, tiada bibir) | `Match-cut from the bedroom lamp to golden candlelight in a grand medieval Islamic library: tall wooden shelves, aged manuscripts, drifting dust motes. [IBN SINA illustration reference, face hidden] writes with a reed pen. Slow dolly along shelves, then macro on parchment with red saffron threads beside it. Amber palette.` (jana 2–3 klip 5–8s dan sambung) |
| **K6** | Hakim 3.2 (7.7s) | `Macro of old manuscript pages turning, saffron threads resting on parchment, candlelight flicker, slow camera glide. Amber tones.` |
| **K7** | Hakim 4.1 (7.9s) | `Clean modern laboratory, cool white-teal light with golden accent. Saffron threads in a petri dish, glowing 3D crocin molecule rotating in holographic space, researcher in lab coat at microscope. Smooth glide.` |
| **K8** | Amir 4 (2.6s) | `Daytime, soft sunlight in the room. Close-up on [AMIR], calmer expression with a small thoughtful smile, speaking.` |
| **K9** | Hakim 4.3 (11.4s) | `Two-shot of [AMIR] and [HAKIM] on the bed in daylight. Hakim speaks sincerely, hand on Amir's shoulder; Amir nods. Warm, hopeful mood.` |
| **K10** | Narator (8.2s, tiada bibir) | `Bright warm table. [AMIR] and [HAKIM] smile, holding glasses of golden saffron drink with threads swirling. Camera glides past them to a premium QAVE saffron jar with a gold lid and burgundy packaging, soft rim light, shallow depth of field. End on a hero shot of the jar on a dark burgundy-to-gold gradient.` |
| **K11** | Logo (3s) | Guna `logo/QAVE_wordmark_tanpa_R.png` dan lambang bunga safron. Animasi: lambang muncul → wordmark QAVE → tagline. Dibuat di CapCut (fade + sedikit kilau emas). |

---
## C. JADUAL SUARA (tiada jeda 0.35s antara ayat)
| # | Watak | Babak | Mula | Tamat | Ayat |
|---|---|---|---|---|---|
| 1 | Amir | B1 | 0.0s | 10.4s | Entah kenapa kebelakangan ni aku asyik… |
| 2 | Hakim (BELUM ADA – anggaran) | B2 | 10.8s | 18.8s | Amir, kau tahu tak?… |
| 3 | Amir | B2 | 19.1s | 21.6s | Saffron? Apa kaitannya dengan aku?… |
| 4 | Hakim | B2 | 21.9s | 28.8s | Ibn Sina, tokoh perubatan Islam yang t… |
| 5 | Hakim | B3 | 29.1s | 45.8s | Kitab ini ialah Al-Qanun fi al-Tibb, k… |
| 6 | Hakim | B3 | 46.2s | 53.9s | Bayangkan... beratus-ratus tahun dahul… |
| 7 | Hakim | B4 | 54.2s | 62.1s | Dan hari ini, saffron masih terus dika… |
| 8 | Amir | B4 | 62.4s | 65.0s | Rupanya banyak benda aku tak tahu tent… |
| 9 | Hakim | B4 | 65.4s | 76.7s | Betul. Tapi ingat, saffron bukan ubat … |
| 10 | Narator | B5 | 77.1s | 85.1s | Saffron. Warisan yang telah dikenali s… |

Tamat suara: **85.1s**; dengan logo penutup 3s = **88.1s**

Fail sari kata: `sarikata/sarikata_QAVE.srt` (masa mengikut jadual ini; baris Hakim 2.1 dianggar 8s, laraskan selepas audio sebenar dijana).

## D. OVERLAY (CapCut)
- 29–31s: `القَانُونُ فِي الطِّبِّ` + `AL-QANUN FI AL-TIBB`
- ±40s: `SAFFRON – Crocus sativus`
- Lower-third Babak 3: `Visual ilustrasi sejarah; bukan gambaran wajah sebenar Ibn Sina.`
- Akhir (3s): lambang → `QAVE` → `DISCOVER THE GOLDEN HERITAGE`
- Disclaimer kecil di hujung: `Saffron bukan pengganti rawatan perubatan.`

## E. TEMPOH
Jumlah ±88s, melebihi sasaran 60–75s. Pilihan memendekkan (pilih satu):
1. Buang ayat 3.2 "Bayangkan… beratus-ratus tahun…" (−7.7s) → ±80s.
2. Buang 3.2 dan ayat 4.1 saintis (−15.6s) → ±72s ✔.
3. Percepatkan semua suara 1.08× di CapCut (−6s), gabung dengan pilihan 1.
