from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-13-WV")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "west-virginia-marathon"
VERSION = "20260605-1"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-West-Virginia-Marathon-clean_files"


EN_BY_INDEX = {
    '丨WEST VIRGINIA丨': '丨WEST VIRGINIA丨',
    '前言': 'Preface',
    '从小就听过这首《Take Me Home, Country Roads》，第一句歌词就是 almost heaven West Virginia，我太喜欢这首歌了，初中上英语课的时候我就经常偷摸着听，Country Roads 算是我美国乡村音乐的启蒙，至于西弗吉尼亚，那时候对我来说太过遥远了，而今，从家开车过去也只需要3个小时。': "I have listened to the song 'Take Me Home, Country Roads' since I was a child. The first line of the lyrics, 'almost heaven West Virginia,' made me fall in love with it. Back in middle school during English class, I would sneakily listen to it on my player. Country Roads was my initiation to American country music. As for West Virginia itself, back then it felt too distant. Now, it is just a three-hour drive from our home.",
    '这首歌是由著名美国歌手约翰·丹佛(John Denver)于1971年创作并演唱的，歌曲旋律轻快，给人描绘了一幅美丽的美国东部西弗吉尼亚风光，趁着写这个文，我也收集了这首歌的几个版本，还是那么的好听….': 'This song was written and performed by the famous American singer John Denver in 1971. The melody is light and brisk, sketching the beautiful scenery of West Virginia in the eastern United States. While writing this story, I collected several versions of the song, and it remains as beautiful as ever...',
    '”简直是天堂啊! 兰岭山，谢纳多阿河，那里的生命年代久远，比树木古老，比群山年轻，像和风一样慢慢生长，乡村路，带我回家，到我生长的地方，西弗吉尼亚，山峦妈妈，乡村路，带我回家……“': '"Almost heaven, West Virginia, Blue Ridge Mountains, Shenandoah River. Life is old there, older than the trees, younger than the mountains, growing like a breeze. Country roads, take me home to the place I belong, West Virginia, mountain mama, take me home country roads..."',
    '▲ Take Me Home, Country Roads @YT': '▲ Take Me Home, Country Roads @YT',
    '▲ Marshall University Marathon @MUM': '▲ Marshall University Marathon @MUM',
    '★': '★',
    '# 西弗吉尼亚州，亨廷顿🏈 Huntington, West Virginia': '# West Virginia: Huntington 🏈 Tri-State Confluence',
    '相比于这首歌，感觉西弗吉尼亚州的存在感并不高，在马拉松版图上，这里更是岌岌无名。': "Compared to the song, the state of West Virginia doesn't seem to have a strong presence. On the marathon map, it is even more obscure.",
    '▲ West Virginia @Google': '▲ West Virginia @Google',
    '▲ Coopers Rock State Forest @Google': '▲ Coopers Rock State Forest @Google',
    '不过西弗吉尼亚州的风景确实可以用壮观来形容，虽然离肯塔基很近，但地形却大不相同，因西弗吉尼亚州内都为山地和高原，没有平原，所以又名山地之州。在波托马克高地，山峰海拔近1500米，这里还拥有许多滑雪场、州立公园、瀑布和蜿蜒曲折的小径。': "However, West Virginia's landscape can truly be described as spectacular. Although it is close to Kentucky, the terrain is completely different. Because West Virginia is entirely covered by mountains and plateaus with no plains, it is also known as the Mountain State. In the Potomac Highlands, the peaks reach nearly 1,500 meters, hosting many ski resorts, state parks, waterfalls, and winding trails.",
    '▲ Grandview National Park @Google': '▲ Grandview National Park @Google',
    '▲ Grandview National Park @Google': '▲ Grandview National Park @Google',
    '▲ West Virginia @Google': '▲ West Virginia @Google',
    '由于地理位置的特殊，在早期时候，西弗吉尼亚州人就已经有了独立意识。阿巴拉契亚和蓝岭山脉将这里与弗吉尼亚州的其余大部分地方分隔开来，因此他们也不那么强烈地认为自己是这个州的一份子，西弗吉尼亚州也是唯一在美国内战中诞生的州。': 'Due to its unique geography, West Virginians developed a sense of independence early on. The Appalachian and Blue Ridge mountains separated this area from the rest of Virginia, so they did not feel a strong connection to that state. In fact, West Virginia is the only state born out of the American Civil War.',
    '▲ West Virginia @Google': '▲ West Virginia @Google',
    '▲ New River Gorge Bridge Archival @Google': '▲ New River Gorge Bridge Archival @Google',
    '▲ New River Gorge Bridge Archival @Google': '▲ New River Gorge Bridge Archival @Google',
    '至于我们要去的亨廷顿（Huntington），也不太出名，毕竟这里是一个很小很小的城市，不过亨廷顿的位置还挺特殊的，正好位于肯塔基州，俄亥俄州和西弗吉尼亚州的交界处，同时也处在俄亥俄河和盖安多特河（Guyandotte River）的交汇处。': "As for Huntington, where we were heading, it isn't very famous either—it is a tiny city. However, its location is quite unique: right at the tri-state junction of Kentucky, Ohio, and West Virginia, and at the confluence of the Ohio River and the Guyandotte River.",
    '▲ Huntington, WV @Google': '▲ Huntington, WV @Google',
    '交界处挺好，说明离我们很近，中途我们还会经过车程1个小时的列克星敦，这里有我俩最爱的中国自助，有周六特供的地三鲜水煮鱼猪蹄和各种川菜，这次出行，我们自然是不会放过。': "The junction location is great because it means it's very close to us. Along the way, we would pass Lexington, which is a one-hour drive away. Lexington has our favorite Chinese buffet, offering Saturday specials like Di San Xian (sauteed potato, eggplant, and green pepper), boiled fish, pork trotter, and various Sichuan dishes. On this trip, we naturally wouldn't miss it.",
    '▲ Panda Cuisine, Lexington @Google': '▲ Panda Cuisine, Lexington @Google',
    '▲ 41th Ave and 10th Street, Huntington @Google': '▲ 41st Ave and 10th Street, Huntington @Google',
    '吃好后又开了2个多小时，我们就到了亨廷顿，城市不大，据说有五万的人口，刚进城时的郊区，看上去还有点破败。': 'After eating our fill, we drove for another two hours and arrived in Huntington. The city is small, with a reported population of about 50,000. The outskirts as we entered looked a bit rundown.',
    '▲ Huntington, WV @Arsenan': '▲ Huntington, WV @Arsenan',
    '这次来亨廷顿，我们是为了跑马歇尔大学马拉松，这是个可以抱着橄榄球冲线的比赛，挺特别的，大家都很喜欢。': "We came to Huntington to run the Marshall University Marathon. This is a race where you get to cross the finish line holding a football. It's very unique, and runners love it.",
    '▲ Expo @Arsenan': '▲ Expo @Arsenan',
    '▲ Expo @Arsenan': '▲ Expo @Arsenan',
    '来到亨廷顿，我们就直接去了Expo去拿马拉松装备，Expo在绿色橄榄球场边的教堂里，布置得很简单，主打的就是简单高效。': 'Upon arriving in Huntington, we went straight to the expo to pick up our gear. The expo was held in a church next to the green football stadium. The setup was simple, focusing on efficiency.',
    '▲ Expo @Siqi': '▲ Expo @Siqi',
    '▲ Expo @Siqi': '▲ Expo @Siqi',
    '取过装备，我们看时间还早，就计划着去马歇尔大学（Marshall University）里转一转，用大学的名字直接用作马拉松的名字，我还是第一次见，确实挺好奇，想看看那里有什么特别。\u200d': 'After grabbing our packets, we had some time, so we decided to stroll around Marshall University. It was my first time seeing a marathon named directly after a university, and I was curious to see what made this place special.',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '刚到马歇尔大学，我就习惯性地搜了一下这个学校的排名，一看排名也没有很高，我有点迷惑，既然这里也不是什么大名校，那为啥感觉整个小城都为这样一所学校自豪呢？甚至还直接用大学的名字命名这个马拉松；后来我们又去了超市（Kroger），甚至超市里都是随处可见的印着学校Logo的纪念品。': "When we first arrived at Marshall University, I habitually searched for the school's ranking. Seeing it wasn't very high, I was a bit puzzled. If it isn't a prestigious university, why does the whole town seem so proud of it? They even named the marathon after it. Later, when we visited Kroger, we saw school-branded souvenirs everywhere.",
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '突然间，我意识到自己陷入了中国式思维的误区，我们的教育太强调成绩，太强调排名了，太张雪峰了，所以我也习惯于用这种思维模式去思考问题。': 'Suddenly, I realized I had fallen into the trap of Chinese-style thinking. Our education overemphasizes academic rankings and test scores, so I was used to analyzing things through that lens.',
    '马歇尔大学最引以为傲的是他们的橄榄球队，被称为 ”the Thundering Herd“，这支橄榄球队赢得过三次NCAA全国冠军，其中包括1992年和1996年的两次，并在1991年、1993年和1995年获得了全国亚军，虽然小城只有五万人，但一场球赛却能吸引超过三万八千多的球迷！': "Marshall University's greatest pride is its football team, the Thundering Herd. This team has won three national championships, including NCAA Division I-AA titles in 1992 and 1996, and finished as runner-up in 1991, 1993, and 1995. Even though the town has only 50,000 residents, a single game can draw over 38,000 fans!",
    '联想到美国社会本来就建立在体育之上，小城居民的骄傲就一点也不奇怪了，我也希望中国有一天能有这样的体育文化，那样就不会有人再说我跑马拉松浪费生命了。': "Considering that American society is practically built on sports, the residents' pride is not surprising. I hope China will have a sports culture like this one day, so no one will say I'm wasting my life by running marathons.",
    '我小时候爱踢足球，自认为踢得还挺好，班主任就总找我谈话，说我总这么踢足球，腿就会变形的；我现在爱跑马，家人朋友就总和我讲，再跑下去，膝盖就废了……… 似乎这样的故事一直在我这无限循环。': 'When I was a kid, I loved playing soccer and thought I was pretty good. But my homeroom teacher would always pull me aside, warning that running around would deform my legs. Now that I run marathons, my family and friends constantly warn me that my knees will be ruined. It feels like an endless loop.',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '扯远了，说回马歇尔大学，校园里的标语也处处都是这种骄傲的体现，绿色的标语牌配上深秋的金黄色，给人一种很舒畅的感觉。': 'Anyway, back to Marshall University. The campus slogans reflect this pride everywhere. The green signs paired with the golden autumn foliage create a very refreshing atmosphere.',
    '▲ Memorial Fountain @Arsenan': '▲ Memorial Fountain @Arsenan',
    '▲ Memorial Fountain @Arsenan': '▲ Memorial Fountain @Arsenan',
    '▲ Memorial Fountain @Siqi': '▲ Memorial Fountain @Siqi',
    '走着走着，我们来到了 Memorial Student Center 外的一个喷泉旁边。这个喷泉是为了纪念1970年飞机失事而离世的75名遇难者而建立的。在1970年11月14日，发生了NCAA体育史上最严重的单一空难事件，造成75人丧生。这次事故发生在西弗吉尼亚州韦恩县多雨的山坡上，不仅马歇尔大学橄榄球队几乎全军覆没，还有教练、机组人员、众多球迷和支持者一同罹难。': 'As we walked, we reached a fountain outside the Memorial Student Center. This fountain was built to honor the 75 victims of the 1970 plane crash. On November 14, 1970, the deadliest single-tragedy aviation crash in NCAA sports history occurred, claiming 75 lives. The crash on a rainy hillside in Wayne County, West Virginia, wiped out almost the entire Marshall University football team, along with coaches, crew, and many dedicated fans.',
    '▲ Football Team (1970) @Google': '▲ Football Team (1970) @Google',
    '这座纪念碑由雕塑家哈利·贝尔托亚创作，高达13英尺，重达6,500磅。他希望这座喷泉能够 “纪念生者，而非死亡 —— 在生命的水面上，上升、消退、涌动，以表达向上的成长、不朽和永恒”。': "The monument was created by sculptor Harry Bertoia, standing 13 feet tall and weighing 6,500 pounds. He designed the fountain to 'commemorate the living, not the dead—on the waters of life, rising, receding, surging, to express upward growth, immortality, and eternity.'",
    '对于马歇尔大学的学生和校友来说，这支球队是这座城市的骄傲，也是他们永远的痛，而 Memorial Fountain 则成了一个象征 —— 坚韧不拔、精神永恒和面向未来。': "For Marshall students and alumni, this team is the city's pride and its eternal scar. The Memorial Fountain stands as a symbol of resilience, eternal spirit, and looking forward.",
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Siqi': '▲ Marshall University @Siqi',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '我们在校园里拍了不少照片，校园环境挺棒的，随后我们又去超市买了点早餐，随后赶回旅馆，这是我第一次住汽车旅馆，感觉超出预期，挺方便的，环境和卫生也都很棒。': 'We took a lot of photos around the campus, which was beautiful. Later, we bought some breakfast at the supermarket and headed back to our motel. This was my first time staying in a motel, and it exceeded my expectations—very convenient, clean, and comfortable.',
    '▲ Motel @Arsenan': '▲ Motel @Arsenan',
    '看了会”花儿与少年“，Siqi又工作了一会儿，我们便早早入睡，汽车旅馆的隔音还不错，第二天据说还有早餐，可惜我们要早早出门，赶不上了。': "We watched some episodes of 'Divas Hit the Road' and Siqi worked for a bit before we went to bed early. The motel had decent soundproofing. They supposedly offered breakfast the next morning, but we had to leave too early to catch it.",
    '★★': '★★',
    '# 19周年，马歇尔大学马拉松🏈 Huntington, West Virginia': '# Marshall University Marathon: 19th Anniversary 🏈 Huntington, West Virginia',
    '这是，西弗吉尼亚州 -- 最大的马拉松比赛，但不得不说，Marshall大学马拉松和半程马拉松确实是一个相对较小的比赛（2023年有超过1800名参与者参加了这两个项目），这个赛道是一个13.1英里的环形路线，马拉松选手需要跑两遍。': "This is West Virginia's largest marathon, but it must be said that the Marshall University Marathon and Half Marathon is still a relatively small race (with just over 1,800 participants across both distances in 2023). The course is a 13.1-mile loop, which marathon runners complete twice.",
    '▲ Course Map @Google': '▲ Course Map @Google',
    '比赛起点/终点位于Marshall大学的Joan C Edward体育场，整个比赛会穿过亨廷顿市中心，普尔曼广场，和几个公园，还有一段笔直的路线，感觉像是一个轻工业区。': "The start and finish lines are at Marshall University's Joan C. Edwards Stadium. The course loops through downtown Huntington, Pullman Square, several parks, and a straight stretch through a light industrial area.",
    '▲ Joan C Edward @Arsenan': '▲ Joan C Edward @Arsenan',
    '▲ Joan C Edward @Arsenan': '▲ Joan C Edward @Arsenan',
    '我喜欢我们穿过的几个社区，也喜欢看沿途的房子，我们在河边的 Harris Riverfront 公园里跑了一小段距离（希望这段路更长一些），后来绕过另一个更大的 Ritter 公园，穿过校园，终点线是在 Joan C Edward 橄榄球场上。': 'I enjoyed running through the neighborhoods and looking at the houses. We ran a short stretch through Harris Riverfront Park along the river (I wish this section had been longer), looped through the larger Ritter Park, ran past the campus, and finished on the field of Joan C. Edwards Stadium.',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Siqi': '▲ Start @Siqi',
    '对我个人来说，这一天的第一个亮点是：在第二次穿过Marshall大学校园之前，我们会接过一朵花，可以放在1970年橄榄球队的纪念碑上。': 'For me, the first highlight of the day was that before running through the Marshall campus for the second time, we were handed a white flower to place on the 1970 football team memorial.',
    '另一个亮点是：马拉松选手在终点线前，志愿者会递给我们一个橄榄球，选手们可以用一种“达阵”的方式冲过终点线，这确实挺特别的。': "Another highlight: just before the finish line, volunteers hand a football to the marathon runners, allowing them to cross the line in a 'touchdown' style. That is truly unique.",
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '比赛日，我们踩着点来到起点的绿色橄榄球场边，起点处已经聚集了很多参赛选手，主持人非常有活力，带领着大家喊：”We are ~~” “Marshall! “ “Marshall”…..': "On race day, we arrived at the starting area next to the green football field right on time. A large crowd of runners had already gathered, and the energetic announcer led the crowd in chanting: 'We are—' 'Marshall!' 'Marshall!'...",
    '▲ 《We Are Marshall》 @Google': '▲ 《We Are Marshall》 @Google',
    '《We Are Marshall》是一部基于真实故事的2006年体育剧情电影。它讲述了1971年马歇尔大学橄榄球队在1970年飞机失事中全部75名成员遇难后，努力重建的故事。': "'We Are Marshall' is a 2006 sports drama film based on a true story. It tells the story of the 1971 Marshall University football team's struggle to rebuild after all 75 members of the 1970 team perished in the plane crash.",
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Start @Arsenan': '▲ Start @Arsenan',
    '▲ Go @Arsenan': '▲ Go @Arsenan',
    '比赛终于开始了，我们1800名参赛选手伴着小城的日出向西边跑去，开始的路线是在3街，两边的房子不算多，日出的光线很好看，一点也不刺眼。': "The race finally started, and our field of 1,800 runners headed west under the morning sunrise. The initial route followed 3rd Avenue. There weren't many houses, and the sunrise cast a beautiful, gentle light.",
    '▲ Sunrise Morning @Arsenan': '▲ Sunrise Morning @Arsenan',
    '▲ Sunrise Morning @Arsenan': '▲ Sunrise Morning @Arsenan',
    '▲ Sunrise Morning @Arsenan': '▲ Sunrise Morning @Arsenan',
    '▲ 50State Club @Arsenan': '▲ 50State Club @Arsenan',
    '在这边，我还看到一个穿着50州衣服的跑者，我知道，很多跑者选择这个比赛来点亮西弗吉尼亚，赛前我还在 50State 的主页里看到有人推荐这个比赛。': 'I spotted a runner wearing a 50 States Marathon Club shirt. I knew many runners choose this race to check off West Virginia. Before the race, I had seen recommendations for this event on the 50 States Club homepage.',
    '▲ Downtown @Arsenan': '▲ Downtown @Arsenan',
    '▲ Downtown @Arsenan': '▲ Downtown @Arsenan',
    '▲ Mile-2 @Arsenan': '▲ Mile-2 @Arsenan',
    '▲ Stadium @Arsenan': '▲ Stadium @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '这段我们会经过大学区域，路边还会有穿着Marshall大学绿色衣服的一家人坐在路边，像极了小时候参加秋游的我们。': 'During this stretch, we ran through the university area. Families dressed in Marshall green sat along the curbs, reminding me of our childhood school field trips.',
    '▲ 430 Pacer @Arsenan': '▲ 430 Pacer @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '3个英里的时候，我们来到了 Harris Riverfront 公园，我太喜欢这个区域了，一看就是来自大学的志愿者们特别热情，搞得我都不好意思不喝几杯。': "Around Mile 3, we reached Harris Riverfront Park. I absolutely loved this section. The college student volunteers were incredibly enthusiastic, making me feel almost guilty if I didn't grab a few cups of water.",
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '右边就是俄亥俄河，感觉和 Louisville 不太一样，这段路很舒服，就是太短了，不过没关系，因为还要再跑3次。': 'On our right was the Ohio River. It felt different from the view in Louisville. This stretch was very pleasant, just too short. But that was fine, as we would run it three more times.',
    '▲ Mile-4 @Arsenan': '▲ Mile-4 @Arsenan',
    '▲ Restroom @Arsenan': '▲ Restroom @Arsenan',
    '▲ Virginia St @Arsenan': '▲ Virginia St @Arsenan',
    '▲ Mile-5 @Arsenan': '▲ Mile-5 @Arsenan',
    '出了公园，我们就来到了笔直的 Virginia 路，这段貌似有一点荒凉，人不多，但是路还挺宽的，阳光还是很温和，我也抓住时机，上了个厕所。': 'Exiting the park, we ran onto the straight Virginia Avenue. This section felt a bit desolate and quiet, but the road was wide, and the sun remained gentle. I took the opportunity to make a quick restroom stop.',
    '▲ Old Central City Gazebo @Arsenan': '▲ Old Central City Gazebo @Arsenan',
    '▲ Old Central City Gazebo @Arsenan': '▲ Old Central City Gazebo @Arsenan',
    '▲ Old Central City Gazebo @Arsenan': '▲ Old Central City Gazebo @Arsenan',
    '▲ Mile-6 @Arsenan': '▲ Mile-6 @Arsenan',
    '▲ Central City @ 14 STW @Arsenan': '▲ Central City @ 14 STW @Arsenan',
    '大概在5英里的时候，我们会左转来到14街，在这边会绕着 Old Central City Gazebo 来增加一点距离，然后穿过 Central City @ 14 STW，这边有一些人气。\u200d': 'Around Mile 5, we turned left onto 14th Street. The route looped around the Old Central City Gazebo to add some distance, then passed through Central City at 14th Street West, which had a bit more crowd energy.',
    '▲ Chad Pennington @Arsenan': '▲ Chad Pennington @Arsenan',
    '▲ Chad Pennington @Arsenan': '▲ Chad Pennington @Arsenan',
    '接着前面有个红色的建筑很漂亮，这是个叫查德·彭宁顿（Chad Pennington）的地方，有种砖墙建筑的复古美感。\u200d': 'Further ahead stood a beautiful red brick building named after Chad Pennington, carrying a vintage aesthetic.',
    '▲ Kiwanis Park @Arsenan': '▲ Kiwanis Park @Arsenan',
    '▲ Kiwanis Park @Arsenan': '▲ Kiwanis Park @Arsenan',
    '▲ Kiwanis Park @Arsenan': '▲ Kiwanis Park @Arsenan',
    '▲ Memorial Blvd @Arsenan': '▲ Memorial Blvd @Arsenan',
    '下面我们会跑一小段的 Kiwanis 公园，然后沿着 Memorial Blvd 和 Fourpole Creek 到达 Ritter 公园的砂地线路，虽然官方说这段路线是快速的 trail，不用担心，但我还是觉得有点滑，稍微有点用不上力。': 'Next, we ran a short stretch through Kiwanis Park, then followed Memorial Boulevard and Fourpole Creek to the dirt paths of Ritter Park. Although the organizers described this as a fast trail, it felt a bit slippery, making it hard to push off.',
    '▲ Ritter Park @Arsenan': '▲ Ritter Park @Arsenan',
    '▲ Mile-8 @Arsenan': '▲ Mile-8 @Arsenan',
    '▲ Ritter Park @Arsenan': '▲ Ritter Park @Arsenan',
    '▲ Ritter Park @Arsenan': '▲ Ritter Park @Arsenan',
    '公园的风景还是不错的，很 refresh，最后在跨过木桥后，我们终于结束了这段滑脚的砂石路面。\u200d': 'The park scenery was beautiful and refreshing. After crossing a wooden bridge, we finally finished the slippery gravel path.',
    '▲ Ritter Park @Arsenan': '▲ Ritter Park @Arsenan',
    '▲ Mile-9 @Arsenan': '▲ Mile-9 @Arsenan',
    '这会儿我们来到了13街，跑过9英里的英里牌后，前面会有一个 Army 的补给点，志愿者看到我穿了阿森纳的队服，还嘘我说阿森纳不行，切尔西才厉害。': 'Now we reached 13th Street. After passing the Mile 9 marker, there was an Army aid station. The volunteers saw me wearing my Arsenal shirt and booed, saying Arsenal was no good and Chelsea was much better.',
    '▲ Army Supply @Arsenan': '▲ Army Supply @Arsenan',
    '▲ Chelsea Guy @Arsenan': '▲ Chelsea Guy @Arsenan',
    '这个嘘我的哥们还被我的 camera 抓了个现行，兄弟！我记住你了！': "The guy who booed me was caught red-handed by my camera. Buddy, I'll remember you!",
    '▲ Turn Around @Arsenan': '▲ Turn Around @Arsenan',
    '▲ Rose Tunnel @Arsenan': '▲ Rose Tunnel @Arsenan',
    '▲ Rose Tunnel @Arsenan': '▲ Rose Tunnel @Arsenan',
    '▲ Rose Tunnel @Arsenan': '▲ Rose Tunnel @Arsenan',
    '▲ Mile-10 @Arsenan': '▲ Mile-10 @Arsenan',
    '▲ Back Harris Riverfront @Arsenan': '▲ Back Harris Riverfront @Arsenan',
    '▲ Back Harris Riverfront @Arsenan': '▲ Back Harris Riverfront @Arsenan',
    'Army补给点前面是个大转弯，需要穿过玫瑰隧道来到8街，然后一路北伐，再次来到 Harris Riverfront 公园。': 'Just past the Army station was a sharp turn. We ran through the Rose Tunnel to 8th Street, then headed north back to Harris Riverfront Park.',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @MUM': '▲ Harris Riverfront Park @MUM',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '在 Harris Riverfront 公园换了个方向往回跑\u200d，感觉风景都不一样了，志愿者们还都在，热闹的氛围丝毫不减。': "Running in the opposite direction through Harris Riverfront Park made the scenery feel completely different. The volunteers were still there, and the lively atmosphere hadn't faded at all.",
    '▲ Marshsall University @Arsenan': '▲ Marshsall University @Arsenan',
    '再次跑回市区，这会儿全马和半马的选手会分开，我们全马队伍会穿过 Marshsall 大学的校园，校园里的路线我和Siqi都很熟悉，就是我们前一天过来摆拍的地方。': 'Returning to the city streets, the marathon and half-marathon runners split up. The full marathon pack headed through the Marshall University campus—a path Siqi and I knew well from our photoshoot the day before.',
    '▲ Left Marshsall University @Arsenan': '▲ Left Marshsall University @Arsenan',
    '▲ Back Stadium @Arsenan': '▲ Back Stadium @Arsenan',
    '离开校园，体育场就在我们眼前，但和半马选手不同，我们只能目送体育馆离开，因为我们还有一半多的距离。': 'Leaving campus, the stadium stood right before us. But unlike the half-marathoners, we had to wave goodbye to it, as we still had more than half the distance left.',
    '▲ Mile-13 @Arsenan': '▲ Mile-13 @Arsenan',
    '▲ Marshsall University @Arsenan': '▲ Marshsall University @Arsenan',
    '再次绕回起点，还是第一圈的路线，我看了一眼手表，半程还不到2个小时，这超出了我的预期，并且前半程我也没有很有意的push自己，我觉得在纳什维尔立的Flag可以竖起来了。': "Looping back to the start, we repeated the first-lap route. I checked my watch: less than two hours for the half. This was better than expected, and since I hadn't pushed myself too hard in the first half, I felt my Nashville flag could finally stand.",
    '▲ Harris Riverfront Park @Arsenan': '▲ Harris Riverfront Park @Arsenan',
    '回到市区，还是熟悉的路线，我心里也有底了，对于前面的地形，我简直是了如指掌，不过还是有点不同的，第三次来到 Harris Riverfront 公园的时候，志愿者们的活力明显不如之前了，不过有补给就行。': "Returning to the city streets, the familiar route gave me confidence. I knew the terrain inside out. However, there were some changes: by the third time we reached Harris Riverfront Park, the volunteers' energy had noticeably dropped. But as long as the supplies were there, it was fine.",
    '▲ Mile-19 @Arsenan': '▲ Mile-19 @Arsenan',
    '我这会儿的预期完赛时间是有超出4小时的pacer的，我想那就按照4小来吧，冲一把。': 'By then, my projected finish time was ahead of the 4-hour pacer. I decided to stick to the sub-4 goal and give it a push.',
    '▲ Chad Pennington @Arsenan': '▲ Chad Pennington @Arsenan',
    '▲ Chad Pennington @Arsenan': '▲ Chad Pennington @Arsenan',
    '▲ Chad Pennington @Arsenan': '▲ Chad Pennington @Arsenan',
    '我的配速很稳，一晃就来到了19英里，大红房子在变强的阳光下，又有了不一样的样子，阳光把我的脸晒得也很有光泽，气色不错。': 'My pace was steady, and in a flash, I reached Mile 19. The red brick building looked different under the stronger sunlight. The sun lit up my face, and I looked in good shape.',
    '▲ Kiwanis Park @Arsenan': '▲ Kiwanis Park @Arsenan',
    '补给还是要吃的，不能说为了省下那几秒就错过补给点，我突然发现好久没这么认真跑步了，我一直计算着时间， 20英里， 21英里…..': "I made sure to grab supplies; you can't skip aid stations just to save a few seconds. I realized it had been a while since I ran so seriously. I kept calculating the time: Mile 20, Mile 21...",
    '▲ Mile-20 @Arsenan': '▲ Mile-20 @Arsenan',
    '▲ Mile-21 @Arsenan': '▲ Mile-21 @Arsenan',
    '▲ Fourpole Creek @Arsenan': '▲ Fourpole Creek @Arsenan',
    '再次回到Army补给点的时候，我还和刚才的切尔西的小哥 Battle 了一下，我说阿森纳是最棒的，这会儿，他们也要收摊了。': 'When I returned to the Army aid station, I had another friendly battle with the Chelsea guy. I yelled that Arsenal was the best. By then, they were already packing up.',
    '▲ Army Water Station @Arsenan': '▲ Army Water Station @Arsenan',
    '▲ Army Water Station @Arsenan': '▲ Army Water Station @Arsenan',
    '再次回到玫瑰隧道，下隧道的下坡并不容易，上隧道的上坡更是一点也不轻松，随着英里数的增加，疲劳感也一点点涌了过来。': "Returning to the Rose Tunnel, the downhill slope wasn't easy, and the uphill climb was even tougher. As the miles piled up, fatigue began to set in.",
    '▲ Turn Around @Arsenan': '▲ Turn Around @Arsenan',
    '▲ Rose Tunnel @Arsenan': '▲ Rose Tunnel @Arsenan',
    '▲ Back @Arsenan': '▲ Back @Arsenan',
    '我不错过每一个补给点，也计算着时间和补充能量胶的时机，在临近 Harris Riverfront 公园的1街上，我还要了一杯可乐。': "I didn't miss a single aid station, calculating my time and gel intake. As we neared Harris Riverfront Park on 1st Street, I grabbed a cup of Coke.",
    '▲ Cole Station @Arsenan': '▲ Cole Station @Arsenan',
    '这会儿的 Harris Riverfront 公园都没啥人了，不过还是有水留给我们，城市的阳光也足了起来，我的配速也有点掉了下来，不过前面我跟的很好，还容得了我稍微挥霍一下，破4的希望还很大。': 'By now, Harris Riverfront Park was nearly empty of spectators, but there was still water left for us. The sun had grown intense, and my pace dropped a bit. However, I had built up enough of a cushion earlier to afford a slight slowdown. The hope of breaking 4 hours was still very strong.',
    '▲ Harris Riverfront @Arsenan': '▲ Harris Riverfront @Arsenan',
    '▲ Mile-25 @Arsenan': '▲ Mile-25 @Arsenan',
    '▲ Back @Arsenan': '▲ Back @Arsenan',
    '第二次来到 Marshall 大学，志愿者在校门口送给我们每位跑者一朵花，以用来纪念1970的罹难者，但我当时没有领会到这样的深意，还有就是跑得也确实有点累了，手里的花也不知道放哪儿，就是觉得挺不方便的，我就送给了路边的志愿者，现在想想，也确实是这次比赛时的一个遗憾。': "Entering the Marshall campus for the second time, volunteers at the gate handed each runner a flower to honor the 1970 victims. I didn't fully grasp the depth of the gesture at the time, and being exhausted, I didn't know where to put it. Finding it inconvenient, I gave it to a volunteer along the road. Looking back, that was a real regret of this race.",
    '▲ Marshall University @Arsenan': '▲ Marshall University @Arsenan',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '▲ Marshall University @MUM': '▲ Marshall University @MUM',
    '离开大学校园，我们即将跑回绿色的 Joan C Edward 橄榄球场，我一直盯着我的手表，破4不破4真的只是一念之间，我想那就冲一把吧，气氛都烘托到这了。': 'Leaving the campus, we were about to run back onto the turf of Joan C. Edwards Stadium. I kept staring at my watch; breaking 4 hours was down to a split-second decision. I decided to sprint—the atmosphere was set.',
    '▲ Joan C Edward Stadium @Arsenan': '▲ Joan C Edward Stadium @Arsenan',
    '▲ Touchdown @Arsenan': '▲ Touchdown @Arsenan',
    '▲ Touchdown @Arsenan': '▲ Touchdown @Arsenan',
    '▲ Touchdown @Arsenan': '▲ Touchdown @Arsenan',
    '刚进体育场，志愿者就给了我一个橄榄球，我旁边穿蓝色衣服的跑者抱着橄榄球跑的飞快，这也激发起了我的斗志，趁他在终点前摆 pose 的机会，我轻松超过了他，也顺利地把我的排名提升了一位。': 'Just as I entered the stadium, a volunteer handed me a football. The runner in blue next to me was sprinting with his football, which triggered my competitive spirit. While he paused to pose near the finish line, I easily passed him, gaining one last position.',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '▲ Touchdown @MUM': '▲ Touchdown @MUM',
    '一看手表，3小时58分钟，后来看官方成绩，确认了我成功破4，说实话，真的挺意外的。': 'I looked at my watch: 3 hours and 58 minutes. Later, the official results confirmed I had successfully broken 4 hours. Honestly, it was a pleasant surprise.',
    '▲ Return Ball @Arsenan': '▲ Return Ball @Arsenan',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '▲ Done @Arsenan': '▲ Done @Arsenan',
    '▲ Finish @Arsenan': '▲ Finish @Arsenan',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '归还了橄榄球，接过奖牌，我站在橄榄球场的广告牌边观看其他的参赛选手”达阵“，也没有觉得很累，这会儿就连蝴蝶都凑过来给我祝贺，心情很舒畅。': "After returning the football and receiving my medal, I stood by the stadium billboard watching other runners score their 'touchdowns.' I didn't feel too exhausted, and even a butterfly hovered around to congratulate me. I felt extremely happy.",
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '▲ Runner @Arsenan': '▲ Runner @Arsenan',
    '▲ Medal Time @Runner Above': '▲ Medal Time @Runner Above',
    '▲ Medal Time @Runner': '▲ Medal Time @Runner',
    'Siqi也完赛了，正在外面吃好吃的，她听到我这么快就完事了也挺意外的。随后我们在体育场拍了几个合影，我还在赛后的拉伸区排队让志愿者给我做了拉伸，很棒，然后我们又到体育场外拍了几个照片，随后心满意足地去 Planet Fitness 洗澡。': 'Siqi finished the race as well and was outside eating some treats. She was surprised that I finished so quickly. We took some photos in the stadium, and I queued at the recovery area to get stretched by a volunteer, which was great. Then we took some photos outside the stadium and headed happily to Planet Fitness to shower.',
    '▲ Massage @Siqi': '▲ Massage @Siqi',
    '▲ Massage @Siqi': '▲ Massage @Siqi',
    '▲ Massage @Siqi': '▲ Massage @Siqi',
    '▲ Leave @Siqi': '▲ Leave @Siqi',
    '▲ Medal Time @Runner': '▲ Medal Time @Runner',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Siqi @Arsenan': '▲ Siqi @Arsenan',
    '▲ Stadium @Arsenan': '▲ Stadium @Arsenan',
    '▲ Stadium @Arsenan': '▲ Stadium @Arsenan',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Siqi': '▲ Medal Time @Siqi',
    '▲ Medal Time @Arsenan': '▲ Medal Time @Arsenan',
    '体育场里的DJ声还在一轮接着一轮此起彼伏，参赛选手们还在陆陆续续地完赛，只是随着车子的远去，这声音变得越来越微弱，直到最后什么也听不到了 … 车子开出越来越远，但这场马拉松带给我的冲击却还是如此的强烈。': "The stadium DJ's music echoed in waves, and runners were still crossing the finish line. But as our car drove away, the sounds grew fainter until everything went silent. The car drove further and further, but the impact of this marathon remained incredibly strong.",
    '▲ Arsenal @Arsenan': '▲ Arsenal @Arsenan',
    '▲ Huntington @Arsenan': '▲ Huntington @Arsenan',
    '▲ Huntington @Arsenan': '▲ Huntington @Arsenan',
    '▲ Planet Fitness @Arsenan': '▲ Planet Fitness @Arsenan',
    '后记': 'Epilogue',
    '回去的路上，我们再次经停列克星敦，Siqi 请我吃了一顿韩国自助火锅 K-Pot，说是庆祝我破4，这个火锅味道还挺好的，听说路城也要开一家。': 'On the way back, we stopped in Lexington again. Siqi treated me to a Korean hotpot buffet at K-Pot to celebrate my sub-4 finish. The hotpot tasted great, and I heard they are planning to open a location in Louisville.',
    '▲ K-Pot @Arsenan': '▲ K-Pot @Arsenan',
    '▲ K-Pot @Arsenan': '▲ K-Pot @Arsenan',
    '▲ K-Pot @Arsenan': '▲ K-Pot @Arsenan',
    '▲ K-Pot @Arsenan': '▲ K-Pot @Arsenan',
    '回家的时候，晚霞染红了I-64的天际，挺漂亮的。我也有点膨胀，心想：好久没有认真跑步了，没想到，稍微一认真，就破4了，看来还是有天赋有实力的选手啊，达标波士顿只是时间问题了。（可以变快，也可以变老）': 'As we headed home, the evening glow painted the horizon along I-64. It was beautiful. I felt a bit proud, thinking: it had been a long time since I ran seriously, and yet with just a little effort, I broke 4 hours. It seems I am a talented and capable runner after all, and qualifying for Boston is only a matter of time. (You can get faster, or you can get older.)',
    '▲ I-64 @Arsenan': '▲ I-64 @Arsenan',
    '当然有信心是好事，但我还不想每次都全力以赴，快有快的刺激，慢有慢的情调，这种变换的节奏可能才更有意思一点。': "Of course, having confidence is good, but I don't want to go all out every time. Fast running has its thrill, while slow running has its own charm. This shifting rhythm is probably more interesting.",
    '更重要的是保持健康和自律，我也不想受伤，跑了这么多年步，我比谁都了解我自己的身体，跑步是一辈子的事，也不急于这一时。': "More importantly, I want to stay healthy and disciplined. I don't want to get injured. Having run for so many years, I know my body better than anyone. Running is a lifelong journey, so there is no rush.",
    '- 本文完 -': '- The end -',
    '文字丨Arsenan': 'Words | Arsenan',
    '摄影丨Arsenan': 'Photos | Arsenan',
    '设计丨Arsenan': 'Design | Arsenan',
    '时隔五年，再破四小时': 'After five years, breaking 4 hours again.',
    '西弗吉尼亚州，亨廷顿': 'West Virginia, Huntington',
    '19周年，马歇尔大学马拉松': '19th Anniversary, Marshall University Marathon',
    '# 西弗吉尼亚州，亨廷顿': '# West Virginia: Huntington 🏈 Tri-State Confluence',
    '# 19周年，马歇尔大学马拉松': '# Marshall University Marathon: 19th Anniversary 🏈 Huntington, West Virginia',
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def should_skip_text(text: str) -> bool:
    return text in {"★", "★★", "★★★", "★★★★"}


def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    root = doc.xpath('//*[@id="js_content"]')[0]
    events = []

    def walk(el):
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src:
                events.append({"type": "img", "src": src})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if text not in ["，赞"] and not text.startswith("鲜花"):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src:
                        events.append({"type": "img", "src": src})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    clean = []
    for idx, event in enumerate(events):
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1][1]["type"], clean[-1][1].get("text") or clean[-1][1].get("src")) if clean else None
        if prev != key:
            clean.append((idx, event))

    return clean


