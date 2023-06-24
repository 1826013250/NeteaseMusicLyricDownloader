"""有关打印的函数"""
from colorama import Fore

from modules.utils.clear_screen import clear
from modules.utils.inputs import rinput


def print_info(self):
    """调用即输出,无返回值"""
    clear()
    print(f"""[NeteaseMusicLyricDownloader]
版本: {self.version}
本软件开源，项目地址:https://github.com/1826013250/NeteaseMusicLyricDownloader
作者:David-123
联系方式:
\tQQ:1826013250
\tE-mail:1826013250@qq.com(mainly)
\t       mc1826013250@gmail.com

特别感谢:
\t- nondanee - ncmdump https://github.com/nondanee/ncmdump
\t- chuyaoxin - 提供了对ncmdump以及ncm文件的详细解说 https://www.cnblogs.com/cyx-b/p/13443003.html

若程序遇到bug请提交至github上的issue""")
    input("按回车键返回...")
    return


def print_menu(menu: dict):
    """传入一个字典, 格式为 {"需要输入的字符": "功能描述", ...}
    将会按照以下格式打印:
    [字符1] 功能描述1
    [字符2] 功能描述2
    ..."""
    for k, v in menu.items():
        print(f"{Fore.LIGHTBLUE_EX}[{k}] {Fore.RESET}{v}")


def input_menu(menu: dict):
    """传入一个字典, 格式为 {"需要输入的字符": "功能描述", ...}
    在 print_menu 末尾添加'请选择: '字样并要求输入, 使用rinput获取输入"""
    print_menu(menu)
    return rinput("请选择: ")
