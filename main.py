import sys
import os
import asyncio

# Ensure Python looks inside 'src' for local modules
sys.path.insert(0, os.path.abspath("src"))

from main import main

if __name__ == "__main__":
    asyncio.run(main())