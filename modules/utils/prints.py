"""该程序的自述信息,调用即输出"""
from modules.utils.clear_screen import clear
from colorama import Fore


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
    """传入一个字典, 格式为 {"需要输入的字符": "功能描述", ...}"""
    for k, v in menu.items():
        print(f"{Fore.LIGHTBLUE_EX}[{k}] {Fore.LIGHTWHITE_EX}{v}")