"""集合设置参数"""

import os
from colorama import Fore, Style
from modules.utils.clear_screen import cls_stay
from modules.utils.inputs import rinput, cinput
from modules.functions.settings.save_load_settings import save_settings
from modules.utils.prints import input_menu


def settings_menu(self):
    """设置菜单主循环"""
    while True:
        if self.settings.auto_save:
            save_settings(self.settings)
        cls_stay(self, f"[设置菜单] "
                       f"{Fore.LIGHTCYAN_EX}自动保存: "
                       f"{({True: f'{Fore.GREEN}开', False: f'{Fore.RED}关'}[self.settings.auto_save])}")
        r = input_menu({
            "0": "返回上级菜单",
            "1": "歌曲保存路径",
            "2": "清空输出文件夹内的内容",
            "3": "歌词文件保存格式",
            "4": "部分动态效果",
            "s": "切换设置自动保存"
        })
        match r:
            case "0":
                return
            case "1":
                __set_lyric_path(self)
            case "2":
                __remove_output_files(self)
            case "3":
                __set_lyric_format(self)
            case "4":
                pass
            case "s":
                self.settings.auto_save = not self.settings.auto_save
            case _:
                input("输入无效！按回车键继续...")


def __remove_output_files(self):
    while True:
        cls_stay(self, "[设置菜单 - 删除文件]")
        r = input_menu({
            "0": "返回上级",
            "1": "清除歌词文件",
            "2": "清除歌曲文件",
            "a": "清除所有文件",
        })  # 选择清除的文件格式
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
    cls_stay(self, "[设置菜单 - 保存路径]")
    print(f"""允许使用相对路径和绝对路径，默认为"./out/"
请{Fore.RED}*不要*{Style.RESET_ALL}使用{Fore.BLUE}反斜杠{Style.RESET_ALL}来确保通用性
当前值:{Fore.GREEN}{self.settings.lyric_path}{Style.RESET_ALL}
留空回车取消当前设置
请输入新的歌词保存路径:""")
    r = cinput()
    if not r:
        input("输入为空!\n按回车继续...")
        return
    if r[-1] != "/":
        r += "/"
    path = ""
    for i in r.split("/"):
        if len(i) >= 30:
            input("抱歉, 目标或子目录名过长!至多30字符\n问题的目录: %s" % i)
            return
    for i in r.split("/"):
        path += i+"/"
        if not os.path.exists(path):
            os.mkdir(path)
    self.settings.lyric_path = r
    save_settings(self.settings)
    input("设置成功!\n按回车继续...")
    return


def __set_lyric_format(self):
    while True:
        cls_stay(self, f"[设置菜单 - 文件名格式]\n{Fore.LIGHTCYAN_EX}当前格式: ", end="")
        if self.settings.lyric_format == "%(name)s":
            print(f"{Fore.GREEN}曲名", end="")
        else:
            print(Fore.GREEN + self.settings.lyric_format % {"name": "曲名", "artists": "歌手名"}, end="")
        print(".xxx")
        r = input_menu({
            "0": "返回上级",
            "1": "%(name)s - %(artists)s" % {"name": "曲名", "artists": "歌手名"},
            "2": "%(artists)s - %(name)s" % {"name": "曲名", "artists": "歌手名"},
            "3": "%(name)s" % {"name": "曲名", "artists": "歌手名"},
        })
        if r == "0":
            return
        elif r == "1":
            self.settings.lyric_format = "%(name)s - %(artists)s"
            break
        elif r == "2":
            self.settings.lyric_format = "%(artists)s - %(name)s"
            break
        elif r == "3":
            self.settings.lyric_format = "%(name)s"
            break
        else:
            input("输入无效!\n按回车继续...")
    input("修改成功! \n按回车返回...")
    return