def local_source_path(src: str) -> Path:
    normalized = src[2:] if src.startswith("./") else src
    return SOURCE_BASE / normalized


def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for _, event in indexed:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        src_path = local_source_path(event["src"])
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=82)
    return count


def render_article(indexed, lang, img_prefix):
    is_zh = lang == "zh"
    blocks = []
    img_idx = 0
    for idx, event in indexed:
        if event["type"] == "img":
            img_idx += 1
            # For en/facebook, references chinese image folder relative to their location
            src = f"{img_prefix}img-{img_idx:03d}.webp"
            # look ahead for caption
            caption = ""
            for next_idx in range(indexed.index((idx, event)) + 1, len(indexed)):
                next_event = indexed[next_idx][1]
                if next_event["type"] == "text":
                    if is_caption(next_event["text"]):
                        txt = next_event["text"]
                        if not is_zh and txt in EN_BY_INDEX:
                            txt = EN_BY_INDEX[txt]
                        caption = txt
                    break
                elif next_event["type"] == "img":
                    break
            
            blocks.append(f'''      <figure>
        <img src="{src}" alt="West Virginia Marathon image {img_idx}" loading="lazy" decoding="async">''')
            if caption:
                blocks.append(f'        <figcaption>{escape(caption)}</figcaption>')
            blocks.append('      </figure>')
        
        elif event["type"] == "text":
            txt = event["text"]
            if not is_zh and txt in EN_BY_INDEX:
                txt = EN_BY_INDEX[txt]
            
            if is_caption(event["text"]) or should_skip_text(event["text"]):
                continue
            
            if txt.startswith("丨"):
                # Channel title tag
                continue
            elif txt.startswith("# "):
                # Heading 1
                blocks.append(f'      <h2 class="section-label">{escape(txt[2:])}</h2>')
            elif txt.startswith("## "):
                # Heading 2
                blocks.append(f'      <h3>{escape(txt[3:])}</h3>')
            elif txt.startswith("- 本文完 -") or txt.startswith("- The end -"):
                blocks.append(f'      <p class="end-mark">{escape(txt)}</p>')
            elif txt.startswith("文字丨") or txt.startswith("摄影丨") or txt.startswith("设计丨") or txt.startswith("Words |") or txt.startswith("Photos |") or txt.startswith("Design |"):
                blocks.append(f'      <p class="credit-line">{escape(txt)}</p>')
            else:
                blocks.append(f'      <p>{escape(txt)}</p>')
                
    return "\n".join(blocks)


