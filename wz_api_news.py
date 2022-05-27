# -*- coding: utf-8 -*-
import os
import requests
import time # 引入time
import logging
import configparser
import json
# ===================全域變數====================
Error_Log_Path = './logs/'
POST_HEADER = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "sso_token_king=5n0n3aa8mr0owc4s404gwo4o8gk8os4c0oo8g8swk8swkcwwss; GCLB=CMXhrtOKrJe3Xg; sso_verify_king=1snckgde8mw0ks4g8okok0skc44sowk40sw8kggoc044kkoggk; PHPSESSID=a1b968c1757fe7a65c96977eda545c7c; BJYSESSION=a1b968c1757fe7a65c96977eda545c7c; Hm_lvt_e5378fff1db5d9e5624629a74e0efbf0=1652675165,1652768641,1652865092,1652932026; Hm_lpvt_e5378fff1db5d9e5624629a74e0efbf0=1652932037; SERVERID=e1aae90670045f45e083e2f835f05d49|1652932050|1652932022",
    "if-modified-since": "Wed, 27 Apr 2022 10:11:03 GMT",
    "if-none-match": 'W/"626916b7-c6a"',
    "referer": "https://www.zhibo16.live/index.php?g=&m=index&a=index",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

# 讀取config
config = configparser.ConfigParser()    # 注意大小寫
config.read("config.ini")   # 配置檔案的路徑
# 紀錄Terminal內error的log
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# 製作檢查用LOG
def create_logger():
    # config
    time_day = time.strftime("%Y%m%d")
    time_hm = time.strftime("%m%d%H%M")
    filename = f'error_{time_hm}.log'    # 設定檔名
    logging.captureWarnings(True)   # 捕捉 py waring message
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger('py.warnings')    # 捕捉 py waring message
    my_logger.setLevel(logging.ERROR)
    
    # 若不存在目錄則新建
    if not os.path.exists(Error_Log_Path+time_day):
        os.makedirs(Error_Log_Path+time_day)
    
    # file handler
    fileHandler = logging.FileHandler(Error_Log_Path+time_day+'/'+filename, 'a+', 'utf-8')
    fileHandler.setFormatter(formatter)
    my_logger.addHandler(fileHandler)
    
    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)
        
    return my_logger

# 轉換日期格式至UNIX
def time_trans(qurey_date):
    struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
    time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
    return time_stamp


# 新聞標題 = post_title  ，標題圖片 = ['smeta']['thumb'] ， 新聞內容 = post_content
def cawler_news():
    time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    api_url = f"https://pwa.zhibo16.live/pwa-api/index.php?g=H5&m=News&a=newsDetail&_={time_trans(time_params)}"
    lastime_cawler_date = config['last_record']['lastime_cawler_date']
    lastime_cawler_id = int(config['last_record']['lastime_cawler_id'])
    news_data = []
    try:
        # 透過發布文章ID為參數獲取文章
        for news_id in range(lastime_cawler_id,lastime_cawler_id + 20):
            data = {'id':'', 'news_title':'', 'title_pic':'', 'news_content':'', 'publish_date':''}
            my_params = {'id': news_id}
            r = requests.post(api_url, data=my_params, headers=POST_HEADER)
            resource_json = r.json()
            # 上一次爬取的最後一篇新聞發布時間
            try:
                # 沒有新文章就不爬了
                if resource_json['data']['detail']['post_title'] != '':
                    # 用發布日期判斷新聞是否已經爬過了
                    publishtime = resource_json['data']['detail']['publishtime']
                    if time_trans(lastime_cawler_date) < time_trans(publishtime):
                        data['id'] = news_id
                        data['news_title'] = resource_json['data']['detail']['post_title']
                        data['title_pic'] = resource_json['data']['detail']['smeta']['thumb']
                        data['news_content'] = resource_json['data']['detail']['post_content']
                        data['publish_date'] = publishtime
                        news_data.append(data)
                    else:
                        pass

                else:
                    break

            except Exception as e:
                pass

    except Exception as e:
        # 紀錄最後一筆新聞ID、發布日期
        logger = create_logger()
        logger.exception(e)
        logger.critical(f'last_get : {news_data}')
        pass

    finally:
        if news_data:
            last_news_data = news_data[-1]
            config.set('last_record', 'lastime_cawler_date', last_news_data['publish_date'])
            config.set('last_record', 'lastime_cawler_id', str(last_news_data['id']))
            config.write(open('config.ini', 'w'))    # 一定要寫入才生效
        else:
            pass

    return news_data

