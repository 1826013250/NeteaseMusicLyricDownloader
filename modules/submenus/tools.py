"""小工具以及菜单"""
import os
from colorama import Fore

from modules.utils.prints import print_menu
from modules.utils.clear_screen import cls_stay
from modules.utils.inputs import cinput
from modules.functions.mainly.load_file_song import load_and_decrypt_from_ncm, process_work



def tools_menu(self):
    while True:
        cls_stay(self, "[小工具菜单]")
        print_menu({
            "0": "返回上级菜单",
            "d": "解锁指定ncm文件/指定文件夹"
        })
        r = cinput("请选择:")
        match r:
            case "0":
                return
            case "d":
                ncm_unlock(self)
                input("按回车继续...")
            case _:
                input("请输入正确的选项\n按回车键继续...")


def ncm_unlock(self):
    cls_stay(self, "[小工具 - 文件解锁]")
    path = cinput("请输入绝对路径:").replace("\\","")
    if not os.path.exists(path):  # 判断目标存在与否
        print("目标不存在！")
        return
    if os.path.isfile(path):  # 目标为文件则执行单文件解密
        r = load_and_decrypt_from_ncm(path, os.path.split(path)[-1], "original", True)
        match r:
            case "file_not_found":
                print("文件未找到")
            case "perm_error":
                print("权限错误。请检查是否拥有对应权限或者文件是否被占用。")
            case _:
                print(f"解锁完毕！文件保存在:\n{Fore.GREEN}{r[-1]}")
        return
    elif os.path.isdir(path):  # 目标为文件夹则执行文件夹遍历
        ...
    else:
        print("无法识别目标文件。请确认目标文件是否正确以及是否拥有对应权限。")