def page_css() -> str:
    return """
    :root {
      --paper: #f4f6f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #dde5ec;
      --river: #0e7490;
      --brick: #a33a2b;
      --gold: #b7892f;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eef5f6 0, var(--paper) 320px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.7;
    }
    a { color: var(--river); text-decoration-thickness: 1px; text-underline-offset: 4px; }
    .story-nav {
      max-width: 860px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      color: var(--muted);
      font-size: 14px;
    }
    .story-nav a {
      color: inherit;
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }
    .story-nav a:hover { border-color: currentColor; }
    .page-header {
      max-width: 860px;
      margin: 0 auto;
      padding: 42px 22px 24px;
    }
    .kicker { margin: 0 0 14px; color: var(--brick); font-size: 14px; font-weight: 800; }
    h1 {
      margin: 0;
      max-width: 780px;
      color: #111827;
      font-size: 34px;
      line-height: 1.22;
      font-weight: 850;
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 18px;
      color: var(--muted);
      font-size: 14px;
    }
    .meta span,
    .meta a {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .72);
      color: var(--muted);
      text-decoration: none;
    }
    .dek {
      margin: 22px 0 0;
      padding-left: 16px;
      border-left: 4px solid var(--river);
      color: #344054;
      font-size: 15px;
    }
    .article-shell {
      background: var(--surface);
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
    }
    .article-body {
      max-width: 720px;
      margin: 0 auto;
      padding: 54px 22px 64px;
    }
    .article-body p {
      margin: 0 0 22px;
      font-size: 17.5px;
      line-height: 1.8;
      color: #2c323f;
    }
    .article-body h2.section-label {
      margin: 48px 0 20px;
      padding-top: 24px;
      border-top: 1px solid var(--line);
      color: var(--brick);
      font-size: 21px;
      font-weight: 800;
    }
    .article-body h3 {
      margin: 32px 0 16px;
      color: #111827;
      font-size: 19px;
      font-weight: 800;
    }
    figure {
      margin: 32px 0;
    }
    figure img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 4px;
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
      font-size: 14px;
    }
    .end-mark {
      margin: 48px 0 12px;
      font-weight: 700;
    }
    .credit-line { margin: 6px 0; }
    .page-footer {
      max-width: 860px;
      margin: 0 auto;
      padding: 42px 22px 64px;
      color: var(--muted);
      font-size: 14px;
      text-align: center;
    }
    """


