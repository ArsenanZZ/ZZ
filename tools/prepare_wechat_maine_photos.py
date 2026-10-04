from pathlib import Path
from PIL import Image,ImageOps
from lxml import html
import json,re,shutil
R=Path.cwd();src=Path(r'Z:\ZhennanZ Folder\0000-ZZ-Run-2026\20260609-0613-New England Series\20260613-ME-Day-6-Marathon\6-文章图')
out=R/'assets/maine-editorial';out.mkdir(exist_ok=True);copy=R/'assets/maine-wechat-copy';copy.mkdir(exist_ok=True)
for p in src.glob('*.jpg'):
 im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');im.thumbnail((2000,2400));im.save(out/p.name,quality=91);im.thumbnail((1080,1600));im.save(copy/p.name,quality=85)
page=R/'run50/wechat-new/maine-sanford-marathon-d-rail.html';archive=page.with_name('maine-sanford-marathon-d-rail-original.html')
if not archive.exists():shutil.copy2(page,archive)
root=html.fromstring(archive.read_text(encoding='utf8')).xpath('//section[@data-cn-content]')[0]
groups={
5:[('ME-01-1','清晨的山间薄雾','')],
6:[('ME-01 ME-02','第五天，来到克莱蒙特','')],
9:[('ME-03','和 Siqi 一起跑进树林',''),('ME-04 ME-04-1','Siqi 和跑友们','Arsenan')],
14:[('ME-05','带着美国国旗的跑友',''),('ME-06 ME-07-2','绿树掩映的河上铁桥',''),('ME-07','河边张开双臂','Siqi'),('ME-07-1','Siqi 站在河边','Arsenan'),('ME-08 ME-08-1','从铁桥上跑过','Siqi'),('ME-09 ME-06-1','小镇清晨的山景与校车',''),('ME-10','雾气里的 Siqi','Arsenan'),('ME-10-1','山间留影','Siqi')],
28:[('ME-11 ME-12','第五天的5K终点','Siqi'),('ME-12-1','Siqi 的花栗鼠上衣','Arsenan'),('ME-13','和跑友合影',''),('ME-13-1','回程经过小镇','')],
30:[('ME-14','红谷仓前挂起奖牌','Siqi'),('ME-15','奖牌挂在小木屋旁',''),('ME-17','和 Paul 合影',''),('ME-18','告别 Xanadu Farm','Arsenan')],
40:[('ME-16','森林里的溪流',''),('ME-16-0','走进树林','Siqi'),('ME-16-1','林间合影','Arsenan'),('ME-19','跟着护林员参观老宅','Siqi'),('ME-19-1','老宅前的合影','Arsenan')],
48:[('ME-20','小镇的白色教堂','')],
50:[('ME-20-0','Cinco’s 墨西哥餐厅',''),('ME-21','Siqi 和奶昔','Arsenan'),('ME-22 ME-23','晚餐与餐厅里的壁画','')],
57:[('ME-24','最后一天，天还没亮就出发','')],
58:[('ME-26','最后一天的 RONALDO 7 球衣','Siqi')],
65:[('ME-24-1 ME-28','雾气里的起点与晨光',''),('ME-25','Siqi 穿着蓝色裙子出发','Arsenan')],
70:[('ME-25-1','和热狗帽跑友碰拳','Siqi')],
75:[('ME-31','继续跑下一圈','Siqi'),('ME-32','阳光照进树林','')],
76:[('ME-27 ME-27-1 ME-27-2','这些天反复遇到的跑友',''),('ME-33 ME-33-1','熟悉的跑者与补给区',''),('ME-33-2','张开双臂跑过镜头','Siqi'),('ME-34','Siqi 跳起来的瞬间','Arsenan'),('ME-35','和跑友一起留影',''),('ME-36','路上继续加油','Siqi')],
87:[('ME-37','带着国旗继续跑',''),('ME-37-1 ME-37-3','树荫里的赛道','Siqi'),('ME-37-2','Siqi 跑过林间','Arsenan'),('ME-29 ME-29-2','每圈回来的补给站','')],
94:[('ME-30','赛道上的自拍','Arsenan'),('ME-38','Siqi 和跑友','Arsenan'),('ME-40','一起张开双臂',''),('ME-42','最后一段路一起走','')],
95:[('ME-39','蓝色冰棒，和球衣一个颜色','Siqi')],
101:[('ME-43 ME-43-1','第35州完赛','Siqi'),('ME-48','42.46公里，5小时32分10秒','')],
103:[('ME-29-1','为 Dave 和 Jennifer 准备的蛋糕','')],
108:[('ME-41jpg','六天的奖牌摆在一起',''),('ME-41-1','缅因州完赛奖牌',''),('ME-44','展开六天的奖牌链','Siqi'),('ME-45 ME-46-1','Siqi 和她的奖牌链','Arsenan'),('ME-46','系列赛的圆形奖牌','Siqi'),('ME-47','六天结束，和 Siqi 合影','')],
122:[('ME-48-1','上车，准备回家','Arsenan'),('ME-49 ME-49-1','回程路上的桥与老建筑','')],
126:[('ME-50','老火车站改成的餐厅',''),('ME-50-1','跑完之后的一餐',''),('ME-51','坐下来吃饭','Arsenan')],
130:[('ME-52','傍晚的归途','')]
}
blocks=[];n=0
for idx,e in enumerate(root):
 if e.xpath('./h2'):
  n+=1;blocks.append(dict(kind='heading',label='前言' if n==1 else f'Chapter {n-1}',title=e.xpath('./h2')[0].text_content().removeprefix('前言：')))
 elif e.tag=='p':
  text=e.text_content().strip().replace('比我的目标 5 个半小时还快一点','接近我5个半小时的目标')
  sentences=re.findall(r'.*?[。！？](?:”)?|.+$',text);chunks=[];chunk=''
  for sent in sentences:
   if len(chunk)+len(sent)>90 and chunk:chunks.append(chunk);chunk=''
   chunk+=sent
  if chunk:chunks.append(chunk)
  figures=[]
  for keys,cap,author in groups.get(idx,[]):
   # Keep portraits standalone; only join related landscape photographs.
   batch=[]
   for key in keys.split():
    im=Image.open(out/(key+'.jpg'))
    if im.width<=im.height:
     if batch:figures.append((batch,cap,author));batch=[]
     figures.append(([key],cap,author))
    else:batch.append(key)
   if batch:figures.append((batch,cap,author))
  for j,s in enumerate(chunks):
   markup=__import__('html').escape(s)
   for phrase in ['最后一个 5K','Live Free or Die','Xanadu Farm','洛克菲勒','松树之州','Mousam Way Trail','14 圈','5 个半小时','5 小时 32 分 10 秒','第 35 个州','六天','四个全马','两个5公里','最后一圈半','一起冲过终点','凌晨4:42','RONALDO','70.3']:
    if phrase in markup:markup=markup.replace(phrase,'<strong>'+phrase+'</strong>',1)
   blocks.append(dict(kind='paragraph',html=markup,source_index=idx))
   for names,cap,author in figures[len(figures)*j//len(chunks):len(figures)*(j+1)//len(chunks)]:
    blocks.append(dict(kind='figure',images=[dict(src='/assets/maine-editorial/'+k+'.jpg',alt=cap) for k in names],caption=cap+('｜摄影 / '+author if author else '')))
allowed={p.stem for p in src.glob('*.jpg')};used=[Path(im['src']).stem for b in blocks if b['kind']=='figure' for im in b['images']]
assert set(used)==allowed,(allowed-set(used),set(used)-allowed)
assert len(used)==len(allowed)
d=dict(title='Run50 第35州｜缅因：桑福德马拉松｜新英格兰六连赛第5天5K与第6天全马',photo_source_folder=str(src),allowed_photo_stems=sorted(allowed),blocks=blocks)
(R/'tools/data/maine-editorial.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Photos',len(used),'paragraphs',sum(b['kind']=='paragraph' for b in blocks))
