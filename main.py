#!/usr/bin/env python3
# ↑ For Linux & MacOS to run this program directly if the user currently installed python and third-party packages.
# -*- coding: utf-8 -*-
# author: David-123


from modules.raw_input import rinput
from modules.information import print_info
from modules.multi_download import mdl
from modules.one_download import download_one_lyric
from modules.settings import settings_menu
from modules.save_load_settings import load_settings
from modules.clear_screen import clear


class MainProcess(object):
    def __init__(self):  # 项目初始化
        self.settings = load_settings()
        self.version = "0.0.0"

    def mainloop(self):
        """程序主循环"""
        while True:
            clear()
            print(f"[NeteaseMusicLyricDownloader Reloaded] {self.version}\n"
                  "[程序主菜单]\n"
                  "[0] 退出程序\n[i] 程序信息\n[1] 单个歌曲的歌词下载\n[2] 多个歌曲的歌词下载\n[s] 进入设置")
            r = rinput("请选择:")

            if r == "1":
                download_one_lyric(self.settings.lyric_path)
            elif r == "2":
                mdl(self.settings.lyric_path)
            elif r == "0":
                exit(0)
            elif r == "i":
                print_info(self)
            elif r == "s":
                settings_menu(self)
            else:
                input("请输入正确的选项\n按回车键继续...")


if __name__ == "__main__":
    app = MainProcess()
    app.mainloop()
