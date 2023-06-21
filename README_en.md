NeteaseMusicLyricDownloader
===========================
**English**|[简体中文](./README.md)

A simple tool to download lyrics in Netease Music

_*Caution:* The author is not native English speaker. If there are some grammar mistakes, please ignore them. Thanks!!!!_

## How does it work?
It uses the module `requests` to fetch the lyric on music.163.com

Netease Music supply us an api that we can get the lyric of the current song, so I make this program...

## Installation
First, you need a python(>=3.10) environment

Second, clone the entire project and install packages with the command below:
```commandline
python3 -m pip install -r requirements.txt
```
Last, run the command `python3 main.py` in the project folder.

## What can it do?
Just download lyrics.

You need to provide the id or the share link of the song, and the program will download the lyrics automatically.

Now it can recognize 163 key in music files that download from Netease Cloudmusic client.

- 2022/8/13 Now it has the function from `ncmdump`, and it can decrypt the ncm files and fetch the specific lyric.

## Todo

Add more functions like searching...

## Others

Just a easy program...

I don't have much time to focus on it...
