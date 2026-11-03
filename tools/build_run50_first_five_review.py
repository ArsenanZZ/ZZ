"""Rebuild the reviewed first five stories from frozen pre-review HTML blocks.

Keep the author's original travel/race narrative and every body photograph.
Run this after legacy generators for these five articles.
"""
from pathlib import Path
from html import escape
import json, re
from bs4 import BeautifulSoup
from normalize_wechat_presentation import normalize

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/data/run50-first-five-20261102'
ASSET='/assets/run50-first-five-20261102/'
SLUGS=['louisville-marathon','kentucky-derby-marathon-2021','cleveland-marathon','new-york-city-marathon','san-francisco-marathon']
PALETTE=['#ad4338','#237953','#306eaa','#966416','#805b45','#ad4e77']
DARK=['#f2a295','#8bd2ad','#99c9ed','#ebcd87','#d4b092','#efaaca']
KEYS=[
 '肯塔基|路易斯维尔|Beckley Creek Park|波本威士忌|俄亥俄河|200周|电动自行车|备用电池|驾照|8点24分|间隔起跑|口罩|社交距离|社交|能量胶|10公里|25公里|30公里|35公里|40公里|华人阿姨|美国女孩|美国大兵|小绿女生|奖牌|康姆士|立冬|正午|疫情|全马|第一场|每年跑个全马',
 '肯塔基|路易斯维尔|赛马|波本威士忌|俄亥俄河|好山好水好无聊|搬家|房东|倔老头|海蒂和爷爷|传奇跑者|Broad Run Park|半马|黄色silo|冬雨|冷风|Derby|分天分时起跑|落汤鸡|大风|大雨|You good?|自行车|最后的倔强|奖牌|四月底拿到正式驾照|开车自由|local|Red River Gorge|BBQ|Cindy|哈尔滨|黄石公园|跑步|寒冬|盛夏',
 '俄亥俄|克利夫兰|伊利湖|凯霍加河|铁锈地带|摇滚乐|摇滚名人堂|骑士队|詹姆斯|吉诺比利|St. Vincent|LeBron James|The Beatles|底特律|Tower City Center|老兵纪念桥|能量胶|橘黄色|凉|冷风|清晨|日出|半程|后半程|终点|奖牌|Public Square|Siqi|卢比奥|凯文乐福|最后的骑士|汉马|疫情|Planet Fitness|辛辛那提',
 '纽约马拉松|纽约州|纽约市|曼哈顿|布鲁克林|皇后区|布朗克斯|史泰登岛|中央公园|时代广场|自由女神|法拉盛|哈德逊河|洛克菲勒中心|50周年|第一个大满贯|42.195公里|赛博朋克|保暖斗篷|热咖啡|橙色区域|世界的十字路口|超级英雄|摄影师|完赛奖牌|CR7|村上春树|科幻|小吃车|韩国BBQ|期待了两年',
 '旧金山马拉松|加州|金门大桥|旧金山|Siqi|Anastasia|Karl|联合广场|加州科学馆|唐人街|九曲花街|金门公园|海湾|Chase Center|Pier 39|彩绘女士|14英里|45周年|电动自行车|韩国火锅|红色的毯子|皮蛋瘦肉粥|叉烧大包子|Very hilly|大雾|奖牌|绿色战袍|海风|摄影师|上坡|下坡|科伊特塔|完赛|流雾|披风|冷风|影像|照片很贵|报名了马拉松，加州也就不远了'
]

def tag(html): return BeautifulSoup(html,'html.parser').find()
def p(text): return tag('<p class="prose">'+text+'</p>')
def chapter(title):return tag('<header class="chapter"><span class="chapter-number"></span><p class="chapter-label">肯塔基 · 路易斯维尔</p><h2>'+title+'</h2></header>')
def source(url,label):return f'<a href="{url}" class="fact-source" title="{label}">〔资料〕</a>'
def replace_paragraph(b,i,text): b[i]=p(text)

