# coding=utf-8
# !/usr/bin/python
import sys
from base.spider import Spider
import json
import requests
from requests import session, utils
import time
import base64
sys.path.append('..')


class Spider(Spider):
    def getDependence(self):
        return ['py_bilibili']

    def getName(self):
        return "哔哩直播"

    # 主页
    def homeContent(self, filter):
        result = {}
        cateManual = {
            "推荐": "推荐",
        }
        url = 'https://api.live.bilibili.com/xlive/web-interface/v1/index/getWebAreaList?source_id=2'
        rsp = self.fetch(url, headers=self.header, cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        parent_area_list = jo['data']['data']
        for parent_area in parent_area_list:
            name = parent_area['name']
            id = str(parent_area['id'])
            cateManual[name] = id
            self.config['filter'][id] = [{
                    'key': 'area_id', 'name': '全部分类', 'value': []
                }]
            area_list = []
            for area in parent_area['list']:
                area_dict = {'n': area['name'], 'v': area['id']}
                area_list.append(area_dict)
                if self.config['filter'].get(id):
                    for i in self.config['filter'].get(id):
                        if i['key'] == 'area_id':
                            i['value'] = area_list

        # cateManual["我的关注"] = "我的关注"
        # cateManual["观看记录"] = "观看记录"

        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if filter:
            result['filters'] = self.config['filter']
        return result

    # 用户cookies
    cookies = ''
    userid = ''
    csrf = ''

    def getCookie(self):
        self.cookies = self.bilibili.getCookie()
        self.userid = self.bilibili.userid
        self.csrf = self.bilibili.csrf
        return self.cookies

        # 单用此文件，请注释掉删除上面4行，取消注释以下
        # import http.cookies
        # raw_cookie_line = ""
        # simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        # cookie_jar = requests.cookies.RequestsCookieJar()
        # cookie_jar.update(simple_cookie)
        # rsp = session()
        # rsp.cookies = cookie_jar
        # content = self.fetch("https://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
        # res = json.loads(content.text)
        # if res["code"] == 0:
        #     self.cookies = rsp.cookies
        #     self.userid = res["data"].get('mid')
        #     self.csrf = rsp.cookies['bili_jct']
        # return cookie_jar

    def init(self, extend=""):
        self.bilibili = extend[0]
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    # 格式化图片，默认为80%质量的webp格式，降低内存占用
    def format_img(self, img):
        img += "@360h_80q.webp"  # 格式，[jpg/png/gif]@{width}w_{high}h_{quality}q.{format}
        return img

    # 将超过10000的数字换成成以万和亿为单位
    def zh(self, num):
        if int(num) >= 100000000:
            p = round(float(num) / float(100000000), 1)
            p = str(p) + '亿'
        else:
            if int(num) >= 10000:
                p = round(float(num) / float(10000), 1)
                p = str(p) + '万'
            else:
                p = str(num)
        return p

    def get_live_userInfo(self, uid):
        url = 'https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?uids[]=%s' % uid
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            info = [jo['data'][str(uid)]['uname'], jo['data'][str(uid)]['keyframe']]
            return info

    def post_live_history(self, room_id):
        url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/roomEntryAction?platform=pc&room_id={0}&csrf={1}'.format(room_id, self.csrf)
        requests.post(url=url, cookies=self.cookies)

    def homeVideoContent(self, ):
        return self.get_hot(1)

    def get_recommend(self, pg):
        result = {}
        url = 'https://api.live.bilibili.com/xlive/web-interface/v1/webMain/getList?platform=web&page=%s' % pg
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['recommend_room_list']
            for vod in vodList:
                aid = str(vod['roomid']).strip()
                title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                img = vod['keyframe'].strip()
                remark = vod['watched_show']['text_small'].strip() + "　" + vod['uname'].strip()
                videos.append({
                    "vod_id": aid + '&live',
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 10
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_hot(self, pg):
        result = {}
        url = 'https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=%s&page_size=12' % pg
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']
            for vod in vodList:
                aid = str(vod['roomid']).strip()
                title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                img = vod['user_cover'].strip()
                remark = vod['watched_show']['text_small'].strip() + "　" + vod['uname'].strip()
                videos.append({
                    "vod_id": aid + '&live',
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_live(self, pg, parent_area_id, area_id):
        result = {}
        url = 'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=%s&area_id=%s&sort_type=online&page=%s' % (
            parent_area_id, area_id, pg)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['roomid']).strip()
                title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                img = vod.get('cover').strip()
                remark = vod['watched_show']['text_small'].strip() + "　" + vod['uname'].strip()
                videos.append({
                    "vod_id": aid + '&live',
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_fav(self, pg, live_status):
        result = {}
        url = 'https://api.live.bilibili.com/xlive/web-ucenter/user/following?page=%s&page_size=10' % pg
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            if live_status == str(vod['live_status']):
                aid = str(vod['roomid']).strip()
                title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                if live_status == "0":
                    img = vod['face'].strip()
                else:
                    img = self.get_live_userInfo(vod['uid'])[1]
                remark = vod['uname'].strip()
                videos.append({
                    "vod_id": aid + '&live',
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_history(self):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/history/cursor?ps=24&type=live'
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['history']['oid']).strip()
                title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                img = vod['cover'].strip()
                remark = str(vod['live_status']).replace("0", "未开播　").replace("1", "") + vod[
                    'author_name'].strip()
                videos.append({
                    "vod_id": aid + '&live',
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        if tid.isdigit():
            parent_area_id = tid
            area_id = 0
            if 'area_id' in extend:
                area_id = extend['area_id']
            return self.get_live(pg=pg, parent_area_id=parent_area_id, area_id=area_id)
        if tid == "推荐":
            return self.get_recommend(pg)
        if tid == "我的关注":
            live_status = "1"
            if 'live_status' in extend:
                live_status = extend['live_status']
            return self.get_fav(pg, live_status)
        if tid == "观看记录":
            return self.get_history()
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        arrays = array[0].split("&")
        aid = arrays[0]
        url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s" % aid
        rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
        jRoot = json.loads(rsp.text)
        if jRoot.get('code') == 0:
            jo = jRoot['data']
            title = jo['title'].replace("<em class=\"keyword\">", "").replace("</em>", "")
            img = jo.get("user_cover")
            desc = jo.get('description')
            dire = self.get_live_userInfo(jo["uid"])[0]
            typeName = jo.get("area_name")
            live_status = str(jo.get('live_status')).replace("0", "未开播").replace("1", "").replace("2", "")
            live_time = str(jo.get('live_time'))[5: 16]
            remark = '在线人数:' + str(jo['online']).strip()
            vod = {
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.format_img(img),
                "type_name": typeName,
                "vod_year": "",
                "vod_area": "bililivedanmu",
                "vod_remarks": remark,
                "vod_actor": "主播：" + dire + "　　" + "房间号：" + aid + "　　" + live_status,
                "vod_director": "关注：" + self.zh(jo.get('attention')) + "　　" + "开播时间：" + live_time,
                "vod_content": desc,
            }
            playUrl = 'flv线路原画$platform=web&quality=4_' + aid + '#flv线路高清$platform=web&quality=3_' + aid + '#h5线路原画$platform=h5&quality=4_' + aid + '#h5线路高清$platform=h5&quality=3_' + aid

            vod['vod_play_from'] = '线路选择'
            vod['vod_play_url'] = playUrl
            result = {
                'list': [
                    vod
                ]
            }
            return result

    def searchContent(self, key, quick):
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=live&keyword={0}&page=1'.format(key)
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url, cookies=self.cookies, headers=self.header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            rspRetry = self.fetch(url, cookies=self.cookies, headers=self.header)
            content = rspRetry.text
        jo = json.loads(content)
        videos1 = []
        if jo['data']['pageinfo']['live_room']['numResults'] != 0:
            vodList = jo['data']['result']['live_room']
            for vod in vodList:
                aid = str(vod['roomid']).strip()
                title = "直播间：" + vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>",
                                                                                                    "") + "⇦" + key
                img = 'https:' + vod['user_cover'].strip()
                remark = vod['watched_show']['text_small'].strip() + "  " + vod['uname'].strip()
                videos1.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
        videos2 = []
        if jo['data']['pageinfo']['live_user']['numResults'] != 0:
            vodList = jo['data']['result']['live_user']
            for vod in vodList:
                aid = str(vod['roomid']).strip()
                title = "直播间：" + vod['uname'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "") + " ⇦" + key
                img = 'https:' + vod['uface'].strip()
                remark = str(vod['live_status']).replace("0", "未开播").replace("1", "") + "  关注：" + self.zh(
                    vod['attentions'])
                videos2.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
        videos = videos1 + videos2
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        ids = id.split("_")

        url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&%s' % (ids[1], ids[0])

        # raise Exception(url)
        if len(self.cookies) <= 0:
            self.getCookie()
        self.post_live_history(ids[1])  # 回传直播间观看记录
        rsp = self.fetch(url, cookies=self.cookies)
        jRoot = json.loads(rsp.text)
        if jRoot['code'] == 0:

            jo = jRoot['data']
            ja = jo['durl']

            url = ''
            if len(ja) > 0:
                url = ja[0]['url']

            result["parse"] = 0
            # result['type'] ="m3u8"
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = {
                "Referer": "https://live.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }

            if "h5" in ids[0]:
                result["contentType"] = ''
            else:
                result["contentType"] = 'video/x-flv'
        return result

    config = {
        "player": {},
        "filter": {
            "我的关注": [
                {"key": "live_status", "name": "全部分类",
                 "value": [{"n": "直播中", "v": "1"}, {"n": "未开播", "v": "0"}, ]}, ],
        }
    }
    header = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def localProxy(self, param):

        return [200, "video/MP2T", action, ""]
