# videogame

A 2D game built with Python and [pygame-ce](https://pyga.me/).

## Setup

```bash
conda env create -f environment.yml
conda activate videogame
```

## Run

```bash
videogame            # or: python -m videogame.main
```

Controls: arrow keys / WASD to move, Esc to quit.

## Layout

- `src/videogame/main.py`: game loop and entities
- `src/videogame/settings.py`: window size, FPS, colors, speeds
- `assets/`: images, sounds, fonts
