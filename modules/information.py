"""该程序的自述信息,调用即输出"""
from modules.clear_screen import clear


def print_info(self):
    """调用即输出,无返回值"""
    clear()
    print(f"""[NeteaseMusicLyricDownloader Reloaded]
版本: {self.version}
本软件开源，项目地址:https://github.com/1826013250/NeteaseMusicLyricDownloader
作者:David-123
联系方式:
\tQQ:1826013250
\tE-mail:1826013250@qq.com(mainly)
\t       mc1826013250@gmail.com

Special Thanks:
\t- chenjunyu19, provided the 163key's cipher
\t- website 'MKLAB', provided the AES decryption service""")
    input("按回车键返回...")