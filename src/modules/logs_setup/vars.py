import os
import platform

target_dir = "logs"
if platform.system() == "Linux":
    root_dir = "home/tg-bot"
else:
    disk = "F:\\"
    dir = """Coding_projects\Python\PycharmProjects\\tg_bot_learn"""
    root_dir = os.path.join(disk, dir)
path = os.path.join(root_dir, target_dir)
