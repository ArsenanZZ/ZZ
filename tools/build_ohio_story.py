from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2021-State-02-OH"
)
CITY_HTML = next(p for p in SOURCE_BASE.glob("*.html") if "摇滚" in p.name)
RACE_HTML = next(p for p in SOURCE_BASE.glob("*.html") if "42.195" in p.name)

SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "cleveland-marathon"
VERSION = "20260615-1"
ENGAGEMENT_VERSION = "20260615"

OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-Cleveland-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-cleveland-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-cleveland-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-oh.jpg"

TITLE_ZH = "Run50 #第2州｜俄亥俄：克利夫兰马拉松｜从黑夜跑到白昼"
TITLE_EN = "Run50 #2 | Ohio: Cleveland Marathon, From Night to Daylight"
TITLE_FB = "Cleveland gave me a cold, industrial 26.2 miles from night into daylight"
DATE_ZH = "2021.10.24"
DATE_EN = "Oct 24, 2021"
RACE_NAME = "44th Union Home Mortgage Cleveland Marathon"


TRANSLATIONS = {
    "丨Rock 'n roll丨": "| Rock 'n roll |",
    "悲情克利夫兰，摇滚乐的故乡": "Melancholy Cleveland, birthplace of rock and roll",
    "▲ Hot in Cleveland @ Arsenan": "▲ Hot in Cleveland @ Arsenan",
    "- Cleveland -": "- Cleveland -",
    "詹姆斯，摇滚乐": "LeBron James and rock and roll",
    "前言": "Preface",
    "离开美味的哥伦布，启程克利夫兰。": "Leaving tasty Columbus, we set off for Cleveland.",
    "与芝加哥相比，这一路上的重型卡车明显少了不少，并且大家都很礼貌，少有人抢占最左侧的高速路。": "Compared with the road to Chicago, there were noticeably fewer heavy trucks on this drive, and people were pretty polite. Hardly anyone hogged the far-left lane.",
    "在走完俄亥俄秋意渐浓的I-76之后，克利夫兰城终于展现在了我的面前。": "After rolling along I-76 through Ohio's deepening autumn, Cleveland finally appeared in front of me.",
    "▲ Cleveland @ Arsenan": "▲ Cleveland @ Arsenan",
    "01": "01",
    "悲情克利夫兰": "Melancholy Cleveland",
    "所谓“悲情”，是指克利夫兰见证分享了美国大工业时代的荣光，也不幸全程体验了去工业化后的衰败，就像破产的底特律一样，现在的克利夫兰依旧不是那么繁荣。": "By \"melancholy,\" I mean Cleveland witnessed and shared in the glory of America's industrial age, and then unfortunately lived through the whole decline that followed deindustrialization. Like bankrupt Detroit, Cleveland still does not feel especially prosperous today.",
    "关于克利夫兰的调侃很多，美国媒体就曾称它为“五大湖上的错误”，在美国文化中，克利夫兰=比地狱还糟糕的地方、宁可去朝鲜也不去克利夫兰。": "There are plenty of jokes about Cleveland. American media once called it \"the mistake on the lake.\" In American pop culture, Cleveland can mean a place worse than hell, the kind of place people joke they would rather avoid at all costs.",
    "不过在中国，我和大多数人一样，对于克利夫兰的印象，大概还停留在LeBron James和他的骑士队。": "But in China, like most people, my impression of Cleveland probably still begins with LeBron James and his Cavaliers.",
    "初中的时候，我经常和隔壁班的老肥打篮球，他总是穿着一件骑士队的23号红白球衣，除了麦迪，詹姆斯就是我们那些小孩里的第一球星，虽然我更喜欢吉诺比利。": "In middle school, I often played basketball with Lao Fei from the class next door. He always wore a red-and-white Cavaliers No. 23 jersey. Besides McGrady, LeBron was the biggest star for us kids, though I personally liked Ginobili more.",
    "不论是EA的NBA live还是cctv5的体育新闻，那个时代的克利夫兰总是以极高的频率出现在我的身边。": "Whether it was EA's NBA Live or sports news on CCTV5, Cleveland showed up around me constantly in that era.",
    "可是，纵观克利夫兰的职业体育，其实也和城市的发展一样悲情，从上世纪最后一次夺冠开始算，1964年的布朗队再到2016年的骑士队，中间时隔了整整半个多世纪。": "But Cleveland's pro sports history is, in its own way, as melancholy as the city's development. From the Browns' last title in 1964 to the Cavaliers' championship in 2016, more than half a century passed.",
    "所以可以想象，当老汉说出“Cleveland！！This is for you！”时，克城人是多么的骄傲和自豪。": "So you can imagine how proud Clevelanders felt when LeBron shouted, \"Cleveland! This is for you!\"",
    "02": "02",
    "摇滚乐的故乡": "Birthplace of rock and roll",
    "但悲情不是悲悯。": "But melancholy is not pity.",
    "即便如今，老汉已经远去，但后詹姆斯时代的克城也不屑于别人的怜悯，因为这里是摇滚乐的故乡。": "Even now, with LeBron gone, Cleveland in the post-LeBron era has no use for anyone's pity, because this is the birthplace of rock and roll.",
    "这座城市有多摇滚，这里的人就有多倔强。": "However rock-and-roll this city is, its people are just as stubborn.",
    "▲ 摇滚乐名人堂博物馆 @ Arsenan": "▲ Rock & Roll Hall of Fame @ Arsenan",
    "1951年，克利夫兰电台节目主持人艾伦·弗里德从一首节奏布鲁斯歌曲《我们要去摇 我们要去滚》(We're Gonna Rock We're Gonna Roll)中创造出了\"摇滚乐\"(Rock n' Roll)这个词，克利夫兰因此被称作“摇滚世界之都”。": "In 1951, Cleveland radio host Alan Freed helped popularize the term \"rock 'n' roll\" from the rhythm-and-blues song \"We're Gonna Rock, We're Gonna Roll.\" Cleveland has been called the capital of the rock world because of it.",
    "我对摇滚世界是向往的，相比于那些华丽的编曲和精致的唱功，这些个扯着破嗓子的undergrounder们可太TM有魅力了。": "I have always been drawn to the rock world. Compared with polished arrangements and delicate vocals, those undergrounders singing with ragged voices are just insanely charismatic.",
    "▲ 猫王 @ Arsenan": "▲ Elvis @ Arsenan",
    "▲ The Beatles @ Arsenan": "▲ The Beatles @ Arsenan",
    "不用立什么人设，足够real，摇滚乐源于叛逆，却归于生活，在我这，音乐可不是什么艺术品，而是该给人带来力量的东西。": "No need to build some persona. Just be real enough. Rock music starts from rebellion but eventually returns to life. To me, music is not some museum object. It should give people strength.",
    "当然，对于那些艺术家们，我respect！": "Of course, for those artists, I have respect.",
    "终于要聊一聊我的克利夫兰之行了，我不算是狂热的音乐发烧友，但克利夫兰摇滚乐名人堂博物馆是必须要去的。": "Now, finally, about my Cleveland trip. I am not a hardcore music nerd, but the Rock & Roll Hall of Fame in Cleveland was a must.",
    "虽然里面的人我大多都不认识，但就是觉得很酷，特别是小剧场里的经典片段回顾，St. Vincent的表演可太有张力了，让人热血沸腾。": "I did not know most of the people inside, but it still felt cool. The classic performance reel in the small theater was especially good. St. Vincent's performance had so much tension it made my blood heat up.",
    "博物馆的后面紧挨着伊利湖，这里可以看到克利夫兰的天际线，还有大游轮和克利夫兰标志适合拍照。": "Behind the museum is Lake Erie. From there you can see the Cleveland skyline, the big cruise ship, and the Cleveland sign that is perfect for photos.",
    "▲ 伊利湖畔 @ Arsenan": "▲ By Lake Erie @ Arsenan",
    "这回我没了兴致去尝一尝伊利湖的湖水，因为这水真的太脏了，听说当年因为污染，流经克利夫兰市区的凯霍加河还着了几十次火。": "This time I had no desire to taste the water of Lake Erie, because it really looked dirty. I had heard that, back in the day, the Cuyahoga River running through downtown Cleveland caught fire dozens of times because of pollution.",
    "▲ 克利夫兰天际线 @ Arsenan": "▲ Cleveland skyline @ Arsenan",
    "▲ 克利夫兰 @ Arsenan": "▲ Cleveland @ Arsenan",
    "▲克利夫兰 @ Arsenan": "▲ Cleveland @ Arsenan",
    "在回Comfort Inn的路上，感受着克城的秋色和安静的街区，会觉得这里其实也挺美的，这是一座经历过大起大落的城市，但只要摇滚乐不死，这座立于铁锈州的工业老城，总会有发光的一天。": "On the way back to the Comfort Inn, feeling Cleveland's autumn colors and quiet neighborhoods, I found the city actually quite beautiful. It is a city that has gone through big rises and hard falls, but as long as rock and roll does not die, this old industrial city in the Rust Belt will have its day to shine again.",
    "▲ 克利夫兰秋天 @ Arsenan": "▲ Cleveland autumn @ Arsenan",
    "这让我想到了我的家乡，东北，同样的老工业区，同样经历过辉煌后又迅速坠落，如果克利夫兰可以用摇滚乐作为精神内核，那东北有什么？二人转么？至少也可以自得其乐吧。": "It made me think of my hometown, Northeast China: another old industrial region, another place that rose brilliantly and then fell quickly. If Cleveland can use rock and roll as its spiritual core, what does the Northeast have? Errenzhuan, maybe? At least we can still entertain ourselves.",
    "03": "03",
    "骑士队主场": "At the Cavaliers' home court",
    "来克利夫兰之前，发现这天正好有一场骑士和老鹰的比赛，相比于看骑士的比赛，其实我更想看看老鹰的吹杨。": "Before coming to Cleveland, I noticed there happened to be a Cavaliers-Hawks game that day. More than watching the Cavaliers, I actually wanted to see Trae Young from the Hawks.",
    "▲ 速贷中心 @ Arsenan": "▲ Rocket Mortgage FieldHouse @ Arsenan",
    "▲ 骑士队 @ Arsenan": "▲ Cavaliers @ Arsenan",
    "这回买了个一层的球票，终于不用在山顶看球了，回想当年在印第安娜，印象最深的就是下面这个大屏幕，又大又清晰，应该比在家看电视好不少，不过票价才20刀，也不能期待更多。": "This time I bought a lower-bowl ticket, so I finally did not have to watch from the mountaintop. Thinking back to Indiana, what impressed me most was the huge screen below, big and clear, probably better than watching TV at home. But the ticket was only $20, so I could not ask for too much.",
    "▲ 头顶的大屏幕 @ Arsenan": "▲ The big screen overhead @ Arsenan",
    "▲ 奏国歌 @ Arsenan": "▲ National anthem @ Arsenan",
    "这回算是看了个真正的NBA，全程体验了球员入场，放国歌，节间的各种互动，速贷中心的氛围特别棒，美国的球迷文化也是没话说。": "This felt like a real NBA experience: player introductions, the national anthem, all the between-quarter games and crowd interactions. The atmosphere at Rocket Mortgage FieldHouse was excellent, and American fan culture is honestly impressive.",
    "▲ 热场 @ Arsenan": "▲ Pregame hype @ Arsenan",
    "▲ 热身 @ Arsenan": "▲ Warmups @ Arsenan",
    "与氛围相比，比赛的过程和结果似乎也就没那么重要了，最后应该是骑士获得了本赛季的第一场胜利，卢比奥全场MVP，西班牙人还进了几个三分球。": "Compared with the atmosphere, the game itself and the final result did not seem that important. I think the Cavaliers ended up getting their first win of the season. Rubio was the MVP of the night, and the Spaniard hit a few threes too.",
    "▲ 节间啦啦队表演 @ Arsenan": "▲ Timeout cheer squad performance @ Arsenan",
    "不过比赛里的一些场景还是挺让人动容的，比如曾经三巨头之一的老将凯文乐福，他在第二节替补出场，全场掌声雷动。这让我想到了一部变形金刚电影《最后的骑士》，对于我们这代人，乐福大概就是这支年轻队伍里最后的骑士了，也是一个时代的余晖。": "Some moments in the game were still moving, especially veteran Kevin Love, once part of the Big Three. When he came off the bench in the second quarter, the whole arena thundered with applause. It made me think of the Transformers movie The Last Knight. For our generation, Love is probably the last knight on this young team, the afterglow of an era.",
    "后记": "Postscript",
    "看完球，混在球迷中间返回旅馆。": "After the game, I walked back to the hotel among the fans.",
    "远处的克利夫兰塔(Tower City Center)清晰可见，建成时，这里可是世界第二高的摩天大楼。": "In the distance, Cleveland's Tower City Center was clearly visible. When it was built, it was once the second-tallest skyscraper in the world.",
    "如今，它立于城市上空，似乎也在诉说着那些独属于克利夫兰的工业荣光。": "Now it stands above the city, as if still telling stories of Cleveland's own industrial glory.",
    "▲ 克利夫兰塔 @ Arsenan": "▲ Cleveland tower @ Arsenan",
    "不过年轻一代的克利夫兰人却并没有多少时间去伤感，他们更爱摇滚乐和NBA，也要为生活辛苦的奔波。": "But the younger generation of Clevelanders does not seem to have much time for melancholy. They love rock and roll and the NBA, and they are busy working hard for life.",
    "我们随着熙熙攘攘的人群一路向前，身边弥漫着赢球的喜悦。": "We moved forward with the crowd, with the joy of a win hanging in the air around us.",
    "我想，现在的克利夫兰，至少是少了一点悲情，多了一分美国梦式的畅然。": "I think Cleveland today has, at least, a little less sorrow and a little more of that free-and-easy American-dream feeling.",
    "丨Cleveland丨": "| Cleveland |",
    "克利夫兰，燃情42.195": "Cleveland, fired up for 42.195",
    "▲ Cleveland Marathon by Arsenan": "▲ Cleveland Marathon by Arsenan",
    "- Cleveland Run -": "- Cleveland Run -",
    "从黑夜跑到白昼": "Running from night into daylight",
    "2021年的克利夫兰马拉松原本是在五月，但因为疫情，被推迟到了十月。": "The 2021 Cleveland Marathon was originally scheduled for May, but because of the pandemic it was postponed to October.",
    "正犹豫要不要去，突然在朋友圈看到2021年的汉马居然和克利夫兰是同一天，想到能和老朋友们隔空一起跑马，吸引力满分，怎么都得去。": "I was still hesitating about whether to go when I suddenly saw on WeChat Moments that the 2021 Wuhan Marathon was on the same day as Cleveland. The idea of running a marathon from afar together with old friends was too appealing. I had to go.",
    "后来的故事很波折，汉马在赛前一天取消，但克利夫兰，我还是去了，虽然少了些仪式感，但跑的还是很尽兴。": "The story later took a twist: Wuhan Marathon was canceled the day before the race. But I still went to Cleveland. It lost a little of the ceremonial feeling, but the run itself was still a lot of fun.",
    "▲Map @ Google": "▲ Map @ Google",
    "克利夫兰马拉松": "Cleveland Marathon",
    "克利夫兰马的起点在 Tower City Center 附近，伴着夜色出行，来到起点处，红色的塔尖十分壮观。": "The Cleveland Marathon start was near Tower City Center. I headed out in the dark, and when I reached the start, the red tower spire looked spectacular.",
    "▲起点 @ Arsenan": "▲ Start area @ Arsenan",
    "清晨的克利夫兰让人瑟瑟发抖，选手们需要伴着夜色起跑。": "Early-morning Cleveland made people shiver. Runners had to start in the dark.",
    "这对我来讲其实并不新鲜，新加坡曼谷也是如此，不过东南亚跑马都是从午夜跑到清晨，而克利夫兰则仅仅是太阳出升的比较晚，并且冷了几个数量级。": "That was not exactly new to me. Singapore and Bangkok were like that too. But Southeast Asian marathons run from midnight into morning, while Cleveland simply had a late sunrise and was several levels colder.",
    "我套了个薄长袖，心想热身开了就赶紧脱掉，谁知道这一跑起来，就真脱不下来了。": "I wore a thin long-sleeve layer and thought I would take it off once I warmed up. Once I started running, though, I really could not take it off.",
    "▲起跑 @ Arsenan": "▲ Starting out @ Arsenan",
    "发枪之后，大家就迫不及待得跑起来了，因为真的太冷了，我也赶紧开动双腿，所有的选手就沿着底特律路朝着西南方向出发。": "After the gun, everyone started running immediately because it was truly cold. I quickly got my legs moving too, and all the runners headed southwest along Detroit Road.",
    "▲出发 @ Arsenan": "▲ Setting off @ Arsenan",
    "后来我才知道，在克利夫兰，不仅有底特律路，还有底特律海岸。": "Only later did I learn that in Cleveland, there is not only Detroit Road, but also Detroit Shoreway.",
    "克利夫兰和底特律，两座城市同处于五大湖边的铁锈州，似乎也在去工业化的大潮中找到了互相取暖的理由。": "Cleveland and Detroit, two Rust Belt cities on the Great Lakes, seem to have found reasons to keep each other company through the tide of deindustrialization.",
    "当然，这些和我今天的跑马无关。": "Of course, none of that had anything to do with today's marathon.",
    "▲跑进市区 @ Arsenan": "▲ Running into the city @ Arsenan",
    "继续向前，在经历了25街，48街和富兰克林路的Loop之后，我们又回到了底特律路，不过这回是朝着市中心的方向。": "Continuing forward, after looping through 25th Street, 48th Street, and Franklin Boulevard, we returned to Detroit Road, this time heading toward downtown.",
    "天还没有大亮，远处的高楼坚毅挺拔，在晨云的映衬下，气势磅礴。这段奔跑，算是整个旅程中最硬朗的一段，记忆深刻。": "The sky was still not fully bright. The distant high-rises stood firm and upright, backed by morning clouds, giving the whole scene a powerful presence. This stretch was the toughest-looking, most memorable part of the journey.",
    "▲老兵纪念桥 @ Arsenan": "▲ Veterans Memorial Bridge @ Arsenan",
    "跑过老兵纪念桥和市中心的一段水泥路，我们转向伊利湖边的漫漫高架。": "After running over Veterans Memorial Bridge and a stretch of concrete road downtown, we turned toward the long elevated section by Lake Erie.",
    "▲右手边 @ Arsenan": "▲ On the right @ Arsenan",
    "▲左手边 @ Arsenan": "▲ On the left @ Arsenan",
    "右手边，火车驶在伊利湖上，蓝色的湖水和粉色的云朵交相辉映；左手边，太阳则刚刚升起，城市的剪影在晨光中清晰可见，勾勒出了克城的天际线。": "On the right, trains moved along Lake Erie, blue water and pink clouds reflecting each other. On the left, the sun had just risen, and the city's silhouette stood clear in the morning light, drawing Cleveland's skyline.",
    "▲克城天际线 @ Arsenan": "▲ Cleveland skyline @ Arsenan",
    "▲人群 @ 摄影师": "▲ Runners @ photographer",
    "跨过高架，来到滨水公园，这时，天已经亮了，我感觉状态很好，能量胶也给得很足。": "After crossing the elevated section, we reached the waterfront park. By then it was daylight. I felt good, and the energy gels were plentiful.",
    "▲下了高架桥 @ Arsenan": "▲ Coming off the overpass @ Arsenan",
    "跑过公园，这会儿已经来到了湖边的居民区，小区居民不论是大人还是小孩都会出来给我们加油，还有各种私补。": "After the park, we entered a lakeside residential area. Residents, adults and kids alike, came out to cheer for us, and there were all kinds of unofficial aid.",
    "▲1/4折返 @ Arsenan": "▲ Quarter-way turnaround @ Arsenan",
    "这段路不宽，可以近距离感受克城居民的热情。居民区的尽头，大家折返回程，这时大概跑了四分之一的路程。": "The road was not wide, so we could feel the enthusiasm of Cleveland residents up close. At the end of the neighborhood, everyone turned back. By then we had run roughly a quarter of the course.",
    "▲返程隧道 @ Arsenan": "▲ Return tunnel @ Arsenan",
    "回去的路程和来的时候差不多，因为是折返，其实并没有太多的新鲜感。直到我跑回到湖边的蓝色高架，这回换了个角度看市区，真的大不相同。": "The return was almost the same as the way out. Because it was an out-and-back, there was not much novelty. But when I ran back to the blue overpass by the lake, the downtown view from the other angle felt completely different.",
    "▲蓝色大桥 @ Arsenan": "▲ Blue bridge @ Arsenan",
    "▲跑回市区 @ Arsenan": "▲ Running back toward downtown @ Arsenan",
    "一眼望去，城市的硬朗和工业风尽数呈现，建筑丛林前的凯霍加河漫漫流淌，它似乎早已褪去了往日的工业痕迹，取而代之的是几只悠闲的小船。": "At a glance, the city's hard-edged industrial feel was fully on display. In front of the concrete-and-steel forest, the Cuyahoga River flowed slowly, as if it had already shed its old industrial traces and replaced them with a few leisurely boats.",
    "如果不是马拉松，可真的难有这样的视角观赏克利夫兰。我们过了大桥跑回城区，然后折返，自此开启了后半程的旅途。": "Without the marathon, it would be hard to see Cleveland from this kind of angle. We crossed the bridge back into the city, then turned around again, beginning the second half of the journey.",
    "▲接近20k @ Arsenan": "▲ Near 20K @ Arsenan",
    "后半程跑者明显少了很多，并且风景和第一趟类似，也就没了拍照的新鲜感，这样反而可以更加专注于跑步本身。": "There were noticeably fewer runners in the second half, and the scenery was similar to the first pass, so the urge to take photos faded. That actually made it easier to focus on the running itself.",
    "▲回程 @ Arsenan": "▲ On the way back @ Arsenan",
    "我在downtown拿了一堆能量胶，就是觉得“能量胶在手，心里不慌”。它也确实管用，每遇到一个水站我就补一条，效果还真不错，至少大大延缓了我撞墙的时间。": "I grabbed a pile of gels downtown, mostly because having gels in hand made me feel calm. They really worked. At every aid station I took another one, and the effect was pretty good, at least delaying the wall by quite a bit.",
    "后半程我又在居民区拿了个香蕉，终于是抗过了最艰难的时刻。过了这段撞墙期，也就没那么辛苦了，可以悠闲的享受最后的距离。": "In the second half, I also grabbed a banana in the residential area and finally got through the hardest stretch. Once the wall passed, it was not so painful anymore, and I could enjoy the final miles more calmly.",
    "▲回程 @ 摄影师": "▲ On the return @ photographer",
    "不到五个小时，完赛了克利夫兰，算是我近期最好的成绩了，因为来美国后变得真的很菜。": "I finished Cleveland in under five hours. That counted as my best recent result, because after coming to the U.S. I had honestly become pretty weak.",
    "▲完赛 @ 摄影师": "▲ Finish @ photographer",
    "▲完赛 @ Arsenan": "▲ Finish @ Arsenan",
    "47在终点可等了半天了，还拍下了我冲过终点后的英姿。": "47 had been waiting at the finish for ages and even captured my heroic look after I crossed the line.",
    "▲完赛 @ 47": "▲ Finish @ 47",
    "▲奖牌 @ Arsenan": "▲ Medal @ Arsenan",
    "克利夫兰的奖牌真的很漂亮，镂空的设计加上金属的质感，很工业风，这很克利夫兰。": "The Cleveland medal was genuinely beautiful. The cutout design and metallic texture had a strong industrial feel, which felt very Cleveland.",
    "戴着奖牌在公共广场拍了很多照片，起跑的时候由于天太黑，没看清它的全貌，这会儿才发现，原来Public Square居然这么精致。": "Wearing the medal, I took a lot of photos in Public Square. At the start it had been too dark to see the place clearly. Only now did I realize how refined Public Square actually was.",
    "▲Public Square @ Arsenan": "▲ Public Square @ Arsenan",
    "跑完后我去Planet Fitness洗了个澡，PF这个全美连锁的健身房可真的太方便了，相比于芝加哥，克利夫兰的设施明显更棒一些。": "After the race, I went to Planet Fitness for a shower. PF, as a nationwide chain, is truly convenient. Compared with Chicago, the Cleveland location was clearly nicer.",
    "Refresh了一下，也要回程了，返回Louisville是接近六个小时的旅程。": "After freshening up, it was time to head back. The drive to Louisville was nearly six hours.",
    "这一路上，我们穿越了俄亥俄的暴雨，又在雨过天晴的辛辛那提吃了一顿Chinese buffet，最后平稳抵达。": "On the way, we drove through heavy Ohio rain, then ate a Chinese buffet in Cincinnati after the sky cleared, and finally arrived safely.",
    "回想这几天，还真是个风尘仆仆的周末，选择用自驾的方式穿越俄亥俄州，确实有点匆忙。": "Looking back on those few days, it really was a dusty, road-worn weekend. Choosing to drive across Ohio was definitely a bit rushed.",
    "虽然有点赶，但这42.195给我带来的满足感却是无以伦比的。": "It was hurried, but the satisfaction that 42.195 brought me was unmatched.",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
}


