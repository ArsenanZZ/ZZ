"""Review Delaware prose, six-colour emphasis and verified literary references."""
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
import re,json
ROOT=Path(__file__).resolve().parents[1]
LIGHT=['#b53635','#237953','#306eaa','#946300','#934634','#b03878'];DARK=['#ff9992','#85c9a6','#91bce8','#f1cf78','#e9ad95','#f5a3ce']
SOURCES=[
 ('惠特曼《大路之歌》原文','https://whitmanarchive.org/item/ppp.00473_00563'),
 ('塔布曼1896年演说 · 美国国家公园管理局','https://home.nps.gov/articles/harriet-tubman-and-the-underground-railroad.htm'),
 ('亨利·赛德尔·坎比生平 · 美国诗人学会','https://poets.org/academy-american-poets/contributor/henry-seidel-canby'),
 ('《The Age of Confidence》书目信息及出版介绍','https://openlibrary.org/works/OL1236214W/The_age_of_confidence'),
 ('艾丽斯·邓巴－纳尔逊档案 · 特拉华大学图书馆','https://findingaids.lib.udel.edu/repositories/2/resources/1534'),
 ('艾丽斯·邓巴－纳尔逊《Sonnet》原文','https://www.poetryfoundation.org/poems/53784/sonnet-56d233695cc6f')]
PHRASES='特拉华|威尔明顿|Siqi|Norton|阿巴拉契亚|布兰迪万|克里斯蒂娜河|Cool Spring|Swinging Footbridge|Jack A. Markell Trail|湿地|Run50|Planet Fitness|南翔|250 周年|官方照片|burn out|第 30 州|The First State|美国第一州|多佛|特拉华大学|雷霍博斯海滩|销售税|周五下班|西弗吉尼亚|十几个小时|橙色|粉红色|朝霞|河滨公园|塔布曼|加勒特|地下铁路|秘密援助路线|铜像|号码布|散步|社区|韩国部队火锅|韩国超市|小笼包|河畔步道|Wilmington Riverwalk|红砖|玻璃幕墙|造船厂|老房子|安妮女王式|Old Louisville|球衣|JVC 发带|封路|队尾出发|姗姗来迟|菲戈|鲁伊·科斯塔|葡萄牙球衣|国旗|大陆军|三角帽|布兰迪万公园|树荫|黑色铁桥|桥面在晃|自拍|蓝色球衣|罗克福德公园|7 英里|Tower Hill School|草坪|碰一下|落樱|花瓣|downtown|红砖教堂|The Grand|Riverwalk|木板路|工业设施|野生动物保护区|淡水潮汐湿地|环境教育中心|木栈道|风声|树林|新堡|折返点|20 英里|22 英里|26 英里|终点|第 30 个州|举起双臂|迟到的第 30 州|没那么胖|暖空气|辅助驾驶|宾夕法尼亚|奖牌|红、白、蓝|建国 250 周年|参赛服|披萨|肯塔基|充电|回去还要上班|惠特曼|大路之歌|哈丽雅特·塔布曼|亨利·赛德尔·坎比|自信时代|艾丽斯·邓巴－纳尔逊|霍华德高中|紫罗兰|四月|开阔的田野|棕色溪流'.split('|')
UNDER=['这是我的生活，又不是我的人设','我自己喜欢就够了','把第 30 州补上','不慌不忙、从从容容','这次终于完成了','没那么胖啊，哈哈','轻快谈不上','从未让列车脱轨，也从未丢失一位乘客','早一点晚一点，倒也没什么','桥面在晃','到了才知道','我还是喜欢跑步','碰一下','先去吃饭','第 30 个州','十几个小时']

