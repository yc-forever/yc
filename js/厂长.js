var rule={
    title:'厂长资源',
    host:'https: //czzzu.com/',
    url:'/fyclass/page/fypage',
    searchUrl:'/xssearch?q=**&f=_all&p=fypage',
    searchable: 2,
    filterable: 0,
    headers: {'User-Agent':'PC_UA',
    },
    class_name:'豆瓣电影Top250&最新电影&热映中&电视剧&国产剧&美剧&韩剧&番剧&动漫',
    class_url:'dbtop250&zuixindianying&reyingzhong&dsj&gcj&meijutt&hanjutv&fanju&dm',
    推荐:'.bt_img;ul&&li;*;*;*;*',
    double: true,
    一级:'.bt_img&&ul&&li;h3.dytit&&Text;img.lazy&&data-original;.jidi&&Text;a&&href',
    二级: {
        "title": "h1&&Text;.moviedteail_list li&&a&&Text",
        "img": "div.dyimg img&&src",
        // "desc": ".moviedteail_list li:eq(3) a&&Text;.moviedteail_list li:eq(2) a&&Text;.moviedteail_list li:eq(1) a&&Text;.moviedteail_list li:eq(7) a&&Text;.moviedteail_list li:eq(5) a&&Text",
        "desc": ".moviedteail_list li:eq(3) a&&Text;.moviedteail_list li:eq(2) a&&Text;.moviedteail_list li:eq(1) a&&Text;.moviedteail_list li:eq(7)&&Text;.moviedteail_list li:eq(5)&&Text",
        "content": ".yp_context&&Text",
        "tabs": ".mi_paly_box span",
        "lists": ".paly_list_btn:eq(#id) a"
    },
    搜索:'.search_list&&ul&&li;*;*;*;*',
    预处理:'rule_fetch_params.headers.Cookie="68148872828e9f4d64e7a296f6c6b6d7=5429da9a54375db451f7f9e4f16ce0ea";let new_host="https://czspp.com";let new_html=request(new_host);if(/正在进行人机识别/.test(new_html)){let new_src=pd(new_html,
        "script&&src",new_host);log(new_src);let hhtml=request(new_src,
        {withHeaders: true
        });let json=JSON.parse(hhtml);let html=json.body;let key=html.match(new RegExp(\'var key="(.*?)"\'))[
            1
        ];let avalue=html.match(new RegExp(\'value="(.*?)"\'))[
            1
        ];let c="";for(let i=0;i<avalue.length;i++){let a=avalue[i
            ];let b=a.charCodeAt();c+=b
        }let value=md5(c);log(value);let yz_url="https://czspp.com/a20be899_96a6_40b2_88ba_32f1f75f1552_yanzheng_ip.php?type=96c4e20a0e951f471d32dae103e83881&key="+key+"&value="+value;log(yz_url);hhtml=request(yz_url,
        {withHeaders: true
        });json=JSON.parse(hhtml);let setCk=Object.keys(json).find(it=>it.toLowerCase()==="set-cookie");let cookie=setCk?json[setCk
        ].split(";")[
            0
        ]: "";log("cookie:"+cookie);rule_fetch_params.headers.Cookie=cookie;setItem(RULE_CK,cookie)
    }',
}
