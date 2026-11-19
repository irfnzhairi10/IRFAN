# QAVE Official: skrip suara latar dan prompt gerakan

Durasi sasaran: kira-kira 75 saat. Format 9:16.
Urutan 15 babak ikut gambar storyboard awak (kiri ke kanan, atas ke bawah).

## 1. Skrip untuk ElevenLabs (jana satu klip audio setiap baris)

Tiga suara: AMIR (muda, lembut, letih), HAKIM (hangat, mesra, yakin), NARATOR (tenang, dalam, sinematik).

| Babak | Masa | Suara | Teks |
|---|---|---|---|
| 1 | 0:00-0:05 | AMIR | Aku tak tahu kenapa kebelakangan ni aku selalu rasa gelisah. |
| 2 | 0:05-0:10 | AMIR | Susah nak tidur, fikiran tak tenang. Rasa macam terlalu banyak benda yang aku tanggung. |
| 3 | 0:10-0:16 | HAKIM | Amir, saffron ni bukan sekadar rempah yang mahal. Ia dah lama dikenali dalam sejarah perubatan. |
| 4 | 0:16-0:25 | AMIR | Saffron? Rempah merah tu? Apa kaitannya dengan masalah emosi aku? |
| 4 | (sambung) | HAKIM | Menariknya, tokoh perubatan Islam, Ibn Sina, pernah membincangkan saffron dalam kitab perubatannya. |
| 5 | 0:25-0:29 | NARATOR | Kitab ini ialah Al-Qanun fi al-Tibb, karya Ibn Sina. |
| 6 | 0:29-0:37 | NARATOR | Menurut satu kajian ilmiah dalam jurnal Phytotherapy Research pada tahun 2013, beliau menyenaraikan saffron dalam kitabnya, termasuk penggunaan tradisionalnya sebagai bahan antikemurungan. |
| 7 | 0:37-0:41 | NARATOR | Saffron sudah lama menjadi sebahagian daripada ilmu perubatan. |
| 8 | 0:41-0:45 | HAKIM | Dan hari ini, saffron masih dikaji oleh para saintis. |
| 9 | 0:45-0:50 | HAKIM | Beberapa kajian klinikal menunjukkan potensi saffron dalam membantu mengurangkan gejala kemurungan dan keresahan. |
| 10 | 0:50-0:53 | AMIR | Rupanya banyak yang aku tak tahu tentang saffron. |
| 11 | 0:53-1:01 | HAKIM | Betul. Tapi ingat, saffron bukan ubat ajaib. Kalau kau mengalami kemurungan atau anxiety, jangan pendam seorang diri. Dapatkan bantuan profesional juga. |
| 12 | 1:01-1:04 | HAKIM | Kita sama-sama berusaha menjaga kesihatan. |
| 13 | 1:04-1:10 | NARATOR | Saffron. Warisan perubatan yang telah dikenali sejak berabad-abad lamanya, kini terus diterokai oleh sains moden. |
| 14 | 1:10-1:13 | (tiada suara, muzik naik) | Logo QAVE OFFICIAL, DISCOVER THE GOLDEN HERITAGE |
| 15 | 1:13-1:16 | (tiada suara, muzik padam) | Logo sahaja |

Perkara pada skrip asal yang saya pendekkan: dialog Babak 1 dan 2, dan satu ayat penutup Babak 3, supaya muat dalam kira-kira 75 saat. Tiada dakwaan baru ditambah.

### Tetapan ElevenLabs
- Model: Multilingual v2. Bahasa: Malay.
- Cari suara dalam Voice Library dengan penapis Malay. Elak suara berlogat Indonesia.
- Stability 45-55, Similarity 75, Style 20-30. Guna tetapan sama untuk semua klip suara yang sama.
- Sebut istilah ikut bunyi jika salah: "Al-Qanun fi al-Tibb" (Al-Qanun fi at-Tibb), "Phytotherapy" (Fito-terapi), "anxiety" (ang-zai-ti).
- Jana setiap baris sebagai fail berasingan, namakan 01.mp3 hingga 13.mp3.

## 2. Prompt gerakan untuk Kling, Hailuo atau Runway (satu klip setiap gambar)

Upload gambar babak tu ke alat video AI, tampal prompt, set 5 saat dan 9:16. Untuk babak berdialog, guna ciri lip sync dengan audio ElevenLabs babak tu.

| Babak | Prompt (Bahasa Inggeris) |
|---|---|
| 1 | Young man sits on the bed at night, slowly lowers his hand from his forehead and sighs, tired eyes, soft lamp flicker, slow camera push in, lip sync to dialogue. |
| 2 | Close-up of the young man looking aside, worried expression, subtle breathing, slight head turn, warm lamp light, slow push in, lip sync to dialogue. |
| 3 | Friend in cream shirt speaks warmly and gestures with an open hand, gentle nod, bookshelf lights glow, slow camera drift, lip sync to dialogue. |
| 4 | Two friends talking, the friend in navy asks curiously, then the cream shirt friend answers with a calm hand gesture, shallow depth of field, slight camera push in, lip sync to dialogue. |
| 5 | Historical scholar writes with a quill in a grand library, ink pen moves slowly, dust particles in warm light, slow camera push in. |
| 6 | Old manuscript with Arabic title, soft golden light sweeps across the parchment, dust particles float, slow zoom in. |
| 7 | Saffron threads on a brass plate beside a purple crocus, petals sway slightly, golden sparkles drift, slow camera orbit. |
| 8 | Scientist looks through a microscope, adjusts the focus knob, lab glass reflects blue light, slow camera push in. |
| 9 | Glowing golden molecule structure rotates slowly, light particles pulse, red saffron threads in the corner, slow zoom out. |
| 10 | Young man listens, thoughtful expression turns into soft understanding, subtle blink and nod, blurred lab lights behind. |
| 11 | Friend in cream shirt speaks sincerely with gentle hand gestures, concerned and kind expression, slow push in, lip sync to dialogue. |
| 12 | Two friends smile and raise tea glasses together, warm cozy light, steam rises from the glasses, slow camera drift. |
| 13 | Slow cinematic push in toward the QAVE saffron jar, golden lid glints, purple crocus petals sway slightly, floating golden particles. |
| 14 | Logo with gold light streaks sweeping across, soft glow pulse, subtle particles, camera static. |
| 15 | Logo glows softly, light waves ripple at the bottom, slow fade to black. |

## 3. Kualiti gambar

Gambar storyboard grid yang awak hantar ialah satu kolaj 3x5, jadi setiap babak kecil sahaja. Untuk video AI, minta ChatGPT jana setiap babak sebagai satu gambar 9:16 penuh (macam gambar minuman dan produk yang awak hantar, yang kualitinya memang bagus). Namakan 01.png hingga 15.png.

## 4. Peringatan kandungan kesihatan

- Sahkan sendiri rujukan jurnal *Phytotherapy Research* 2013 sebelum siar. Saya belum menyemaknya.
- Kekalkan ayat "saffron bukan ubat ajaib" dan nasihat jumpa profesional. Jangan tulis saffron menyembuhkan kemurungan atau anxiety.
