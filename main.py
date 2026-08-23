import asyncio
import os
import sys

# 1. Force Pygame import & initialization before importing submodules
import pygame
pygame.init()

# 2. Add root directory to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# 3. Import main entrypoint AFTER Pygame is safely loaded
from src.main import main

if __name__ == "__main__":
    asyncio.run(main())