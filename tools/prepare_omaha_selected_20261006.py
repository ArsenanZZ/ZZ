"""Import the author's 102 selected photographs and revised manuscript."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, re, concurrent.futures

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'Z:\ZhennanZ Folder\0000-ZZ-Run-2026\20260927-NE-Omaha Marathon\05-文章照片')
OUT=ROOT/'assets/omaha-2026/selected-20261006'
TITLE='Run50 #第36州 | 内布拉斯加州：奥马哈马拉松 | 去巴菲特老家跑马，玉米管够，公里数也多送！'
OFFICIAL={'NE-17-1','NE-17-2','NE-18','NE-22-1-2','NE-28-8-3','NE-28-8-4','NE-28-99','NE-28-99-1','NE-50-11','NE-50-12'}
SIQI={'NE-51','NE-51-11','NE-54','NE-54-1'}
def credit(key):
    if key in OFFICIAL:return '摄影 / 赛事官方摄影'
    if key in SIQI:return '摄影 / Siqi'
    if key == 'NE-44':return '摄影 / 志愿者'
    if key == 'NE-55':return ''
    return '摄影 / Arsenan'
CAPTIONS={
'NE-00':'下班出发，公路尽头的粉色天空','NE-00-1':'中秋的月亮已经升起来了',
'NE-01':'印第安纳的傍晚','NE-01-2':'车窗外的火烧云','NE-01-3':'金黄色的天边',
'NE-02':'赶路途中，健身房也要打卡','NE-03':'健身房外的中秋月亮','NE-03-1':'晚上停车时拍个合影','NE-03-2':'云缝里的月亮',
'NE-04':'后视镜里的晨光','NE-04-1':'周六继续往西开','NE-04-2':'路旁的农田',
'NE-05':'没看到大拱门，先看到车上的版本','NE-05-1':'路过教堂的双塔','NE-06':'公路上的卡车与远处的粮仓',
'NE-07':'田里的圆草捆','NE-07-1':'一路经过的农业设施','NE-07-2':'田边的粮仓','NE-07-3':'城市的楼群出现在远处',
'NE-08':'赶在收摊前领到参赛包','NE-09':'两个人，两张号码布','NE-10':'领物处附近的“小黄人”大楼','NE-11':'奥马哈的晚霞','NE-11-1':'领完东西，再慢慢看天',
'NE-12':'民宿外的夜色','NE-12-1':'今晚住的小房子','NE-13':'和民宿主人聊起中国与玉米',
'NE-14':'全马起跑前，天还没亮','NE-15':'灯光下的起跑拱门','NE-16':'跑友们陆续集合','NE-17':'排队走向起跑线','NE-17-1':'清晨出发的跑友','NE-17-2':'橙色上衣，出发','NE-18':'7点，全马开跑','NE-19':'起跑的人群','NE-20':'跟着队伍往前跑','NE-21':'薄雾里的奥马哈天际线',
'NE-22':'河边的木栈道','NE-22-1':'穿过步道上的桥下空间','NE-22-1-1':'Charles Schwab Field，大学棒球世界大赛的主场','NE-22-1-2':'跑进城市街道','NE-22-2':'Fertile Ground，《沃土》壁画','NE-22-3':'大约5英里，状态还不错','NE-22-4':'白色筒仓出现在路边',
'NE-23':'沿着绿地继续跑','NE-24':'湖边树荫下的步道','NE-25':'跑错一圈以后，继续往前','NE-26':'重新回到城市的方向','NE-27':'Omaha North Mill 老面粉厂与白色粮仓',
'NE-28':'沿街道跑回市区','NE-28-8-3':'看见摄影师，调整一下姿势','NE-28-8-4':'城市高楼前的跑步照','NE-28-99':'这场比赛的照片可以免费下载','NE-28-99-1':'镜头前把双手展开',
'NE-29':'BIG EAST，大东联盟的旗子','NE-30':'又一次跑回市区','NE-31':'走上大桥的引道','NE-32':'跟着跑友上桥','NE-33':'Bob Kerrey 步行桥','NE-33-1':'桥下的密苏里河','NE-34':'跨州大桥上的跑友','NE-35':'从爱荷华一侧回望奥马哈','NE-35-1':'桥头的志愿者',
'NE-36':'Looking Up，巨人仰头，小朋友在脚边玩','NE-37':'太阳出来了，河堤上开始热起来','NE-37-1':'爱荷华一侧的跑步自拍','NE-37-2':'补点水，再往前跑','NE-38':'终于跑到折返点','NE-39':'折返点附近的跑友','NE-40':'24英里，我的手表已经全马了','NE-40-1':'朝着城市天际线往回跑','NE-41':'后半程，帽子也要换个方向','NE-42':'回程的步道','NE-43':'河对岸的城市高楼','NE-43-1':'侧着戴帽子，遮一点太阳','NE-44':'停一下，请人帮忙拍张照','NE-45':'返程桥上的视野','NE-45-1':'在大桥上自拍','NE-46':'从引道看回体育场一带','NE-47':'远处又能看到《沃土》壁画','NE-48':'从草地上看跨州大桥',
'NE-49':'沿河岸继续朝终点跑','NE-49-1':'最后一段步道','NE-50':'26英里的牌子，终点快到了','NE-50-1':'最后这段，跑跑拍拍','NE-50-11':'张开双手冲线','NE-50-12':'第36州，完成','NE-51':'终点拱门前','NE-51-11':'跑完以后，先缓一缓','NE-52':'Siqi 已经完赛，等我一起拍照','NE-53':'蓝黄奖牌，上面还有跨州大桥','NE-54':'举起奖牌留个纪念','NE-54-1':'内布拉斯加，跑到了','NE-55':'我们和第36州的奖牌','NE-55-1':'两个人的完赛合影',
'NE-56':'返程路上经过彩绘筒仓','NE-57':'驶入爱荷华','NE-58':'回程的粮仓与铁轨','NE-58-0':'晚上又停进熟悉的停车场','NE-58-1':'返程时，月亮还是圆的','NE-58-2':'开车回家，还得继续赶路','NE-59':'公路上的晨光'
}
def main():
    OUT.mkdir(exist_ok=True)
    text=(ROOT/'tools/data/omaha-20261006.txt').read_text(encoding='utf8')
    blocks=[];keys=[]
    for line in text.splitlines():
        if not line.strip():continue
        if line.startswith('## '):
            label,title=line[3:].split('｜',1);blocks.append(dict(kind='heading',label=label,title=title))
        elif line.startswith('@ '):
            for key in line[2:].split():
                keys.append(key);blocks.append(dict(kind='photos',ids=[key],caption=CAPTIONS[key],credit=credit(key)))
        else:blocks.append(dict(kind='paragraph',text=line))
    actual={p.stem for p in SOURCE.glob('*.jpg')}
    assert len(keys)==len(set(keys))==102 and set(keys)==actual,(actual-set(keys),set(keys)-actual)
    assert not re.search('[—–]',text)
    def convert(key):
        dest=OUT/f'{key}.webp'
        with Image.open(SOURCE/f'{key}.jpg') as src:
            im=ImageOps.exif_transpose(src).convert('RGB')
            im.save(dest,'WEBP',quality=90,method=5)
            with Image.open(dest) as check:assert check.size==im.size
        return key
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i,key in enumerate(pool.map(convert,keys),1):
            if i%20==0:print(f'Imported {i}/102',flush=True)
    data=dict(title=TITLE,date='2026-09-27',state='内布拉斯加',city='奥马哈',photo_folder='selected-20261006',blocks=blocks)
    (ROOT/'tools/data/omaha-wechat-editorial.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    # The hero is a separate slideshow; article photographs above are never cropped.
    frames=[]
    for key,center in [('NE-17-2',(.5,.4)),('NE-33',(.5,.4)),('NE-50-12',(.5,.35)),('NE-55',(.5,.3)),('NE-53',(.5,.45))]:
        with Image.open(OUT/f'{key}.webp') as im:
            if key == 'NE-53':
                frames.append(ImageOps.fit(im.convert('RGB'), (900,900), method=Image.Resampling.LANCZOS, centering=(.5,1.0)))
            else:
                frames.append(ImageOps.fit(im.convert('RGB'),(900,900),method=Image.Resampling.LANCZOS,centering=center))
    frames[0].save(OUT/'hero-still.jpg',quality=93)
    frames[0].save(OUT/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)
    check=Image.new('RGB',(1250,250),'white')
    for i,im in enumerate(frames):check.paste(im.resize((250,250)),(i*250,0))
    (ROOT/'tmp').mkdir(exist_ok=True);check.save(ROOT/'tmp/omaha-hero-check.jpg')
    print('102 selected photographs and revised story prepared',flush=True)
if __name__=='__main__':main()
