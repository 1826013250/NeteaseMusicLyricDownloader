"""集合设置参数"""

import os
from modules.utils.clear_screen import clear
from modules.utils.inputs import rinput, cinput
from modules.functions.save_load_settings import save_settings


def settings_menu(self):
    """设置菜单主循环"""
    while True:
        clear()
        print(f"[NeteaseMusicLyricDownloader] {self.version}\n"
              "[设置菜单]\n"
              "[0] 返回上级\n[1] 歌曲保存路径\n[2] 清空输出文件夹内的内容\n[3] 歌词文件保存格式\n[4] 部分动态效果\n"
              "[s] 将设置保存到文件")
        r = rinput("请选择:")
        if r == "0":
            return
        elif r == "1":
            __set_lyric_path(self)
        elif r == "2":
            __remove_output_files(self)
        elif r == "3":
            pass
        elif r == "4":
            pass
        elif r == "s":
            __save_settings(self)
        else:
            input("输入无效！按回车键继续...")


def __remove_output_files(self):
    while True:
        clear()
        print(f"[NeteaseMusicLyricDownloader] {self.version}\n"
              "[设置菜单 - 删除文件]\n"
              "[0] 返回上级\n[1] 清除歌词文件\n[2] 清除歌曲文件\n[a] 清除所有文件")
        r = rinput("请选择:")  # 选择清除的文件格式
        if r == "0":
            return
        elif r == "1":
            dellist = [".lrc"]
            break
        elif r == "2":
            dellist = [".mp3", ".flac"]
            break
        elif r == "a":
            dellist = ["ALL"]
            break
        else:
            input("输入无效!\n按回车键继续...")
    files = []
    for i in os.listdir(self.settings.lyric_path):  # 列出所有文件
        if dellist[0] == "ALL":
            files = os.listdir(self.settings.lyric_path)
            break
        elif os.path.splitext(i)[-1] in dellist:  # 匹配文件
            files.append(i)  # 将匹配到的文件加入到列表, 等待删除
    if len(files) != 0:
        if len(files) > 30:
            special_text = "\033[F"
        else:
            special_text = "\n"
        for i in range(0, len(files)):
            print("删除进度: %d/%d\n -> %s%s" % (i+1, len(files), files[i], special_text), end="")  # 删除进度提示
            os.remove(self.settings.lyric_path+files[i])
        input("\n\033[K删除完毕!\n按回车继续...")
        return
    else:
        input("文件夹内没有要删除的东西\n按回车继续...")
        return


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
    return


def __set_lyric_format(self):
    pass


def __save_settings(self):
    return save_settings(self.settings)
