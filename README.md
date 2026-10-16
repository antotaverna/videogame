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

Pick a mode from the menu (Up/Down + Enter, or press 1/2):

- **Classic**: eat cookies at your own pace. Touch a small cookie to eat it and grow.
- **Challenge**: 20 seconds to eat as many as you can. Burnt (dark) cookies shrink you,
  and big angry cookies chase you; if one catches you, the round ends.

Controls: arrow keys / WASD to move, Esc to go back to the menu (or quit from the menu).

## Layout

- `src/videogame/main.py`: game loop, menu, and rounds
- `src/videogame/entities.py`: player, cookies, and chasers
- `src/videogame/settings.py`: window size, colors, speeds, challenge tuning
- `assets/`: images, sounds, fonts