def edits(slug,b):
 if slug=='louisville-marathon':
  b[4]=tag('<section class="intro"><p>2020年，能有一场马拉松跑已经很难得了。比赛搬到了郊外，车也买了，驾照却还没拿到，只能花近100刀打车去跑这个全马。</p></section>')
  b[8]=p('2020年的第一个马拉松，比预想中来得晚了一些。入坑四年多，回头一看，跑步200周了，也算是完成了一个不大不小的成就。')
  b.insert(11,p('说到肯塔基，赛马和波本威士忌都很有名。我住的路易斯维尔就在俄亥俄河边，是州里最大的城市。这回跑的Louisville Marathon和春天的Derby马拉松是两场不同的比赛，别看都在路城，时间和路线可不一样。'+source('https://www.kentuckytourism.com/places-to-go/cities-and-regions/bourbon-horses-and-history-region','肯塔基旅游局：路易斯维尔与波本产区')))
  for i,title in [(46,'最后两公里，互相打气'),(38,'立冬这天，跑出了东南亚的感觉'),(27,'小树林里的前半程')]:b.insert(i,chapter(title))
 elif slug=='kentucky-derby-marathon-2021':
  b[4]=tag('<section class="intro"><p>在美国待了一年，跑个半马都比以前费劲了，偏偏还喜欢管自己叫“传奇跑者”。这半年搬了家、跑了Derby，也终于拿到了驾照，生活总算不只围着家门口转了。</p></section>')
  b[63]=None
  # Geography belongs beside the Ohio River photographs, not in a detached essay.
  b.insert(13,p('路易斯维尔在肯塔基北边，隔着俄亥俄河就是印第安纳。肯塔基的马场、赛马和波本酒很出名，不过这一阵对我来说，最熟悉的还是家门口这些街道，跑着跑着就到了河边。'+source('https://www.kentuckytourism.com/places-to-go/cities-and-regions/bluegrass-horses-bourbon-and-boone-region','肯塔基旅游局：Bluegrass地区')))
 elif slug=='cleveland-marathon':
  b[4]=tag('<section class="intro"><p>本来想和同一天跑汉马的朋友隔空一起跑，结果汉马临时取消了，克利夫兰我还是去了。摇滚名人堂、骑士队的比赛都赶上了，就是没想到，跑步这天能冷成这样。</p></section>')
  b[89]=p('克利夫兰和摇滚乐的关系，得说到电台DJ艾伦·弗里德。1951年，他在这里把节奏布鲁斯介绍给更多听众，也让“rock and roll”这个说法流行起来。这个词并不是他凭空发明的，但这座城确实赶上了摇滚乐最早的热闹。'+source('https://library.rockhall.com/otr/big_bang','摇滚名人堂：摇滚乐的诞生'))
  b[102]=p('这回我没了兴致去尝伊利湖的湖水，看着就没什么食欲。克利夫兰的水污染还真有过一段出名的历史：1969年，火车火星点着了凯霍加河上沾着油的杂物，河面着了火。如今河流经过治理，也成了划船游玩的地方。'+source('https://www.nps.gov/articles/000/the-cuyahoga-river-once-on-fire-now-a-recreation-destination.htm','美国国家公园管理局：凯霍加河'))
  b[15]=p('克利夫兰马的起点在Tower City Center附近，伴着夜色出行，来到起点处，Terminal Tower红色的塔尖十分壮观。')
  b[25]=p('克利夫兰和底特律，同在五大湖沿岸的铁锈地带，都经历过工业繁荣和工厂外迁。至于路为什么叫底特律路，我当时没细查，先跑步吧。')
  b[26]=None
  b[34]=p('右手边，河口附近的铁路和水面铺在晨光里，蓝色的水和粉色的云交相辉映；左手边，太阳刚刚升起，城市的剪影也越来越清楚。这段跑得挺过瘾，忍不住一直拍照。')
  b[50]=p('我在downtown拿了一堆能量胶，就是觉得“能量胶在手，心里不慌”。后半程一边补水一边补胶，心里踏实了不少，至少那会儿还没怎么撞墙。')
  b[118]=p('远处的Terminal Tower清晰可见，就是早晨起跑时看到的那座塔。晚上再看，灯光打上去，和白天又是两种感觉。')
  b[119]=None
  # Join the two source essays into a chronological trip, retaining all photos.
  city=b[70:124]; race=b[9:68]
  first=tag('<header class="chapter"><span class="chapter-number">01</span><p class="chapter-label">俄亥俄</p><h2>先去克利夫兰看看</h2></header>')
  geo=p('俄亥俄州在美国中西部，北边靠着伊利湖，南边是俄亥俄河。哥伦布是州首府，克利夫兰在湖边，辛辛那提则在南边靠近肯塔基。这趟从路易斯维尔开过去，几座城挨着跑下来，光开车就得花不少时间。')
  b=b[:6]+[first,geo]+city+race+[b[-1]]
 elif slug=='new-york-city-marathon':
  b[4]=tag('<section class="intro"><p>等了两年的纽约马拉松，终于在50周年这届跑上了。起跑前冷得够呛，跑起来却一直有人加油，偷偷走两步都觉得不好意思，看到摄影师更得赶紧装作还有劲。</p></section>')
  b[63]=p('从史泰登岛的韦拉扎诺桥出发，先过布鲁克林、皇后区，再跨桥进曼哈顿，向北到布朗克斯后折回曼哈顿，最后跑进中央公园。五个区一个不少，桥也没少过，光看路线就知道这一路不会轻松。'+source('https://www.nyc.gov/assets/bronxcb1/pdf/notices/TCSNewYorkCityMarathon.pdf','2021纽约马拉松官方路线图'))
  b[113]=p('比赛先聊到这儿，再倒回去说说这几天逛的纽约。好不容易来一趟，光跑马肯定不够，吃饭、坐船、逛街，一个也没少安排。')
  b[109]=None # Remove the duplicate, unidiomatic English translation; retain Chinese quotation.
  b[115]=p('很喜欢黎明的《神经质女主角》，周耀辉填的词，开头一句“斜阳照纽约”。歌里一路走过街道、橱窗和约会的情人，有点乱，又很迷人，倒是很像我眼前的纽约。'+source('https://www.mulanci.org/lyric/sl136824/','黎明《神经质女主角》，周耀辉词'))
  b[116]=None;b[117]=None # Keep the cultural reference without reprinting a long lyric.
  b.insert(10,p('纽约市只是纽约州东南角的一部分。州府其实在奥尔巴尼，再往北还有阿迪朗达克的山林。这趟我的活动范围基本没离开纽约市，光五个区和这些街头巷尾，就够看好几天。'+source('https://www.iloveny.com/places-to-go/capital-saratoga/spotlight-albany/','纽约州旅游局：州府奥尔巴尼')))
 elif slug=='san-francisco-marathon':
  b[4]=tag('<section class="intro"><p>为了金门大桥报了旧金山马拉松。结果桥倒是跑了两遍，海风也吹了个够，绿色长袖前半程舍不得脱，后半程又热得穿不住。同一场比赛，两种天气。</p></section>')
  b[22]=p('叮当车从1873年就开始在这些坡上跑。它靠地下钢缆牵引，不是普通的电车；到我来的2022年，已经快150年了。看它慢悠悠地爬上坡，再看看我和Siqi的箱子，确实有点羡慕。'+source('https://www.sfmta.com/getting-around/muni/cable-cars/cable-car-history','旧金山交通局：缆车历史'))
  b[27]=p('加州科学馆创立于1853年，里面有水族馆、天文馆、自然历史博物馆，还有一座四层高的室内雨林。这个组合可太合我们口味了，够在里面逛很久。'+source('https://www.calacademy.org/our-history','加州科学院历史'))
  b[29]=p('它就在金门公园里，几种展馆在同一栋建筑里。先看水里的，再看天上的，确实省得来回跑。')
  b[65]=p('这段花街只有一个街区长，却塞进了八个急弯。路太陡，车道只能绕着花坛一点点往下走，站在旁边看汽车拐弯，也挺替司机忙的。')
  b[100]=p('回去还车的时候，我们特意去看了科伊特塔（Coit Tower），外形有点像消防水龙头。塔的名字来自莉莉安·科伊特，她长期支持旧金山的消防员，还留下了一笔用于美化城市的遗产，这座塔就是用这笔钱建的。'+source('https://www.sfrecpark.org/Facilities/Facility/Details/Coit-Tower-290','旧金山公园局：科伊特塔'))
  b[119]=p('回想这一天，我又想到了Scott McKenzie唱的《San Francisco》。那首歌唱起头戴鲜花、来到旧金山的人，后来也用在《阿甘正传》的配乐里。我们没戴花，倒是一路裹着毯子、顶着风，和想象中的加州夏天差得有点远。')
  for i in range(120,128):b[i]=None
  b[136]=None;b[137]=None # Unsupported timeless ranking and unattributed newspaper quotation.
  b[200]=p('前面是当时叫Stow Lake的湖，水绿绿的，还有野鸭子和中国式的凉亭。我当时把名字记成了Slow Lake，干脆也慢下来，停着走了一会儿。')
  b[177]=p('然后我又在海边帮着几位印度裔的朋友拍了一些不同角度的大桥照片，他们也帮我拍了几张。')
  b[179]=None
  b[246]=p('接下来就要回家了，我们在机场等了很久。');b[248]=None
  b[250]=p('飞机几次延误，等着也是等着，我就买了这次跑步的照片。好几十张，价格大概一半报名费那么多。照片是挺贵，不过金门大桥那几张我很喜欢，还是买了。')
  # Use existing race photographs next to the closing race discussion.
  photo=b[140];b[140]=None;b.insert(257,photo)
  b.insert(13,p('加州沿着美国西海岸铺了很长一段，旧金山在北加州的海湾边。我以前一说加州，先想到的还是阳光和沙滩，这回刚落地就发现，旧金山的雾和海风完全是另一回事。'))
 return [x for x in b if x is not None]

