import requests
import os
from urllib.parse import quote

# 1. 搜索歌曲，获取歌曲列表
def search_music(keyword):
    url = f"https://www.kuwo.cn/search/searchMusicBykeyWord?vipver=1&client=kt&ft=music&cluster=0&strategy=2012&encoding=utf8&rformat=json&mobi=1&issubtitle=1&show_copyright_off=1&pn=0&rn=20&all={quote(keyword)}"
    headers = {
        "cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1752049254; HMACCOUNT=F2F07F5DFFD2834B; _ga=GA1.2.90468476.1752049254; _gid=GA1.2.1081785489.1752049254; _ga_ETPBRPM9ML=GS2.2.s1752049254$o1$g1$t1752049258$j56$l0$h0; _gat=1; Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324=jFdak2xyHt7D6Qdj8ActFBDGtDMJzz6Q; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1752049368",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    }
    response = requests.get(url, headers=headers)
    return response.json().get("abslist", [])

# 2. 获取歌曲真实播放链接
def get_music_url(mid):
    url = f"https://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}&type=music&httpsStatus=1&reqId=e5b59970-5c9d-11f0-b81c-1fd126b5188e&plat=web_www&from="
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "connection": "keep-alive",
        "cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1752049254; HMACCOUNT=F2F07F5DFFD2834B; _ga=GA1.2.90468476.1752049254; _gid=GA1.2.1081785489.1752049254; _ga_ETPBRPM9ML=GS2.2.s1752049254$o1$g1$t1752049258$j56$l0$h0; _gat=1; Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324=jFdak2xyHt7D6Qdj8ActFBDGtDMJzz6Q; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1752049368",
        "host": "www.kuwo.cn",
        "referer": "https://www.kuwo.cn/search/list?key=%E5%96%9C%E6%AC%A2%E4%BD%A0",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "secret": "4916efc37a151052965197d57debd547308e92a371b8d8407dc436d3fcfc53dd04febb39",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("code") == 200 and data.get("data") and data["data"].get("url"):
        return data["data"]["url"]
    return None

# 3. 下载歌曲
def download_music(url, title):
    folder = os.path.join(os.getcwd(), "mp3")
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{title}.mp3")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return filename

# 4. 主流程示例
if __name__ == "__main__":
    keyword = input("请输入歌曲名称: ")
    songs = search_music(keyword)
    if not songs:
        print("未找到歌曲")
        exit()

    print(f"共找到{len(songs)}首歌曲，展示前5首：")
    for i, song in enumerate(songs[:5]):
        print(f"{i+1}. {song['SONGNAME']} - {song['ARTIST']}")

    choice = int(input("请输入要下载的歌曲序号: ")) - 1
    if choice < 0 or choice >= len(songs[:5]):
        print("无效序号")
        exit()

    selected = songs[choice]
    print(f"正在获取《{selected['SONGNAME']}》的播放链接...")
    music_url = get_music_url(selected["DC_TARGETID"])
    if not music_url:
        print("获取播放链接失败，可能是VIP或接口限制")
        exit()

    print(f"开始下载《{selected['SONGNAME']}》...")
    filepath = download_music(music_url, selected["SONGNAME"])
    print(f"下载完成，文件保存到：{filepath}")