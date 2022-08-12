"""集合设置参数"""

import os
import re
from modules.clear_screen import clear
from modules.raw_input import rinput, cinput
from modules.save_load_settings import save_settings


def settings_menu(self):
    """设置菜单主循环"""
    while True:
        clear()
        print(f"[NeteaseMusicLyricDownloader] {self.version}\n"
              "[设置菜单]\n"
              "[0] 返回上级\n[1] 设置歌曲保存路径\n[2] 清空输出文件夹内的所有歌词\n[s] 将设置保存到文件")
        r = rinput("请选择:")
        if r == "0":
            return
        elif r == "1":
            __set_lyric_path(self)
        elif r == "2":
            __remove_lyric_files(self.settings.lyric_path)
        elif r == "s":
            __save_settings(self)
        else:
            input("输入无效！按回车键继续...")


def __remove_lyric_files(path):
    clear()
    files = []
    for i in os.listdir(path):
        if re.match(r".*(\.lrc)$", i):
            files.append(i)
    if len(files) != 0:
        for i in range(0, len(files)):
            print("正在删除(%d/%d): %s" % (i+1, len(files), files[i]))
            os.remove(path+files[i])
        input("删除完毕!\n按回车继续...")
    else:
        input("文件夹内没有要删除的东西\n按回车继续...")


def __set_lyric_path(self):
    clear()
    print("允许使用相对路径和绝对路径，默认为\"./out/\"\n请*不要*使用反斜杠来确保通用性\n"
          "当前值:%s\n请输入新的歌词保存路径:" % self.settings.lyric_path)
    r = cinput()
    if not r:
        input("输入为空!\n按回车继续...")
        return
    if r[-1] != "/":
        r += "/"
    path = ""
    for i in r.split("/"):
        path += i+"/"
        if not os.path.exists(path):
            os.mkdir(path)
    self.settings.lyric_path = r
    input("设置成功!\n按回车继续...")


def __save_settings(self):
    return save_settings(self.settings)
