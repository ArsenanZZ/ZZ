from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2021-State-03-NY"
)
CITY_HTML = next(p for p in SOURCE_BASE.glob("*.html") if "赛博朋克" in p.name)
RACE_HTML = next(p for p in SOURCE_BASE.glob("*.html") if "纽约马拉松" in p.name)

SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "new-york-city-marathon"
VERSION = "20260615-3"
ENGAGEMENT_VERSION = "20260615"

OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-NewYorkCity-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-new-york-city-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-new-york-city-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-ny.jpg"

TITLE_ZH = "Run50 #第3州｜纽约：纽约马拉松｜50周年打卡"
TITLE_EN = "Run50 #3 | New York: Checking in at the 50th NYC Marathon"
TITLE_FB = "New York turned 26.2 miles into one enormous five-borough street party"
DATE_ZH = "2021.11.07"
DATE_EN = "Nov 7, 2021"
RACE_NAME = "50th TCS New York City Marathon"


TRANSLATIONS = {
    "丨NYC丨": "| NYC |",
    "50周年打卡：我的纽约马拉松": "Checking in at the 50th NYC Marathon",
    "▲ NYC Marathon by Arsenan": "▲ NYC Marathon by Arsenan",
    "- NYC Run -": "- NYC Run -",
    "第一个大满贯": "My first World Marathon Major",
    "前言": "Preface",
    "从鱼龙混杂的布鲁克林街区到世界中心曼哈顿，纽约就像一出掺杂着各种味道的小品剧。": "From the mixed-up neighborhoods of Brooklyn to Manhattan, the so-called center of the world, New York feels like a little stage sketch with every flavor thrown in.",
    "LOVE和HATE是对孪生儿，有多少人爱纽约，也会有多少人恨纽约， 而作为马拉松爱好者，却很少有人会对纽约马拉松说不。": "LOVE and HATE are twins. As many people as love New York, just as many probably hate it. But for marathon lovers, very few people can say no to the New York City Marathon.",
    "▲ Classic Marathon Finish @ LeRoy Neiman 1983": "▲ Classic Marathon Finish @ LeRoy Neiman 1983",
    "作为世界六大马拉松之一，没有哪一项比赛可以像纽约马拉松这样，吸引如此众多来自世界各地的跑者。": "As one of the six World Marathon Majors, no race draws runners from all over the world quite like New York.",
    "纽约作为疫情之初，全美最严重的城市，能够让纽马在跨越两年的疫情后重新归来，自然是意义非凡。": "New York was the hardest-hit city in America at the start of the pandemic, so seeing the marathon return after two pandemic years carried a special meaning.",
    "而我有幸以亲历者的身份参与其中，更是无比激动。": "And I was lucky enough to be there in person, which made it even more exciting.",
    "▲ NYC Marathon Finish @ MarathonFoto 2021": "▲ NYC Marathon Finish @ MarathonFoto 2021",
    "01": "01",
    "赛前领物": "Packet pickup",
    "马拉松的前一天，我们先是跑到了纽约35街的Jacob K. Javits会议中心领取跑步装备，纽约的防疫很严，会场门口也会有专门的志愿者检测大家是否打了疫苗。": "The day before the marathon, we first went to the Jacob K. Javits Convention Center on 35th Street to pick up the race gear. New York's COVID rules were strict, and volunteers at the entrance checked whether everyone had been vaccinated.",
    "▲ 领物路上 @ Arsenan": "▲ On the way to packet pickup @ Arsenan",
    "▲ 门口志愿者 @ Arsenan": "▲ Volunteers at the entrance @ Arsenan",
    "进到会场中心就可以很容易地找到领取号码簿的地点，志愿者还会特别仔细地讲解存包的细节和跑步日的行程。": "Once inside the convention center, it was easy to find bib pickup. The volunteers explained the bag-check details and race-day schedule very carefully.",
    "▲ NYC马博会 @ Arsenan": "▲ NYC Marathon Expo @ Arsenan",
    "▲ 领取号码薄 @ Arsenan": "▲ Picking up the bib @ Arsenan",
    "领完号码簿接着往前走，就到了T恤领取处，纽马的组委会很贴心，还专门开辟了一个区域，让大家试穿，然后可以选择最适合自己的尺码。": "After picking up the bib, we kept moving and reached the T-shirt area. The NYC Marathon organizers were thoughtful enough to set aside a fitting area, so runners could try things on and pick the size that worked best.",
    "整体领物流程十分高效，人也没有想象中多，基本10分钟就能搞定。": "The whole packet-pickup process was very efficient, and there were fewer people than I expected. It basically took ten minutes.",
    "然后就会进入50周年纽约马的logo纪念品跑步装备专卖区，很多衣服真的很吸引人，我也没忍住整了一件外套和两个帽子。": "After that came the 50th-anniversary NYC Marathon logo shop, full of souvenirs and running gear. A lot of the clothes were genuinely tempting, and I could not resist buying a jacket and two hats.",
    "本来我是想，回去后在和美国朋友跑步的时候拿出来秀一秀，但没想到这件外套和空顶帽却成了我跑纽约马的主装备。": "Originally I thought I would show them off later when running with American friends, but I did not expect that jacket and visor to become my main NYC Marathon outfit.",
    "结账的时候特别有意思，志愿者会问你是不是第一次跑马，如果是，他们会特别骄傲地大声广播：“我这里有一位第一次跑马的runner！” 然后就是全场的欢呼和掌声，这样的欢呼声此起起伏，也让身处其中的每个人，不由自主地嘴角上扬。": "Checkout was especially fun. Volunteers would ask whether it was your first marathon. If it was, they would proudly announce, \"We have a first-time marathon runner here!\" Then the whole place would cheer and clap. Those cheers kept rising around the room, and everyone inside could not help smiling.",
    "我说我是第一次跑纽约马，但也得到了这样的优待，有点受宠若惊。": "I said it was my first time running New York, and I somehow got the same treatment. I felt a little spoiled.",
    "▲ 中央公园 @ Arsenan": "▲ Central Park @ Arsenan",
    "▲中央公园 @ Arsenan": "▲ Central Park @ Arsenan",
    "想要存包的跑者需要下午到中央公园，那里可以提前存包，貌似还可以得到一件保暖披风。": "Runners who wanted to check a bag needed to go to Central Park that afternoon. You could drop off your bag in advance and apparently get a warm poncho too.",
    "虽然我没有存包的需求，但还是打算去转转，整个中央公园为了迎接这场大party，被装扮得氛围感满满，到处都是纽约马的logo，这也让我更加期待第二天的跑步。": "I did not need bag check, but I still wanted to walk around. Central Park was dressed up for this huge party, full of NYC Marathon logos everywhere, and it made me even more excited for the next day's run.",
    "02": "02",
    "漫长的等待": "The long wait",
    "跑步日的清晨，将会有33000多名来自世界各地的跑者涌向纽约湾畔的Verrazano Bridge，开始一段42.195公里的奇妙旅途。": "On race morning, more than 33,000 runners from around the world would head toward the Verrazzano Bridge by New York Bay and begin a wonderful 42.195-kilometer journey.",
    "▲ TS地铁站 @ Arsenan": "▲ Times Square subway station @ Arsenan",
    "▲TS地铁站 @ Arsenan": "▲ Times Square subway station @ Arsenan",
    "但从我们酒店所在的时代广场，到起点的斯坦顿岛，中间的路程挺波折的，要先地铁，再轮渡，最后大巴。但绝对不虚此行，因为风景真的很不错。": "But getting from our hotel near Times Square to the start on Staten Island was a whole process: subway first, then ferry, then bus. It was absolutely worth it, though, because the scenery was really good.",
    "▲ 跑者地铁 @ Arsenan": "▲ Runners on the subway @ Arsenan",
    "清晨的地铁站，已经聚集了很多乘客，不用细问，一看装备，就知道是跑马的，虽然大家来自不同的国家，有着不一样的信仰，但一照面，就会觉得亲切。": "The early-morning subway station was already full of passengers. No need to ask: one look at the gear and you knew they were marathon runners. Even though everyone came from different countries and had different beliefs, seeing each other instantly felt familiar.",
    "▲ 德国跑者 @ Arsenan": "▲ German runners @ Arsenan",
    "接着是去斯坦顿的轮渡，伴着朝阳出发，轮渡在水面上荡起涟漪，曼哈顿渐行渐远，没过多久，自由女神像出现在不远处，大家纷纷从船舱出来拍照。": "Next came the ferry to Staten Island. We set off with the morning sun, the ferry rippling across the water as Manhattan slowly drifted away. Before long, the Statue of Liberty appeared not far off, and everyone came out of the cabin to take photos.",
    "▲ 曼哈顿清晨 @ Arsenan": "▲ Manhattan morning @ Arsenan",
    "▲ 曼哈顿清晨 by Arsenan": "▲ Manhattan morning by Arsenan",
    "▲ 轮渡 @ Arsenan": "▲ Ferry @ Arsenan",
    "和夜晚的自由女神像相比，清晨的自由女神显得更加恬静，对于那些行行色匆匆的跑者们，这可能是他们唯一的一次机会看到自由女神，这个照面所带来的满足感可能远比想象中的强烈。": "Compared with the Statue of Liberty at night, the morning version felt much quieter. For those hurried runners, this might be their only chance to see her, and the satisfaction from that brief encounter was probably stronger than expected.",
    "▲ 自由女神 @ Arsenan": "▲ Statue of Liberty @ Arsenan",
    "▲自由女神 @ Arsenan": "▲ Statue of Liberty @ Arsenan",
    "我们的渡轮边还会一艘快艇护航，大家也会热情地和船员们打招呼，这样的礼遇温暖了纽约的早晨。": "A speedboat escorted our ferry, and everyone waved warmly to the crew. That little courtesy warmed up the New York morning.",
    "▲ 护航快艇 @ Arsenan": "▲ Escort boat @ Arsenan",
    "到岸后还需要乘坐大巴赶赴起点，也就是韦拉扎诺海峡大桥边，这边会有比较严格的安检，然后大家才可以进入跑者园区。": "After landing, we still had to take a bus to the start, near the Verrazzano-Narrows Bridge. There was fairly strict security there before runners could enter the village.",
    "▲ 安检 @ Arsenan": "▲ Security check @ Arsenan",
    "▲ 起点志愿者 @ Arsenan": "▲ Start-area volunteer @ Arsenan",
    "园区根据跑者的起跑时间分为不同的颜色区，我开始没有仔细研究规则，就一路跑到了蓝色起跑区，还蹭了一杯早晨的热咖啡。": "The village was divided into color zones based on start times. I had not studied the rules carefully at first, so I wandered all the way to the blue start area and even managed to get a cup of hot morning coffee.",
    "▲ 分区起跑 @ Arsenan": "▲ Start corrals @ Arsenan",
    "后来发现走错了，问了志愿者，才回到橙色区域，可惜这边并没有热咖啡，而且离起跑还有一个多小时。": "Later I realized I was in the wrong place. After asking a volunteer, I made my way back to the orange area. Unfortunately, there was no hot coffee there, and we still had more than an hour before the start.",
    "▲ 起点 @ Arsenan": "▲ Start area @ Arsenan",
    "对于大多数业余跑者来说，起点的等待是漫长的，并且真的挺冷的。": "For most amateur runners, waiting at the start is long, and it was genuinely cold.",
    "村上春树就曾经这样形容过11月的纽约马拉松：“从来不曾有过暖和的迹象。无论哪一次，肯定都是像魔女的心一样冰冷的星期日。”": "Haruki Murakami once described the New York City Marathon in November like this: \"There was never any sign of warmth. Every time, it was surely a Sunday as cold as a witch's heart.\"",
    "虽然漫长，但并不一定无聊，对于那些习惯了长跑的选手们，总可以乐在其中。": "The wait was long, but not necessarily boring. For runners used to long-distance running, there was always a way to enjoy it.",
    "因为起点温度很低，许多参赛者都会穿着很厚的衣服去起点。发枪前，他们都会将衣物遗弃。后来的纽马组织者会安排志愿者将这些衣物回收，捐助给当地需要救济的人们。光是2013年那届，就总共捐赠了26吨的衣物。": "Because the start area is so cold, many runners wear heavy clothes there. Before the gun, they leave those layers behind. The NYC Marathon later arranges volunteers to collect the clothing and donate it to people in need locally. In 2013 alone, the race donated 26 tons of clothing.",
    "▲ 收纳箱 @ Arsenan": "▲ Collection bins @ Arsenan",
    "▲ 橙色起点 @ Arsenan": "▲ Orange start @ Arsenan",
    "终于快到我们的起跑时间了，橙色区域的每个小起跑区这时对跑者开放，我也随着人流慢慢向大桥移动，期待了两年的纽约马拉松，终于要开始了。": "At last our start time was getting close. Each small corral in the orange area opened to runners, and I slowly moved with the crowd toward the bridge. After two years of waiting, the New York City Marathon was finally about to begin.",
    "▲ 起跑区 @ Arsenan": "▲ Start corral @ Arsenan",
    "03": "03",
    "我爱NYC马拉松": "I love the NYC Marathon",
    "马拉松是一道饕餮大餐，如何规划赛道对所有城市来说都是个大课题，纽约也不例外。如今的纽约马拉松早已不是几十年前绕着中央公园跑四圈的“无聊赛事”。为了庆祝独立宣言通过200周年，1976年开始，纽约马拉松的路线改为穿过纽约各区。": "A marathon is a feast, and designing the course is a major question for every city. New York is no exception. Today's NYC Marathon is no longer the \"boring race\" that looped four times around Central Park decades ago. To celebrate the 200th anniversary of the Declaration of Independence, the route changed in 1976 to run through New York's boroughs.",
    "▲ 2021我的纽约马拉松（第一视角） @ Arsenan": "▲ My 2021 NYC Marathon, first-person view @ Arsenan",
    "老友记里的中央公园、欲望都市里第五大道、所有关于纽约的影像回忆，纽约马拉松都会把NYC这些最精华的部分呈现出来：从纽约湾长而陡的韦拉扎诺桥Verrazano Bridge出发，选手们一出发便会经历上坡和桥震，然后一路北上，穿过布鲁克林区、长岛，跑进曼哈顿岛，最后8公里，跑向跑者的圣殿--中央公园。": "Central Park from Friends, Fifth Avenue from Sex and the City, all those cinematic memories of New York: the NYC Marathon puts the city's best parts right in front of you. Starting from the long, steep Verrazzano Bridge by New York Bay, runners immediately face a climb and the bridge shaking underfoot, then head north through Brooklyn and Long Island, run into Manhattan, and spend the final eight kilometers heading toward every runner's temple: Central Park.",
    "▲ 出发 @ Arsenan": "▲ Setting off @ Arsenan",
    "纽约马拉松的赛道要经过五座桥，除此以外，还有连绵不断的长坡，也算是大满贯赛事中难度相对较大的赛道。": "The NYC Marathon course crosses five bridges. Add the long, rolling climbs, and it is one of the tougher courses among the World Marathon Majors.",
    "▲ 韦拉扎诺桥 @ Arsenan": "▲ Verrazzano Bridge @ Arsenan",
    "▲ 韦拉扎诺桥 @ MarathonFoto": "▲ Verrazzano Bridge @ MarathonFoto",
    "跑过1.8公里的韦拉扎诺桥，我们便来到了布鲁克林，著名球星迈克尔•乔丹就出生在这里。": "After running across the 1.8-kilometer Verrazzano Bridge, we arrived in Brooklyn, where basketball legend Michael Jordan was born.",
    "▲ 布鲁克林 @ Arsenan": "▲ Brooklyn @ Arsenan",
    "纽约的街道向来都是车水马龙，但在这一天，只有跑者才是马路上的主宰。": "New York's streets are usually packed with traffic, but on this day, runners owned the road.",
    "一向以鱼龙混杂著称的布鲁克林街区，这会变得格外热情，可能是被大家的热情所感染，布鲁克林成了跑的最快的行政区。": "Brooklyn, a borough known for being a mixed bag, became especially enthusiastic. Maybe I was carried by the crowd's energy, but Brooklyn became the borough where I ran the fastest.",
    "但跑纽马的价值并非在于速度，而是参与，在NYC，每个人都是纽约客。一个标榜宽容自由的城市骨子里却也往往有着十足最势利狭隘的傲气，但是当这些遇到马拉松时，都如春风化雨。": "But the value of running New York is not speed. It is participation. In NYC, everyone becomes a New Yorker. A city that advertises tolerance and freedom can still carry a deeply snobbish, narrow pride in its bones, but when that meets the marathon, it all softens like rain in spring.",
    "▲ 皇后区 @ Arsenan": "▲ Queens @ Arsenan",
    "在马拉松的赛道上，人们会给拖着残疾双腿以10小时走/跑完全程的老兵跑者送上和冠军们同样热烈的掌声。": "On a marathon course, people give the same thunderous applause to a veteran dragging disabled legs through a ten-hour walk-run as they give to the champions.",
    "和布鲁克林相比，皇后区就显得安静很多，这样反而可以更加享受纽约的赛道本身。": "Compared with Brooklyn, Queens felt much quieter. That actually made it easier to enjoy the course itself.",
    "▲ 曼哈顿 @ Arsenan": "▲ Manhattan @ Arsenan",
    "时间过得很快，不知不觉就跑回了世界中心曼哈顿，一路上看到了许多不同国家的旗子，其实我也一直在期待五星国旗，但直到最后也没有发现。": "Time passed quickly, and before I knew it I had run back into Manhattan, the center of the world. Along the way I saw flags from many countries. I had actually been waiting to see the five-star red flag, but never found one by the end.",
    "▲ 跑步照片 @ MarathonFoto": "▲ Race photo @ MarathonFoto",
    "但并不需要遗憾，因为在这一天，纽约只有两种人，加油者和被加油者，作为最多元化的都市，这一天没有种族，没有阶级，无论是哈林区的平民还是上东区的精英，都是这场盛会的关键元素。": "But there was no need for regret, because on this day New York had only two kinds of people: those cheering and those being cheered. In this most diverse city, race and class disappeared for a day. Whether ordinary people from Harlem or elites from the Upper East Side, everyone was a key part of the celebration.",
    "▲ 志愿者 @ Arsenan": "▲ Volunteers @ Arsenan",
    "作为世界现代艺术的中心，纽约马拉松就如百老汇的舞台，从来不会单调乏味。比如穿着各种颜色斗篷的志愿者，他们就是这一路上最靓丽的风景。": "As a center of modern art, the New York City Marathon is like a Broadway stage: never flat, never dull. Volunteers in ponchos of every color were among the brightest scenery along the way.",
    "还有超人老爷子，我不知道他的年龄，也不知道这是他的第多少届纽约马，但我敢肯定，这一刻，他就是我们所有人心中的超人。": "There was also the old Superman. I do not know how old he was, or how many NYC Marathons he had run, but I am sure that in that moment he was Superman in all our hearts.",
    "▲ 超人老爷子 @ Arsenan": "▲ The old Superman @ Arsenan",
    "还有各种标语，“Last damn bridge!” 还真就是那会儿的内心写照。": "There were all kinds of signs too. \"Last damn bridge!\" really did capture my state of mind at that moment.",
    "▲ 标语 @ Arsenan": "▲ Sign @ Arsenan",
    "▲ Last damn bridge @ Arsenan": "▲ Last damn bridge @ Arsenan",
    "接近中央公园了，赛道周边的观众又多了起来，欢呼声，加油声，此起彼伏。": "As we got close to Central Park, the crowds along the course grew again. Cheers and shouts came in waves.",
    "我也快没油了，所以我会在人少的时候偷偷走一会，但看到观众们，又会强撑着跑起来，特别是看到摄影师，装作能量满满，怎么也得有范。": "I was almost out of fuel too, so when there were fewer people around I would sneak in a short walk. But when I saw spectators, I forced myself to run again. Especially when I saw photographers, I had to pretend I was full of energy and at least look the part.",
    "▲ 中央公园 @ MarathonFoto": "▲ Central Park @ MarathonFoto",
    "跑进中央公园，这里的摄影师密度很大，赛道变得狭窄，也让跑者们可以更加地贴近观众。终点近在咫尺，这会似乎所有的疲劳都被打散了，留下更多的是意犹未尽。": "Once we ran into Central Park, photographers were everywhere. The course narrowed, bringing runners closer to the spectators. The finish was almost there. At that point, all the fatigue seemed to break apart, leaving more of a feeling that I still wanted more.",
    "就是感觉42.195公里太短了，还不够时间把纽约的经历道尽。三万多名选手和沿途上百万观众组成了一条漫长缤纷的河，共同成为了纽约故事的一部分。": "It felt like 42.195 kilometers was too short, not enough time to tell the whole New York experience. More than 30,000 runners and millions of spectators along the route formed one long, colorful river, all becoming part of the New York story together.",
    "▲ 冲线 @ MarathonFoto": "▲ Finish line @ MarathonFoto",
    "冲过终点，领取奖牌，披上保暖斗篷，我的纽约马拉松结束了，但好像又没完全结束，就像还在梦里。": "I crossed the finish, received the medal, and put on the warm poncho. My New York City Marathon was over, but somehow not completely over, as if I were still inside a dream.",
    "▲ 赛后 @ Arsenan": "▲ After the race @ Arsenan",
    "▲ Finisher @ Arsenan": "▲ Finisher @ Arsenan",
    "拉伸过后，我和大家一起走出中央公园，你会发现，蓝色的完赛斗篷成了这天纽约最常见的装扮，在地铁站，在酒店，在餐馆，我们都有一个共同的身份，Finisher。": "After stretching, I walked out of Central Park with everyone else. You could see that the blue finisher poncho had become the most common outfit in New York that day. In subway stations, hotels, and restaurants, we all shared one identity: Finisher.",
    "奖牌没有我想象中的惊艳，但收藏价值大于颜值。": "The medal was not as stunning as I had imagined, but its collectible value mattered more than its looks.",
    "▲ 奖牌 @ Arsenan": "▲ Medal @ Arsenan",
    "纽约马拉松是我的第一个大满贯赛事，但肯定不会是最后一个。": "The New York City Marathon was my first World Marathon Major, but it definitely will not be my last.",
    "▲ 完赛视频 @ 官方": "▲ Finish video @ official",
    "后记": "Postscript",
    "纽约的故事还远没有结束，赛后一天，在洛克菲勒中心，在纽约的机场，你总会看到戴着完赛奖牌的人出现在身边。": "The New York story was far from over. The day after the race, at Rockefeller Center and at the airport, people wearing finisher medals kept appearing around you.",
    "▲ 洛克菲勒中心 @ Arsenan": "▲ Rockefeller Center @ Arsenan",
    "▲洛克菲勒中心 @ Arsenan": "▲ Rockefeller Center @ Arsenan",
    "他们毫不掩饰地炫耀着这份骄傲，但却不会有人去过分苛责，反而很多人向他们投来崇拜的目光，这是属于跑者的高光时刻。": "They showed off that pride without hiding it, and no one really judged them for it. Instead, many people looked at them with admiration. This was the runners' spotlight moment.",
    "▲ 机场 @ Arsenan": "▲ Airport @ Arsenan",
    "“If you love a person, delivers him to go to New York, because there is a heaven; If you hate a person, delivers him to go to New York, because there is a hell.”": "\"If you love someone, send them to New York, because there is heaven there. If you hate someone, send them to New York, because there is hell there.\"",
    "“如果你爱一个人，送他去纽约，因为那里是天堂；如果你恨一个人，送他去纽约，因为那里是地狱。”": "\"If you love someone, send them to New York, because there is heaven there. If you hate someone, send them to New York, because there is hell there.\"",
    "我想，2021年11月7日，纽约就是属于所有跑者的天堂……": "I think that on November 7, 2021, New York belonged to all runners as their heaven...",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "纽约，赛博朋克": "New York, Cyberpunk",
    "- New York -": "- New York -",
    "站在世界的十字路口": "Standing at the crossroads of the world",
    "品尝大苹果城": "A taste of the Big Apple",
    "很喜欢作词人周耀辉写的一首歌的歌词，“斜阳照纽约，第四街穿过，污糟的气窗，第五街一对情人正相约，第八街走过高级商店飘低级发香。需要在地球另一个角落，漫游混乱城内美艳寂寞……”": "I really like a lyric written by Chow Yiu Fai: \"The setting sun shines on New York, crossing Fourth Street, dirty air vents, a pair of lovers meeting on Fifth Street, walking past Eighth Street where expensive shops drift cheap perfume. In another corner of the earth, wandering through a chaotic city, beautiful and lonely...\"",
    "纽约，一座极具魅力的城市，它收纳着肮脏，诱引着欲望，又挑起了罪恶，把尖端科技与底层生活都展现到了极致。": "New York is a city with immense charm. It holds filth, tempts desire, stirs up sin, and pushes both cutting-edge technology and bottom-level life to their extremes.",
    "这个城市，曾经、现在，正要发生的一切，在我眼中，是如此的赛博朋克。": "Everything that has happened, is happening, and is about to happen in this city feels, to me, so cyberpunk.",
    "出发去纽约": "Heading to New York",
    "都说纽约是这一生一定要去的地方，全世界没有一个城市，会同时有着如此多爱恨两极的评论。": "People say New York is a place you have to visit at least once in your life. No other city in the world seems to gather such extreme love-and-hate opinions at the same time.",
    "纽约市的魅力，在於它的兼容并蓄，纽约是纽约，它不是美国，因为它和美国其它地方完全不一样。": "New York City's charm lies in its inclusiveness. New York is New York. It is not America, because it is completely different from the rest of America.",
    "带着无比的期待和好奇，搭了早晨的飞机，两个小时就到了纽约。": "With a lot of anticipation and curiosity, we took a morning flight and reached New York in two hours.",
    "▲Go @ Arsenan": "▲ Go @ Arsenan",
    "▲New York @ Arsenan": "▲ New York @ Arsenan",
    "纽约的公共交通很方便，一路上看着纽约的街景，果然是大城市的感觉，高楼密布，人流涌动，说不出的繁华。": "New York's public transit is convenient. Watching the street scenes along the way, it really felt like a major city: dense high-rises, moving crowds, and a kind of prosperity that is hard to put into words.",
    "大巴加地铁，半个小时，我们就顺利到达了位于时代广场边的CR7酒店，听说这里是C罗在美国开的第一家连锁酒店。房间不大，隐藏在钢铁丛林中，看不到太远处的风景，我猜想楼下大概就是繁忙的街区。": "Bus plus subway, and in half an hour we smoothly reached the CR7 hotel near Times Square. I heard this was Cristiano Ronaldo's first chain hotel in the U.S. The room was not large, hidden inside the steel jungle, with no distant view. I guessed that downstairs was probably a busy street district.",
    "▲CR7 View @ Arsenan": "▲ CR7 View @ Arsenan",
    "法拉盛": "Flushing",
    "挑选了一家韩国自助，跟着导航走进了时代广场地铁站。": "We picked a Korean buffet and followed navigation into the Times Square subway station.",
    "纽约地铁给我的第一感觉是有落差的，锈迹斑斑，还弥漫着一股屎尿味，地铁和行人之间没有防护门，看着列车呼啸而过，总会不由自主地捏把汗。": "My first impression of the New York subway was a gap between expectation and reality: rusty, with a smell of urine and worse hanging in the air. There were no platform doors between trains and pedestrians, and watching trains rush by always made me tense up.",
    "这一刻，地上的繁华街景和地下的交通世界，分分钟让人觉得撕裂，纽约的魔幻现实主义清晰可见。": "In that moment, the glamorous street life aboveground and the underground transit world felt split apart. New York's magical realism was easy to see.",
    "坐上地铁，没过多久，列车从地下涌出，旁边不时穿过一些职业乞讨人，窗外高楼的倒影打在他们的脸上，忽明忽暗。": "After we got on the subway, the train soon surged out from underground. Professional panhandlers passed by now and then, while reflections of tall buildings outside flashed across their faces, bright and dim by turns.",
    "随着指引，在一个忘记名字的地铁站下车。出站之后，仿佛回到了祖国，中国字和亚洲面孔在这里随处可见，繁闹拥挤的街区伴着商贩们的吆喝声，此起彼伏，这会儿，热气腾腾的大包子刚刚出锅，白雾弥漫，到处是中国三四线城市的错觉。": "Following the directions, we got off at a subway station whose name I forgot. After exiting, it felt as if we had returned to China. Chinese characters and Asian faces were everywhere. The busy, crowded blocks mixed with vendors calling out from all directions. Steaming buns had just come out, white vapor drifting around, and for a moment it felt like a third- or fourth-tier city in China.",
    "▲法拉盛 @ Arsenan": "▲ Flushing @ Arsenan",
    "看了一眼地图，才知道误入了法拉盛，法拉盛是全纽约甚至全美都极富盛名的唐人街。不过却完全看不出任何的高大上，都是中国八九十年代的样子。": "Only after checking the map did I realize we had wandered into Flushing. Flushing is one of the most famous Chinatowns in New York, even in all of America. But it did not look fancy at all. It looked like China in the 1980s and 1990s.",
    "后来和朋友聊天，他告诉我：“说法拉盛是中国的三四线都高抬了，也许只能算是七八线吧。”": "Later, when I chatted with a friend, he told me, \"Calling Flushing a third- or fourth-tier Chinese city is already generous. Maybe it only counts as seventh or eighth tier.\"",
    "在法拉盛坐大巴到韩国街，这里的交通很混乱，过程中就看到一位出租车司机探出头大声的抱怨交通状况，既好笑又无奈。": "We took a bus from Flushing to Koreatown. Traffic there was chaotic, and along the way we saw a taxi driver stick his head out and loudly complain about it. It was funny and helpless at the same time.",
    "▲韩国街 @ Arsenan": "▲ Koreatown @ Arsenan",
    "纽约的防疫规定很严，吃饭的地方都要求出示疫苗卡，并且取餐的时候都需要佩戴口罩。韩国BBQ自助确实很棒，算是来美国后吃的最好的一次，因为限时，最后一口气拿了好多，吃的很辛苦。": "New York's COVID rules were strict. Restaurants required vaccine cards, and you had to wear a mask when getting food. The Korean BBQ buffet was genuinely excellent, probably the best meal I had eaten since coming to America. Because there was a time limit, I grabbed a lot at the end and ate very hard.",
    "▲韩国BBQ @ Arsenan": "▲ Korean BBQ @ Arsenan",
    "因为吃的有点多，最后决定从韩国街走回法拉盛，再搭乘地铁回CR7，十一月份的纽约，阳光正好，走在街上，偶尔会和行人擦肩而过，这种感觉既熟悉又陌生，仿佛回到了老家。": "Because we had eaten a bit too much, we decided to walk from Koreatown back to Flushing, then take the subway to the CR7 hotel. New York in November had just the right sunlight. Walking along the street and occasionally brushing past pedestrians felt both familiar and strange, as if I had returned to my hometown.",
    "时代广场": "Times Square",
    "晚上下楼探索时代广场，这算是离我们最近的纽约地标了。": "That evening we went downstairs to explore Times Square, probably the New York landmark closest to us.",
    "有人说，不到纽约算不上到过美国 ，不到时代广场算不上到过纽约。原名为朗埃克广场的时代广场，因为《纽约时报》在此设立总部大楼而更名。": "Some people say that if you have not been to New York, you have not really been to America, and if you have not been to Times Square, you have not really been to New York. Originally called Longacre Square, it was renamed Times Square after The New York Times built its headquarters there.",
    "▲时代广场 @ Arsenan": "▲ Times Square @ Arsenan",
    "时代广场给我的感受，除了绚丽无比的灯光，还有这里的人物群像，十足的烟火气。": "What Times Square gave me, beyond the dazzling lights, was its crowd of characters and its strong everyday human energy.",
    "时代广场是世界的十字路口，各种肤色的人汇集在这里，大家说着不同的语言，欣赏着一样的风景，这里就像一面镜子，刻画着时代的众生相，又像个大熔炉，包容着不同的信仰。": "Times Square is the crossroads of the world. People of every skin color gather here, speaking different languages while admiring the same view. It is like a mirror reflecting the faces of an era, and also like a melting pot holding different beliefs.",
    "这里有很多的Food truck，很平价，偶尔蒸腾起的食物香气，四处飘散，十分诱人。": "There are many food trucks here, and they are quite affordable. Every so often, the smell of hot food rises and drifts around, extremely tempting.",
    "▲Food truck @ Arsenan": "▲ Food truck @ Arsenan",
    "▲人力车 @ Arsenan": "▲ Pedicab @ Arsenan",
    "路上还有很多人力车，他们穿行在黄色的出租车中间招揽生意，既生动又魔幻。": "There were also many pedicabs on the road, weaving among yellow taxis to look for business. The scene felt lively and surreal.",
    "▲街头艺人 @ Arsenan": "▲ Street performer @ Arsenan",
    "这里还有很多街头艺人，有吹萨克斯风的，有画画的，也有穿着各种超级英雄衣服的……大家共同勾勒出了时代广场无比丰富的夜晚。": "There were also many street performers: saxophone players, painters, people dressed as superheroes... Together, they sketched out an incredibly rich Times Square night.",
    "喧闹又迷醉，嘈杂又动人。": "Noisy and intoxicating, chaotic and moving.",
    "04": "04",
    "中央公园": "Central Park",
    "第二天上午吃了个天津大包子，取了跑步装备，下午打算去看一看中央公园。": "The next morning, after eating a big Tianjin-style bun and picking up my race gear, I planned to visit Central Park in the afternoon.",
    "我们都知道纽约的摩天大楼、街区都是工工整整的，城市规划非常方正，这是属于城市的气派。": "We all know New York's skyscrapers and blocks are laid out neatly, with very square urban planning. That is the city's kind of grandeur.",
    "而中央公园就像一张台球桌，平铺在了纽约曼哈顿的市中心，营造出了一种完全不同于城市的风格，": "Central Park is like a billiard table laid flat in the middle of Manhattan, creating a style completely different from the city around it.",
    "为了凸出这种反差感，中央公园里的道路、溪流、湖泊、草坪都被设计得弯弯曲曲、形状不一。": "To emphasize that contrast, the roads, streams, lakes, and lawns inside Central Park were designed to curve and vary in shape.",
    "中央公园很大很美，周边的建筑也很有特色，特别是那几栋细细长长的高楼，像是从地里长出来的一样，直挺挺的伫立在远处，很震撼。": "Central Park is huge and beautiful, and the surrounding buildings are distinctive too. Especially those thin, tall towers, standing straight in the distance as if they had grown out of the ground. It was striking.",
    "▲中央公园门口 @ Arsenan": "▲ Entrance to Central Park @ Arsenan",
    "出了中央公园，城市已经渐渐入夜，这正是游览纽约曼哈顿夜景的好时候。": "After leaving Central Park, the city was gradually entering night, which was a perfect time to see Manhattan's night view.",
    "05": "05",
    "哈德逊河游船": "Hudson River cruise",
    "我们在哈德逊河边的码头出发，这夜风很大，本来计划在船顶露天看风景，但是因为天气很冷，所以也会偶尔躲回船舱听解说。": "We set off from a pier on the Hudson River. The wind was strong that night. I had planned to watch the view from the open deck on top, but because it was cold, I occasionally hid back inside the cabin to listen to the commentary.",
    "▲游船 @ Arsenan": "▲ Cruise boat @ Arsenan",
    "伴着游船驶出码头，远处的城市，灯火通明，我想也许这里就是《赛博朋克2077》里的夜之城吧。": "As the boat left the pier, the city in the distance was lit up. I thought maybe this was Night City from Cyberpunk 2077.",
    "▲曼哈顿夜景 @ Arsenan": "▲ Manhattan night view @ Arsenan",
    "我不知道，对面的码头是否发生过《秋天的童话》，也不知道船头尺的那句“table for two”后的回答。": "I did not know whether An Autumn's Tale had happened on the pier across the water, and I did not know what answer followed the line \"table for two.\"",
    "我也不知道，那些忙碌的曼哈顿写字楼间，究竟是《北京人在纽约》里的天堂，还是地狱。": "I also did not know whether those busy Manhattan office buildings were the heaven or the hell from A Beijinger in New York.",
    "一代人的美国狂热已经褪去，又有新一代的年轻人来到这里，这里是给人极富畅享的赛博朋克，也是需要付出极大努力才能生存下来的弱肉丛林。": "One generation's American fever has faded, and a new generation of young people keeps arriving here. This is a cyberpunk place that gives people endless room to imagine, and also a brutal jungle where surviving takes enormous effort.",
    "我站在纽约的寒风里，迷了眼，想象着这一切与我无关，这一刻，我只想作为一个路人，醉在纽约的夜里。": "Standing in New York's cold wind, my eyes blurred. I imagined that none of this had anything to do with me. In that moment, I just wanted to be a passerby, drunk on the New York night.",
    "游船的夜景很美，我们还穿越了几座桥，不知道其中的一座是不是布鲁克林大桥。": "The cruise-night view was beautiful. We also passed under several bridges, though I was not sure whether one of them was the Brooklyn Bridge.",
    "终于要靠近自由女神像了，大家都出来拍照，开船师傅也特别贴心地带着我们在自由女神边绕了个圈，并且放缓了船速。": "At last we were getting close to the Statue of Liberty. Everyone came out to take photos, and the captain thoughtfully circled around her and slowed the boat down.",
    "▲下船了 @ Arsenan": "▲ Getting off the boat @ Arsenan",
    "这是我第一次看到真的自由女神，心想，此行也算是圆满了。": "This was my first time seeing the real Statue of Liberty. I thought, all right, this trip now feels complete.",
    "06": "06",
    "洛克菲勒中心": "Rockefeller Center",
    "跑步后的第二天，我们来到墨西哥街区吃了个中国自助，美国的这种中国自助基本都是福建人开的，味道差不多，不过纽约的店面就显得小了很多。": "The day after the race, we went to a Mexican neighborhood and ate at a Chinese buffet. In the U.S., these Chinese buffets are basically run by Fujianese owners and taste fairly similar, though the New York storefront was much smaller.",
    "▲Chinese buffet @ Arsenan": "▲ Chinese buffet @ Arsenan",
    "▲墨西哥街区 @ Arsenan": "▲ Mexican neighborhood @ Arsenan",
    "街道上，公交车上，基本都是说着西班牙语的amigo，他们偶尔也会为了谁先下车而争吵。": "On the streets and buses, most people were Spanish-speaking amigos. Occasionally they would argue over who got off first.",
    "▲阿特拉斯铜像 @ Arsenan": "▲ Atlas statue @ Arsenan",
    "▲圣帕特里克大教堂 @ Arsenan": "▲ St. Patrick's Cathedral @ Arsenan",
    "整理好了行李，最后去瞅了一眼洛克菲勒中心，并且路过了著名的圣帕特里克大教堂，相比于时代广场和法拉盛，这里就显得很美国了。": "After packing our luggage, we took one last look at Rockefeller Center and passed the famous St. Patrick's Cathedral. Compared with Times Square and Flushing, this place felt much more American.",
    "▲洛克菲勒中心街景 @ Arsenan": "▲ Rockefeller Center street scene @ Arsenan",
    "在我眼中，纽约就是这样，既矛盾着，又和谐着。": "In my eyes, this is New York: contradictory, yet harmonious.",
    "其实每个人在这里都拥有属于自己的故事，至少在我的记忆里，十一月份的纽约是这样的：": "Everyone here has their own story. At least in my memory, New York in November was like this:",
    "当我们都习惯了裹着厚厚的衣服出门的时候，纽约的街头却可以看到很多人穿着T恤在跑步，或是背着瑜伽垫准备去锻炼；": "When we were already used to going out wrapped in thick clothes, you could still see plenty of people on New York streets running in T-shirts or carrying yoga mats to go work out;",
    "走在路上，脚步会不由自主地加快，生怕一个不注意就会和对面的人撞了个满怀，或者因为一个急停而追尾；": "Walking on the street, your pace speeds up without realizing it, afraid that if you are not careful you will crash into someone coming the other way, or rear-end someone after a sudden stop;",
    "这里的城市夜景绚丽迷人，这里的摩天大楼高耸入云，这里的屎尿味和脏乱差在地下铁泛滥成灾；": "The city's night views are dazzling and charming, the skyscrapers reach into the clouds, and the subway is flooded with smells, filth, disorder, and grime;",
    "这里的咖啡馆就像东北的烧烤摊一样随处可见，几乎人手都会拿着一杯咖啡，城市也因此弥漫着咖啡香；": "Coffee shops here are as common as barbecue stalls in Northeast China. Almost everyone carries a cup of coffee, and the city is filled with its aroma;",
    "这个时候你会发现，“纽约”二字，更是代表了一种生活态度。无关欢喜厌恶， 纽约就是如此的独一无二。": "At that point you realize the words \"New York\" represent a way of life. Whether you like it or hate it, New York is simply that unique.",
    "我不能说多喜欢纽约，但还是希望再次见面，依然不会太久。": "I cannot say I love New York that much, but I still hope we meet again before too long.",
    "▲Bye bye New York @ Arsenan": "▲ Bye bye New York @ Arsenan",
}

