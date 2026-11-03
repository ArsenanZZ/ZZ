"""Publish the user-approved dictated Qinghai story with reusable WeChat formatting."""
from pathlib import Path
from html import escape
import json,re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/data'
text=(DATA/'qinghai-story-20261103.txt').read_text(encoding='utf-8')
refs=json.loads((DATA/'qinghai-sources-20261103.json').read_text(encoding='utf-8'))
old=json.loads((DATA/'qinghai-editorial.json').read_text(encoding='utf-8'))
photos={Path(b['src']).stem.removeprefix('QH-'):b for b in old['blocks'] if b['kind']=='figure'}
soup=BeautifulSoup((ROOT/'run50/wechat/qinghai-xining-marathon-editorial.html').read_text(encoding='utf-8'),'html.parser')
main=soup.select_one('main')
first=main.select_one('.chapter')
for node in list(first.next_siblings): node.extract()
first.extract()
title='RunCN #第30站｜青海：西宁高原马拉松｜逛完青海湖，在夏都的雨里跑个全马'
soup.title.string=title
main.select_one('h1').string=title
main.select_one('.intro').clear()
intro=soup.new_tag('p')
intro.string='青海这场，我本来没多大兴趣。又得飞一趟，比赛才办第二届，值不值得折腾？在拉萨认识的吕兄是西宁人，一个劲儿推荐。再看看地图，青海这么大一块还没跑过，算了，去吧。'
main.select_one('.intro').append(intro)
palette=['#b53635','#237953','#946300','#306eaa','#934634','#b03878']
dark=['#ff9992','#85c9a6','#f1cf78','#91bce8','#e9ad95','#f5a3ce']
keywords='青海 西宁 吕兄 小青稞 日月山 青海湖 茶卡盐湖 生命树 胡歌 祁建青 龙仁青 王洛宾 唐荣尧 王昌龄 甜哥 万兄 阿森纳 路易斯维尔大学 哈尔滨 黑马河 大新街 小新街 湟水 南川河 4小时15分 2261 2419 凤凰台 浦宁之珠 天空之镜 狗浇尿 盐冰淇淋 7点30分 五四西路 同仁路 香格里拉路 时代大道'.split()
phrases={
    0:['四十二公里','7点30分','4小时15分','红衣服','红帽子','号码布要放胸前','半马','全马'],
    1:['西宁','小青稞','河谷','牧场','绿地','湿地','南川河','比我预期好了不少','比赛比我预想的好不少','按自己的节奏','自给自足','接驳大巴','顺利','不太值'],
    2:['金黄色','金色的灯光','盐冰淇淋','金色的外圈','金色云纹','奖牌','太阳','日落','飞机'],
    3:['青海湖','茶卡盐湖','湟水','天空之镜','浅水','蓝色','湖面','盐水','青海','雨'],
    4:['母校','家乡','狗浇尿','文成公主','吕兄','祁建青','龙仁青','唐荣尧','王洛宾','王昌龄'],
    5:['甜哥','万兄','阿森纳','Luna','拍照','晚霞','假装跑一跑','有点二','不务正业','涂地图','费钱费腿','幸好听了吕兄的推荐','别停啊，跑起来','跟我们这个“特种兵旅行”完全不是一个难度']
}
extra_emphasis={
    0:['差一点就没来','我一开始真没多大兴趣','机票、酒店和时间','下午有飞机','全部家当','最后几百米'],
    1:['办得还挺像样啊','一路欢迎','一个人出门确实方便多了','这回推荐得靠谱','接驳、领物、存箱子','绿化也多'],
    2:['金黄','看个日落','看城市','盐雕','热乎','吃饱','赶上了','这趟来得值'],
    3:['三千多米','2200多米','倒影','湖边的风','高原这个日头','城市周围的山更多','雨中赶路'],
    4:['故乡，就应该有一缕淡淡的咸涩的味道','并非悬浮的英雄符号','莫听穿林打叶声，何妨吟啸且徐行','我们叫它的名字，只用一个亲昵的单字：海','一面面缩小的湖水','苏轼','韩红','天路','郑君里','杨紫','环保志愿者','来西宁还能认识阿森纳球迷','终于在赛道上见到本人了','一路互相喊','我还是有点犹豫','留几天逛逛西宁','这块奖牌我还挺喜欢','阿森纳铁杆球迷','比我想象中热闹多了','感觉自己被哄着买了票','这下可好，又进盐水了','都到青海了，还能看到大油边','幸好当时没退缩','小青稞','倒影特别清楚','上去高山望平川','夕阳住进了心里','青海湖边我的家','陈小虎','朱仲禄'],
    5:['至于杨洋，他反正也没意见','球迷这点挺方便','隔天我们还真在赛道上碰到了','鞋已经湿了','没必要什么都亲自验证','这双鞋比我安排得还充实','照片里有精神就行','原本各跑各的，后面倒互相管上了','先用两条腿看看这座城','跑家乡的马拉松']
}
extra_emphasis[0] += ['比赛才办第二届','号码布要放胸前','最后几百米','四十二公里','跑三走一']
extra_emphasis[1] += ['青海体育中心','帮着安排好','特别热情','绿地也多起来','箱子和包寄存好']
extra_emphasis[2] += ['小火车挺舒服','钱也没多花多少','蓝黄配色','一身黄衣服','金色的外圈']
extra_emphasis[3] += ['有些站之间没多远','跟着人群起跑','水面还是很开阔','浅褐色的山','南川河谷']
extra_emphasis[4] += ['被哄着买了票','有点不爽','也不能高兴太早','愿意推荐','回美国，接着上班、接着跑']
extra_emphasis[5] += ['盐水','小青稞也特别热情','拍照很好看','跑完再去','互相分享','我今天坐大巴']
for tone,words in extra_emphasis.items():phrases[tone].extend(words)
tone_map={word:tone for tone,words in phrases.items() for word in words}
for i,word in enumerate(keywords):tone_map.setdefault(word,i%6)
underlined={'比我预期好了不少','比赛比我预想的好不少','按自己的节奏','假装跑一跑','幸好听了吕兄的推荐','费钱费腿','别停啊，跑起来','不务正业'}
underlined.update(word for tone,words in extra_emphasis.items() for word in words if len(word)>=7)
keywords=list(tone_map)
rx=re.compile('('+'|'.join(map(re.escape,sorted(keywords,key=len,reverse=True)))+')')
def prose(s):
    parts=rx.split(s)
    out=''.join(f'<strong class="voice-tone-{tone_map[p]}"><u class="voice-underline" style="text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px">{escape(p)}</u></strong>' if i%2 and p in underlined else f'<strong class="voice-tone-{tone_map[p]}">{escape(p)}</strong>' if i%2 else escape(p) for i,p in enumerate(parts))
    return re.sub(r'〔(\d+)〕',lambda m:f'<a class="reference" href="{escape(refs[int(m[1])-1][1],quote=True)}" title="{escape(refs[int(m[1])-1][0],quote=True)}">〔{m[1]}〕</a>',out)
