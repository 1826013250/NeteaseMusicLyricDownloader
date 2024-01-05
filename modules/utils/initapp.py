from os import mkdir as raw_mkdir
from os.path import exists

INIT_DIRECTORIES = [
    'out'
]

def mkdir(dirpath: str) -> bool:
    if not exists(dirpath):
        raw_mkdir(dirpath)

    return [True if exists(dirpath) else False][0]


def init_directories():
    for dir_name in INIT_DIRECTORIES:
        mkdir(dir_name)