SKIP_TEXTS = {"0/0", "继续观看", "★"}
SECTION_HEADINGS = {
    "前言", "后记", "01", "02", "03", "04", "05", "06",
    "赛前领物", "漫长的等待", "我爱NYC马拉松",
    "出发去纽约", "法拉盛", "时代广场", "中央公园", "哈德逊河游船", "洛克菲勒中心",
    "50周年打卡：我的纽约马拉松", "纽约，赛博朋克",
}
KICKER_LINES = {"丨NYC丨", "- NYC Run -", "第一个大满贯", "- New York -", "站在世界的十字路口", "品尝大苹果城"}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1800


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
            src = el.get("src") or el.get("data-src") or ""
            if re.search(r"_files/640(\(|$)", src):
                source = (path.parent / src.replace("./", "")).resolve()
                events.append({"type": "image", "source": source, "article": article})
        elif el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and text not in SKIP_TEXTS and not is_styleish(text) and not has_desc_leaf_container(el):
                if text not in seen_text:
                    events.append({"type": "text", "text": text, "article": article})
                    seen_text.add(text)

    end = next(
        (
            index + 1
            for index, event in enumerate(events)
            if event["type"] == "text" and event["text"] == "设计丨Arsenan"
        ),
        len(events),
    )
    return events[:end]


