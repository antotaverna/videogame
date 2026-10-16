# videogame

Cookie eats cookies: a tiny 2D game built with Python and [pygame-ce](https://pyga.me/).
Move a hungry cookie around, eat the small cookies, and grow.

## Setup

```bash
conda env create -f environment.yml
conda activate videogame
```

## Run

```bash
videogame            # or: python -m videogame.main
```

Controls: arrow keys / WASD to move, Esc to quit. Touch a small cookie to eat it.

## Layout

- `src/videogame/main.py`: game loop and entities
- `src/videogame/settings.py`: window size, FPS, colors, speeds
- `assets/`: images, sounds, fonts