def main():
 s=BeautifulSoup((ROOT/'tools/data/delaware-review-base-20261103.html').read_text(encoding='utf8'),'html.parser');main=s.select_one('main');ps=s.select('.prose');photos=[i['src'] for i in main.select('img')]
 edits={
 9:'天边先亮起一条橙色，车开过几个弯，云已经变成粉红色。起得是早了点，不过赶上了这么一场朝霞，挺值的。',
 16:'附近墙上还有一大幅壁画，国旗、人物和自由女神像排在一起，颜色很醒目。装备领完，我和 Siqi 也饿了，先去吃饭。',
 20:'这段河岸以前有造船厂、皮革厂，后来陆续改成步道、餐厅和公共活动场所。老建筑还在，旁边已经有人遛狗、慢跑。我们吃完饭沿河走走，明天比赛还要从这里经过。',
 52:'返程又看到了威尔明顿的楼群，先从桥后面露出来，越跑越近，终于回到昨天散步的 Riverwalk。昨天吃完饭在这里晃，今天已经跑了二十多英里，看见这些熟悉的楼，总算觉得快到了。',
 57:'更让我高兴的是，后来翻官方照片，好像也没那么胖啊，哈哈。体重是真涨了不少，但照片拍得还不错。同一段冲线拍了好几张，都舍不得删，干脆都放上来。',
 61:'下一次停车充电，已经到了宾夕法尼亚，天也放晴。我把奖牌拿出来补拍：金色外圈一圈星星，里面是红、白、蓝，中间画的是塔布曼—加勒特河滨公园的入口。2026 年恰逢美国建国 250 周年，这次的奖牌也用了相应的纪念元素。',
 67:'这两个月状态不太好，也确实有过不想跑的时候。但跟 Norton 的朋友一起训练，和 Siqi 出门跑完这一场，又觉得我还是喜欢跑步。开这么远的车当然累，下次选比赛，大概还是会先看看哪些州没去过。',
 68:'特拉华，第 30 州终于补上了。原计划二月，拖到四月，早一点晚一点，倒也没什么。这趟有朝霞、有湿地，还有跑完在车里吃的小笼包，我和 Siqi 都没白折腾。'}
 for i,t in edits.items():ps[i].clear();ps[i].append(t)
 # Add one short, scene-specific reference after the associated photograph.
 additions={
 8:('惠特曼《大路之歌》的开头是：“Afoot and light-hearted, I take to the open road.” 大意是，步履轻快，走上大路。我们这次先要在车里坐十几个小时，轻快谈不上，不过一路的朝霞还真不错。',[1]),
 13:('哈丽雅特·塔布曼后来谈起这段经历，说自己“从未让列车脱轨，也从未丢失一位乘客”。这句是从她1896年的演说中译来的。她一次次返回蓄奴地区带人逃离，威尔明顿的加勒特则接应、提供帮助。',[2]),
 21:('威尔明顿还出过一位作家亨利·赛德尔·坎比。他的《自信时代》（The Age of Confidence）回忆十九世纪末在这座小城长大的生活。我这趟只住一晚，老街、门廊和屋顶就够看一阵了。',[3,4]),
 41:('在威尔明顿教过多年书的艾丽斯·邓巴－纳尔逊，写过一首关于四月和紫罗兰的《十四行诗》。其中一句是“I had forgot wide fields; and clear brown streams”，说自己曾忘了开阔的田野和清澈的棕色溪流。她在本地的霍华德高中教书，也写文章、办报。',[5,6])}
 for i,(text,refs) in additions.items():
  p=s.new_tag('p',attrs={'class':'prose'});p.string=text
  for num in refs:
   a=s.new_tag('a',attrs={'class':'fact-ref','href':SOURCES[num-1][1],'title':SOURCES[num-1][0]});a.string=f'〔{num}〕';p.append(a)
  photo=ps[i].find_next_sibling('figure');photo.insert_after(p)
 main.select_one('.location-poster img')['src']='/assets/delaware-review-20261103/map.png'
 # Preserve all existing photographs and their credits; only the map is replaced.
 assert [x for x in photos if 'map-delaware' not in x]==[i['src'] for i in main.select('img') if '/delaware-review-' not in i['src']]
 rx=re.compile('('+'|'.join(map(re.escape,sorted(set(PHRASES+UNDER),key=len,reverse=True)))+')')
 for pi,p in enumerate(main.select('.prose,.intro p')):
  for mark in p.select('strong,b'):mark.unwrap()
  for leaf in list(p.descendants):
   if not isinstance(leaf,NavigableString) or leaf.find_parent('a'):continue
   chunks=rx.split(str(leaf))
   if len(chunks)==1:continue
   for j,t in enumerate(chunks):
    if not t:continue
    el=s.new_tag('strong') if j%2 else NavigableString(t)
    if j%2:el.string=t
    leaf.insert_before(el)
   leaf.extract()
  marks=p.select('strong')
  for k,m in enumerate(marks):
   m['data-cn-tone']=str((pi+k)%6)
   if m.get_text() in UNDER:m['data-cn-emphasis']='underline'
  if pi%3==0 and not p.select('[data-cn-emphasis]'):
   possible=[m for m in marks if 3<=len(m.get_text())<=16]
   if possible:possible[-1]['data-cn-emphasis']='underline'
 # Same author is credited once per connected photo group.
 for fig in main.select('figure.photo-strip'):
  cap=fig.find('figcaption')
  if not cap:continue
  lines=[t.strip() for t in cap.get_text('\n').splitlines() if t.strip()]
  if len(lines)>1 and all(' · 摄影 / ' in t for t in lines):
   names=[t.split(' · 摄影 / ')[-1] for t in lines]
   if len(set(names))==1:
    cap.clear()
    for t in lines:cap.append(t.split(' · 摄影 / ')[0]);cap.append(s.new_tag('br'))
    cap.append('摄影 / '+names[0])
 st=s.new_tag('style',id='delaware-review-colours');st.string=''.join(f'.prose [data-cn-tone="{i}"],.intro [data-cn-tone="{i}"]{{color:{c};font-weight:700}}html[data-theme="dark"] [data-cn-tone="{i}"]{{color:{DARK[i]}}}' for i,c in enumerate(LIGHT))+'.prose [data-cn-emphasis="underline"]{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}.fact-ref{font-size:10px;color:var(--muted);text-decoration:none}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}.location-poster img{display:block;width:100%;padding:0;margin:0}.source-note a{overflow-wrap:anywhere}'
 s.head.append(st)
 foot=s.new_tag('section',attrs={'class':'source-note'});p=s.new_tag('p');p.string='作品与背景资料（英文短句的中文解释为本文译述）：';foot.append(p)
 for i,(title,url) in enumerate(SOURCES,1):
  p=s.new_tag('p');a=s.new_tag('a',href=url);a.string=f'〔{i}〕{title}';p.append(a);foot.append(p)
 main.append(foot)
 for script in s.select('script[src]'):
  if 'delaware-editorial-copy.js' in script['src']:script['src']='/assets/delaware-editorial-copy.js?v=20261103-review'
 for dest in ['run50/wechat-new/delaware-marathon-modern-rail.html','run50/wechat/delaware-marathon-modern-rail.html','run50/wechat/delaware-marathon-editorial.html']:(ROOT/dest).write_text(str(s),encoding='utf8')
 (ROOT/'tools/data/delaware-review-sources-20261103.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2),encoding='utf8')
 (ROOT/'assets/delaware-editorial-copy.js').write_text((ROOT/'tools/data/delaware-copy-template.js').read_text(encoding='utf8'),encoding='utf8')
 print('Highlights',len(main.select('[data-cn-tone]')),'underlines',len(main.select('[data-cn-emphasis]')))
if __name__=='__main__':main()