def facebook_css() -> str:
    return """
    :root {
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --red: #0b67c2;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #f8fafc;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.62;
    }
    a { color: var(--red); text-decoration: none; }
    .breaking {
      background: var(--ink);
      color: #ffffff;
      padding: 10px 22px;
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    .breaking-inner {
      max-width: 1180px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
    }
    .breaking-inner a { color: inherit; }
    .site-head {
      background: #ffffff;
      border-bottom: 3px solid var(--red);
    }
    .site-head-inner {
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .wordmark {
      font-size: 28px;
      font-weight: 900;
      color: var(--ink);
      letter-spacing: -.03em;
      text-decoration: none;
    }
    .section-nav {
      display: flex;
      gap: 18px;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .section-nav a { color: var(--muted); }
    .section-nav a:hover { color: var(--red); }
    .article {
      max-width: 1180px;
      margin: 0 auto;
      padding: 42px 22px 64px;
    }
    .hero {
      margin-bottom: 34px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 34px;
    }
    .label {
      color: var(--red);
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    h1 {
      margin: 12px 0 16px;
      font-size: clamp(30px, 5vw, 48px);
      line-height: 1.1;
      font-weight: 900;
      letter-spacing: -.02em;
    }
    .dek {
      margin: 0 0 24px;
      font-size: clamp(17px, 3vw, 21px);
      line-height: 1.45;
      color: var(--muted);
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .lead-media {
      margin: 30px 0 0;
    }
    .lead-media img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
    }
    .lead-media figcaption {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      font-style: italic;
    }
    .story-grid {
      display: grid;
      grid-template-columns: minmax(220px, 300px) minmax(0, 720px);
      gap: 34px;
      align-items: start;
      padding: 34px 0 12px;
    }
    .rail {
      position: sticky;
      top: 18px;
      display: grid;
      gap: 18px;
    }
    .brief-box,
    .share-note,
    .context-note,
    .section-bridge {
      border: 1px solid var(--line);
      padding: 18px;
    }
    .brief-box {
      border: 0;
      border-top: 5px solid var(--red);
      background: var(--soft);
      padding: 16px;
    }
    .brief-box h2,
    .section-bridge h2 {
      margin: 0 0 12px;
      font-size: 19px;
      line-height: 1.1;
    }
    dl { margin: 0; display: grid; gap: 12px; }
    dt {
      color: var(--red);
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    dd {
      margin: 2px 0 0;
      color: #222222;
      font-size: 14px;
      line-height: 1.45;
    }
    .share-note {
      color: #333333;
      font-size: 14px;
      line-height: 1.6;
    }
    .share-note strong {
      display: block;
      color: var(--ink);
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: .08em;
      margin-bottom: 6px;
    }
    .copy {
      min-width: 0;
    }
    .copy p {
      margin: 0 0 19px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 19px;
      line-height: 1.72;
    }
    .copy h2 {
      margin: 36px 0 16px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      font-size: 30px;
      line-height: 1.1;
      letter-spacing: 0;
    }
    .copy h3 {
      margin: 24px 0 12px;
      font-size: 22px;
      line-height: 1.25;
      font-weight: 800;
    }
    .copy .section-label {
      color: var(--red);
      font-size: 13px;
      font-family: Arial, Helvetica, sans-serif;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }
    .copy .place {
      margin: 0 0 18px;
      color: var(--red);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .copy figure {
      margin: 25px 0 30px;
    }
    .copy figure img {
      display: block;
      width: 100%;
      border: 1px solid var(--line);
      background: var(--soft);
    }
    .context-note,
    .section-bridge {
      margin: 0 0 28px;
    }
    .context-note {
      padding: 18px 0 18px 18px;
      border: 0;
      border-left: 7px solid var(--red);
      background: #fafafa;
    }
    .context-note p,
    .section-bridge p {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 16px;
      line-height: 1.65;
    }
    .section-bridge {
      margin: 40px 0 26px;
      border: 0;
      border-top: 5px solid var(--red);
      background: #f7f7f7;
    }
    .section-bridge h2 {
      margin: 0 0 10px;
      padding: 0;
      border: 0;
      font-size: 24px;
    }
    .context-note p:last-child,
    .section-bridge p:last-child {
      margin-bottom: 0;
    }
    .copy hr {
      width: 74px;
      height: 5px;
      margin: 34px 0;
      border: 0;
      background: var(--red);
    }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
    }
    .zz-engagement {
      max-width: 1180px;
      padding-left: 0;
      padding-right: 0;
    }
    .zz-engagement-kicker,
    .zz-engagement h2 {
      color: var(--red);
    }
    @media (max-width: 820px) {
      .story-grid { grid-template-columns: 1fr; }
      .rail { position: static; }
    }
    @media (max-width: 860px) {
      .site-head-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 16px 0;
      }
      .section-nav {
        justify-content: flex-start;
      }
    }
    """


