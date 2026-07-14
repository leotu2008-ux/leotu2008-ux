<div align="center">

<img src="assets/hero.gif" alt="Pixel-art lofi room: a CRT computer reading STARTING SOON, a city window, shelves of books" width="100%" />

# ▚ Hi there, I'm **leotu2008-ux** ▞

*starting soon…*

<img src="https://img.shields.io/badge/status-starting_soon-7ee8d4?style=for-the-badge&labelColor=0e1814" alt="status: starting soon" />
<img src="https://img.shields.io/badge/signal-CRT-52b89c?style=for-the-badge&labelColor=0e1814" alt="signal: CRT" />
<img src="https://komarev.com/ghpvc/?username=leotu2008-ux&color=2c8874&style=for-the-badge&label=visitors" alt="visitor counter" />

</div>

<br>

## 📼 About me

- 🔭 I'm currently working on ...
- 🌱 I'm currently learning ...
- 👯 I'm looking to collaborate on ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- ⚡ Fun fact: the banner above is **not a video** — it's procedurally generated pixel art

<br>

## 📊 Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=leotu2008-ux&show_icons=true&hide_border=true&bg_color=0e1814&title_color=7ee8d4&text_color=9ab4a8&icon_color=52b89c&ring_color=7ee8d4" alt="GitHub stats" height="165" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=leotu2008-ux&layout=compact&hide_border=true&bg_color=0e1814&title_color=7ee8d4&text_color=9ab4a8" alt="Top languages" height="165" />

</div>

<br>

## 🎨 About the banner

The looping animation at the top is drawn entirely in code — no image files, no AI upscaling, just
[**~400 lines of Python**](art/generate_hero.py) placing pixels on a 400 × 225 grid, upscaled 3×
so it keeps its detail but still reads as pixels. The whole room is built in perspective — angled
desk, turned monitor, receding shelves — and the animation is deliberately subtle:

| | |
|---|---|
| 📺 **The screen** | "STARTING SOON" breathes in a slow glow, a scanline band makes one full sweep per loop, and a cursor blinks |
| 🌆 **The skyline** | a red antenna beacon fades in and out on the rooftop |
| ✨ **The air** | dust motes drift through the window light, barely there |
| ⌨️ **The desk** | the screen's glow spills onto the keyboard, breathing in sync with the text |

Every periodic motion completes an integer number of cycles across the 48 frames,
so the GIF loops forever without a seam. Regenerate it with:

```bash
python3 art/generate_hero.py
```

<div align="center">

<sub>▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ starting soon — stay tuned ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓</sub>

</div>
