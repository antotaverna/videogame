# Entry point for the browser build (pygbag looks for a top-level main.py).
# On desktop, run the game with the `videogame` command instead.
import asyncio

# pygbag only loads packages it sees imported here, so pygame must be imported
# directly even though only videogame.main uses it.
import pygame  # noqa: F401

from videogame.main import run

asyncio.run(run())