def engagement(locale: str, page_key: str, mount_id: str) -> str:
    is_zh = locale == "zh-CN"
    kicker = "留言 / 阅读" if is_zh else "Comments / Views"
    title = "跑完也可以聊两句" if is_zh else "Say something after the run"
    note = "不用登录就可以留言，新留言会直接显示。" if is_zh else "No account is needed to submit a comment. New comments appear right away."
    loading = "留言区加载中..." if is_zh else "Loading comments..."
    views = "阅读" if is_zh else "Views"
    return f'''
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{escape(kicker)}</p>
        <h2>{escape(title)}</h2>
        <p class="zz-engagement-note">{escape(note)}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{escape(views)}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{mount_id}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{escape(loading)}</p></div>
    </div>
  </section>'''


def normal_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = "Run50 #第13州｜西弗吉尼亚：马歇尔大学马拉松｜抱着橄榄球达阵，在乡村路跑进四小时！" if is_zh else "Run50 #13 | West Virginia: Marshall University Marathon"
    short = "Run50 #13 | Marshall University Marathon"
    desc = (
        "十一月初的西弗吉尼亚亨廷顿，在秋高气爽的马歇尔大学校园，将一朵花送给1970年空难的离世队员们；在终点抱着橄榄球“达阵”冲线，成功破4！"
        if is_zh
        else "Race date: November 5, 2023. Running U.S. State 13: Marshall University Marathon in Huntington, West Virginia, featuring a stadium finish with a football touchdown, placing a white flower on the 1970 sports tragedy memorial, and achieving a sub-4 hour PR."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    kicker = "Run50 #第13州 · 西弗吉尼亚" if is_zh else "Run50 #13 · West Virginia"
    footer = "© 2023-2026 ArsenanZZ. Built with love."
    locale = "zh-CN" if is_zh else "en"
    key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    mount = f"supabase-comments-west-virginia-zh" if is_zh else f"supabase-comments-west-virginia-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{locale}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:secure_url" content="{og_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="West Virginia Marathon cover with Appalachian mountains, country road and a football.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-11-05T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav" aria-label="页面导航">
    {nav}
  </nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">
      <span>By Arsenan</span>
      <span>Race: November 5, 2023</span>
    </div>
    <div class="dek">{escape(desc)}</div>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
  </main>
  {engagement(locale, key, mount)}
  <footer class="page-footer">{escape(footer)}</footer>
  <script src="../../../assets/zz-engagement-config.js?v={VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={VERSION}"></script>
</body>
</html>
'''


def facebook_page(content: str) -> str:
    title = "I ran West Virginia's university marathon for a stadium finish, scored a touchdown to break 4 hours, and paid my respects to a local tragedy"
    desc = "Race date: November 5, 2023. Running U.S. State 13: Marshall University Marathon in Huntington, West Virginia, featuring a stadium finish with a football touchdown, placing a white flower on the 1970 sports tragedy memorial, and achieving a sub-4 hour PR."
    canonical = f"{SITE}/run50/facebook/{SLUG}.html"
    locale = "en"
    key = f"run50-{SLUG}-facebook-en"
    mount = f"supabase-comments-west-virginia-facebook-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Marshall University Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:secure_url" content="{og_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="West Virginia Marathon cover with Appalachian mountains, country road and a football.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-11-05T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={VERSION}">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="breaking">
    <div class="breaking-inner">
      <a href="./index.html">Run50 Facebook</a>
      <span>Race date: November 5, 2023</span>
    </div>
  </div>
  <header class="site-head">
    <div class="site-head-inner">
      <a class="wordmark" href="./index.html" aria-label="Run50 Facebook home">RUN50 WORLD</a>
      <nav class="section-nav" aria-label="Story navigation">
        <a href="../index.html">Run50</a>
        <a href="../stories/english/{SLUG}.html">Full English Story</a>
        <a href="../stories/chinese/{SLUG}.html">Chinese Original</a>
      </nav>
    </div>
  </header>
  <article class="article">
    <section class="hero">
      <span class="label">World / USA / Marathon</span>
      <h1>{escape(title)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline">
        <span>By Arsenan</span>
        <span>Race: November 5, 2023</span>
        <span>Huntington, WV</span>
        <span>Run50 #13</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="Icon-style West Virginia Marathon cover"><figcaption>West Virginia icon cover with Appalachian mountains, winding country road and a football.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Marshall University Marathon, Run50 State 13.</dd></div><div><dt>Course</dt><dd>Huntington downtown, Ohio riverfront paths, central neighborhoods, and a stadium finish inside the Joan C. Edwards Stadium.</dd></div><div><dt>What stayed with me</dt><dd>Country Roads morning sunrise, the 1970 football team memorial flower tribute, running past local homes, and carrying a football touchdown at the finish line to secure a sub-4 hour PR.</dd></div></dl></section>
      </aside>
      <div class="copy full-story">
        {content}
      </div>
    </section>
  </article>
  {engagement("en", key, mount)}
  <script src="../../assets/zz-engagement-config.js?v={VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={VERSION}"></script>
</body>
</html>
'''


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">West Virginia Marathon icon cover</title>
<desc id="desc">Icon style cover with West Virginia title, Run50 badge, Appalachian mountains, winding country road, and football.</desc>
<rect width="1200" height="750" fill="#fffbeb"/>
<g transform="translate(70 104)">
  <text x="0" y="0" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">W. VIRGINIA</text>
  <text x="0" y="46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#0b67c2">MOUNTAINS · COUNTRY ROADS · FOOTBALL</text>
</g>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #13</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">W. VIRGINIA</text>

<!-- Sun -->
<circle cx="250" cy="350" r="50" fill="#f97316"/>

<!-- Layered Appalachian Mountains -->
<path d="M0 520 Q200 420 450 490 T900 460 T1200 480 L1200 750 L0 750 Z" fill="#a7f3d0"/>
<path d="M0 560 Q300 470 650 540 T1200 510 L1200 750 L0 750 Z" fill="#34d399"/>
<path d="M0 600 Q450 520 850 580 T1200 550 L1200 750 L0 750 Z" fill="#10b981"/>
<path d="M0 650 Q600 600 1200 620 L1200 750 L0 750 Z" fill="#047857"/>

<!-- Winding Country Road -->
<path d="M450 750 C540 680 575 630 590 580 L610 580 C625 630 650 680 750 750 Z" fill="#374151" stroke="#20242b" stroke-width="4"/>
<path d="M600 750 C580 700 570 630 600 580" fill="none" stroke="#fbbf24" stroke-dasharray="15 10" stroke-width="4"/>

<g transform="translate(860, 540) rotate(15)">
  <ellipse cx="50" cy="50" rx="90" ry="60" fill="#78350f" stroke="#20242b" stroke-width="7"/>
  <!-- Laces -->
  <line x1="-15" y1="50" x2="115" y2="50" stroke="#ffffff" stroke-width="8"/>
  <line x1="10" y1="35" x2="10" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="30" y1="35" x2="30" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="50" y1="35" x2="50" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="70" y1="35" x2="70" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="90" y1="35" x2="90" y2="65" stroke="#ffffff" stroke-width="6"/>
  <!-- End stripes -->
  <path d="M-10 20 Q-25 50 -10 80" fill="none" stroke="#ffffff" stroke-width="8"/>
  <path d="M110 20 Q125 50 110 80" fill="none" stroke="#ffffff" stroke-width="8"/>
</g>
</svg>
"""


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except IOError:
        try:
            return ImageFont.truetype("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf", size)
        except IOError:
            return ImageFont.load_default()


def write_clean(path: Path, text: str):
    path.write_text(text, encoding="utf-8", newline="\n")


def write_svg():
    write_clean(REPO / "assets" / f"thumb-run50-{SLUG}-icons.svg", SVG)


def write_png():
    image = Image.new("RGB", (1200, 630), "#fffbeb")
    draw = ImageDraw.Draw(image)
    text_color = "#20242b"
    blue = "#0b67c2"
    
    # Title
    draw.text((64, 64), "W. VIRGINIA", font=font(66, True), fill=text_color)
    draw.text((66, 136), "MOUNTAINS · COUNTRY ROADS · FOOTBALL", font=font(26, True), fill=blue)
    
    # Badge Box
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text_color, width=7)
    draw.text((790, 112), "Run50 #13", font=font(40, True), fill=text_color)
    draw.text((790, 166), "W. VIRGINIA", font=font(50, True), fill=blue)
    
    # Sun
    draw.ellipse((200, 290, 300, 390), fill="#f97316")
    
    # Layered Mountains (simplified polygon vertices approximating the SVG curves)
    draw.polygon([(0, 630), (0, 450), (200, 380), (450, 430), (700, 390), (950, 440), (1200, 400), (1200, 630)], fill="#a7f3d0")
    draw.polygon([(0, 630), (0, 480), (300, 420), (650, 480), (900, 430), (1200, 460), (1200, 630)], fill="#34d399")
    draw.polygon([(0, 630), (0, 510), (450, 460), (850, 510), (1200, 480), (1200, 630)], fill="#10b981")
    draw.polygon([(0, 630), (0, 550), (600, 510), (1200, 530), (1200, 630)], fill="#047857")
    
    # Winding Country Road
    draw.polygon([(450, 630), (540, 570), (575, 530), (590, 510), (610, 510), (625, 530), (650, 570), (750, 630)], fill="#374151", outline=text_color, width=2)
    
    # Dashed yellow center line (drawn in segments for thickness gradient/fade)
    draw.line([(600, 630), (598, 600)], fill="#fbbf24", width=4)
    draw.line([(596, 580), (598, 550)], fill="#fbbf24", width=3)
    draw.line([(599, 535), (600, 515)], fill="#fbbf24", width=2)
    
    # Football
    fb_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    fb_draw = ImageDraw.Draw(fb_img)
    fb_draw.ellipse((10, 40, 190, 160), fill="#78350f", outline="#20242b", width=7)
    # Laces
    fb_draw.line((10, 100, 190, 100), fill="#ffffff", width=8)
    for lx in range(40, 170, 24):
        fb_draw.line((lx, 80, lx, 120), fill="#ffffff", width=6)
    # Stripes
    fb_draw.arc((10, 50, 60, 150), 90, 270, fill="#ffffff", width=8)
    fb_draw.arc((140, 50, 190, 150), 270, 90, fill="#ffffff", width=8)
    
    # Rotate football by 15 degrees
    rotated_fb = fb_img.rotate(15, resample=Image.Resampling.BICUBIC)
    image.paste(rotated_fb, (840, 420), rotated_fb)
    
    image.save(REPO / "assets" / f"og-run50-{SLUG}-icons.png", "PNG")


def update_indexes():
    new_card_zh = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="西弗吉尼亚马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">西弗吉尼亚亨廷顿 · 2023.11.05</p>
          <h2 class="story-title">Run50 #第13州｜西弗吉尼亚马拉松</h2>
          <p class="story-desc">十一月初的西弗吉尼亚亨廷顿，在秋高气爽的马歇尔大学校园，将一朵花送给1970年空难的离世队员们；在终点抱着橄榄球“达阵”冲线，成功破4！</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
    </section>'''

    new_card_en = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon cover for West Virginia Marathon" />
        <div class="story-card-content">
          <div class="meta">West Virginia · Huntington · 2023.11.05</div>
          <h2>Marshall University Marathon: scoring a football touchdown in West Virginia</h2>
          <p>Running U.S. State 13 quest under the autumn sunshine, honoring the 1970 sports plane tragedy memorial on campus, and scoring a touchdown at the finish line inside the football stadium to break 4 hours.</p>
        </div>
      </a>
    </section>'''

    new_card_fb = f'''    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>West Virginia gave me a touchdown stadium finish to break 4 hours</h2>
        <p>Race date: November 5, 2023. Running U.S. State 13 at Marshall University in Huntington, WV. A beautiful autumn loop race with a football stadium finish, placing a flower on the 1970 team plane crash memorial, and a PR.</p>
        <div class="meta">
          <span>Huntington, WV</span>
          <span>touchdown secured</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon-style West Virginia Marathon cover">
    </a>
  </main>'''

    # Update Chinese index
    zh_idx_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    zh_text = zh_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in zh_text:
        zh_text = zh_text.replace("    </section>", new_card_zh)
        write_clean(zh_idx_path, zh_text)

    # Update English index
    en_idx_path = REPO / "run50" / "stories" / "english" / "index.html"
    en_text = en_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in en_text:
        en_text = en_text.replace("    </section>", new_card_en)
        write_clean(en_idx_path, en_text)

    # Update Facebook index
    fb_idx_path = REPO / "run50" / "facebook" / "index.html"
    fb_text = fb_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in fb_text:
        fb_text = fb_text.replace("  </main>", new_card_fb)
        write_clean(fb_idx_path, fb_text)


def main():
    zh_path = REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html"
    en_path = REPO / "run50" / "stories" / "english" / f"{SLUG}.html"
    fb_path = REPO / "run50" / "facebook" / f"{SLUG}.html"

    print("Extracting raw story blocks...")
    indexed_story = extract_story()
    
    print("Processing and copying WebP images...")
    img_count = copy_story_images(indexed_story)
    print(f"Copied {img_count} optimized WebP images.")

    print("Rendering Chinese Page...")
    zh_article = render_article(indexed_story, "zh", f"Run50-West-Virginia-Marathon-clean_files/")
    write_clean(zh_path, normal_page("zh", zh_article))

    print("Rendering English Page...")
    en_article = render_article(indexed_story, "en", f"../chinese/Run50-West-Virginia-Marathon-clean_files/")
    write_clean(en_path, normal_page("en", en_article))

    print("Rendering Facebook Page...")
    fb_article = render_article(indexed_story, "en", f"../stories/chinese/Run50-West-Virginia-Marathon-clean_files/")
    write_clean(fb_path, facebook_page(fb_article))

    print("Generating SVG Thumbnail Cover...")
    write_svg()

    print("Generating PNG OpenGraph Cover...")
    write_png()

    print("Registering cards on Listing Indexes...")
    update_indexes()

    print("Done! West Virginia Marathon story successfully published.")


if __name__ == "__main__":
    main()
