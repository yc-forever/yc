var rule={
    title:'厂长资源',
    host:'https://czzzu.com',
    url:'/fyclass/page/fypage',
    searchUrl:'/xssearch?s=**',
    searchable:2,
    filterable:0,
    headers:{'User-Agent':'PC_UA', },
    class_name:'豆瓣电影Top250&最新电影&热映中&电视剧&国产剧&美剧&韩剧&日剧&海外剧&番剧&动漫',
    class_url:'dbtop250&zuixindianying&reyingzhong&dsj&gcj&meijutt&hanjutv&movie_bt_series/rj&movie_bt_series/hwj&fanju&dm',
    推荐:'.bt_img;ul&&li;*;*;*;*',
    double:true,
    一级:'.bt_img&&ul&&li;h3.dytit&&Text;img.lazy&&data-original;.jidi&&Text;a&&href',
    二级:{
    	"title": "h1&&Text;.moviedteail_list li&&a&&Text",
    	"img": "div.dyimg img&&src",
    	// "desc": ".moviedteail_list li:eq(3) a&&Text;.moviedteail_list li:eq(2) a&&Text;.moviedteail_list li:eq(1) a&&Text;.moviedteail_list li:eq(7) a&&Text;.moviedteail_list li:eq(5) a&&Text",
    	"desc": ".moviedteail_list li:eq(3) a&&Text;.moviedteail_list li:eq(2) a&&Text;.moviedteail_list li:eq(1) a&&Text;.moviedteail_list li:eq(7)&&Text;.moviedteail_list li:eq(5)&&Text",
    	"content": ".yp_context&&Text",
    	"tabs": ".mi_paly_box span",
    	"lists": ".paly_list_btn:eq(#id) a"
	},
    搜索:'.search_list&&ul&&li;*;*;*;*',
    }