if __name__ == '__main__':
    # result = cawler_news()
    result = [{'id': 31449, 'news_title': '【羽球】3-0！中国女团闯入4强，创下20届神迹，剑指尤伯杯冠军', 'title_pic': 'https://a0-prod-up.luziedu.com/data/upload/20220512/627c9e0ec25ca.jpg', 'news_content': '<p>北京时间5月12日，世界羽联尤伯杯1/4决赛打响 。在率先进行的一场对决中，中国女团3-0横扫印度尼西亚，顺利晋级4强。这也是中国女团连续第20届晋级尤杯半决赛，自从。中国队在半决赛的对手，将是印度和泰国之间的胜者。</p><p><br/></p><p style="text-align:center"><img src="https://a0-prod-up.luziedu.com/data/upload/20220512/627c9d1969506.jpg" title="" alt="" width="480" height="310" border="0" vspace="0" style="width: 480px; height: 310px;"/></p><p><br/></p><p>首场比赛，中国一号女单陈雨菲对阵印尼选手德维。陈雨菲世界排名高居第三，去年还拿下了奥运女单金牌，是世界顶尖选手。而对手的世界排名则是203位。这场比赛并没有太大的悬念，陈雨菲21-12/21-11拿下对手，帮助中国队拿下第一分。</p><p><br/></p><p style="text-align:center"><img src="https://a0-prod-up.luziedu.com/data/upload/20220512/627c9d309f403.jpg" title="" alt="" width="480" height="314" border="0" vspace="0" style="width: 480px; height: 314px;"/></p><p><br/></p><p>第二场比赛，中国一号女双陈清晨/贾一凡对阵库苏玛/普拉蒂维。中国组合世界排名第一，而对手的世界排名仅有第103位。这场比赛第一局，陈清晨/贾一凡打得相对艰难，一路战至19平后，陈清晨/贾一凡连得2分拿下。第二局，中国组合状态提升明显，21-16再胜，最终2-0击败对手。</p><p><br/></p><p style="text-align:center"><img src="https://a0-prod-up.luziedu.com/data/upload/20220512/627c9d4815f05.jpg" title="" alt="" width="480" height="306" border="0" vspace="0" style="width: 480px; height: 306px;"/></p><p><br/></p><p>第三场比赛，中国二号女单何冰娇对阵小将普拉西斯。何冰娇一上来显得比较慢热，第一局出人意料地19-21告负。不过何冰娇很快提升状态，第二局21-18拿下。第三局，对手体能出现明显问题，何冰娇21-7再胜，2-1取得 胜利。</p><p><br/></p><p style="text-align:center"><img src="https://a0-prod-up.luziedu.com/data/upload/20220512/627c9d82aca91.jpg" title="" alt="" width="480" height="240" border="0" vspace="0" style="width: 480px; height: 240px;"/></p><p><br/></p><p>就此，中国队闯入尤伯杯4强，连续20届赛事晋级4强，稳定性非常出色。考虑到日本、韩国和中国台北都被分在上半区，面对泰国和印度之间的胜者，中国队有望直通决赛。</p><p><br/></p><p>来源:腾讯体育</p>', 'publish_date': '2022-05-12 15:02:00'},
    
     {'id': 31451, 'news_title': '【欧冠之王（4）】C罗沦落全英公敌？ 曼联差点失去这位天才 ', 'title_pic': 'https://a0-prod-up.luziedu.com/data/upload/20220512/627cb5860dc32.png', 'news_content': '<p style="text-align: center;"><video class="edui-upload-video  vjs-default-skin video-js" controls="" preload="none" width="880" height="480" src="https://a0-prod-up.luziedu.com/data/upload/20220512/627cb57fc3d3d.mp4" data-setup="{}"><source src="https://a0-prod-up.luziedu.com/data/upload/20220512/627cb57fc3d3d.mp4" type="video/mp4"/></video></p>', 'publish_date': '2022-05-12 15:21:00'},
     
     
      {'id': 31452, 'news_title': '【NBA】恩比德哈登迎生死战，必将全力出击', 'title_pic': 'https://a0-prod-up.luziedu.com/data/upload/20220512/627cbc885d208.jpg', 'news_content': '<p style="text-align: center;"><video class="edui-upload-video  vjs-default-skin video-js" controls="" preload="none" width="800" height="480" src="https://a0-prod-up.luziedu.com/data/upload/20220512/627cbc9c19a1d.mp4" data-setup="{}"><source src="https://a0-prod-up.luziedu.com/data/upload/20220512/627cbc9c19a1d.mp4" type="video/mp4"/></video></p>', 'publish_date': '2022-05-12 15:51:00'}]

    with open('./data/news_data.json', 'w') as file:
        json.dump(result, file)


