import json
import os
import re
from tinytag import TinyTag
from requests import post
from modules.get_song import get_song_lyric
from modules.clear_screen import clear


def load_information_from_mp3(path):
    """从音乐文件中的 Comment 字段获取 163 key 并解密返回歌曲信息"""
    file = TinyTag.get(path)  # 使用 TinyTag 获取歌曲信息
    if file.comment:
        if file.comment[:7] == "163 key":
            ciphertext = file.comment[22:]
        else:
            return "not_support"
    else:
        return "not_support"
    data = {
        "data": ciphertext,
        "type": "aes_decrypt",
        "encode": "base64",
        "key": "#14ljk_!\\]&0U<'(",  # 感谢大佬 chenjunyu19 在 MorFans Dev 上提供的密文密钥
        "digit": 128,
        "mode": "ECB",
        "pad": "Pkcs5Padding"
    }
    try:
        r = post("https://www.mklab.cn/utils/handle", data=data).text[17:-2].replace("\\\"", "\"")  # 十分感谢 MKLAB 网站提供的解密接口!!
    except ConnectionError:
        return "dl_err_connection"
    if r:
        return json.loads(r)
    else:
        return "decrypt_failed"


def get_lyric_from_folder(lyric_path: str):
    clear()
    path = input("请输入歌曲的保存文件夹(绝对路径):").strip().replace("\\", "/")
    if not os.path.exists(path):
        input("路径不存在,请检查输入...")
        return
    if path[-1] != "/":
        path += "/"

    print("正在遍历目录,请稍后...")
    musics = []
    fails = 0
    for i in os.listdir(path):  # 遍历目录,查找目标文件
        match = re.match(r".*\.((mp3)|(flac))$", i)
        if match:
            result = load_information_from_mp3(path+match.group())
            if result == "not_support":
                fails += 1
                print(f"文件 \"{i}\" 未包含 163 key ,跳过")
            elif result == "decrypt_failed":
                fails += 1
                print(f"文件 \"{i}\" 内 163 key 解密失败,跳过")
            elif result == "dl_err_connection":
                input("获取解密结果失败!请检查网络连接是否正常,若确信自身没有问题请向作者反馈是否解密接口出现问题!")
                return
            else:
                musics.append({"id": result['musicId'], "name": result["musicName"], "artists": result["artist"]})

    # 汇报索引结果
    print(f"\n索引完毕!共找到{fails+len(musics)}个目标文件\n{len(musics)}个文件已载入\n{fails}个文件失败\n")
    while True:
        r = input("你希望如何保存这些歌曲的歌词?\n[1]保存到刚刚输入的绝对路径中\n[2]保存到程序设定的下载路径中\n请选择: ").strip().lower()
        if r == "1":
            break
        elif r == "2":
            path = lyric_path
            break
        else:
            try:
                input("无效选择, 若取消请按 ^C ,继续请按回车")
                clear()
            except KeyboardInterrupt:
                return

    clear()
    for i in range(0, len(musics)):  # 根据索引结果获取歌词
        print("\n进度: %d/%d" % (i + 1, len(musics)))
        if get_song_lyric(musics[i], path, allinfo=True) == "dl_err_connection":
            input("下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
    input("按回车键返回...")
    return