def captions(s,slug):
 # Expand legacy credits while keeping explicitly identified photographers.
 for c in s.select('figcaption'):
  h=c.decode_contents()
  for old,new in [('by Joyrun','资料 / 悦跑圈'),('by Someone','摄影 / 现场跑友'),('by Santosh','摄影 / Santosh'),('by Cindy','摄影 / Cindy'),('@摄影师','摄影 / 官方摄影'),('@47','摄影 / Siqi')]:h=h.replace(old,new)
  c.clear();c.extend(BeautifulSoup(h,'html.parser').contents)
 if slug!='cleveland-marathon':return
 descriptions={2:'湖边的场馆与远处的天空',3:'云层下的克利夫兰市区',5:'摇滚名人堂外的纪念牌',6:'展柜里的吉他和唱片',9:'博物馆中庭，楼层上下相通',10:'抬头看悬挂的展品',11:'彩绘巴士也是展品',12:'乐手的衣服和演出纪念',13:'墙上的音乐人照片',14:'一整面彩色演出海报',17:'港口的吊桥与船只',18:'草坪对面的城市天际线',21:'秋天的街道和广场',32:'天还没亮，先在起点等一等',36:'朝着市中心跑，天色开始变亮',37:'远处的楼群出现在晨光里',38:'继续跑向市区',40:'穿过老兵纪念桥的钢架',44:'日出后的城市轮廓',45:'赛道上的跑者',52:'从桥上看河道与楼群',55:'后半程再次看见城市天际线',56:'橘黄色长袖，继续向前跑',57:'跑向终点',59:'Siqi在终点拍下这一张',61:'奖牌和城市建筑',62:'奖牌与骑士队的衣服',63:'举着奖牌，在公共广场拍照',64:'换个角度再来一张'}
 for f in s.select('figure.photo-strip:not(.location-poster)'):
  imgs=f.select('img');lines=[];names=[]
  for im in imgs:
   n=int(re.search(r'img-(\d+)',im['src'])[1]);name='官方摄影' if n in [45,56,57] else 'Siqi' if n==59 else 'Arsenan'
   if n==30:name='赛事组委会'
   desc=descriptions.get(n,im.get('alt','').strip())
   desc=re.sub(r'(?:@|by\s+).*','',desc).strip(' ·')
   if not desc:desc='克利夫兰赛道' if n>30 else '克利夫兰旅行'
   lines.append(desc);names.append(name);im['alt']=desc
  labels=['上','下'] if len(imgs)==2 else ['上','中','下']
  if len(set(names))==1:
   h='<br>'.join(escape((labels[i]+'：' if len(imgs)>1 else '')+v) for i,v in enumerate(lines))+'<br>'+('资料 / ' if names[0]=='赛事组委会' else '摄影 / ')+names[0]
  else:h='<br>'.join(escape(labels[i]+'：'+v+' · 摄影 / '+names[i]) for i,v in enumerate(lines))
  c=f.find('figcaption');c.clear();c.extend(BeautifulSoup(h,'html.parser').contents)

