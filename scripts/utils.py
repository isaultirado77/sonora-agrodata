# utils.py

from scripts.config import DIRS

def init_dirs(dirs=DIRS):
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
