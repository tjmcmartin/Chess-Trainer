from pathlib import Path

#Groups
pieces = {}
tiles = {}
arrows = []

#project directory
project_root = Path(__file__).parent

#global trackers
move_tree_ui = None
node = None