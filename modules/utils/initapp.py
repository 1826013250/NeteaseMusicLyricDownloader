from os import mkdir
from os.path import exists

INIT_DIRECTORIES = [
    'out'
]

def init_directories():
    for dir_name in INIT_DIRECTORIES:
        if not exists(dir_name):
            mkdir(dir_name)