def append(html):
    for el in list(BeautifulSoup(html,'html.parser').contents): main.append(el)
seen=[];n=0
for line in text.splitlines():
    if not line.strip():continue
    if line.startswith('# '):
        n+=1;label,heading=line[2:].split('｜',1)
        append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(label)}</p><h2>{escape(heading)}</h2></header>')
    elif line.startswith('@'):
        keys=line[1:].split();seen+=keys
        for start in range(0,len(keys),2):
            group=[photos[k] for k in keys[start:start+2]]
            credits=[p['caption'].split(' · 摄影 / ',1)[-1] for p in group]
            captions=[p['caption'].split(' · 摄影 / ',1)[0] for p in group]
            imgs=''.join(f'<img src="{p["src"]}" srcset="{p["src"].replace("/QH-","/preview/QH-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{p["src"].replace("/QH-","/preview/QH-")}" width="{p["width"]}" height="{p["height"]}" alt="{escape(p["alt"])}" loading="lazy" decoding="async">' for p in group)
            if len(set(credits))==1:
                caption='<br>'.join(map(escape,captions))+'<br>摄影 / '+escape(credits[0])
            else:caption='<br>'.join(escape(c+' · 摄影 / '+a) for c,a in zip(captions,credits))
            append('<figure class="photo-strip voice-photo">'+imgs+'<figcaption>'+caption+'</figcaption></figure>')
    else:append('<p class="prose">'+prose(line)+'</p>')
append('<footer class="ending"><p class="end-mark">本文完</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、官方摄影</p></footer>')
append('<div class="source-note"><p>背景资料与作品出处；旅行和比赛经历依据作者口述。报道中的其他跑友故事已在正文区分。</p>'+''.join(f'<p>〔{i}〕<a href="{escape(url,quote=True)}">{escape(name)}</a></p>' for i,(name,url) in enumerate(refs,1))+'</div>')
style=soup.new_tag('style')
style.string='\n'.join(f'.voice-tone-{i}{{color:{c}}}html[data-theme="dark"] .voice-tone-{i}{{color:{dark[i]}}}' for i,c in enumerate(palette))+'''
.voice-underline{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}.reference{font-size:11px;color:var(--muted);text-decoration:none}.voice-photo img{width:100%;height:auto;display:block}.source-note p{margin:8px 0;overflow-wrap:anywhere}
'''
style['id']='qinghai-voice-style'
for previous in soup.select('#qinghai-voice-style'): previous.decompose()
soup.head.append(style)
assert len(seen)==len(set(seen))==123 and set(seen)==set(photos)
milestones={'009-6-alt':5,'009-8':8,'009-8-2':12,'009-8-4':20,'009-8-5':30,'009-8-8':36,'009-9':40,'009-9-1':42}
assert [milestones[k] for k in seen if k in milestones]==sorted(milestones.values())
from refresh_qinghai_emphasis import enhance
for mark in main.select('strong[class]'):
    match=re.search(r'voice-tone-(\d)', ' '.join(mark.get('class',[])))
    if match: mark['data-cn-tone']=str([0,1,3,2,4,5][int(match[1])])
    if mark.select_one('u'): mark['data-cn-emphasis']='underline'
rendered=enhance(str(soup))
for suffix in ['editorial','modern-rail']:
    out=ROOT/f'run50/wechat/qinghai-xining-marathon-{suffix}.html'
    out.write_text(rendered,encoding='utf-8')
clean='\n\n'.join(l[2:] if l.startswith('# ') else l for l in text.splitlines() if l and not l.startswith('@'))
clean+='\n\n资料出处\n'+'\n'.join(f'〔{i}〕{name}\n{url}' for i,(name,url) in enumerate(refs,1))
(DATA/'qinghai-reading-20261103.txt').write_text(title+'\n\n'+clean,encoding='utf-8')
print(json.dumps({'chapters':n,'photos':len(seen),'references':len(refs),'output':str(out)},ensure_ascii=False))
