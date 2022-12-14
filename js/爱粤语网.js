var rule={
    title:'爱粤语网',
    host:'https://www.iyueyuz.com/',
    url:'/index.php/vod/show/id/fyclass/page/fypage.html',  
    searchUrl:'/index.php/vod/search/page/fypage/wd/**.html',
    searchable:2,
    quickSearch:0,
    filterable:0,
    headers:{
        'User-Agent':'PC_UA',
    },
    class_name:'电影&连续剧&综艺&动漫',
    class_url:'1&2&3&4',
    double:true, 
    一级:'.fed-list-info li; a:eq(1)&&Text;a&&data-original;.fed-text-center&&Text;a&&href',
    二级:{
    title:"h1&&Text;.fed-list-remarks&&Text",
    img:".fed-lazy&&data-original",
    desc:".fed-deta-content&&.fed-part-rows&&li:eq(1)&&Text;.fed-deta-content&&.fed-part-rows&&li:eq(2)&&Text;.fed-deta-content&&.fed-part-rows&&li:eq(3)&&Text",
    content:".fed-part-esan&&Text",
    tabs:".fed-drop-btns",
    lists:".fed-drop-boxs div:eq(#id) ul:eq(1) li a"
    },
    搜索:'.fed-deta-info;h1&&Text;.fed-lazy&&data-original;.fed-text-white&&Text;a&&href;.fed-deta-content&&Text',
}