def extract_story():
    city_events = extract_article(CITY_HTML, "city")
    race_events = extract_article(RACE_HTML, "race")
    source_texts = [event["text"] for event in city_events + race_events if event["type"] == "text"]
    missing = sorted({text for text in source_texts if text not in TRANSLATIONS})
    if missing:
        raise RuntimeError("Missing English translations:\n" + "\n".join(missing))
    return city_events, race_events


def font(size: int, bold: bool = False):
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
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
        tag = "h3" if re.fullmatch(r"\d{2}", original) else "h2"
        return f"<{tag}>{escape(text)}</{tag}>"
    if original == "- 本文完 -":
        return f'<p class="end-mark">{escape(text)}</p>'
    if original in KICKER_LINES:
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
    page_key = f"run50-{SLUG}-zh" if lang == "zh" else f"run50-{SLUG}-en"
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
        <div id="supabase-comments-new-york-zh" data-zz-supabase-comments></div>
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
        <div id="supabase-comments-new-york-en" data-zz-supabase-comments></div>
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
        "城市篇与比赛篇合并：赛博朋克纽约、法拉盛、时代广场、哈德逊河游船，以及50周年纽约马拉松的五区奔跑。"
        if zh
        else "A full two-part New York story: cyberpunk city wandering, Flushing, Times Square, a Hudson River cruise, and the 50th NYC Marathon across five boroughs."
    )
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="../english/{SLUG}.html">English</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        if zh
        else f'<a href="./index.html">← English Stories</a><a href="../chinese/{SLUG}.html">中文</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>纽约 · 纽约州</span><span>2021.11.07</span><span>Run50 #3</span><span>城市篇 + 比赛篇</span>'
        if zh
        else '<span>New York City, New York</span><span>Nov 7, 2021</span><span>Run50 #3</span><span>City story + race story</span>'
    )
    city_heading = "城市篇｜纽约，赛博朋克" if zh else "City Story | New York, cyberpunk"
    race_heading = "比赛篇｜50周年打卡：我的纽约马拉松" if zh else "Race Story | Checking in at the 50th NYC Marathon"
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
  <meta property="og:image" content="{SITE}/assets/og-run50-new-york-city-marathon-icons.png?v={VERSION}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-new-york-city-marathon-icons.png?v={VERSION}">
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
        <p class="eyebrow">Run50 #3 · New York</p>
        <h1>{escape(title)}</h1>
        <p class="dek">{escape(desc)}</p>
        <div class="meta-row">{meta}</div>
      </div>
      <img class="cover" src="../../../assets/thumb-run50-new-york-city-marathon-icons.svg?v={VERSION}" alt="New York City Marathon icon cover">
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
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-{SLUG}-facebook-en">
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
        <div id="supabase-comments-new-york-fb" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def facebook_page(race_article: str, city_article: str) -> str:
    desc = "The 50th NYC Marathon first, then the city that made those five boroughs feel electric: subway platforms, Staten Island sunrise, Central Park, Times Square, and a cyberpunk New York night."
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
  <meta property="og:image" content="{SITE}/assets/og-run50-new-york-city-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-new-york-city-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>
    :root {{ --bg:#f5f7fa; --paper:#fff; --ink:#101828; --muted:#667085; --line:#d0dfe8; --accent:#0b67c2; }}
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
      <nav><a href="../hub.html">Run50 Hub</a><a href="../stories/english/{SLUG}.html">English</a><a href="../stories/chinese/{SLUG}.html">中文</a></nav>
    </div>
  </header>
  <section class="hero">
    <div class="hero-inner">
      <div>
        <p class="section-label">World / USA / Marathon</p>
        <h1>{escape(TITLE_FB)}</h1>
        <p class="dek">On November 7, 2021, the 50th running of the New York City Marathon brought runners back across the five boroughs after two pandemic years. For Run50, it was State 3 and my first World Marathon Major.</p>
        <div class="meta-row"><span>New York City, NY</span><span>{DATE_EN}</span><span>Run50 #3</span><span>World Major #1</span></div>
      </div>
      <img src="../../assets/thumb-run50-new-york-city-marathon-icons.svg?v={VERSION}" alt="New York City Marathon icon cover">
    </div>
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race day</p>
      <p>New York is loud before the gun ever goes off: subway platforms full of runners, the Staten Island Ferry at sunrise, a long cold wait, then the climb onto the Verrazzano Bridge. That is where this story begins.</p>
{race_article}
      <p class="transition">The marathon made the city feel like one long moving river. But the weekend around it had already shown me New York's other faces: cyberpunk lights, subway grime, Flushing, Times Square, Central Park, the Hudson River, and a night view that felt unreal.</p>
      <p class="section-label">The city around the race</p>
{city_article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{RACE_NAME}</dd></div>
          <div><dt>Date</dt><dd>{DATE_EN}</dd></div>
          <div><dt>State</dt><dd>New York · Run50 #3</dd></div>
          <div><dt>Route memory</dt><dd>Staten Island to Central Park, five boroughs, five bridges, and a city that becomes one crowd.</dd></div>
        </dl>
      </div>
      <div class="related">
        <strong>More versions</strong>
        <a href="../stories/english/{SLUG}.html">Read in original order</a>
        <a href="../stories/chinese/{SLUG}.html">中文原文整理版</a>
      </div>
    </aside>
  </main>
{facebook_engagement()}
</body>
</html>
"""


def draw_badge(draw, x, y, w, h):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((x + 30, y + 48), "Run50 #03", fill="#20242b", font=font(38, True))
    draw.text((x + 30, y + 113), "NEW YORK", fill="#0b67c2", font=font(44, True))


def draw_nyc_scene(draw, height: int):
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    sky = "#cfe9f4"
    water = "#6ec7d8"
    island = "#9fd46e"
    road = "#27384a"
    yellow = "#ffc83d"
    orange = "#ff8a45"
    navy = "#1f2a44"
    green = "#2f9f72"
    draw.rectangle((0, 0, int(1200 * scale), int(height)), fill=sky)
    draw.ellipse((p(910, 110), p(1005, 205)), fill="#f7bc3b")
    draw.polygon([p(0, 430), p(1200, 360), p(1200, 630), p(0, 630)], fill=water)
    draw.polygon([p(0, 460), p(1200, 410), p(1200, 630), p(0, 630)], fill="#8ac7b7")
    draw.rectangle((0, int(510 * scale), int(1200 * scale), int(630 * scale)), fill=island)
    draw.rectangle((0, int(565 * scale), int(1200 * scale), int(630 * scale)), fill="#6caf47")

    # Manhattan skyline
    base_y = 410
    buildings = [
        (470, 270, 48, 140, "#8bb0c7"), (525, 240, 60, 170, "#6f93b0"),
        (595, 300, 42, 110, "#89b6c6"), (650, 220, 54, 190, "#587794"),
        (715, 260, 72, 150, "#7fa4ba"), (800, 285, 50, 125, "#9ababf"),
        (858, 245, 62, 165, "#6689a8"), (930, 300, 42, 110, "#83a9c0"),
    ]
    for x, y, w, h, color in buildings:
        draw.rectangle((p(x, y), p(x + w, base_y)), fill=color)
        for wx in range(x + 10, x + w - 5, 18):
            for wy in range(y + 14, base_y - 14, 28):
                draw.rectangle((p(wx, wy), p(wx + 7, wy + 10)), fill="#f7f3c4")
    draw.polygon([p(665, 220), p(677, 165), p(689, 220)], fill="#415f7d")

    # Statue of Liberty, kept below title zone.
    draw.rectangle((p(150, 410), p(190, 520)), fill=green)
    draw.polygon([p(135, 410), p(205, 410), p(190, 340), p(150, 340)], fill="#38b983")
    draw.ellipse((p(157, 315), p(183, 342)), fill="#2f9f72")
    for angle_x in [145, 156, 168, 180, 191]:
        draw.line((p(170, 318), p(angle_x, 292)), fill=green, width=max(2, int(3 * scale)))
    draw.line((p(188, 360), p(230, 318)), fill=green, width=max(5, int(8 * scale)))
    draw.polygon([p(226, 305), p(238, 322), p(218, 324)], fill="#ffc83d")

    # Verrazzano-style bridge arc and cables.
    draw.arc((p(215, 350), p(560, 560)), start=192, end=344, fill=navy, width=max(5, int(8 * scale)))
    draw.line((p(285, 390), p(285, 520)), fill=navy, width=max(5, int(7 * scale)))
    draw.line((p(500, 350), p(500, 500)), fill=navy, width=max(5, int(7 * scale)))
    for x in range(305, 500, 26):
        draw.line((p(x, 386), p(x + 28, 510)), fill="#f4f0d0", width=max(1, int(2 * scale)))
    draw.rectangle((p(230, 515), p(575, 532)), fill=road)

    # Yellow cab and runners.
    draw.rounded_rectangle((p(830, 512), p(1010, 585)), radius=int(14 * scale), fill=yellow, outline=navy, width=max(3, int(4 * scale)))
    draw.rectangle((p(875, 475), p(950, 525)), fill=yellow, outline=navy, width=max(3, int(4 * scale)))
    draw.rectangle((p(892, 486), p(930, 516)), fill="#bde6f3")
    draw.ellipse((p(860, 570), p(900, 610)), fill=navy)
    draw.ellipse((p(940, 570), p(980, 610)), fill=navy)
    draw.rectangle((p(890, 458), p(937, 475)), fill="#ffffff", outline=navy, width=max(2, int(3 * scale)))
    draw.text(p(900, 459), "NYC", fill=navy, font=font(max(10, int(14 * scale)), True))
    for x, color in [(680, orange), (730, "#0b67c2"), (780, "#f2545b")]:
        draw.ellipse((p(x, 510), p(x + 24, 534)), fill=color)
        draw.line((p(x + 12, 534), p(x + 6, 575)), fill=navy, width=max(3, int(4 * scale)))
        draw.line((p(x + 12, 542), p(x + 35, 560)), fill=navy, width=max(3, int(4 * scale)))
        draw.line((p(x + 8, 575), p(x - 12, 602)), fill=navy, width=max(3, int(4 * scale)))
        draw.line((p(x + 8, 575), p(x + 30, 602)), fill=navy, width=max(3, int(4 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#cfe9f4")
    draw = ImageDraw.Draw(image)
    draw_nyc_scene(draw, 630)
    draw.text((64, 64), "NEW YORK", fill="#20242b", font=font(66, True))
    draw.text((66, 136), "FIVE BOROUGHS · 50TH RUNNING", fill="#667085", font=font(26, True))
    draw_badge(draw, 760, 64, 362, 164)
    image.save(OG_PATH)


def generate_cover_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <rect width="1200" height="750" fill="#cfe9f4"/>
  <circle cx="930" cy="132" r="58" fill="#f7bc3b"/>
  <path d="M0 522 L1200 438 L1200 750 L0 750Z" fill="#6ec7d8"/>
  <path d="M0 555 L1200 500 L1200 750 L0 750Z" fill="#8ac7b7"/>
  <rect x="0" y="610" width="1200" height="140" fill="#9fd46e"/>
  <rect x="0" y="680" width="1200" height="70" fill="#6caf47"/>
  <g>
    <rect x="470" y="330" width="50" height="170" fill="#8bb0c7"/>
    <rect x="530" y="290" width="66" height="210" fill="#6f93b0"/>
    <rect x="606" y="360" width="48" height="140" fill="#89b6c6"/>
    <rect x="665" y="265" width="60" height="235" fill="#587794"/>
    <polygon points="683,265 695,195 707,265" fill="#415f7d"/>
    <rect x="742" y="315" width="78" height="185" fill="#7fa4ba"/>
    <rect x="835" y="292" width="66" height="208" fill="#6689a8"/>
    <rect x="918" y="350" width="48" height="150" fill="#83a9c0"/>
  </g>
  <g fill="#f7f3c4">
    <rect x="545" y="318" width="10" height="15"/><rect x="575" y="348" width="10" height="15"/>
    <rect x="681" y="318" width="10" height="15"/><rect x="693" y="370" width="10" height="15"/>
    <rect x="760" y="360" width="10" height="15"/><rect x="790" y="410" width="10" height="15"/>
    <rect x="850" y="322" width="10" height="15"/><rect x="878" y="380" width="10" height="15"/>
  </g>
  <g>
    <rect x="150" y="490" width="40" height="120" fill="#2f9f72"/>
    <polygon points="134,490 206,490 190,405 150,405" fill="#38b983"/>
    <circle cx="170" cy="383" r="15" fill="#2f9f72"/>
    <line x1="170" y1="380" x2="145" y2="348" stroke="#2f9f72" stroke-width="5"/>
    <line x1="170" y1="380" x2="166" y2="342" stroke="#2f9f72" stroke-width="5"/>
    <line x1="170" y1="380" x2="191" y2="348" stroke="#2f9f72" stroke-width="5"/>
    <line x1="188" y1="427" x2="232" y2="377" stroke="#2f9f72" stroke-width="10"/>
    <polygon points="228,360 243,380 218,383" fill="#ffc83d"/>
  </g>
  <path d="M230 618 Q390 478 570 615" fill="none" stroke="#1f2a44" stroke-width="10"/>
  <line x1="292" y1="475" x2="292" y2="625" stroke="#1f2a44" stroke-width="8"/>
  <line x1="505" y1="430" x2="505" y2="600" stroke="#1f2a44" stroke-width="8"/>
  <rect x="230" y="618" width="345" height="20" fill="#27384a"/>
  <g>
    <rect x="832" y="610" width="178" height="75" rx="15" fill="#ffc83d" stroke="#1f2a44" stroke-width="5"/>
    <rect x="875" y="565" width="78" height="55" fill="#ffc83d" stroke="#1f2a44" stroke-width="5"/>
    <rect x="893" y="578" width="38" height="30" fill="#bde6f3"/>
    <circle cx="880" cy="690" r="22" fill="#1f2a44"/><circle cx="955" cy="690" r="22" fill="#1f2a44"/>
    <rect x="890" y="545" width="50" height="20" fill="#fff" stroke="#1f2a44" stroke-width="3"/>
    <text x="900" y="561" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="900" fill="#1f2a44">NYC</text>
  </g>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">NEW YORK</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">FIVE BOROUGHS · 50TH RUNNING</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #03</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#0b67c2">NEW YORK</text>
</svg>
'''
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source = RACE_HTML.parent / f"{RACE_HTML.stem}_files" / "640(70)"
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        target_ratio = 1200 / 750
        width, height = image.size
        crop_width = width
        crop_height = int(width / target_ratio)
        if crop_height > height:
            crop_height = height
            crop_width = int(height * target_ratio)
        left = max(0, (width - crop_width) // 2)
        top = max(0, (height - crop_height) // 2)
        image = image.crop((left, top, left + crop_width, top + crop_height)).resize((1200, 750), Image.LANCZOS)
        image.save(MEDAL_COVER_PATH, quality=92)


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
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="纽约马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">纽约纽约市 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第3州｜纽约马拉松</h2>
          <p class="story-desc">城市篇与比赛篇合并：赛博朋克纽约、法拉盛、时代广场、哈德逊河游船，以及50周年纽约马拉松的五区奔跑。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for New York City Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">New York · New York City · {DATE_ZH}</div>
          <h2>New York City Marathon: the 50th running across five boroughs</h2>
          <p>A two-part New York weekend: cyberpunk city scenes, Flushing, Times Square, Central Park, the Hudson River, then my first World Marathon Major.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>New York turned 26.2 miles into one enormous five-borough street party</h2>
        <p>Race date: November 7, 2021. State 3 of Run50 and my first World Marathon Major: Staten Island, the Verrazzano Bridge, Brooklyn, Queens, Manhattan, and Central Park.</p>
        <div class="meta"><span>New York City, NY</span><span>Run50 #3</span><span>World Major #1</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style New York City Marathon cover">
    </a>
"""

    text = remove_existing_card(zh_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./cleveland-marathon.html", zh_card, '<section class="story-grid" aria-label="中文故事列表">')
    text = re.sub(r"\s*'NY-[^']+': 'new-york-city-marathon.html',?\n", "\n", text)
    text = re.sub(r"(\s*)'OH-[^']+': 'cleveland-marathon.html',?\n\s*'OH-[^']+': 'cleveland-marathon.html',?", r"\1'OH-克利夫兰': 'cleveland-marathon.html',", text)
    text = text.replace("'OH-克利夫兰': 'cleveland-marathon.html'", "'OH-克利夫兰': 'cleveland-marathon.html',\n      'NY-纽约市': 'new-york-city-marathon.html'")
    zh_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(en_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./cleveland-marathon.html", en_card, '<section class="story-grid" aria-label="English story list">')
    text = re.sub(r"\s*'NY-New York City': 'new-york-city-marathon.html',?\n", "\n", text)
    text = re.sub(r"(\s*)'OH-Cleveland': 'cleveland-marathon.html',?\n\s*'OH-Cleveland': 'cleveland-marathon.html',?", r"\1'OH-Cleveland': 'cleveland-marathon.html',", text)
    text = text.replace("'OH-Cleveland': 'cleveland-marathon.html'", "'OH-Cleveland': 'cleveland-marathon.html',\n      'NY-New York City': 'new-york-city-marathon.html'")
    en_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./cleveland-marathon.html", fb_card, '<main class="shell">')
    fb_path.write_text(clean_text(text), encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- New York Run50 story -->.*?<!-- /New York Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- New York Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="New York turned 26.2 miles into one enormous five-borough street party">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style New York City Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">New York turned 26.2 miles into one enormous five-borough street party</a>
            <p class="video-sub">New York City, NY &middot; Nov 7, 2021</p>
          </div>
        </div>
      </article>
      <!-- /New York Run50 story -->

"""
    if "<!-- /Ohio Run50 story -->" in text:
        text = text.replace("      <!-- /Ohio Run50 story -->\n", "      <!-- /Ohio Run50 story -->\n" + card, 1)
    else:
        text = text.replace("      <!-- Water Header -->", card + "      <!-- Water Header -->", 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("'Cleveland':{lat:41.4993,lon:-81.6944},'Cincinnati'", "'Cleveland':{lat:41.4993,lon:-81.6944},'New York City':{lat:40.7128,lon:-74.0060},'Cincinnati'")
    text = re.sub(r"^\s*'NY':\[\{city:'New York City'.*?\}\],\n", "", text, flags=re.M)
    text = text.replace(
        "  'OH':[{city:'Cleveland',date:'Oct 24, 2021',story:'stories/english/cleveland-marathon.html',fb:'facebook/cleveland-marathon.html'}],",
        "  'OH':[{city:'Cleveland',date:'Oct 24, 2021',story:'stories/english/cleveland-marathon.html',fb:'facebook/cleveland-marathon.html'}],\n"
        "  'NY':[{city:'New York City',date:'Nov 7, 2021',story:'stories/english/new-york-city-marathon.html',fb:'facebook/new-york-city-marathon.html'}],",
        1,
    )
    text = re.sub(
        r"\n\s*<!-- New York City story dot -->.*?<!-- /New York City story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    dot = """
    <!-- New York City story dot -->
    <circle cx="249" cy="125" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="249" cy="125" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="New York City, NY" data-date="Nov 7, 2021" data-story="stories/english/new-york-city-marathon.html"/>
    <!-- /New York City story dot -->
"""
    text = text.replace("    <!-- /Ohio Cleveland story dot -->\n", "    <!-- /Ohio Cleveland story dot -->\n" + dot, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 14 stories", " 15 stories")
    text = text.replace("<strong>14</strong> stories", "<strong>15</strong> stories")
    path.write_text(clean_text(text), encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        "run50-new-york-city-marathon-facebook-en",
        "run50-new-york-city-marathon-en",
        "run50-new-york-city-marathon-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-cleveland-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(clean_text(text), encoding="utf-8")


def main():
    city_events, race_events = extract_story()
    all_events = city_events + race_events
    image_count = copy_story_images(all_events)
    city_zh = render_events(city_events, "zh", "Run50-NewYorkCity-Marathon-clean_files/", "纽约照片")
    race_zh = render_events(race_events, "zh", "Run50-NewYorkCity-Marathon-clean_files/", "纽约马拉松照片")
    city_en = render_events(city_events, "en", "../chinese/Run50-NewYorkCity-Marathon-clean_files/", "New York photo")
    race_en = render_events(race_events, "en", "../chinese/Run50-NewYorkCity-Marathon-clean_files/", "New York City Marathon photo")
    city_fb = render_events(city_events, "en", "../stories/chinese/Run50-NewYorkCity-Marathon-clean_files/", "New York photo")
    race_fb = render_events(race_events, "en", "../stories/chinese/Run50-NewYorkCity-Marathon-clean_files/", "New York City Marathon photo")

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
    print(f"Built {SLUG}: {image_count} images, {len(city_events)} city events, {len(race_events)} race events")


if __name__ == "__main__":
    main()
