"""Apply the established magazine layout to RunCN and RunWorld source blocks."""
from pathlib import Path
import json,re,math,sys
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
import build_run50_remaining_editorials as common
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/data/next-series-refresh-20261020'
SELECT=json.loads((ROOT/'tools/data/next-series-refresh-selection.json').read_text(encoding='utf8'))
base_credit=common.credit
def series_credit(c):
 c=base_credit(c)
 c=re.sub(r'[。·\s]*摄影\s*[/：:]\s*',' · 摄影 / ',c)
 c=re.sub(r'(摄影 / )阿森男',r'\1Arsenan',c)
 return c
common.credit=series_credit

def mountain_intro(slug):
 out=ROOT/'assets/series-intros-20261020'/slug;out.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',53)
 for theme,bg in [('light','#ffffff'),('dark','#191919')]:
  ink=SELECT[slug][theme];frames=[];points=[(30,110),(65,110),(100,68),(135,110),(158,88),(190,110),(250,110)]
  for k in range(24):
   im=Image.new('RGBA',(280,280),(0,0,0,0));dr=ImageDraw.Draw(im)
   for j in range(min(6,(k+1)//2)):dr.line([points[j],points[j+1]],fill=ink,width=5)
   if k>=12:
    layer=Image.new('RGBA',(280,280));ld=ImageDraw.Draw(layer);ld.text((140,151),'RunCN',font=font,fill=ink,anchor='mm')
    if k>=17:
     river=[(x,200+6*math.sin((x-60)*math.pi/70)) for x in range(60,221)];end=min(len(river),int(len(river)*(k-16)/6))
     if end>1:ld.line(river[:end],fill=ink,width=3);ld.line([(x,y+12) for x,y in river[:end]],fill=ink,width=2)
    alpha=min(1,(k-11)/5)
    if alpha<1:layer.putalpha(layer.getchannel('A').point(lambda x:int(x*alpha)))
    im=Image.alpha_composite(im,layer)
   frames.append(im)
  frames[-1].save(out/f'{theme}-still.png')
  # Reserve palette index 255 for transparency in every full frame. Disposal 2
  # clears the previous frame, including at the loop boundary, without a matte.
  indexed=[]
  for frame in frames:
   pal=frame.convert('RGB').quantize(colors=255)
   pal.paste(255,mask=frame.getchannel('A').point(lambda a:255 if a<128 else 0))
   pal.info['transparency']=255
   indexed.append(pal)
  indexed[0].save(out/f'{theme}.gif',save_all=True,append_images=indexed[1:],duration=[70]*23+[1600],loop=0,optimize=False,transparency=255,disposal=2)

def prepare(d):
 d=dict(d);out=[];photo_count=0
 triggers={'wuhan-marathon-2018':{'周四我和小胖':'赛前，在武汉相聚','比赛日，我和小胖':'金色人流，穿越武汉三镇','进入东湖绿道':'跑进东湖，回味汉马'},'wuhan-wuxi-marathon-notes':{'东湖绿道樱花半程马拉松':'东湖樱花马，第一次当兔子','东湖确实是块风水宝地':'珞珈跑团，出征大学生马拉松'}}
 headings={
 'steel-tank-story':['远安的田野','武汉的暴雨','合肥的生日','长治的骄阳','鄂尔多斯的夜','哈尔滨的美食'],
 'three-city-pilgrimage':['广安——邓小平','宜昌——我的导师','长沙——毛主席'],
 'dalian-trail':['越野：心中的江湖','大连：自由斑驳','黄渤海分界线：这是一本东北的近代史','越过山丘，在大连，在东北......'],
 'guiyang-marathon-climb':['夜郎古国 你不能不知','阳明哲思 好想拜他为师','奔跑身影 要像星辰般闪耀','慕名圣贤，龙场悟道'],
 'haikou-marathon':['海口的诗和远方','海口的征途，是星沉大海','9102，On the Road'],
 'lanzhou-marathon':['河西走廊之梦','兰州，兰州','兰马，总是在清晨出走'],
 'wuhan-marathon-2018':['想读懂汉马，请先读懂武汉'],
 'wuhan-han-marathon':['独家记忆 · 武汉','独家记忆 · 汉马','下一站，街道口'],
 'singapore-sundown-marathon':['从二零零八到二零一八','从樟宜机场到南洋理工','从《强风吹拂》到《月亮与六便士》','超越平凡，归去依旧少年'],
 'xian-city-wall-marathon':['出行','八百里秦川，三千年传奇','强风吹拂长安城，','这座城市很年轻','那些关于山河的传说，从来不曾被遗忘','题外话'],
 'xiamen-marathon':['赛场']}
 for b in d['blocks']:
  if b['kind']=='figure':
   if d['slug']=='wuhan-wuxi-marathon-notes' and photo_count==43:out.append({'kind':'heading','title':'无锡，粉色的跑步周末'})
   photo_count+=1
  text=b.get('title','') if b['kind']=='heading' else BeautifulSoup(b.get('html',''),'html.parser').get_text().strip()
  if text in ['留言 / 访问次数','跑完也说两句']:break
  if b['kind']=='heading' and not text:continue
  if b['kind']=='paragraph':
   for prefix,title in triggers.get(d['slug'],{}).items():
    if text.startswith(prefix):out.append({'kind':'heading','title':title})
   el=BeautifulSoup(b['html'],'html.parser').p
   automatic=d['slug'] in ['guilin-marathon','hong-kong-marathon','xiangyang-marathon'] and 'border-left' in el.get('style','') and not re.match(r'^[⛰💎🏯]',text)
   if automatic or text in headings.get(d['slug'],[]):
    if out and out[-1]['kind']=='heading' and out[-1]['title']==text:continue
    b={'kind':'heading','title':text}
  out.append(b)
 d['blocks']=out;return d

def render(d,hero=True):
 d=prepare(d)
 slug=d['slug'];series='RunWorld' if d['title'].startswith('RunWorld') else 'RunCN';station=re.search(r'第([\d-]+)站',d['title'])[1]
 common.SELECT=SELECT;common.render(d,hero=hero)
 if series=='RunCN':mountain_intro(slug)
 p=ROOT/f'run50/wechat/{slug}-editorial.html';s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser');s.main['data-edition']=series.lower()+'-'+slug
 for el in s.select('.chapter-label,.ending .series'):
  el.string=f'{series.upper()} · 第{station}站'
 caption=s.select_one('.location-poster figcaption')
 if caption:caption.clear();caption.append(f'{series} · 第{station}站');caption.append(s.new_tag('br'));caption.append('制图 / Arsenan')
 m=s.select_one('.location-poster img')
 if m:m['alt']=f'{series} 本站地图'
 link=s.select_one('.copy-tools a');link['href']='/CN/#'+series.lower()+'-series';link.string=series+' 目录'
 brand=s.select_one('.brand-intro');brand['data-logo-theme']='paired';base='/assets/series-intros-20261020/'+slug+'/'
 for node in brand.select('img,source'):
  still=node.name=='source';suffix='-still.png' if still else '.gif';node['srcset' if still else 'src']=base+'light'+suffix
  node['data-light-src']=base+'light'+suffix;node['data-dark-src']=base+'dark'+suffix
  if not still:node['alt']=series+(' 山路片头' if series=='RunCN' else ' 机器人片头');node['height']=280 if series=='RunCN' else 350
 # The old title remains exact; only series labels and opening identity change.
 ending=s.select_one('.ending h2');place=d['title'].split('｜')[1].split('：')[0] if '｜' in d['title'] else '这一站';ending.string=place+'，点亮'
 html=str(s)
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{slug}-{suffix}.html').write_text(html,encoding='utf8')

if __name__=='__main__':
 for p in sorted(DATA.glob('*.json')):
  if len(sys.argv)>1 and sys.argv[1] not in p.stem:continue
  render(json.loads(p.read_text(encoding='utf8')),hero='--no-hero' not in sys.argv)
