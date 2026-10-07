"""One-time import of the five legacy Rail stories; retain story text and photo order."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
ROOT=Path(__file__).resolve().parents[1]
LABELS={
'kentucky-derby-marathon-2025':['前言','周五夜跑','穿过市区','主场相聚','第50场'],
'fargo-marathon':['前言','北达科他','一路向北','起跑时分','大学城里','最后6英里','返程路上','半程回望'],
'hell-on-gravel-marathon':['前言','堪萨斯','赛前一天','十人的起点','砂石与烈日','返程路上','冠军后记'],
'mad-marathon':['前言','佛蒙特','穿过五州','抵达山谷','比赛日清晨','跑进绿山','山间路上','终点之前','赛后小聚'],
'rocket-city-marathon':['前言','阿拉巴马','抵达火箭城','零下起跑','迎风而跑','室内终点','年末回望']}
def clean(p):
 for x in [p,*p.find_all()]:
  x.attrs={k:v for k,v in x.attrs.items() if k in ['href','data-cn-tone','data-cn-emphasis']}
 return str(p)
if __name__=='__main__':
 for slug,labels in LABELS.items():
  out=ROOT/f'tools/data/{slug}-editorial.json'
  if out.exists():continue
  s=BeautifulSoup((ROOT/f'run50/wechat/{slug}-modern-rail.html').read_text(encoding='utf-8'),'html.parser')
  main=s.select_one('[data-cn-content]');children=main.find_all(recursive=False)
  title=s.title.get_text().split(' | 公众号')[0]
  cover=children[4].img['src'];mp=main.select_one('.article-map-panel');maps=mp.select('img')
  data={'slug':slug,'title':title,'intro':children[2].find_all('p')[-1].get_text(),'map':next(x['src'] for x in maps if 'light' in x['src']),'poster':cover,'blocks':[]}
  active=False;n=0
  for el in children:
   txt=el.get_text(' ',strip=True)
   if 'RUN50 FINISH LINE' in txt:break
   if el.find('h2') and 'FIELD NOTE' in txt:
    active=True;data['blocks'].append({'kind':'heading','title':el.h2.get_text(),'label':labels[n]});n+=1
   elif active and el.find('img'):
    imgs=el.find_all('img');ps=el.find_all('p');caption=ps[-1].get_text(' ',strip=True) if ps else ''
    for img in imgs:data['blocks'].append({'kind':'figure','src':img['src'],'alt':img.get('alt',''),'caption':caption})
   elif active and el.name=='p':data['blocks'].append({'kind':'paragraph','html':clean(el)})
   elif active and txt:raise ValueError((slug,str(el)[:300]))
  out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
  print(slug,len(data['blocks']),n)
