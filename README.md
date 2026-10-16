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

- **Classic**: eat cookies at your own pace. Touch a small cookie to eat it and grow;
  burnt (dark) cookies shrink you.
- **Challenge**: 20 seconds to eat as many as you can, with burnt cookies too, while
  big angry cookies chase you (one slow, one fast); if one catches you, the round ends.

Controls: arrow keys / WASD to move, Esc to go back to the menu (or quit from the menu).

## Browser version

The game also runs in a web browser via [pygbag](https://github.com/pygame-web/pygbag),
which `src/main.py` is the entry point for.

```bash
cd src
python -m pygbag --title "Cookie eats cookies" .   # serves it at http://localhost:8000
python -m pygbag --build --title "Cookie eats cookies" .   # just build into src/build/web
```

The page needs a click before the game starts (browsers block audio and focus until then).

## Layout

- `src/main.py`: entry point for the browser build
- `src/videogame/main.py`: game loop, menu, and rounds
- `src/videogame/entities.py`: player, cookies, and chasers
- `src/videogame/settings.py`: window size, colors, speeds, challenge tuning
- `assets/`: images, sounds, fonts