def moderate_paragraphs(m):
 # Only merge adjacent prose in the same scene. Never join across photographs/headings.
 for e in list(m.find_all(recursive=False)):
  if e.parent is None or 'prose' not in e.get('class',[]):continue
  nxt=e.find_next_sibling()
  while nxt and 'prose' in nxt.get('class',[]) and len(e.get_text())+len(nxt.get_text())<=225:
   if len(e.get_text())>=110 and len(nxt.get_text())>=55:break
   e.append('');e.extend(list(nxt.contents));nxt.decompose();nxt=e.find_next_sibling()

def emphasize(m,index):
 keys=set(KEYS[index].split('|'))
 for el in m.select('.prose strong,.intro strong'):
  t=el.get_text()
  if 3<=len(t)<=24:keys.add(t)
  el.unwrap()
 pat=re.compile('('+'|'.join(map(re.escape,sorted(keys,key=len,reverse=True)))+')')
 count=0
 for para in m.select('.prose,.intro p'):
  used=0
  for node in list(para.find_all(string=True)):
   if node.find_parent('a'):continue
   parts=pat.split(str(node))
   if len(parts)<2:continue
   for i,t in enumerate(parts):
    if i%2 and used<4:
     el=tag('<strong></strong>');el.string=t;el['data-cn-tone']=str(count%6)
     if count%4==0 and len(t)>=3:el['data-cn-emphasis']='underline'
     node.insert_before(el);count+=1;used+=1
    else:node.insert_before(t)
   node.extract()

