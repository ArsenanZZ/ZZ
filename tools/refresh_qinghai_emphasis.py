"""Add Qinghai's six-colour emphasis without rewriting prose or moving photographs."""
from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString
ROOT=Path(__file__).resolve().parents[1]
LIGHT=['#b53635','#237953','#306eaa','#946300','#934634','#b03878']
DARK=['#ff9992','#85c9a6','#91bce8','#f1cf78','#e9ad95','#f5a3ce']
PHRASES='日月山|青海湖|茶卡盐湖|赶下午的飞机|盐水还进了鞋|踩着盐跑|四十二公里|群山之间的一座城|机场就有赛事志愿者|带着行李跑比赛|两千两百多米|彩色旗帜|黄色马甲|太热情了|拖着箱子|2261米|小青稞|赛事T恤|号码布|杨洋|东大街|哈尔滨|莫家街|灯笼|本地人|南山公园|高架|凤凰台|2419|晚霞|天黑之前|热腾腾的摊位|五点半|一日团|开元大饭店|大经幡|文成公主|唐蕃古道|青藏高原|黄土高原|白牦牛|羊群|骑行的人|摆渡车|最大的内陆咸水湖|3196米|经幡|到此一游|高原的湖|金黄的田野|宽檐帽|墨西哥人|紫外线|小火车|柴达木盆地|天空之镜|3059米|鞋里还是进了盐水|鞋套|盐雕|粉色的小火车|四十分钟|夜市|狗浇尿烙饼|淋油|7:30|青海体育中心|存一个箱子|路易斯维尔大学|下午三点半|四个半小时到五个小时|舒服的状态|上坡|每五公里补一次|阿森纳球衣|摄影师|八公里|十二公里|十五公里|二十公里|折返|湟水河|河谷|二十五公里|能量胶|三十公里|东北烧烤、大油边|走一走|三十六公里|四十公里|四十一公里|四百米|假装跑一跑|金色花瓣|蓝色山峰|水纹|绿箱子|谢谢、辛苦了|志愿者|打车|登机牌|酸奶|四小时多|高原全马'.split('|')
PAT=re.compile('('+'|'.join(map(re.escape,sorted(PHRASES,key=len,reverse=True)))+')')
def enhance(html):
 s=BeautifulSoup(html,'html.parser');before=s.select_one('main').get_text();photos=[str(x) for x in s.select('main img')]
 for pi,p in enumerate(s.select('.prose')):
  for leaf in list(p.descendants):
   if not isinstance(leaf,NavigableString) or leaf.find_parent(['strong','b','a','u']):continue
   parts=PAT.split(str(leaf))
   if len(parts)==1:continue
   for j,t in enumerate(parts):
    if not t:continue
    n=s.new_tag('strong') if j%2 else NavigableString(t)
    if j%2:n.string=t
    leaf.insert_before(n)
   leaf.extract()
  marks=p.select('strong,b')
  for k,m in enumerate(marks):m['data-cn-tone']=str((pi+k)%6)
  if pi%2==0 and marks and not p.select('[data-cn-emphasis="underline"],u'):
   candidates=[m for m in marks if 3<=len(m.get_text())<=18]
   if candidates:candidates[-1]['data-cn-emphasis']='underline'
 st=s.find('style',id='qinghai-six-colours')
 if st:st.decompose()
 st=s.new_tag('style',id='qinghai-six-colours');st.string=''.join(f'.prose [data-cn-tone="{i}"]{{color:{c};font-weight:700}}html[data-theme="dark"] .prose [data-cn-tone="{i}"]{{color:{DARK[i]}}}' for i,c in enumerate(LIGHT))+'.prose [data-cn-emphasis="underline"]{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}'
 s.head.append(st)
 for script in s.select('script[src]'):
  if 'runcn-qinghai-copy.js' in script['src']:script['src']='/assets/runcn-qinghai-copy.js?v=20261103-clean-copy'
 assert s.select_one('main').get_text()==before
 assert [str(x) for x in s.select('main img')]==photos
 return str(s)
def apply():
 for suffix in ['editorial','modern-rail']:
  p=ROOT/f'run50/wechat/qinghai-xining-marathon-{suffix}.html';p.write_text(enhance(p.read_text(encoding='utf8')),encoding='utf8')
 p=ROOT/'assets/runcn-qinghai-copy.js';js=p.read_text(encoding='utf8');js=js if "node.matches('.fact-ref, .reference, .source-note')" in js else js.replace("      const tag = node.tagName.toLowerCase();\n", "      const tag = node.tagName.toLowerCase();\n      if (node.matches('.fact-ref, .reference, .source-note')) return document.createTextNode('');\n");js=re.sub(r'const palette = dark \? \[[^\n]+? : \[[^\n]+?;', 'const palette = dark ? '+repr(DARK)+' : '+repr(LIGHT)+';',js);p.write_text(js,encoding='utf8')
if __name__=='__main__':apply()