SKIP_TEXTS = {"继续观看", "★", "0/0"}
SECTION_HEADINGS = {
    "前言",
    "后记",
    "01",
    "02",
    "03",
    "悲情克利夫兰",
    "摇滚乐的故乡",
    "骑士队主场",
    "克利夫兰马拉松",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1500


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def extract_article(path: Path, article: str):
    doc = html.fromstring(path.read_text(encoding="utf-8", errors="replace"))
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events = []
    seen_text = set()
    for el in root.iter():
        if el.tag == "img":
            src = el.get("src") or ""
            if re.search(r"_files/640(\(|$)", src):
                source = (path.parent / src.replace("./", "")).resolve()
                events.append({"type": "image", "source": source, "article": article})
        elif el.tag in ("p", "section"):
            if has_desc_leaf_container(el):
                continue
            text = norm("".join(el.itertext()))
            if (
                not text
                or text in SKIP_TEXTS
                or text in seen_text
                or is_styleish(text)
                or "Your browser does not support video tags" in text
            ):
                continue
            seen_text.add(text)
            events.append({"type": "text", "text": text, "article": article})
    return events


def extract_story():
    city_events = extract_article(CITY_HTML, "city")
    race_events = extract_article(RACE_HTML, "race")
    return city_events, race_events


def font(size: int, bold: bool = False):
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def copy_story_images(all_events):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()
    image_index = 0
    for event in all_events:
        if event["type"] != "image":
            continue
        image_index += 1
        out_name = f"img-{image_index:03d}.webp"
        out_path = OUT_IMG_DIR / out_name
        with Image.open(event["source"]) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.save(out_path, "WEBP", quality=88, method=6)
        event["out"] = out_name
    return image_index


def translate(text: str) -> str:
    if text not in TRANSLATIONS:
        raise KeyError(f"Missing translation for: {text}")
    return TRANSLATIONS[text]


def render_text(original: str, lang: str) -> str:
    text = original if lang == "zh" else translate(original)
    if original in SECTION_HEADINGS:
        tag = "h2" if original not in {"01", "02", "03"} else "h3"
        return f"<{tag}>{escape(text)}</{tag}>"
    if original in {"- 本文完 -"}:
        return f'<p class="end-mark">{escape(text)}</p>'
    if original.startswith("丨") or original.startswith("- ") or original in {
        "詹姆斯，摇滚乐",
        "从黑夜跑到白昼",
    }:
        return f'<p class="story-kicker-line">{escape(text)}</p>'
    return f"<p>{escape(text)}</p>"


def render_events(events, lang: str, image_prefix: str, alt_prefix: str) -> str:
    output = []
    for event in events:
        if event["type"] == "image":
            number = event["out"].split("-")[1].split(".")[0]
            output.append(
                f'<figure><img src="{image_prefix}{event["out"]}" '
                f'alt="{escape(alt_prefix)} {number}" loading="lazy" decoding="async"></figure>'
            )
            continue

        original = event["text"]
        translated = original if lang == "zh" else translate(original)
        if is_caption(original):
            caption = escape(translated)
            if output and output[-1].endswith("</figure>") and "<figcaption>" not in output[-1]:
                output[-1] = output[-1].replace("</figure>", f"<figcaption>{caption}</figcaption></figure>")
            else:
                output.append(f'<p class="caption-line">{caption}</p>')
            continue
        output.append(render_text(original, lang))
    return "\n".join(output)


def engagement_block(lang: str) -> str:
    page_key = (
        "run50-cleveland-marathon-zh"
        if lang == "zh"
        else "run50-cleveland-marathon-en"
    )
    if lang == "zh":
        return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="zh-CN" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">留言 / 阅读</p>
        <h2>跑完也说两句</h2>
        <p class="zz-engagement-note">不用登录，留下名字就可以评论。新评论会直接显示。</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>阅读</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-cleveland-zh" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>评论加载中...</p>
      </div>
    </div>
  </section>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-cleveland-en" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def story_page(lang: str, city_article: str, race_article: str) -> str:
    zh = lang == "zh"
    title = TITLE_ZH if zh else TITLE_EN
    desc = (
        "城市篇与比赛篇合并：摇滚名人堂、骑士主场、伊利湖和清晨冷风中的克利夫兰马拉松。"
        if zh
        else "A complete two-part Cleveland story: Rock Hall, Cavaliers, Lake Erie, and a cold dawn Cleveland Marathon."
    )
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/cleveland-marathon.html">English</a><a href="../../facebook/cleveland-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/cleveland-marathon.html">中文</a><a href="../../facebook/cleveland-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>克利夫兰 · 俄亥俄</span><span>2021.10.24</span><span>Run50 #2</span><span>城市篇 + 比赛篇</span>'
        if zh
        else '<span>Cleveland, Ohio</span><span>Oct 24, 2021</span><span>Run50 #2</span><span>City story + race story</span>'
    )
    city_heading = "城市篇｜悲情克利夫兰，摇滚乐的故乡" if zh else "City Story | Melancholy Cleveland, birthplace of rock and roll"
    race_heading = "比赛篇｜克利夫兰，燃情42.195" if zh else "Race Story | Cleveland, fired up for 42.195"
    lang_attr = "zh-CN" if zh else "en"
    canonical = (
        f"{SITE}/run50/stories/chinese/{SLUG}.html"
        if zh
        else f"{SITE}/run50/stories/english/{SLUG}.html"
    )
    return f"""<!doctype html>
<html lang="{lang_attr}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-cleveland-marathon-icons.png?v={VERSION}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-cleveland-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>
    :root {{ --bg:#edf3f7; --paper:#fff; --ink:#20242b; --muted:#667085; --line:#d0dfe8; --accent:#0b67c2; --soft:#f8fbfd; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter, "Segoe UI", Arial, "Microsoft YaHei", sans-serif; line-height:1.78; }}
    a {{ color:inherit; }}
    .nav {{ position:sticky; top:0; z-index:10; display:flex; gap:14px; flex-wrap:wrap; justify-content:center; padding:13px 18px; background:rgba(237,243,247,.92); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }}
    .nav a {{ text-decoration:none; color:#475467; font-size:14px; font-weight:800; }}
    .hero {{ max-width:1120px; margin:0 auto; padding:54px 20px 20px; }}
    .hero-card {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(260px,430px); gap:28px; align-items:center; }}
    .eyebrow {{ margin:0 0 12px; color:var(--accent); text-transform:uppercase; letter-spacing:.08em; font-size:13px; font-weight:900; }}
    h1 {{ margin:0; font-family:Georgia, "Times New Roman", serif; font-size:clamp(34px,5vw,64px); line-height:1.05; letter-spacing:0; }}
    .dek {{ margin:18px 0 0; color:#475467; font-size:18px; max-width:760px; }}
    .cover {{ width:100%; border:1px solid var(--line); border-radius:8px; box-shadow:0 24px 60px rgba(15,23,42,.13); background:#fff; }}
    .meta-row {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:22px; }}
    .meta-row span {{ border:1px solid var(--line); background:rgba(255,255,255,.78); color:#475467; padding:7px 11px; border-radius:999px; font-size:13px; font-weight:800; }}
    main {{ max-width:860px; margin:0 auto; padding:20px 20px 64px; }}
    .part-label {{ margin:52px 0 20px; padding-top:26px; border-top:1px solid var(--line); color:var(--accent); font-size:15px; font-weight:900; letter-spacing:.04em; text-transform:uppercase; }}
    article {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,46px); box-shadow:0 18px 50px rgba(15,23,42,.08); }}
    article + article {{ margin-top:34px; }}
    article p {{ margin:0 0 18px; font-size:17px; }}
    article h2 {{ margin:34px 0 16px; font-size:26px; line-height:1.25; }}
    article h3 {{ margin:30px 0 10px; color:var(--accent); font-size:18px; }}
    .story-kicker-line {{ color:#6b7a86; font-weight:900; text-align:center; }}
    .end-mark {{ text-align:center; color:#6b7a86; font-weight:800; }}
    figure {{ margin:28px 0; }}
    figure img {{ display:block; width:100%; height:auto; border-radius:8px; border:1px solid #e5edf3; background:#f8fafc; }}
    figcaption, .caption-line {{ margin-top:8px; color:#667085; text-align:center; font-size:13px; line-height:1.5; }}
    @media (max-width:760px) {{
      .hero-card {{ grid-template-columns:1fr; }}
      .hero {{ padding-top:36px; }}
      .cover {{ max-width:520px; }}
      article {{ padding:22px; }}
      article p {{ font-size:16px; }}
    }}
  </style>
</head>
<body>
  <nav class="nav">{nav}</nav>
  <header class="hero">
    <div class="hero-card">
      <div>
        <p class="eyebrow">Run50 #2 · Ohio</p>
        <h1>{escape(title)}</h1>
        <p class="dek">{escape(desc)}</p>
        <div class="meta-row">{meta}</div>
      </div>
      <img class="cover" src="../../../assets/thumb-run50-cleveland-marathon-icons.svg?v={VERSION}" alt="Cleveland Marathon icon cover">
    </div>
  </header>
  <main>
    <p class="part-label">{escape(city_heading)}</p>
    <article>
{city_article}
    </article>
    <p class="part-label">{escape(race_heading)}</p>
    <article>
{race_article}
    </article>
  </main>
{engagement_block(lang)}
</body>
</html>
"""


