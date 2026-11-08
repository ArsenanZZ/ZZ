"""Reviewed Rocket City credits, contextual quotations and clearer map."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
('哈珀·李与门罗维尔 · 阿拉巴马旅游局','https://www.alabama.travel/plan-your-trip/road-trips/monroeville-the-to-kill-a-mockingbird-experience/'),
('肯尼迪1962年莱斯大学演说 · NASA','https://www.nasa.gov/image-article/president-john-f-kennedy-rice-university/'),
('霍默·希卡姆生平、NASA工作与电影改编 · 美国退伍军人事务部','https://news.va.gov/98184/veteranoftheday-army-veteran-homer-hickam/')]
def main():
 s=BeautifulSoup((ROOT/'tools/data/rocket-city-review-base-20261108.html').read_text(encoding='utf8'),'html.parser')
 main=s.select_one('main');before=[i.get('src') for i in main.select('img')]
 d=json.loads((ROOT/'tools/data/rocket-city-marathon-editorial.json').read_text(encoding='utf8'))
 credits={int(re.search(r'img-(\d+)',b['src'])[1]):b for b in d['blocks'] if b['kind']=='figure'}
 # User confirmed Siqi's photographs of the author. Selfies retain Arsenan.
 siqi={6,7,9,20,30,33,36,43,44,77,104,105,113}
 official={48,49,50,51,52,89,90,91}
 pending={72,74,96,97}
 overrides=ROOT/'tools/data/rocket-city-credit-confirmations.json'
 if overrides.exists():
  for num,name in json.loads(overrides.read_text(encoding='utf8')).items():
   num=int(num)
   if name=='Siqi':siqi.add(num)
   if name=='官方摄影':official.add(num)
   pending.discard(num)
 for n,b in credits.items():
  name='Siqi' if n in siqi else '官方摄影' if n in official else None
  if name:b['caption']=re.sub(r'\s*·?\s*摄影\s*/.*$','',b['caption']).strip()+' · 摄影 / '+name
 credits[48]['caption']='清晨，跑者从起点出发 · 摄影 / 官方摄影'
 credits[48]['alt']='清晨，跑者从起点出发'
 for n,caption in {74:'穿着蓝毛衣，在赛道旁留影',77:'补给点前，穿着蓝毛衣继续向前'}.items():
  credits[n]['alt']=caption
  credits[n]['caption']=caption+' · 摄影 / Siqi'

 for f in main.select('figure'):
  ims=f.select('img')
  if not ims or not all(re.search(r'img-(\d+)',i.get('src','')) for i in ims):continue
  caps=[]
  for i in ims:
   n=int(re.search(r'img-(\d+)',i['src'])[1]);b=credits[n];i['alt']=b['alt'];caps.append(b['caption'])
  cap=f.find('figcaption')
  if not cap:cap=s.new_tag('figcaption');f.append(cap)
  cap.clear();names=[c.split(' · 摄影 / ')[-1] if ' · 摄影 / ' in c else None for c in caps]
  same=len(set(names))==1 and names[0]
  labels=['上','下'] if len(caps)==2 else ['上','中','下']
  for k,c in enumerate(caps):
   if k:cap.append(s.new_tag('br'))
   line=c.split(' · 摄影 / ')[0] if same else c
   cap.append((labels[k]+'：' if len(caps)>1 else '')+line)
  if same:cap.append(s.new_tag('br'));cap.append('摄影 / '+names[0])
 additions=[
 ('img-026.webp','阿拉巴马还有一位很出名的作家：写《杀死一只知更鸟》的哈珀·李。她的家乡门罗维尔，是小说里梅科姆镇的原型。当地旅游局还记着她跟出版社争标点的事：书名《Go Set a Watchman》要不要加逗号，她坚持不加，说“这是我的书，没有逗号”。老太太连一个逗号都不肯让。',1),
 ('img-030.webp','1962年，肯尼迪在休斯顿的莱斯大学说：“not because they are easy, but because they are hard”——不是因为容易，而是因为困难。当时说的是登月。这趟我刚在休斯顿出完差，又来到亨茨维尔看土星五号，倒是把这两个地方接上了。',2),
 ('img-103.webp','说起在 NASA 上班，电影《十月的天空》里的那个男孩，后来还真成了这里的工程师。电影改编自霍默·希卡姆的回忆录《火箭男孩》：小时候在西弗吉尼亚的煤矿小镇造小火箭，后来到马歇尔航天飞行中心工作。他回忆每天醒来都很高兴：“Oh boy, I get to go work for NASA today.” 今天又能去 NASA 上班了。这班上得，确实让人羡慕。',3)]
 for filename,text,num in additions:
  im=next(i for i in main.select('img') if filename in i.get('src',''))
  p=s.new_tag('p',attrs={'class':'prose'});p.string=text
  a=s.new_tag('a',attrs={'class':'fact-ref','href':SOURCES[num-1][1]});a.string=f'〔{num}〕';p.append(a)
  im.find_parent('figure').insert_after(p)
  for word in ['哈珀·李','杀死一只知更鸟','一个逗号','肯尼迪','莱斯大学','登月','土星五号','十月的天空','霍默·希卡姆','火箭男孩','马歇尔航天飞行中心']:
   for t in list(p.find_all(string=True)):
    if t.parent.name=='a' or word not in t:continue
    parts=str(t).split(word)
    for k,v in enumerate(parts):
     if k:
      st=s.new_tag('strong',attrs={'data-cn-tone':str((num+k)%6),'data-cn-emphasis':'underline' if k==1 else 'color'});st.string=word;t.insert_before(st)
     t.insert_before(v)
    t.extract()
 mapimg=next(i for i in main.select('img') if 'map-textured-' in i.get('src',''));mapimg['src']='/assets/wechat-rocket-city-map-clear-20261108.png'
 d['map']=mapimg['src']
 st=s.new_tag('style',id='rocket-review-20261108')
 colors=['#b53635','#237953','#306eaa','#946300','#934634','#b03878'];dark=['#ff9992','#85c9a6','#91bce8','#f1cf78','#e9ad95','#f5a3ce']
 st.string=''.join(f'.prose [data-cn-tone="{i}"]{{color:{c}}}html[data-theme="dark"] .prose [data-cn-tone="{i}"]{{color:{dark[i]}}}' for i,c in enumerate(colors))+'.fact-ref{font-size:10px;text-decoration:none;color:#888}.source-note{font-size:12px;line-height:1.8;color:#888;margin-top:32px}.map-poster img{width:100%;display:block}'
 s.head.append(st)
 refs=s.new_tag('section',attrs={'class':'source-note'})
 for num,(title,url) in enumerate(SOURCES,1):
  p=s.new_tag('p');a=s.new_tag('a',href=url);a.string=f'〔{num}〕{title}';p.append(a);refs.append(p)
 main.append(refs)
 for el in s.select('script[src]'):
  if 'editorial-copy' in el['src']:el['src']='/assets/rocket-city-editorial-copy.js?v=20261108-review'
 after=[i.get('src') for i in main.select('img')]
 assert [x for x in before if 'map-textured-' not in x]==[x for x in after if 'map-clear-' not in x]
 for suffix in ['modern-rail','editorial']:(ROOT/f'run50/wechat/rocket-city-marathon-{suffix}.html').write_text(str(s),encoding='utf8')
 (ROOT/'tools/data/rocket-city-marathon-editorial.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 (ROOT/'tools/data/rocket-city-review-sources-20261108.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2),encoding='utf8')
 print('Corrected:',len(siqi),'Siqi,',len(official),'official. Pending',sorted(pending))
if __name__=='__main__':main()
