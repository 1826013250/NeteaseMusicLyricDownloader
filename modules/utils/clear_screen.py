"""用来清空命令行的信息，自动判别系统"""
import os


def clear():
    name = os.name
    if name == "nt":
        os.system("cls")
    elif name == "posix":
        os.system("clear")
    else:
        os.system("clear")


def cls_stay(self, custom=""):
    """保留版本号清除屏幕"""
    clear()
    print(f"[NeteaseMusicLyricDownloader] {self.version}")
    print(custom)