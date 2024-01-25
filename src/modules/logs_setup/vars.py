import os
import platform
from dotenv import load_dotenv

load_dotenv()
windows_dir = os.getenv("path")

target_dir = "logs"
if platform.system() == "Linux":
    root_dir = "home/tg-bot-gpt"
else:
    disk = "F:\\"
    dir = f"""{windows_dir}"""
    root_dir = os.path.join(disk, dir)
path = os.path.join(root_dir, target_dir)
