import socket
import os
from configparser import ConfigParser

VERSION = 'DEV_CHAO'

HOME_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])
HOST_NAME = socket.gethostname()

local_config = ConfigParser()
local_config.read("local.ini")

section = local_config[VERSION]

env_content = ""
for sec in section:
    env_content += "{}={}\n".format(sec.upper(), section[sec])

with open(".env", "w", encoding="utf8") as env:
    env.write(env_content)