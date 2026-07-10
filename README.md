<div align="center">

<img src="assets/hero.gif" alt="Pixel-art alley: a staircase climbing toward the light between neon-signed buildings" width="100%" />

# 赤 · Hi there, I'm **leotu2008-ux** · 黒

*somewhere between the last step and the light at the top*

<img src="https://img.shields.io/badge/status-climbing-c6202a?style=for-the-badge&labelColor=0d0b0e" alt="status: climbing" />
<img src="https://img.shields.io/badge/mode-pixel-ee3a3a?style=for-the-badge&labelColor=0d0b0e" alt="mode: pixel" />
<img src="https://komarev.com/ghpvc/?username=leotu2008-ux&color=c6202a&style=for-the-badge&label=visitors" alt="visitor counter" />

</div>

<br>

## 🏮 About me

- 🔭 I'm currently working on ...
- 🌱 I'm currently learning ...
- 👯 I'm looking to collaborate on ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- ⚡ Fun fact: the banner above is **not a video** — it's procedurally generated pixel art

<br>

## 📊 Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=leotu2008-ux&show_icons=true&hide_border=true&bg_color=0d0b0e&title_color=ee3a3a&text_color=9c99a0&icon_color=c6202a&ring_color=ee3a3a" alt="GitHub stats" height="165" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=leotu2008-ux&layout=compact&hide_border=true&bg_color=0d0b0e&title_color=ee3a3a&text_color=9c99a0" alt="Top languages" height="165" />

</div>

<br>

## 🎨 About the banner

The looping animation at the top is drawn entirely in code — no image files, no AI upscaling, just
[**~300 lines of Python**](art/generate_hero.py) placing pixels on a 220 × 124 grid:

| | |
|---|---|
| 🏮 **Neon signs** | pseudo-kanji glyphs generated from random strokes, breathing and sputtering on a loop |
| 🌸 **Red petals** | fall at 1–2 px/frame through a 72 px band, so they wrap seamlessly |
| 🚶 **The figure** | a 12-pixel-tall silhouette with a 2-phase walk cycle and a swinging coat |
| 🐈 **The cat** | is watching |

Every periodic motion completes an integer number of cycles across the 36 frames,
so the GIF loops forever without a seam. Regenerate it with:

```bash
python3 art/generate_hero.py
```

<div align="center">

<sub>▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 登り続けろ — keep climbing ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓</sub>

</div>