def facebook_engagement() -> str:
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-cleveland-marathon-facebook-en">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-cleveland-fb" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def facebook_page(race_article: str, city_article: str) -> str:
    desc = "Race day first, then the Cleveland weekend: Rock Hall, Cavaliers, Lake Erie, and the industrial city that made the marathon feel unmistakably Ohio."
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-cleveland-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-cleveland-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>
    :root {{ --bg:#f5f7fa; --paper:#fff; --ink:#101828; --muted:#667085; --line:#d0dfe8; --accent:#0b67c2; --blue:#0b67c2; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter, "Segoe UI", Arial, sans-serif; line-height:1.72; }}
    a {{ color:inherit; }}
    .topbar {{ background:#0b1018; color:#fff; border-bottom:4px solid var(--accent); }}
    .topbar-inner {{ max-width:1180px; margin:0 auto; padding:14px 18px; display:flex; justify-content:space-between; gap:14px; align-items:center; flex-wrap:wrap; }}
    .brand {{ font-weight:950; letter-spacing:.08em; text-transform:uppercase; }}
    .brand span {{ color:#8ab4f8; }}
    .topbar nav {{ display:flex; gap:14px; flex-wrap:wrap; }}
    .topbar a {{ color:#dbe7ff; text-decoration:none; font-size:13px; font-weight:800; }}
    .hero {{ background:#fff; border-bottom:1px solid var(--line); }}
    .hero-inner {{ max-width:1180px; margin:0 auto; padding:42px 18px 30px; display:grid; grid-template-columns:minmax(0,1.08fr) minmax(280px,.72fr); gap:30px; align-items:center; }}
    .section-label {{ margin:0 0 12px; color:var(--accent); text-transform:uppercase; letter-spacing:.08em; font-size:13px; font-weight:950; }}
    h1 {{ margin:0; font-family:Georgia, "Times New Roman", serif; font-size:clamp(36px,5.2vw,72px); line-height:1; letter-spacing:0; }}
    .dek {{ max-width:780px; margin:18px 0 0; color:#475467; font-size:19px; }}
    .hero img {{ width:100%; border:1px solid var(--line); border-radius:8px; box-shadow:0 28px 70px rgba(15,23,42,.16); background:#fff; }}
    .meta-row {{ margin-top:22px; display:flex; gap:10px; flex-wrap:wrap; }}
    .meta-row span {{ background:#eef5fb; border:1px solid #cddfec; color:#344054; border-radius:999px; padding:7px 11px; font-size:13px; font-weight:850; }}
    .layout {{ max-width:1180px; margin:0 auto; padding:32px 18px 66px; display:grid; grid-template-columns:minmax(0,780px) minmax(230px,1fr); gap:32px; align-items:start; }}
    article {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,44px); box-shadow:0 20px 52px rgba(15,23,42,.08); }}
    article p {{ margin:0 0 18px; font-size:17px; }}
    article h2 {{ margin:36px 0 16px; font-size:28px; line-height:1.22; }}
    article h3 {{ margin:30px 0 12px; color:var(--accent); font-size:18px; }}
    .story-kicker-line {{ color:#667085; font-weight:900; text-align:center; }}
    .end-mark {{ text-align:center; color:#667085; font-weight:800; }}
    figure {{ margin:28px 0; }}
    figure img {{ display:block; width:100%; height:auto; border-radius:8px; border:1px solid #e5edf3; }}
    figcaption, .caption-line {{ margin-top:8px; color:#667085; text-align:center; font-size:13px; line-height:1.45; }}
    .rail {{ position:sticky; top:18px; display:grid; gap:16px; }}
    .brief {{ background:#101828; color:#fff; border-radius:8px; padding:18px; }}
    .brief h2 {{ margin:0 0 12px; font-size:18px; }}
    .brief dl {{ display:grid; gap:12px; margin:0; }}
    .brief dt {{ color:#9ec5ff; font-size:12px; font-weight:900; text-transform:uppercase; letter-spacing:.08em; }}
    .brief dd {{ margin:2px 0 0; color:#eef4ff; font-size:14px; line-height:1.45; }}
    .related {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px; }}
    .related a {{ display:block; color:#0b67c2; font-weight:900; text-decoration:none; margin-top:10px; }}
    .transition {{ margin:42px 0 22px; padding-top:24px; border-top:1px solid var(--line); color:#475467; font-weight:850; }}
    @media (max-width:860px) {{
      .hero-inner, .layout {{ grid-template-columns:1fr; }}
      .rail {{ position:static; }}
      article p {{ font-size:16px; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">Run50 <span>Facebook</span></div>
      <nav><a href="../hub.html">Run50 Hub</a><a href="../stories/english/cleveland-marathon.html">English</a><a href="../stories/chinese/cleveland-marathon.html">中文</a></nav>
    </div>
  </header>
  <section class="hero">
    <div class="hero-inner">
      <div>
        <p class="section-label">World / USA / Marathon</p>
        <h1>{escape(TITLE_FB)}</h1>
        <p class="dek">On October 24, 2021, Cleveland turned State 2 of Run50 into a cold dawn run: Tower City in the dark, Lake Erie at sunrise, industrial bridges, a long out-and-back, and one medal that looked exactly like the city felt.</p>
        <div class="meta-row"><span>Cleveland, Ohio</span><span>{DATE_EN}</span><span>Run50 #2</span><span>Full story</span></div>
      </div>
      <img src="../../assets/thumb-run50-cleveland-marathon-icons.svg?v={VERSION}" alt="Cleveland Marathon icon cover">
    </div>
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race day</p>
      <p>The marathon is the spine of this Cleveland weekend. The city story matters, too, but the reason I drove across Ohio was this: a pandemic-postponed race that started before sunrise and slowly revealed Cleveland mile by mile.</p>
{race_article}
      <p class="transition">Before the cold start and the medal photos, Cleveland had already introduced itself through rock and roll, Lake Erie, and a Cavaliers night that made the city feel less tragic and more alive.</p>
      <p class="section-label">The city around the race</p>
{city_article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{RACE_NAME}</dd></div>
          <div><dt>Date</dt><dd>{DATE_EN}</dd></div>
          <div><dt>State</dt><dd>Ohio · Run50 #2</dd></div>
          <div><dt>Route memory</dt><dd>Dark start, Lake Erie sunrise, industrial bridges, and a gritty downtown finish.</dd></div>
        </dl>
      </div>
      <div class="related">
        <strong>More versions</strong>
        <a href="../stories/english/cleveland-marathon.html">Read in original order</a>
        <a href="../stories/chinese/cleveland-marathon.html">中文原文整理版</a>
      </div>
    </aside>
  </main>
{facebook_engagement()}
</body>
</html>
"""


def draw_badge(draw, x, y, w, h):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((x + 30, y + 48), "Run50 #02", fill="#20242b", font=font(38, True))
    draw.text((x + 30, y + 112), "OHIO", fill="#0b67c2", font=font(54, True))


def draw_cleveland_scene(draw, height: int):
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    width = int(1200 * scale)
    draw.rectangle([0, int(250 * scale), width, height], fill="#b7dce8")
    draw.rectangle([0, int(470 * scale), width, height], fill="#4d8ca4")
    draw.rectangle([0, int(560 * scale), width, height], fill="#2f6f88")
    draw.polygon([p(0, 470), p(160, 430), p(340, 455), p(520, 418), p(720, 460), p(920, 420), p(1200, 455), p(1200, 560), p(0, 560)], fill="#7fb069")

    # Rock & Roll Hall of Fame inspired glass pyramid.
    draw.polygon([p(135, 560), p(335, 315), p(535, 560)], fill="#d7eef4", outline="#20242b")
    draw.polygon([p(335, 315), p(420, 560), p(535, 560)], fill="#b2d6e2", outline="#20242b")
    for x in (190, 245, 300, 355, 410, 465):
        draw.line([p(335, 315), p(x, 560)], fill="#6f93a0", width=max(2, int(3 * scale)))
    for y in (390, 450, 510):
        draw.line([p(175, y), p(495, y)], fill="#6f93a0", width=max(2, int(3 * scale)))

    # Downtown skyline and Terminal Tower.
    skyline = [
        (610, 380, 52, 160, "#374151"),
        (672, 340, 54, 200, "#2f3a46"),
        (744, 300, 58, 240, "#26313d"),
        (820, 390, 74, 150, "#405163"),
        (915, 360, 70, 180, "#2f3a46"),
        (1015, 420, 62, 120, "#44586a"),
    ]
    for x, y, w, h, color in skyline:
        draw.rectangle([int(x * scale), int(y * scale), int((x + w) * scale), int((y + h) * scale)], fill=color)
        for wy in range(y + 20, y + h - 10, 28):
            draw.line([p(x + 10, wy), p(x + w - 10, wy)], fill="#8fb2c5", width=max(1, int(2 * scale)))
    draw.polygon([p(744, 300), p(773, 250), p(802, 300)], fill="#26313d")
    draw.rectangle([int(770 * scale), int(224 * scale), int(778 * scale), int(252 * scale)], fill="#26313d")

    # Guitar and basketball signals.
    draw.line([p(160, 610), p(305, 470)], fill="#20242b", width=max(6, int(12 * scale)))
    draw.ellipse([int(95 * scale), int(580 * scale), int(185 * scale), int(665 * scale)], fill="#f5b840", outline="#20242b", width=max(3, int(6 * scale)))
    draw.ellipse([int(112 * scale), int(598 * scale), int(168 * scale), int(650 * scale)], outline="#20242b", width=max(2, int(4 * scale)))
    draw.ellipse([int(990 * scale), int(515 * scale), int(1090 * scale), int(615 * scale)], fill="#d97706", outline="#20242b", width=max(3, int(6 * scale)))
    draw.arc([int(990 * scale), int(515 * scale), int(1090 * scale), int(615 * scale)], 90, 270, fill="#20242b", width=max(2, int(4 * scale)))
    draw.arc([int(990 * scale), int(515 * scale), int(1090 * scale), int(615 * scale)], -90, 90, fill="#20242b", width=max(2, int(4 * scale)))
    draw.line([p(1040, 515), p(1040, 615)], fill="#20242b", width=max(2, int(4 * scale)))
    draw.line([p(990, 565), p(1090, 565)], fill="#20242b", width=max(2, int(4 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(image)
    draw_cleveland_scene(draw, 630)
    draw.rectangle([0, 0, 1200, 242], fill="#edf3f7")
    draw.text((64, 66), "CLEVELAND", fill="#20242b", font=font(70, True))
    draw.text((68, 142), "LAKE ERIE · ROCK HALL · DAWN MARATHON", fill="#536a79", font=font(25, True))
    draw_badge(draw, 758, 62, 364, 166)
    image.save(OG_PATH, "PNG")


def generate_cover_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
  <title id="title">Cleveland Marathon Run50 icon cover</title>
  <desc id="desc">Cleveland icon cover with Lake Erie, Rock Hall pyramid, skyline, guitar, basketball, and Ohio Run50 badge.</desc>
  <rect width="1200" height="750" fill="#edf3f7"/>
  <rect y="300" width="1200" height="450" fill="#b7dce8"/>
  <rect y="560" width="1200" height="190" fill="#4d8ca4"/>
  <rect y="665" width="1200" height="85" fill="#2f6f88"/>
  <path d="M0 560 L160 510 L340 540 L520 496 L720 548 L920 504 L1200 540 V665 H0Z" fill="#7fb069"/>
  <text x="64" y="112" fill="#20242b" font-family="Arial, Helvetica, sans-serif" font-size="70" font-weight="900">CLEVELAND</text>
  <text x="68" y="160" fill="#536a79" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="800">LAKE ERIE · ROCK HALL · DAWN MARATHON</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #02</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="#0b67c2">OHIO</text>
  <path d="M135 665 L335 374 L535 665 Z" fill="#d7eef4" stroke="#20242b" stroke-width="7"/>
  <path d="M335 374 L420 665 L535 665 Z" fill="#b2d6e2" stroke="#20242b" stroke-width="5"/>
  <g stroke="#6f93a0" stroke-width="4">
    <path d="M335 374 L190 665 M335 374 L245 665 M335 374 L300 665 M335 374 L355 665 M335 374 L410 665 M335 374 L465 665"/>
    <path d="M175 465 H495 M175 535 H495 M175 605 H495"/>
  </g>
  <g fill="#26313d">
    <rect x="610" y="452" width="52" height="190"/><rect x="672" y="404" width="54" height="238"/>
    <rect x="744" y="356" width="58" height="286"/><path d="M744 356 L773 296 L802 356Z"/><rect x="770" y="266" width="8" height="34"/>
    <rect x="820" y="464" width="74" height="178"/><rect x="915" y="428" width="70" height="214"/><rect x="1015" y="500" width="62" height="142"/>
  </g>
  <g stroke="#8fb2c5" stroke-width="3" opacity=".75">
    <path d="M620 478 H652 M682 430 H716 M754 386 H792 M832 492 H884 M925 456 H975 M1025 528 H1067"/>
  </g>
  <path d="M160 724 L305 558" stroke="#20242b" stroke-width="12" stroke-linecap="round"/>
  <circle cx="140" cy="692" r="52" fill="#f5b840" stroke="#20242b" stroke-width="7"/>
  <circle cx="140" cy="692" r="30" fill="none" stroke="#20242b" stroke-width="4"/>
  <circle cx="1040" cy="632" r="55" fill="#d97706" stroke="#20242b" stroke-width="7"/>
  <path d="M1040 577 V687 M985 632 H1095" stroke="#20242b" stroke-width="5"/>
  <path d="M1000 590 Q1040 632 1000 674 M1080 590 Q1040 632 1080 674" fill="none" stroke="#20242b" stroke-width="5"/>
</svg>
"""
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source_path = next(p for p in (SOURCE_BASE / "克利夫兰，燃情42.195_files").iterdir() if p.name == "640(31)")
    with Image.open(source_path) as source:
        source = ImageOps.exif_transpose(source).convert("RGB")
        background = ImageOps.fit(source, (1200, 750), method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(26))
        background = Image.blend(background, Image.new("RGB", background.size, "#162f4d"), 0.28)
        foreground = ImageOps.contain(source, (1110, 720), method=Image.Resampling.LANCZOS)
    canvas = background.convert("RGBA")
    x = (canvas.width - foreground.width) // 2
    y = (canvas.height - foreground.height) // 2
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [x + 12, y + 16, x + foreground.width + 12, y + foreground.height + 16],
        radius=18,
        fill=(3, 12, 22, 105),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))
    canvas.paste(foreground, (x, y))
    canvas.convert("RGB").save(MEDAL_COVER_PATH, "JPEG", quality=92, optimize=True)


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(
        rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>',
        re.S,
    )
    return pattern.sub("", text)


def clean_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def insert_after_card(text: str, target_href: str, card: str, fallback_marker: str) -> str:
    pattern = re.compile(
        rf'(\n\s*<a class="story-card [^"]+" href="{re.escape(target_href)}">.*?</a>\s*)',
        re.S,
    )
    if pattern.search(text):
        return pattern.sub(lambda match: match.group(1) + "\n" + card, text, count=1)
    return text.replace(fallback_marker, fallback_marker + "\n" + card, 1)


def update_story_indexes():
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="克利夫兰马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">俄亥俄克利夫兰 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第2州｜克利夫兰马拉松</h2>
          <p class="story-desc">城市篇与比赛篇合并：摇滚名人堂、骑士主场、伊利湖晨光、工业风高架和从黑夜跑到白昼的42.195公里。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for Cleveland Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">Ohio · Cleveland · {DATE_ZH}</div>
          <h2>Cleveland Marathon: from night into daylight</h2>
          <p>A two-part Cleveland weekend: Rock Hall, Cavaliers, Lake Erie, then a cold dawn marathon through bridges, skyline, and industrial grit.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Cleveland gave me a cold 26.2-mile run from night into daylight</h2>
        <p>Race date: October 24, 2021. State 2 of Run50 started in the dark near Tower City, crossed Lake Erie light and industrial bridges, and ended with a medal that looked exactly like Cleveland felt.</p>
        <div class="meta"><span>Cleveland, OH</span><span>Run50 #2</span><span>Rock Hall weekend</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Cleveland Marathon cover">
    </a>
"""

    text = remove_existing_card(zh_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./louisville-marathon.html", zh_card, '<section class="story-grid" aria-label="中文故事列表">')
    text = text.replace("'WV-亨廷顿': 'west-virginia-marathon.html'", "'WV-亨廷顿': 'west-virginia-marathon.html',\n      'OH-克利夫兰': 'cleveland-marathon.html'")
    zh_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(en_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./louisville-marathon.html", en_card, '<section class="story-grid" aria-label="English story list">')
    text = text.replace("'WV-Huntington': 'west-virginia-marathon.html'", "'WV-Huntington': 'west-virginia-marathon.html',\n      'OH-Cleveland': 'cleveland-marathon.html'")
    en_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./louisville-marathon.html", fb_card, '<main class="shell">')
    fb_path.write_text(clean_text(text), encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- Ohio Run50 story -->.*?<!-- /Ohio Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- Ohio Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="Cleveland gave me a cold 26.2-mile run from night into daylight">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Cleveland Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">Cleveland gave me a cold 26.2-mile run from night into daylight</a>
            <p class="video-sub">Cleveland, OH &middot; Oct 24, 2021</p>
          </div>
        </div>
      </article>
      <!-- /Ohio Run50 story -->

"""
    if "<!-- /Kentucky Run50 story -->" in text:
        text = text.replace("      <!-- /Kentucky Run50 story -->\n", "      <!-- /Kentucky Run50 story -->\n" + card, 1)
    else:
        text = text.replace("      <!-- Water Header -->", card + "      <!-- Water Header -->", 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*'OH':\[\{city:'Cleveland'.*?\}\],\n", "", text, flags=re.M)
    text = text.replace(
        "  'IL':[{city:'Chicago',date:'Oct 2024',story:'stories/english/chicago-marathon.html',fb:'facebook/chicago-marathon.html'}],",
        "  'OH':[{city:'Cleveland',date:'Oct 24, 2021',story:'stories/english/cleveland-marathon.html',fb:'facebook/cleveland-marathon.html'}],\n"
        "  'IL':[{city:'Chicago',date:'Oct 2024',story:'stories/english/chicago-marathon.html',fb:'facebook/chicago-marathon.html'}],",
        1,
    )
    text = re.sub(
        r"\n\s*<!-- Ohio Cleveland story dot -->.*?<!-- /Ohio Cleveland story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    dot = """
    <!-- Ohio Cleveland story dot -->
    <circle cx="241" cy="123" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="241" cy="123" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Cleveland, OH" data-date="Oct 24, 2021" data-story="stories/english/cleveland-marathon.html"/>
    <!-- /Ohio Cleveland story dot -->
"""
    text = text.replace("    <!-- /Kentucky Louisville story dot -->\n", "    <!-- /Kentucky Louisville story dot -->\n" + dot, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 13 stories", " 14 stories")
    text = text.replace("<strong>13</strong> stories", "<strong>14</strong> stories")
    path.write_text(clean_text(text), encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        "run50-cleveland-marathon-facebook-en",
        "run50-cleveland-marathon-en",
        "run50-cleveland-marathon-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-louisville-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(clean_text(text), encoding="utf-8")


def main():
    city_events, race_events = extract_story()
    all_events = city_events + race_events
    image_count = copy_story_images(all_events)
    city_zh = render_events(city_events, "zh", "Run50-Cleveland-Marathon-clean_files/", "克利夫兰照片")
    race_zh = render_events(race_events, "zh", "Run50-Cleveland-Marathon-clean_files/", "克利夫兰马拉松照片")
    city_en = render_events(city_events, "en", "../chinese/Run50-Cleveland-Marathon-clean_files/", "Cleveland photo")
    race_en = render_events(race_events, "en", "../chinese/Run50-Cleveland-Marathon-clean_files/", "Cleveland Marathon photo")
    city_fb = render_events(city_events, "en", "../stories/chinese/Run50-Cleveland-Marathon-clean_files/", "Cleveland photo")
    race_fb = render_events(race_events, "en", "../stories/chinese/Run50-Cleveland-Marathon-clean_files/", "Cleveland Marathon photo")

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(
        story_page("zh", city_zh, race_zh), encoding="utf-8"
    )
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(
        story_page("en", city_en, race_en), encoding="utf-8"
    )
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(
        facebook_page(race_fb, city_fb), encoding="utf-8"
    )

    generate_cover_png()
    generate_cover_svg()
    generate_medal_cover()
    update_story_indexes()
    update_root_home()
    update_hub()
    update_landing_counts()
    update_supabase_sql()

    text_count = sum(event["type"] == "text" for event in all_events)
    print(
        f"Built Ohio story with {image_count} images, "
        f"{text_count} text blocks, and {len(all_events)} source events."
    )


if __name__ == "__main__":
    main()
