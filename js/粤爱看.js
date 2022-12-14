var rule={
    title:'粤爱看',
    host:'https://www.yakgj.com',
    // homeUrl:'/',
    url:'/vod-type-id-fyclass-page-fypage.html',
    searchUrl:'/index.php?m=vod-search',
    searchable:2,//是否启用全局搜索,
    quickSearch:0,//是否启用快速搜索,
    filterable:0,//是否启用分类筛选,
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        // "Cookie": "searchneed=ok"
    },
    class_name:'电影&连续剧&综艺&动漫&港剧',
    class_url:'1&2&3&4&13',
    lazy:'',
    limit:6,
    推荐:'.stui-vodlist li;a&&title;.lazyload&&data-original;.stui-vodlist__title&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'.stui-vodlist li;a&&title;.lazyload&&data-original;.stui-vodlist__title&&Text;a&&href',
    二级:{"title":"h3&&Text;.stui-content__detail&&Text","img":".lazyload&&data-original","desc":".stui-content__detail:eq(1)&&Text;.stui-content__detail:eq(2)&&Text;.stui-content__detail:eq(3)&&Text","content":".desc.hidden-xs&&Text","tabs":".stui-pannel__head","lists":".stui-content__playlist:eq(#id) a"},
    搜索:'.stui-vodlist.clearfix;.*;.*;.*;.*',
}