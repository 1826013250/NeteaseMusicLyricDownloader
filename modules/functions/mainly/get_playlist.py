"""获取歌单中歌曲id"""
from typing import Dict, List
from requests import get
from json import loads

headers = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

def getplaylist(playlist_id: int | str, get_count: int | str = "all") -> Dict[str, str | List[str]]:
    url1 = f"http://play.onlyacat233.top:10002/playlist/track/all?id={playlist_id}"
    url2 = f"http://play.onlyacat233.top:10002/playlist/detail?id={playlist_id}"
    context2 = loads(get(url2).text)

    context1 = loads(get(url1).text)

    playlist = []

    for song in context1['songs']:
        playlist.append(song['id'])

    return {"name": context2['playlist']['name'], "playlist": playlist}

if __name__ == "__main__":
    print(getplaylist("8134802489"))
