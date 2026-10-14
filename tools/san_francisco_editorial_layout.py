"""Scene-checked captions and interleaving for the complete San Francisco story."""
import re
from html import escape

CAPTIONS='''旧金山的雾，有个名字叫Karl
旧金山旅行海报，出发前的城市想象
机窗外，河流在峡谷间蜿蜒
越过山脉，向加州飞去
联合广场附近，抬头都是城市的层次
叮当车从街道深处驶来
沿着轨道，听旧金山的铃声
加州科学馆里，先走进一片绿意
玻璃两侧，和水中的动物打个照面
圆形窗口里的水下世界
珊瑚与灯光，把水族馆染成紫色
巨大的水箱前，人也成了剪影
坐进穹幕下，准备看一场宇宙短片
科学馆外，晴空下的摩天轮
和Anastasia一起吃韩国火锅
我和Siqi，先把这一顿吃饱
夕阳慢慢落到海湾对岸
把日落留在手心和镜头里
披上红毯子，去金门大桥边吹风
海风太大，红毯子派上了用场
桥边拍照，装备齐全就不怕冷
没有被雾遮住的金门大桥
Siqi在桥边，把夕阳拍下来
金门大桥旁，恰好遇见求婚
夜色降下，桥塔变成剪影
第二天的旧金山，流雾漫过楼顶
雾气里的街口，叮当车照常经过
走进唐人街，准备找早餐
街边早点铺，满是熟悉的烟火气
中文招牌下，大家买菜、吃早饭
唐人街的楼房和老招牌
意大利咖啡，配一顿中式早餐
咖啡店窗外，公交车从眼前经过
意大利街区的教堂
九曲花街，车道绕着花坛往下走
在九曲花街，停下来拍一张
花街边，Siqi也在记录这趟旅行
汽车沿着急弯慢慢下行
从高处回望，一条街直伸向海湾
戴好头盔，跟着车队游旧金山
渡轮大厦旁的自行车道
蓝天海水间，湾桥横跨眼前
骑到Rincon公园，在湾桥边停一停
沿海骑行，Siqi和自行车一起入镜
路过勇士队主场Chase Center
车队停下来，去吃露天午餐
路边等待换车，先看一眼手机
换好车，继续骑进旧金山街头
Mission Dolores公园，大家在草坪上晒太阳
花丛后，金色塔楼格外醒目
草坪与学校，组成晴朗的午后
近看Mission High School的塔楼
公园旁的小吃摊，烤架上热气腾腾
彩绘女士，整整齐齐站在坡上
在Alamo广场，坐下来看看城市
树影之下，彩绘女士与远处的天际线
草坪前的彩色房屋，是旧金山的另一张脸
抬头看旧金山市政厅的穹顶
从市政厅前骑过，阳光照着路面
日本城的和平塔
广场上，围着舞台看表演的人
科伊特塔，立在电报山上
从树枝之间，再看一眼科伊特塔
从山顶望出去，海湾铺在城市后面
远处的恶魔岛，浮在蓝色海面上
绕了一大圈，又回到渔人码头
老式有轨电车从码头旁经过
码头边，游客停下来围观
街边小吃，给热闹的码头添一口香气
饮料摊和走走停停的人群
走回唐人街，路边都是彩色涂鸦
壁画前，行人从画面里经过
街角的绿巨人，和旧金山打个照面
中餐馆墙上，排着来过这里的名人照片
骑完车，先吃一盘青菜
再来一道热菜，把肚子填饱
跑在旧金山，绿色长袖是前半程的装备
举起双手，把45周年跑进记忆
Festival Pavilion，领取比赛装备
赛前先拿到一块45周年纪念奖牌
旧金山全程马拉松路线图
天还没亮，跑者聚在渡轮大厦前
晨色中的渔人码头，赛道从钟楼旁经过
迎着海风，向金门大桥跑去
沿着Presidio的道路前进
金门大桥，终于从晨雾里出现
桥塔的上半截，仍藏在雾中
把大桥放进背景，认真跑过镜头
桥下折返之后，迎来上桥的长坡
跑友帮忙，留下和金门大桥的合影
沿着海岸，跑向桥塔
越接近大桥，跑者越兴奋
终于跑上桥面，风声就在耳边
雾里的桥塔，仰头也看不到尽头
桥上有人轻装上阵，我却觉得很冷
跑下北侧桥头，摄影师就在前方
桥边继续奔跑，绿色战袍很醒目
隔着海岸的植物，回望金门大桥
互相帮忙拍照，留下桥下的这一刻
海边遇见镜头，张开双臂
再挥挥手，在镜头前跑得很开心
接近半程，拉下长袖继续跑
又是一段上坡，准备第二次上桥
回程桥面，顶着风雨慢慢向前
14英里，终于从大桥路段缓过来了
小朋友守在路边，为跑者递补给
跑进街区，前方又有一个长坡
接过一根能量棒，补一点力气
来到金门公园，半程终点就在旁边
半马终点区，跑者陆续抵达
湖里的野鸭，游得不紧不慢
绿水对岸，藏着一座中式凉亭
公园里，跑者顺着树荫向前
跑回城市，天气渐渐热了起来
太热了，和绿色长袖告个别
阳光下，彩绘墙面格外鲜艳
赛道旁，旧金山的房屋各有模样
蓝天下的街区，长坡还在继续
更多跑者加入，城市又热闹起来
路边的一小杯啤酒，给后半程加点快乐
路过Chase Center，先和勇士主场合个影
换上背心，继续跑过镜头
阳光里的后半程，脚步还在向前
25英里标牌，巨人队主场就在眼前
球场边的吊桥，跨在水道上
回到海湾，帆船桅杆排成一片
棕榈树下，最后一英里
湾桥横在前面，终点已经不远
沿着湾桥下的道路，继续向终点跑
快到了，最后一段继续坚持
穿过终点拱门，五个多小时的旅程完成
完赛照片与成绩纪念卡
完赛后的影子，也要留下来
方方正正的45周年完赛奖牌
奖牌和湾桥，放进同一个画面
换个角度，把旧金山装进奖牌照
棕榈树下，再留一张完赛纪念
赛后去水族馆，从海底隧道走过
水中漂浮的水母，像透明的花
再近一点，看水母的细长触须
来到Pier 39，准备登船
码头边，海湾和游船都在眼前
从码头回望，山坡上的城市层层叠叠
游船驶过海面，远处是恶魔岛
从海上看旧金山，天际线换了一个角度
船只在海湾穿行
越靠近西边，雾气越浓
完赛奖牌，和雾中的金门大桥
船上再拍一张，桥就在身后
桥下的Siqi，解锁“大法师”造型
从水面仰望金门大桥
驶回晴朗的海湾，城市又亮了起来
靠岸之前，回望山坡与科伊特塔
码头水面上，海狮挤在浮台休息
停泊的船只和远处的恶魔岛
机场外，流雾还贴着远处山脊
等到天色变了，航班仍没有起飞
Welcome to San Francisco，再多留半天'''.splitlines()