def build(slug,index):
 d=json.loads((DATA/(slug+'.json')).read_text(encoding='utf8'))
 b=edits(slug,[tag(x) for x in d['original_blocks']])
 s=BeautifulSoup('<main></main>','html.parser');m=s.main;m.attrs=d['main_attributes'];m.extend(b)
 if index<3:m.select_one('.byline').string=['2020年11月8日','2021年4月24日','2021年10月24日'][index]+' · 文字 / Arsenan'
 for x in m.select('footer .closing'):x.decompose()
 for x in m.select('.prose'):
  # Correct transcription/typing errors, not the author's conversational asides.
  for n in list(x.find_all(string=True)):
   n.replace_with(str(n).replace('我门','我们').replace('太阳出升','太阳初升').replace('抗过了','扛过了').replace('铁锈州','铁锈地带').replace('号码簿','号码布').replace('斯坦顿岛','史泰登岛').replace('去斯坦顿的轮渡','去史泰登岛的轮渡').replace('去了了','去了'))
 if slug=='cleveland-marathon':
  for h in m.select('.chapter h2'):
   if h.get_text()=='前言':h.string='天还没亮，去跑马'
 moderate_paragraphs(m);captions(s,slug);emphasize(m,index)
 for n,h in enumerate(m.select('.chapter'),1):
  h.select_one('.chapter-number').string=f'{n:02}'
  lab=h.select_one('.chapter-label')
  if lab and lab.get_text()=='Chapter':lab.string='纽约 · 旅行与赛记'
 # The paper poster and map share the exact same outer box; no crop transforms.
 loc=m.select_one('.location-poster'); imgs=loc.select('img')
 imgs[0]['src']=ASSET+('kentucky' if index<2 else ['','','cleveland','new-york','san-francisco'][index])+'-map.png'
 if index<3:imgs[1]['src']=ASSET+['louisville-poster.png','kentucky-derby-2021-poster.png','cleveland-poster.png'][index]
 for w in loc.select('.poster-window'):w.unwrap()
 for im in loc.select('img'):im.attrs={k:v for k,v in im.attrs.items() if k in ['src','alt']}
 m['data-copy-chunks']='original'
 for im in m.select('img'):
  src=im.get('src','').split('?')[0]
  path=ROOT/src.lstrip('/') if src.startswith('/') else (ROOT/'run50/wechat'/src).resolve()
  if path.exists():im['data-copy-bytes']=str(path.stat().st_size)
 loc.select_one('figcaption').clear();loc.select_one('figcaption').append('Run50 · '+['肯塔基第1州','肯塔基第1州 · 第二篇','俄亥俄第2州','纽约第3州','加州第4州'][index]);loc.select_one('figcaption').append(s.new_tag('br'));loc.select_one('figcaption').append('制图与海报 / Arsenan × AI')
 css=d['styles']+'\n/* Reviewed first-five edition: full-width paper artwork and readable accents. */\n'
 css+='main{padding-left:20px;padding-right:20px}.location-poster{margin:32px 0!important;padding:0!important;border:0!important}.location-poster img{display:block!important;width:100%!important;max-width:100%!important;margin:0!important;padding:0!important;transform:none!important;border:0!important;box-sizing:border-box}.brand-intro img{width:96px;height:auto}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}.fact-source{font-size:11px;color:var(--muted)}'
 for i,c in enumerate(PALETTE):css+=f'[data-cn-tone="{i}"]{{color:{c};font-weight:800}}html[data-theme="dark"] [data-cn-tone="{i}"]{{color:{DARK[i]}}}'
 css+='[data-cn-emphasis="underline"]{text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:4px}'
 nav='<nav class="copy-tools"><a href="/CN/#run50-series">Run50目录</a><button data-theme-choice="light" aria-pressed="true">白底</button><button data-theme-choice="dark" aria-pressed="false">黑底</button><button id="copy-wechat">一键复制到公众号</button><span id="copy-status" role="status"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(d['title'])+'</title>'+''.join(d.get('metadata',[]))+'<link rel="canonical" href="https://zhennanzhang.com/run50/wechat/'+slug+'-modern-rail.html"><script src="/analytics.js" defer></script><style>'+css+'</style></head><body>'+nav+str(m)+'<script src="/assets/run50-first-five-copy.js?v=20261102" defer></script></body></html>'
 html,_=normalize(html,slug+'-modern-rail.html')
 html=re.sub(r'</(header|figure|section|p|footer)>(?=<)',r'</\1>\n',html)
 for suffix in ['modern-rail','editorial']:(ROOT/f'run50/wechat/{slug}-{suffix}.html').write_text(html,encoding='utf8')
 out=BeautifulSoup(html,'html.parser')
 print(slug,'photos',len(out.select('main img')),'paragraphs',len(out.select('.prose')),'accents',len(out.select('[data-cn-tone]')),'underlines',len(out.select('[data-cn-emphasis]')))

if __name__=='__main__':
 for i,slug in enumerate(SLUGS):build(slug,i)
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf8')
 js=js.replace("['#f09589','#85c9a6','#91bce8','#e8c481']",str(DARK)).replace("['#ac4336','#237953','#306eaa','#9a681c']",str(PALETTE))
 (ROOT/'assets/run50-first-five-copy.js').write_text(js,encoding='utf8')
