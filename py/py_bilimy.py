# coding=utf-8
# !/usr/bin/python
import sys
from base.spider import Spider
import json
import requests
from requests import session, utils
import threading
import os
import time
import base64

sys.path.append('..')


class Spider(Spider):
    box_video_type = ''

    def getDependence(self):
        return ['py_bilibili']

    def getName(self):
        return "我的哔哩"

    def init(self, extend=""):
        self.bilibili = extend[0]
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            # "视频动态": "视频动态",
            "历史记录": "历史记录",
            "我的收藏": "我的收藏",
            "全部关注": "全部关注",
            "追番追剧": "追番追剧",
            "直播中心": "直播中心",
            # ————————以下可自定义UP主，冒号后须填写UID———————————
            # "徐云流浪中国": "697166795",

            # ————————以下可自定义关键词，结果以搜索方式展示————————
            # "宅舞": "宅舞",
            # "cosplay": "cosplay",
            # "周杰伦": "周杰伦",

        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if filter:
            filters = {}
            for lk in cateManual:
                if lk in self.bilibili.config['filter']:
                    filters.update({
                        cateManual[lk]: self.bilibili.config['filter'][lk]
                    })
                elif not cateManual[lk].isdigit() and cateManual[lk] not in ["视频动态", "历史记录", "稍后再看", "我的收藏", "全部关注",
                                                                             "追番追剧", "直播中心"]:
                    link = cateManual[lk]
                    filters.update({
                        link: [{"key": "order", "name": "排序",
                                "value": [{"n": "综合排序", "v": "totalrank"}, {"n": "最新发布", "v": "pubdate"},
                                          {"n": "最多点击", "v": "click"}, {"n": "最多收藏", "v": "stow"},
                                          {"n": "最多弹幕", "v": "dm"}, ]},
                               {"key": "duration", "name": "时长",
                                "value": [{"n": "全部", "v": "0"}, {"n": "60分钟以上", "v": "4"},
                                          {"n": "30~60分钟", "v": "3"}, {"n": "5~30分钟", "v": "2"},
                                          {"n": "5分钟以下", "v": "1"}]}]
                    })
            self.config['filter']['视频动态'] = self.bilibili.config['filter']['动态']
            filters.update(self.config['filter'])
            result['filters'] = filters
        return result

    # 用户cookies，请在py_bilibili里填写，此处不用改
    cookies = ''
    userid = ''
    csrf = ''

    def getCookie(self):
        self.cookies = self.bilibili.getCookie()
        self.userid = self.bilibili.userid
        self.csrf = self.bilibili.csrf
        return self.cookies

    def homeVideoContent(self):
        return {'list': self.bilibili.get_history(1)['list'] + self.bilibili.get_history(2)['list'][0:2]}

    def get_follow(self, pg, sort):
        result = {}
        if sort == "最常访问":
            url = 'https://api.bilibili.com/x/relation/followings?vmid={0}&pn={1}&ps=10&order=desc&order_type=attention' .format(self.userid, pg)
        elif sort == "最近关注":
            url = 'https://api.bilibili.com/x/relation/followings?vmid={0}&pn={1}&ps=10&order=desc&order_type='.format(self.userid, pg)
        elif sort == "特别关注":
            url = 'https://api.bilibili.com/x/relation/tag?mid={0}&tagid=-10&pn={1}&ps=10'.format(self.userid, pg)
        elif sort == "悄悄关注":
            url = 'https://api.bilibili.com/x/relation/whispers?pn={0}&ps=10'.format(pg)
        else:
            url = 'https://api.bilibili.com/x/relation/followers?vmid={0}&pn={1}&ps=10&order=desc&order_type=attention'.format(self.userid, pg)
        rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        if sort == "特别关注":
            vodList = jo['data']
        else:
            vodList = jo['data']['list']
        for vod in vodList:
            aid = str(vod['mid']).strip()
            title = vod['sign'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = vod['face'].strip()
            remark = vod['uname'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.bilibili.format_img(img),
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_zhui(self, pg, mode):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type={2}&follow_status=0&pn={1}&ps=10&vmid={0}'.format(
            self.userid, pg, mode)
        rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            aid = 'ss' + str(vod['season_id']).strip()
            title = vod['title']
            img = vod['cover'].strip() + "@800h_80q.webp"
            remark = vod['new_ep']['index_show'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    lock = threading.Lock()

    def get_vod_play_url(self, vod, aid):
        url = "https://api.bilibili.com/x/web-interface/view?aid=%s" % str(aid)
        rsp = self.fetch(url, headers=self.header)
        jRoot = json.loads(rsp.text)
        part = jRoot['data']['title'].replace("#", "﹟").replace("$", "﹩")
        pages = jRoot['data']['pages']
        playUrl = ''
        if len(pages) > 1:
            for p in pages:
                cid = p['cid']
                p_part = str(p['part']).strip()
                if p_part != part:
                    p_part = (str(p['page']) + "P | " + p_part + "•" + part).replace("#", "﹟").replace("$", "﹩")
                playUrl += '{0}${1}_{2}#'.format(p_part, aid, cid)
        else:
            cid = jRoot['data']['cid']
            playUrl += '{0}${1}_{2}#'.format(part, aid, cid)
        with self.lock:
            vod['vod_play_url'] += playUrl
        return vod

    def categoryContent(self, tid, pg, filter, extend):
        if len(self.cookies) <= 0:
            self.getCookie()

        if tid == '视频动态':
            self.box_video_type = "视频"
            return self.bilibili.categoryContent("动态", pg, filter, extend)

        if tid == "全部关注":
            self.box_video_type = "UP主"
            sort = "最常访问"
            if 'sort' in extend:
                sort = extend['sort']
            return self.get_follow(pg, sort)

        if tid == "追番追剧":
            self.box_video_type = "影视"
            mode = '1'
            if 'mode' in extend:
                mode = extend['mode']
            return self.get_zhui(pg, mode)

        if tid == "直播中心":
            self.box_video_type = "直播"
            tid = '观看记录'
            if 'tid' in extend:
                tid = extend['tid']
            if tid == '在播关注':
                return self.get_live_fav(pg)
            return self.get_live_history()

        if tid.isdigit():
            self.box_video_type = "视频"
            order = 'pubdate'
            if 'order' in extend:
                order = extend['order']
            return self.bilibili.get_up_videos(tid, pg, order)
        else:
            self.box_video_type = "视频"
            result = self.bilibili.categoryContent(tid, pg, filter, extend)
            return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        if self.box_video_type == "UP主":
            mid = array[0]
            self.bilibili.up_mid = mid
            # 获取UP主视频列表，ps后面为视频数量
            url = 'https://api.bilibili.com/x/space/arc/search?mid={0}&pn=1&ps=30'.format(mid)
            rsp = self.fetch(url, headers=self.header)
            content = rsp.text
            jRoot = json.loads(content)
            jo = jRoot['data']['list']['vlist']

            url2 = "https://api.bilibili.com/x/web-interface/card?mid={0}".format(mid)
            rsp2 = self.fetch(url2, headers=self.header)
            jRoot2 = json.loads(rsp2.text)
            jo2 = jRoot2['data']['card']
            name = jo2['name'].replace("<em class=\"keyword\">", "").replace("</em>", "")
            img = jo2['face']
            desc = jo2['Official']['desc'] + "　" + jo2['Official']['title']
            vod = {
                "vod_id": mid,
                "vod_name": name + "　" + "个人主页",
                "vod_pic": self.bilibili.format_img(img),
                "type_name": "最近投稿",
                "vod_year": "",
                "vod_area": "bilidanmu",
                "vod_remarks": "",  # 不会显示
                'vod_tags': 'mv',  # 不会显示
                "vod_actor": "粉丝数：" + self.bilibili.zh(jo2['fans']),
                "vod_director": name,
                "vod_content": desc,
                "vod_play_from": '最新视频',
                "vod_play_url": ""
            }

            for tmpJo in jo:
                aid = tmpJo['aid']
                t = threading.Thread(target=self.get_vod_play_url, args=(vod, aid))
                t.start()
            while True:
                _count = threading.active_count()
                # 计算线程数，不出结果就调大，结果少了就调小
                if _count <= 2:
                    break

            result = {
                'list': [
                    vod
                ]
            }
            return result
        if self.box_video_type == "直播":
            return self.live_detailContent(array)
        else:
            return self.bilibili.detailContent(array)

    def searchContent(self, key, quick):
        self.box_video_type = "UP主"
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword={0}'.format(key)
        rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['mid'])  # str(vod["res"][0]["aid"])
            title = "UP主：" + vod['uname'].strip() + "  ☜" + key
            img = 'https:' + vod['upic'].strip()
            remark = "粉丝数" + self.bilibili.zh(vod['fans'])
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.bilibili.format_img(img),
                "vod_remarks": remark
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        if self.box_video_type == "直播":
            return self.live_playerContent(flag, id, vipFlags)
        else:
            return self.bilibili.playerContent(flag, id, vipFlags)

    config = {
        "player": {},
        "filter": {
            "全部关注": [{"key": "sort", "name": "分类",
                      "value": [{"n": "最常访问", "v": "最常访问"}, {"n": "最近关注", "v": "最近关注"},
                                {"n": "特别关注", "v": "特别关注"}, {"n": "悄悄关注", "v": "悄悄关注"},
                                {"n": "我的粉丝", "v": "我的粉丝"}]}],
            "追番追剧": [{"key": "mode", "name": "分类",
                      "value": [{"n": "追番", "v": "1"}, {"n": "追剧", "v": "2"}, ]}, ],
            "直播中心": [{"key": "tid", "name": "分类",
                      "value": [{"n": "观看记录", "v": "观看记录"}, {"n": "在播关注", "v": "在播关注"}, ]}, ],
        }
    }

    header = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]

    def post_live_history(self, room_id):
        url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/roomEntryAction?platform=pc&room_id={0}&csrf={1}'.format(room_id, self.csrf)
        requests.post(url=url, cookies=self.cookies)

    def get_live_userInfo(self, uid):
        url = 'https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?uids[]=%s' % uid
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            info = [jo['data'][str(uid)]['uname'], jo['data'][str(uid)]['keyframe']]
            return info

    def get_live_fav(self, pg):
        result = {}
        url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/xfetter/GetWebList?page=%s&page_size=10' % pg
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['rooms']
        for vod in vodList:
            aid = str(vod['room_id']).strip()
            title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = vod['cover_from_user'].strip()
            remark = vod['uname'].strip()
            videos.append({
                "vod_id": aid + '&live',
                "vod_name": title,
                "vod_pic": self.bilibili.format_img(img),
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_live_history(self):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/history/cursor?ps=20&type=live'
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
                    "vod_pic": self.bilibili.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def live_detailContent(self, array):
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
                "vod_pic": self.bilibili.format_img(img),
                "type_name": typeName,
                "vod_year": "",
                "vod_area": "bililivedanmu",
                "vod_remarks": remark,
                "vod_actor": "主播：" + dire + "　　" + "房间号：" + aid + "　　" + live_status,
                "vod_director": "关注：" + self.bilibili.zh(jo.get('attention')) + "　　" + "开播时间：" + live_time,
                "vod_content": desc,
            }
            playUrl = 'flv线路原画$platform=web&quality=4_' + aid + '#flv线路高清$platform=web&quality=3_' + aid + '#h5线路原画$platform=h5&quality=4_' + aid + '#h5线路高清$platform=h5&quality=3_' + aid

            vod['vod_play_from'] = '线路选择'
            vod['vod_play_url'] = playUrl
            result = {'list': [vod]}
            return result

    def live_playerContent(self, flag, id, vipFlags):
        result = {}
        ids = id.split("_")
        url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&%s' % (ids[1], ids[0])
        # raise Exception(url)
        if len(self.cookies) <= 0:
            self.getCookie()
        self.post_live_historystr(ids[1])  # 回传直播间观看记录
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