def captions(d):
 assert len(CAPTIONS)==158,len(CAPTIONS)
 official={77,78,88,96,97,100,101,102,110,114,122,123,130,131,132}
 siqi={19,20,21,36}
 for b in d['blocks']:
  if b['kind']!='figure':continue
  n=b['id'];credit='摄影 / Arsenan'
  if n in official:credit='摄影 / FinisherPix'
  if n in siqi:credit='摄影 / Siqi（47）'
  if n==16:credit='摄影 / Anastasia'
  if n in {90,99}:credit='摄影 / 现场跑友'
  if n in {1,2,81}:credit='资料图 / 原文来源：Google'
  if n in {47,48}:credit='摄影 / Siqi'
  b['alt']=CAPTIONS[n-1];b['caption']=CAPTIONS[n-1]+' · '+credit

def arrange(d):
 images={b['id']:b for b in d['blocks'] if b['kind']=='figure'}
 # Correct source-adjacent pictures whose captions belonged to a later paragraph.
 moves={7:(1,5),23:(3,4),24:(3,5),48:(6,8),54:(7,1),66:(8,4),77:(11,2),78:(11,9),96:(14,10),97:(14,10),98:(14,11),99:(14,11),104:(15,5),124:(17,2),125:(17,2),126:(17,1),133:(18,3),134:(18,1),135:(18,2),136:(18,2),137:(18,3),143:(19,2),144:(19,2),145:(19,2),146:(19,2),147:(19,2),148:(19,3),149:(19,3),152:(20,0),153:(20,0),154:(20,0),155:(20,0),156:(20,1),157:(20,2),158:(20,8)}
 result=[];bs=d['blocks'];i=0
 while i<len(bs):
  b=bs[i]
  if b['kind']=='heading':result.append(b);i+=1;continue
  if b['kind']=='figure':
   if b['id'] not in moves:result.append(b)
   i+=1;continue
  j=i+1;photos=[]
  while j<len(bs) and bs[j]['kind']=='figure':
   if bs[j]['id'] not in moves:photos.append(bs[j])
   j+=1
  photos.extend(images[n] for n,dest in moves.items() if dest==(b['chapter'],b['paragraph']))
  photos.sort(key=lambda x:x['id'])
  sentences=re.findall(r'.*?[。！？](?:[”’])?|.+$',b['text'])
  count=max(1,(len(photos)+2)//3)
  if len(sentences)<count:sentences=re.findall(r'.*?[，。！？；](?:[”’])?|.+$',b['text'])
  count=min(count,len(sentences));cuts=[round(k*len(sentences)/count) for k in range(count+1)];pics=[round(k*len(photos)/count) for k in range(count+1)]
  for k in range(count):
   chunk=''
   for t in sentences[cuts[k]:cuts[k+1]]:
    if chunk and len(chunk)+len(t)>130:result.append({'kind':'paragraph','text':chunk,'original_html':'<p>'+escape(chunk)+'</p>'});chunk=''
    chunk+=t
   if chunk:result.append({'kind':'paragraph','text':chunk,'original_html':'<p>'+escape(chunk)+'</p>'})
   result.extend(photos[pics[k]:pics[k+1]])
  i=j
 ids=[b['id'] for b in result if b['kind']=='figure']
 assert len(ids)==len(set(ids))==158,(len(ids),set(images)-set(ids))
 assert ''.join(b['text'] for b in result if b['kind']=='paragraph')==''.join(d['original_paragraphs'])
 return result
