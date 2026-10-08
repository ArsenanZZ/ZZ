"""Import complete curated photo sequences, verifying every source file against the NAS inventory."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(r'Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025')
SOURCES={
'kentucky-derby-marathon-2025':('20250426-KY-Derby Marathon-My 50th/3-Polished',['前言','周五夜跑','周六起跑','主场相聚','第50场','后记']),
'fargo-marathon':('20250529-ND-Fargo Marathon-25st/4-Polished Photos',['前言','北达科他','赛前夜','起跑以后','跨过红河','最后6英里','返程路上','半程回望']),
'hell-on-gravel-marathon':('20250628-KS-Gravel on the hell-St26/6-Polished Photos',['前言','堪萨斯','赛前一天','十人的起点','砂石与烈日','返程路上','冠军后记']),
'mad-marathon':('20250717-VT-Mad Marathon-St27/4-Polished Photos',['前言','佛蒙特','穿过五州','抵达山谷','比赛日清晨','跑进绿山','山间路上','终点之前','赛后小聚'])}
def key(name):return re.sub(r'^copy #\d+ of ','',name.lower())
def run():
 report={}
 audit_path=ROOT/'tools/data/run50-caption-audit-20261008.json'
 audit=json.loads(audit_path.read_text(encoding='utf8')) if audit_path.exists() else {}
 for slug,(folder,labels) in SOURCES.items():
  path=ROOT/f'tools/data/{slug}-editorial.json';d=json.loads(path.read_text(encoding='utf8'))
  soup=BeautifulSoup((ROOT/f'run50/wechat/{slug}-magazine-wechat.html').read_text(encoding='utf8'),'html.parser')
  source=BASE/folder;files={key(p.name):p for p in source.rglob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}}
  blocks=[];n=0;mapping=[]
  for el in soup.select_one('[data-cn-content]').find_all(recursive=False):
   if el.name=='h2':
    blocks.append({'kind':'heading','label':labels[n],'title':re.sub(r'^\d+\s*','',el.get_text(' ',strip=True))});n+=1
   elif 'body-paragraph' in el.get('class',[]):
    for t in [el,*el.find_all()]:t.attrs={k:v for k,v in t.attrs.items() if k in ['href','data-cn-tone','data-cn-emphasis']}
    blocks.append({'kind':'paragraph','html':str(el)})
   elif 'photo' in el.get('class',[]):
    k=key(el['data-photo']);assert k in files,(slug,k)
    ps=el.find_all('p',recursive=False);cap=ps[0].get_text(' ',strip=True);credit=ps[1].get_text(' ',strip=True) if len(ps)>1 else ''
    if '待确认' in credit:credit=''
    src=el.img['src'];assert (ROOT/src.lstrip('/')).exists(),src
    blocks.append({'kind':'figure','src':src,'alt':cap,'caption':cap+(' · '+credit.replace(' | ',' / ') if credit else ''),'source_file':files[k].name})
    mapping.append({'source_file':files[k].name,'asset':src})
  used={key(x['source_file']) for x in mapping};missing=set(files)-used
  assert not missing,(slug,'missing',missing)
  assert len(mapping)==len(used),(slug,'duplicate image')
  for b in blocks:
   if b.get('src') in audit.get(slug,{}):b.update(audit[slug][b['src']])
  d['blocks']=blocks;d['source_folder']=str(source)
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
  report[slug]={'source_folder':str(source),'source_count':len(files),'article_count':len(mapping),'missing':sorted(missing),'photos':mapping}
  print(slug,len(files),len(mapping),'complete')
 (ROOT/'tools/data/run50-polished-reconciliation-20261008.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':run()
