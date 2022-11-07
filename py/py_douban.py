#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

host_url = 'https://frodo.douban.com/api/v2'
apikey = "?apikey=0ac44ae016490db2204ce0a042db2916"

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "豆瓣"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"热门电影": "hot_gaia",
			"热播剧集": "tv_hot",
			"热播综艺": "show_hot",
			"电影筛选": "movie",
			"电视筛选": "tv",
			"电影榜单": "rank_list_movie",
			"电视榜单": "rank_list_tv"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		url = host_url + '/subject_collection/subject_real_time_hotest/items' + apikey
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		joList = jo.get("subject_collection_items")
		lists = []
		for item in joList:
			rating = item['rating']['value'] if item['rating'] else ""
			lists.append({
				"vod_id": f'msearch:{item.get("type", "")}__{item.get("id", "")}',
				"vod_name": item['title'],
				"vod_pic": item['pic']['normal'],
				"vod_remarks": rating
			})
		result = {
			'list':lists
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		if extend:
			sort = extend.pop('sort') if "sort" in extend else "T"
			tags = ",".join(item for item in extend.values())
		else:
			sort = "T"
			tags = ""
		if tid == "hot_gaia":
			urlpath = f"/movie/{tid}"
			getdata = "items"
			sort = extend.get("sort", "recommend")
			area = extend.get("area", "全部")
			sort = sort + "&area=" + area
		elif tid == "tv_hot" or tid == "show_hot":
			urlpath = f"/subject_collection/{tid}/items"
			getdata = "subject_collection_items"
		elif tid.startswith("rank_list"):
			id = "movie_real_time_hotest" if tid == "rank_list_movie" else "tv_real_time_hotest"
			urlpath = f"/subject_collection/{id}/items"
			getdata = "subject_collection_items"
		else:
			urlpath = f"/{tid}/recommend"
			getdata = "items"

		url = host_url + urlpath + apikey + '&sort=' + sort + '&tags=' + tags + '&start=' + str((int(pg) - 1) * 30)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		jolist = jo[getdata]

		videos = []
		for vod in jolist:
			rating = vod.get("rating", "").get("value", "") if vod.get("rating", "") else ""
			pic = vod.get("pic", "").get("normal", "") if vod.get("pic", "") else ""
			videos.append({
				"vod_id": f'msearch:{vod.get("type", "")}__{vod.get("id", "")}',
				"vod_name": vod['title'],
				"vod_pic": pic,
				"vod_remarks": rating
			})

		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result

	def detailContent(self,array):
		pass
	def searchContent(self,key,quick):
		pass
	def playerContent(self,flag,id,vipFlags):
		pass

	config = {
		"player": {},
		"filter": {"hot_gaia":[{"key":"sort","name":"排序","value":[{"n":"热度","v":"recommend"},{"n":"最新","v":"time"},{"n":"评分","v":"rank"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":"全部"},{"n":"华语","v":"华语"},{"n":"欧美","v":"欧美"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"}]}],"tv_hot":[{"key":"type","name":"分类","value":[{"n":"综合","v":"tv_hot"},{"n":"国产剧","v":"tv_domestic"},{"n":"欧美剧","v":"tv_american"},{"n":"日剧","v":"tv_japanese"},{"n":"韩剧","v":"tv_korean"},{"n":"动画","v":"tv_animation"}]}],"show_hot":[{"key":"type","name":"分类","value":[{"n":"综合","v":"show_hot"},{"n":"国内","v":"show_domestic"},{"n":"国外","v":"show_foreign"}]}],"movie":[{"key":"类型","name":"类型","value":[{"n":"全部类型","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"动作","v":"动作"},{"n":"科幻","v":"科幻"},{"n":"动画","v":"动画"},{"n":"悬疑","v":"悬疑"},{"n":"犯罪","v":"犯罪"},{"n":"惊悚","v":"惊悚"},{"n":"冒险","v":"冒险"},{"n":"音乐","v":"音乐"},{"n":"历史","v":"历史"},{"n":"奇幻","v":"奇幻"},{"n":"恐怖","v":"恐怖"},{"n":"战争","v":"战争"},{"n":"传记","v":"传记"},{"n":"歌舞","v":"歌舞"},{"n":"武侠","v":"武侠"},{"n":"情色","v":"情色"},{"n":"灾难","v":"灾难"},{"n":"西部","v":"西部"},{"n":"纪录片","v":"纪录片"},{"n":"短片","v":"短片"}]},{"key":"地区","name":"地区","value":[{"n":"全部地区","v":""},{"n":"华语","v":"华语"},{"n":"欧美","v":"欧美"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"},{"n":"中国大陆","v":"中国大陆"},{"n":"美国","v":"美国"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"英国","v":"英国"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"意大利","v":"意大利"},{"n":"西班牙","v":"西班牙"},{"n":"印度","v":"印度"},{"n":"泰国","v":"泰国"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"加拿大","v":"加拿大"},{"n":"澳大利亚","v":"澳大利亚"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"丹麦","v":"丹麦"}]},{"key":"sort","name":"排序","value":[{"n":"近期热度","v":"T"},{"n":"首映时间","v":"R"},{"n":"高分优先","v":"S"}]},{"key":"年代","name":"年代","value":[{"n":"全部年代","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2010年代","v":"2010年代"},{"n":"2000年代","v":"2000年代"},{"n":"90年代","v":"90年代"},{"n":"80年代","v":"80年代"},{"n":"70年代","v":"70年代"},{"n":"60年代","v":"60年代"},{"n":"更早","v":"更早"}]}],"tv":[{"key":"类型","name":"类型","value":[{"n":"不限","v":""},{"n":"电视剧","v":"电视剧"},{"n":"综艺","v":"综艺"}]},{"key":"电视剧形式","name":"电视剧形式","value":[{"n":"不限","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"悬疑","v":"悬疑"},{"n":"动画","v":"动画"},{"n":"武侠","v":"武侠"},{"n":"古装","v":"古装"},{"n":"家庭","v":"家庭"},{"n":"犯罪","v":"犯罪"},{"n":"科幻","v":"科幻"},{"n":"恐怖","v":"恐怖"},{"n":"历史","v":"历史"},{"n":"战争","v":"战争"},{"n":"动作","v":"动作"},{"n":"冒险","v":"冒险"},{"n":"传记","v":"传记"},{"n":"剧情","v":"剧情"},{"n":"奇幻","v":"奇幻"},{"n":"惊悚","v":"惊悚"},{"n":"灾难","v":"灾难"},{"n":"歌舞","v":"歌舞"},{"n":"音乐","v":"音乐"}]},{"key":"综艺形式","name":"综艺形式","value":[{"n":"不限","v":""},{"n":"真人秀","v":"真人秀"},{"n":"脱口秀","v":"脱口秀"},{"n":"音乐","v":"音乐"},{"n":"歌舞","v":"歌舞"}]},{"key":"地区","name":"地区","value":[{"n":"全部地区","v":""},{"n":"华语","v":"华语"},{"n":"欧美","v":"欧美"},{"n":"国外","v":"国外"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"},{"n":"中国大陆","v":"中国大陆"},{"n":"中国香港","v":"中国香港"},{"n":"美国","v":"美国"},{"n":"英国","v":"英国"},{"n":"泰国","v":"泰国"},{"n":"中国台湾","v":"中国台湾"},{"n":"意大利","v":"意大利"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"西班牙","v":"西班牙"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"丹麦","v":"丹麦"},{"n":"印度","v":"印度"},{"n":"加拿大","v":"加拿大"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"澳大利亚","v":"澳大利亚"}]},{"key":"sort","name":"排序","value":[{"n":"近期热度","v":"T"},{"n":"首播时间","v":"R"},{"n":"高分优先","v":"S"}]},{"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2010年代","v":"2010年代"},{"n":"2000年代","v":"2000年代"},{"n":"90年代","v":"90年代"},{"n":"80年代","v":"80年代"},{"n":"70年代","v":"70年代"},{"n":"60年代","v":"60年代"},{"n":"更早","v":"更早"}]},{"key":"平台","name":"平台","value":[{"n":"全部","v":""},{"n":"腾讯视频","v":"腾讯视频"},{"n":"爱奇艺","v":"爱奇艺"},{"n":"优酷","v":"优酷"},{"n":"湖南卫视","v":"湖南卫视"},{"n":"Netflix","v":"Netflix"},{"n":"HBO","v":"HBO"},{"n":"BBC","v":"BBC"},{"n":"NHK","v":"NHK"},{"n":"CBS","v":"CBS"},{"n":"NBC","v":"NBC"},{"n":"tvN","v":"tvN"}]}],"rank_list_movie":[{"key":"榜单","name":"榜单","value":[{"n":"实时热门电影","v":"movie_real_time_hotest"},{"n":"一周口碑电影榜","v":"movie_weekly_best"},{"n":"豆瓣电影Top250","v":"movie_top250"}]}],"rank_list_tv":[{"key":"榜单","name":"榜单","value":[{"n":"实时热门电视","v":"tv_real_time_hotest"},{"n":"华语口碑剧集榜","v":"tv_chinese_best_weekly"},{"n":"全球口碑剧集榜","v":"tv_global_best_weekly"},{"n":"国内口碑综艺榜","v":"show_chinese_best_weekly"},{"n":"国外口碑综艺榜","v":"show_global_best_weekly"}]}]}
	}
	header = {
		"Host": "frodo.douban.com",
		"Connection": "Keep-Alive",
		"Referer": "https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html",
		"content-type": "application/json",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]