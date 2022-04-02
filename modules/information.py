"""该程序的自述信息,调用即输出"""
from modules.clear_screen import clear


def print_info(self):
    """调用即输出,无返回值"""
    clear()
    print(f"""[NeteaseMusicLyricDownloader Reloaded]
版本: {self.version}
本软件开源，项目地址:<url>
作者:David-123
联系方式:
    QQ:1826013250
    E-mail:1826013250@qq.com(mainly)
           mc1826013250@gmail.com""")
    input("按回车键返回...")