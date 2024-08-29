import requests
import re
import json
import subprocess
from DrissionPage import ChromiumPage
from pprint import pprint
# 定义一个访问请求的方法
def GetResponse(url):
    headers = {
        "Cookie":"buvid3=8A30507C-FEE6-4B00-B57F-06C4059D9DE0148792infoc; b_nut=1633419475; LIVE_BUVID=AUTO5516334372509588; buvid_fp_plain=undefined; is-2022-channel=1; buvid4=585863B1-E69D-5578-843A-8FBE5F1F329216757-022012118-ho21%2BqF6LZrjF2BtMHe%2Fpj83ME6qv6VIF6ISNRVipbA8TtjIMRZZDw%3D%3D; header_theme_version=CLOSE; CURRENT_FNVAL=4048; _uuid=32DB810A4-52A5-B49C-D61F-144866B9F106644470infoc; enable_web_push=ENABLE; iflogin_when_web_push=1; b_nut=100; rpdid=|(kmRYul|R|)0J'u~|Jkl)RYl; FEED_LIVE_VERSION=V_DYN_LIVING_UP; hit-dyn-v2=1; CURRENT_QUALITY=80; fingerprint=aa72cfce179a4a6a4eb34549f31f37be; blackside_state=0; CURRENT_BLACKGAP=0; DedeUserID=290773504; DedeUserID__ckMd5=4dd2bd01904e8ff8; dy_spec_agreed=1; PVID=1; home_feed_column=5; SESSDATA=6a511a5d%2C1740372206%2C6f09f%2A81CjC_fIeqLYr2WnpAlhv-N2lTSJb8J4POS9vCMKU3MB8ngWSPYBG80uQUDBHF7yqgtl8SVmptRkprZlZWLTJVN1Bodk0xbGZEaUVoRGJmeGpwY1JSWWtZYllSbTBNQnQtTFlMQTVNeDdLdDVOaFdZZzBWZFJEekRKRzRpa25CYmk0ZnFYc1ZuT1dRIIEC; bili_jct=c4c1763b769210beda01451824bbb9a3; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; browser_resolution=1872-966; sid=8eso5ob0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUxNjU4MjcsImlhdCI6MTcyNDkwNjU2NywicGx0IjotMX0.MAHTomt9VYtwobpWiYG86-6rPTSJsqHJXKROIHa16GM; bili_ticket_expires=1725165767; buvid_fp=aa72cfce179a4a6a4eb34549f31f37be; bp_t_offset_290773504=971060035104800768; b_lsid=9BFC8E62_1919EA463D5",
        "Referer":"https://space.bilibili.com/486487299/video",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }
    response = requests.get(url=url,headers=headers)
    return response
# 获取视频信息
def GetVideoInfo(bv):
    link = f'https://www.bilibili.com/video/{bv}/?spm_id_from=333.999.0.0&vd_source=87b1e885df109569d1174b24b6ebf378'
    response = GetResponse(url=link)
    html = response.text
    info = re.findall('<script>window.__playinfo__=(.*?)</script>',html)[0]
    json_data = json.loads(info)
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    title = re.findall('<h1 data-title="(.*?)" title="',html)[0]
    # print(title)
    # print(audio_url)
    # print(video_url)
    return title,audio_url,video_url
# 保存数据
def Save(title,audio_url,video_url):
    audio_connet = GetResponse(url=audio_url).content
    video_connet = GetResponse(url=video_url).content
    with open('audio\\' + title + '.mp3',mode='wb') as audio:
        audio.write(audio_connet)
    with open('video\\' + title + '.mp4', mode='wb') as video:
        video.write(video_connet)

    cmd = f"ffmpeg -hide_banner -i video\\{title}.mp4 -i audio\\{title}.mp3 -c:v copy -c:a aac -strict experimental output\\{title}.mp4"
    subprocess.run(cmd)
if __name__ == '__main__':
    try:
        ID = input("请输入up的uid：")
        driver = ChromiumPage()
        driver.listen.start('api.bilibili.com/x/space/wbi/arc/search')
        driver.get(f'https://space.bilibili.com/{ID}/video')
        for page in range(1):
            resp = driver.listen.wait()
            JsonData = resp.response.body
            for index in JsonData['data']['list']['vlist']:
                bv = index['bvid']
                title,audio_url,video_url = GetVideoInfo(bv=bv)
                Save(title,audio_url,video_url)
            driver.ele('css:.be-pager-next').click()
    except ZeroDivisionError:
        print("结束")