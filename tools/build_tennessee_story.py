from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-12-TN")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "nashville-marathon"
VERSION = "20260605-1"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-Nashville-Marathon-clean_files"

TRANSLATIONS_MAP = {
    '丨TENNESSEE丨': '丨TENNESSEE丨',
    '前言': 'Preface',
    '上周二，我和合作课题组，位于田纳西范德彪大学（Vanderbilt University）的黑人小姑娘Gloria开zoom会议，我们讨论了一些关于模型设计和数值仿真的细节，还有几个公式的含义，挺无聊的。': 'Last Tuesday, I had a Zoom meeting with Gloria, a young Black researcher from our collaborating group at Vanderbilt University in Tennessee. We discussed details about model design, numerical simulation, and the meaning of a few formulas—pretty boring stuff.',
    '聊完了这些生涩的技术细节后，我寻思简单唠几句家常吧，因为这是个小会，老板们都不在，就比较随意。': "Once we wrapped up those dry technical details, I thought it would be nice to have some casual chit-chat. Since it was just a small meeting and the bosses weren't around, the vibe was quite relaxed.",
    '然后我就很自然地扯到我十月底跑的纳什维尔马拉松，在那么一瞬间，我发现小姑娘的眼睛一下子就亮了起来，她说她也计划和她的朋友一起跑四月份的纳什维尔Rock’n Roll半马，还问我跑了半马还是全马，好玩么？空气一下子就快活了起来。': "Then, I naturally brought up the Nashville Marathon I ran at the end of October. In that split second, I saw her eyes light up. She said she was planning to run the Nashville Rock 'n' Roll Half Marathon in April with her friends, and asked if I did the half or the full, and whether it was fun. The atmosphere instantly became lively and cheerful.",
    '最后，我们的会议在笑声中结束，我也祝她圣诞假期快乐，明年四月跑步好运。': 'In the end, our meeting concluded with laughter. I wished her a happy Christmas holiday and good luck with her run next April.',
    '我突然就发现这个关于城市和马拉松的社交属性真不错！简直破冰神器。我也有兴趣继续补全今年的时间线，在芝加哥之后，聊聊纳什维尔，聊聊这个我今年跑的最慢的——田纳西州纳什维尔马拉松（Run Nash）': "I suddenly realized how great the social aspect of cities and marathons is! It is the ultimate icebreaker. I'm also keen to keep filling in my timeline for this year. After Chicago, let's talk about Nashville—and about the slowest run I had this year: the Nashville Marathon in Tennessee (Run Nash).",
    '# 乡村音乐之都，纳什维尔🎸 Nashiville, Tennessee': '# Capital of Country Music: Nashville 🎸 Nashville, Tennessee',
    '美国人习惯用一个短语来形容不毛之地：in the middle of nowhere；田纳西州对于一些生活在东西海岸大都市群的人来说，无疑就是这样一个地方了，当然，肯塔基肯定也是。': "Americans often use a phrase to describe a middle-of-nowhere place: 'in the middle of nowhere.' For people living in the metropolitan areas of the East and West coasts, Tennessee is undoubtedly one of those places—and Kentucky certainly is, too.",
    '就是这样一个地方，美国著名的三大音乐重镇：路易斯安那州的新奥尔良（爵士乐）、田纳西州的孟秘斯（摇滚和蓝调音乐）以及纳什维尔（乡村音乐），田纳西州就有两个，因此田纳西也被称为音乐之州，纳什维尔则被被叫做“美国乡村音乐之都” ”音乐之城“。': 'Yet, despite this perception, Tennessee is home to two of America\'s three great music landmarks: New Orleans in Louisiana (jazz), Memphis in Tennessee (rock and blues), and Nashville (country music). Thus, Tennessee is known as the Music State, and Nashville is crowned the "Capital of Country Music" and "Music City."',
    '就是这样一个地方，美国著名的三大音乐重镇：路易斯安那州的新奥尔良（爵士乐）、田纳西州的孟菲斯（摇滚和蓝调音乐）以及纳什维尔（乡村音乐），田纳西州就有两个，因此田纳西也被称为音乐之州，纳什维尔则被被叫做“美国乡村音乐之都” ”音乐之城“。': 'Yet, despite this perception, Tennessee is home to two of America\'s three great music landmarks: New Orleans in Louisiana (jazz), Memphis in Tennessee (rock and blues), and Nashville (country music). Thus, Tennessee is known as the Music State, and Nashville is crowned the "Capital of Country Music" and "Music City."',
    '音乐是纳什维尔的灵魂。纳什维尔最早的定居者们在17世纪安全从坎伯兰河岸边下船之后，就在河边演奏起了小提琴曲跳起了巴克舞庆祝。到了18世纪，第一支进行全球巡回演唱会的Fisk Jubilee Singers（一支以大学为背景的人声合唱团）就始于纳什维尔市的菲斯克大学，也让纳什维尔成为远近闻名的“音乐之城”。': 'Music is the soul of Nashville. After safely disembarking on the banks of the Cumberland River in the 17th century, Nashville\'s earliest settlers celebrated by playing fiddles and dancing buck dances along the waterfront. In the 18th century, the Fisk Jubilee Singers—an a cappella ensemble from Nashville\'s Fisk University—became the first group to embark on a global concert tour, cementing Nashville\'s reputation as "Music City."',
    '这里有被称作乡村音乐灵魂的Grand Ole Opry剧院，每周都会举办舞台音乐会，演出的历史由1925年延续至今，风雨不改，这里还有世界最大的博物馆之一，乡村音乐名人堂（Country Music Hall of Fame and Museum）': "The city features the Grand Ole Opry, often called the soul of country music, which has hosted weekly live stage concerts since 1925, rain or shine. It is also home to one of the world's largest museums, the Country Music Hall of Fame and Museum.",
    '我喜欢乡村音乐，旋律简单，听着不累，从《Take Me Home, Country Roads》，到泰勒·斯威夫特。我清晰地记得，第一次听泰勒·斯威夫特的歌是在高中自习课的一个下午。同桌雪莹同学和我说，有一首歌很漂亮MV也很好看，想不想瞅一瞅？就是那首 《You belong with me》，第一次听泰勒·斯威夫特的歌是一种什么感觉呢？大概就像90年代的人第一次听邓丽君吧，在那之后，我的MP3里就装满了她的歌。': "I love country music—the melodies are simple and easy to listen to, from 'Take Me Home, Country Roads' to Taylor Swift. I clearly remember the first time I heard a Taylor Swift song. It was during a high school self-study session one afternoon. My desk mate Xueying told me, 'There's a really beautiful song with a great music video, want to check it out?' It was 'You Belong with Me.' What did it feel like hearing her for the first time? Probably like how people in the 1990s felt when they first heard Teresa Teng. After that, my MP3 player was filled with her songs.",
    '在纳什维尔街头，不管是店面招牌、车身还是建筑涂鸦，到处都是与音乐相关的元素；行色匆匆的歌手背着他们承载着音乐梦想的硕大琴盒奔走在街上；五彩缤纷的霓虹灯、音乐和歌声不断冲击着人们的视觉和听觉，你会感觉到空气里都飘荡着音乐的元素。': 'On the streets of Nashville, music elements are everywhere: shop signs, vehicles, and wall graffiti. Busy singers carry their bulky guitar cases—loaded with musical dreams—as they rush through the streets. Colorful neon lights, music, and vocals constantly wash over your eyes and ears, making you feel as though the very air is filled with music.',
    '2001年，11岁的泰勒·斯威夫特（Taylor Swift）在电视上观看了乡村歌手菲丝·希尔的节目后，使她产生了成为一名乡村歌手、去美国纳什维尔的念头。在学完和弦后，她创作了第一首歌曲《Lucky You》。泰勒·斯威夫特父母为了帮助女儿追逐音乐梦想，举家搬到了纳什维尔，并前往拥有多家唱片公司的音乐街，将原创的音乐小样送去每一家唱片公司的前台。': "In 2001, after watching a program featuring country singer Faith Hill on TV, 11-year-old Taylor Swift decided she wanted to become a country singer and move to Nashville. After learning basic chords, she wrote her first song, 'Lucky You.' To help their daughter pursue her musical dreams, her parents moved the entire family to Nashville, where they visited music labels along Music Row, hand-delivering her demo CDs to every receptionist.",
    '百老汇音乐街上的酒吧是乡村音乐创作者的聚集地，它为音乐家们提供了一个实现梦想的舞台。许多著名的乡村音乐歌手都曾在这里驻唱，并开启了他们的演艺生涯。一些成名的音乐艺术家也时常来这里与年轻歌手一同登台演唱。': "The honky-tonk bars along Broadway are gathering spots for country music creators, providing a stage for musicians to realize their dreams. Many famous country singers started their careers performing here. Even established artists frequently return to perform alongside young talent.",
    '吉他、皮靴和帽子是美国乡村音乐的象征物，因此常常出现在酒吧。每家酒吧都有自己独特的风格，在街边走过时总会有一家吸引你驻足。聆听着原汁原味的乡村音乐，一定能感受到纳什维尔的热情与浪漫吧。': "Guitars, leather boots, and cowboy hats are symbols of American country music and are common sights in the bars. Every bar has its own unique style, and walking down the street, one is bound to draw you in. Listening to original country music here makes you truly feel the passion and romance of Nashville.",
    '# 周五下午的纳什维尔🎸 Nashiville, Tennessee': '# Nashville on Friday Afternoon 🎸 Nashville, Tennessee',
    '纳什维尔离我们不远，开车过去也就3个多小时，周五没啥急活，我们就提前出发了，开车前往纳什维尔。': "Nashville isn't far from us—just over a three-hour drive. Since we didn't have any urgent work on Friday, we set off early and headed to Nashville.",
    '刚到纳什维尔，我们找了一家很不错的印度自助餐，店员还非常好奇地问我这个胸前的Camera是啥，我告诉他是DJI Action2，后来我告诉他我们来跑纳什维尔马拉松，他说他知道这个比赛。': "Right after arriving in Nashville, we found a great Indian buffet. The waiter was very curious about the action camera on my chest. I told him it was a DJI Action 2, and when I mentioned we were here to run the Nashville Marathon, he said he was familiar with the race.",
    '吃好后，我们去了Music City Center的马拉松Expo取装备，排场没有很大，这确实也在意料之中，毕竟这个10月底的比赛相对于4月份的规模还是小了一些。': "After eating, we headed to the marathon expo at the Music City Center to pick up our packets. The setup wasn't huge, which was expected, since the late October race is smaller than the big one in April.",
    '在Expo取取装备，拍拍照，我们看时间还早，就寻思着去旁边的街区走一走，这次来也没啥旅行计划，也没有攻略，主打一个随心。': "After collecting our gear and taking some photos at the expo, we realized it was still early, so we decided to wander around the nearby neighborhoods. We had no specific travel plans or itinerary for this trip—just going with the flow.",
    'Music City Center这边的街区很热闹，不一会就会驶过一辆酒吧车，人们在车里载歌载舞的。': 'The streets around the Music City Center were bustling. Every now and then, a pedal tavern/party bike would pass by, with people singing and dancing on board.',
    '我们搜了个地标，田纳西州议会大厦（Tennessee State Capitol），不远，也就1个多英里，我们打算散步过去，大概走了两个街区吧，街道一下子就喧闹了起来，有种人山人海的感觉，我们一个不小心，居然误入了百老汇音乐街。': "We searched for a landmark: the Tennessee State Capitol. It wasn't far—just over a mile—so we planned to walk. After walking about two blocks, the streets suddenly became noisy and packed with people. By accident, we had wandered right onto Broadway's honky-tonk highway.",
    '这还只是周五的下午，人多得不像话，我们也加入了人群，在街上走走，果然和传说中的一样，各种各样的音乐元素琳琅满目，在这里听一场音乐会一定很过瘾。': "And this was only Friday afternoon! The crowds were unreal. We joined the flow of people walking down the street. It was exactly as described: an abundance of music-related elements everywhere. Catching a live show here must be an incredible experience.",
    '接着我们来到田纳西州议会大厦（Tennessee State Capitol），这座州议会大厦是由著名建筑师威廉·斯特拉克（William Strickland）在19世纪初设计并建造的。它展示了古典希腊建筑风格，是田纳西州政府的核心和标志性建筑物。': "Next, we arrived at the Tennessee State Capitol, which was designed and built in the early 19th century by the renowned architect William Strickland. Showcasing classical Greek Revival architecture, it is the heart and iconic symbol of Tennessee's state government.",
    '可以免费参观，看门的大叔看到我们取的马拉松装备，热情地和我们打招呼，还告诉我们参观的最佳路线。': "Admission is free. The security guard saw the marathon packets we were holding, greeted us warmly, and pointed out the best route for our self-guided tour.",
    '议会大厦里面很漂亮，我还看到了熟悉的Greek Key标志，不虚此行。': "The interior of the Capitol is beautiful, and I even spotted the familiar Greek Key pattern. It was definitely worth the visit.",
    '这里面还会有给人放风的天台，可以看到外面市区的风景，印象比较深刻的是一座骑马的雕塑和市区里轰隆远去的列车。': 'There is also an outdoor terrace where visitors can get fresh air and enjoy views of the city center. What left a lasting impression on me was a horseback statue and a train rumbling off into the distance.',
    '参观完议会大厦，我们顺着坎伯兰河（Cumberland River） 散步，发源于肯塔基州东南部哈维尔山的Cumberland River在美国历史上扮演了重要的角色，早期的殖民者和开拓者使用这条河作为水上交通的要道，帮助促进了经济的发展。': "After touring the Capitol, we took a stroll along the Cumberland River. Originating in Harlan County in southeastern Kentucky, the Cumberland River has played a vital role in American history, serving as a primary water transport route for early settlers and pioneers, thereby driving economic growth.",
    '岸边会有一些流浪的人群，他们悠然自得地躺在河边的草地上，看书读报，并不会觉得不安全。': "There were some homeless folks along the banks, relaxing peacefully on the grassy riverbank, reading books and newspapers. The area didn't feel unsafe at all.",
    '不知不觉我们就漫步到约翰·西根萨勒步行桥（John Seigenthaler Pedestrian Bridge），这座桥就在百老汇的旁边，河的对面是日产体育场（Nissan Stadium），这个是NFL田纳西泰坦队（Tennessee Titans）的主场，在约翰·西根萨勒步行桥上挂满了泰坦队球员的画像，可以看出美国人真的很爱橄榄球。': "Without realizing it, we wandered onto the John Seigenthaler Pedestrian Bridge. The bridge is right next to Broadway, and across the river stands Nissan Stadium, home of the NFL's Tennessee Titans. The bridge was adorned with banners of Titans players, showing just how much Americans love football.",
    '在大桥上可以看到壮丽的纳什维尔天际线，还会有路人过来希望我们帮着拍个合影，然后她们也很友好地给我和Siqi也拍了一张，大桥上的景色很漂亮，我也拿出号码布和纳什维尔城市的天际线来了一次合照，这是独属于2023年10月Run Nash的纳什维尔天际线。': "The bridge offers a spectacular view of the Nashville skyline. A passerby asked us to take a photo for them, and they kindly returned the favor for Siqi and me. The scenery was beautiful. I took out my bib and captured a photo with the city skyline in the background—a snapshot of the Nashville skyline unique to Run Nash in October 2023.",
    '我们没有走到桥的尽头，因为接下来一天的马拉松我们还会路过，并且深入北纳什维尔。': "We didn't walk all the way to the end of the bridge, because we would cross it again during the marathon the next day, which would take us deeper into North Nashville.",
    '回去拿车的时候，我们还路过了一个很漂亮的金色天使雕像，这个雕像叫做 The Recording Angle statue， The Recording Angel 是奥黛丽·弗拉克（Audrey Flack）创作的一座青铜雕塑，高14英尺，位于田纳西州纳什维尔的舍默霍恩交响乐中心的庭院里。': "On our way back to the car, we passed a beautiful golden angel statue called 'The Recording Angel.' Created by Audrey Flack, this 14-foot bronze sculpture stands in the courtyard of the Schermerhorn Symphony Center in Nashville, Tennessee.",
    '弗拉克于2006年12月揭幕了这座雕像。雕像上刻有铭文："The recording angel inscribes the tones that envelopes the heart and heal the bones, that lighten life\'s toll, and soothe the soul — 录音天使记录了包裹心脏和治愈骨骼的音调，减轻生活的负担，抚慰灵魂”。': 'Flack unveiled the statue in December 2006. An inscription on it reads: "The recording angel inscribes the tones that envelopes the heart and heal the bones, that lighten life\'s toll, and soothe the soul."',
    '开车回到民宿，我们刚到小区里就感受到了浓厚的万圣节氛围；民宿也很舒服温馨，比酒店得劲儿，我们看了一会 “花儿与少年” 2023年第一期的沙特阿拉伯之行后，就早早休息了，准备迎接第二天的City Walk City Run…。': 'We drove back to our Airbnb. As soon as we entered the neighborhood, we could feel the festive Halloween atmosphere. The Airbnb was very comfortable and cozy—much better than a hotel. After watching an episode of "Divas Hit the Road" (the 2023 season premiere focusing on the trip to Saudi Arabia), we went to bed early to rest up for the next day\'s City Walk and City Run.',
    '开车回到民宿，我们刚到小区里就感受到了浓厚的万圣节氛围；民宿也很舒服温馨，比酒店得劲儿，我们看了一会 “花儿与少年” 2023年第一期的沙特阿拉伯之行后，就早早休息了，准备迎接第二天的City Walk City Run….' : 'We drove back to our Airbnb. As soon as we entered the neighborhood, we could feel the festive Halloween atmosphere. The Airbnb was very comfortable and cozy—much better than a hotel. After watching an episode of "Divas Hit the Road" (the 2023 season premiere focusing on the trip to Saudi Arabia), we went to bed early to rest up for the next day\'s City Walk and City Run.',
    '# 纳什维尔马拉松🎸 Nashiville, Tennessee': '# Nashville Marathon 🎸 Nashville, Tennessee',
    '这个秋天的纳什维尔马拉松是纳什维尔第二大的跑步活动，这个比赛主打的是半程，所以全马选手并没有很多。这场比赛因为在十月底举行，所以通常天气会比较凉爽。': "This autumn's Nashville Marathon is the second-largest running event in the city. The half marathon is the main attraction, so there weren't many full marathon runners. Held at the end of October, the race usually enjoys cool weather.",
    '在过去的几年中，纳什维尔全程马拉松的赛道由两个13英里的环形组成。也就是说要重复跑两次半马的路线。': 'In past years, the full marathon course in Nashville consisted of two 13-mile loops, meaning runners had to repeat the half marathon route twice.',
    '但是在2022年的比赛中，为了避免重复走回头路，马拉松赛道进行了改变。与其重复走回路线的前半段，现在选手们会沿着绿道跑到泰德·罗兹高尔夫球场（Ted Rhodes Golf）完成26.2英里的距离。我最开始还是觉得挺好的，至今我仍然对克利夫兰的重复路线心有余悸。': "However, for the 2022 edition, the organizers changed the course to avoid repetitive loops. Instead of repeating the first half, runners now follow the greenway out to the Ted Rhodes Golf Course to complete the 26.2-mile distance. I thought this was a great change at first, as I still have nightmares about the repetitive course in Cleveland.",
    '比赛日，天还未亮我们就出发了，刚到达位于起点的田纳西议会大厦时，天也亮了起来。': "On race day, we set off before dawn. As we arrived at the starting line by the Tennessee Capitol, the sky began to brighten.",
    '起点处很热闹，还有绿色马里奥和粉色公主的cosplay跑者，我们加入人群，没多大一会，比赛就开始了。': "The start area was lively, featuring runners cosplaying as Mario and Princess Peach. We joined the crowd, and before long, the race kicked off.",
    '前5个英里，我们都是在纳什维尔市区奔跑，在这边，我们可以看到远处尖尖的教堂和高楼，在路边的酒吧车里，还会有小孩和大家击掌。': "For the first five miles, we ran through downtown Nashville. We could see the distant spires of churches and modern high-rises, and kids were giving out high-fives from the party bikes parked along the road.",
    '接着我们会在2英里的时候路过"音乐" 雕像（"Musica" Statue），这个雕塑由九个跳舞的人物组成，既有男性又有女性，呈环形构图。雕塑高40英尺，传达了一种感觉，即”舞蹈是音乐的身体表达“。': 'Around Mile 2, we ran past the "Musica" statue. This sculpture features nine dancing figures, both male and female, arranged in a circular composition. Standing 40 feet tall, the monument conveys the idea that "dance is the physical expression of music."',
    '在3英里的时候，我们会到达比赛的最南段，然后折返再次路过位于4英里时"Musica" Statue，接着沿着德蒙布伦街（Demonbreun Street）穿越纳什维尔市区，直达约翰·西根萨勒步行桥（John Seigenthaler Pedestrian Bridge）': "At Mile 3, we reached the southernmost point of the course before doubling back, passing the 'Musica' statue again at Mile 4. We then headed along Demonbreun Street through downtown Nashville, leading straight to the John Seigenthaler Pedestrian Bridge.",
    '早晨的约翰·西根萨勒步行桥和前一天的下午有点不同，阳光透过云层洒在脸上，很舒服，大桥上还有给我们加油的队伍，当我拿出运动相机的时候，她们还会朝我大声欢呼。': "The bridge in the morning felt different from the previous afternoon. Sunlight filtered through the clouds, warming our faces. Cheering squads lined the pedestrian path, and when I pulled out my action camera, they cheered loudly for me.",
    '过了大桥，我们就来到了北纳什维尔（East Nashiville），我简单上了个厕所，还遇到了两位Cosplay of 音乐人，西红柿炒蛋配色的musician还很热情地和我打招呼。': "After crossing the bridge, we entered East Nashville. I made a quick restroom stop and encountered two cosplaying musicians. One of them, dressed in a bright red-and-yellow outfit resembling tomato and scrambled eggs, greeted me warmly.",
    '过了大桥，我们就来到了北纳什维尔（East Nashiville），我简单上了个厕所，还遇到了两位Cosplay的音乐人，西红柿炒蛋配色的musician还很热情地和我打招呼。': "After crossing the bridge, we entered East Nashville. I made a quick restroom stop and encountered two cosplaying musicians. One of them, dressed in a bright red-and-yellow outfit resembling tomato and scrambled eggs, greeted me warmly.",
    '接着的一段是沿着坎伯兰河（Cumberland River）和谢尔比公园路（Shelby Park Road）一路东行，在8英里之后，全马队伍会和半马队伍分开，我们优秀的全马选手还要沿着河流在 Shelby Bottoms Greenway 再往东跑一会，直到10英里处折返。': "The next segment headed east along the Cumberland River and Shelby Park Road. After Mile 8, the full marathoners split from the half marathoners. We, the full marathon pack, continued east along the river on the Shelby Bottoms Greenway until looping back at Mile 10.",
    '回去的路上我还看到一位盲人跑者在朋友的带领下跑在绿道上，还挺感动的，志愿者的笑容也很治愈。': "On my way back, I saw a visually impaired runner guided by a companion on the greenway, which was deeply moving. The volunteers' bright smiles were also very comforting.",
    '因为一直没看到Siqi，我在12英里处track了一下她，看到Siqi还在赛道了，觉得问题不大。': "Since I hadn't spotted Siqi, I tracked her position around Mile 12. Seeing that she was still moving steadily on the course, I figured she was doing fine.",
    '因为万圣节马上到了，路边还会有一些装饰品，氛围感不错。': "With Halloween just around the corner, there were several spooky decorations along the road, adding a festive vibe.",
    '13英里之后，我们又回到了约翰·西根萨勒桥，这会儿纳什维尔的温度已经有点升高了，就觉得这个上桥的大破还挺费劲。': "After Mile 13, we returned to the John Seigenthaler Pedestrian Bridge. By this time, the temperature in Nashville had begun to rise, making the long incline up the bridge feel like a real grind.",
    '在我前面的粉色小公主独自走在大桥上，也不知道她的马里奥王子跑到了哪里？': "The Princess Peach runner in front of me was walking alone on the bridge. I wondered where her Mario had run off to.",
    '接下来是一段很短暂的市区路线，阳光越来越足，我注意到有跑者体力不支，倒在了路边，志愿者赶紧过来帮忙，还示意其他跑者注意绕行。': "A brief stretch of city streets followed. As the sun beat down harder, I noticed a runner who had collapsed from exhaustion. Volunteers rushed to help and gestured for others to run around them.",
    '太阳越来越足了，我也赶紧在14英里处的河边补给点喝了几大杯水。阳光很晒，我想是时候变身了，就赶紧换上我新买的墨镜，露出帽子上“NEVER GIVE UP”的 Logo，这是“传奇”跑者该有的态度。': "The sun grew increasingly intense, prompting me to gulp down several cups of water at the Mile 14 riverside aid station. With the heat rising, I decided it was time to gear up: I put on my new sunglasses and adjusted my cap to display the 'NEVER GIVE UP' logo. That is the true attitude of a 'legendary' runner.",
    '路边还有音乐人给大家助威，他们很聪明，躲在比较阴凉的地方。': "Local musicians lined the streets to cheer us on, wisely setting up their instruments in the shade.",
    '这会儿，半马选手就要冲线了，我们全马队伍会沿着盖伊街（Gay Street）向西跑，在穿过一大片工地和涂鸦墙之后，到达沿河的MetroCenter Levee Greenway，这是一条沿河的绿道，风景还不错。': "At this point, the half marathoners were heading to the finish line, while we turned onto Gay Street heading west. After passing construction sites and graffiti-covered walls, we reached the MetroCenter Levee Greenway—a scenic riverside path along the Cumberland.",
    '我在16公里处吃了个补给，我还心想：这个绿道真不错，还能看看坎伯兰河的风景，这段有点像肯塔基德比马拉松的后半程。': "I took a gel at the 16 km mark. I thought to myself: this greenway is quite nice, offering views of the Cumberland River. This section felt similar to the second half of the Kentucky Derby Marathon.",
    '不过令我万万没想到的是，这段足足有8英里的绿道只有一个补给点（19.5英里处），刚到绿道时，天还阴阴的，没想到，不一会，阳光又变得很足。背着阳光我觉得还OK的，但还是有点辛苦。': "But to my surprise, this 8-mile greenway stretch had only a single aid station (around Mile 19.5). When we first entered, it was overcast, but the hot sun soon broke through. Running with my back to the sun was bearable, but it was still a tough stretch.",
    '终于迎来了19.5英里处的补给点，我看到好多跑者都停在这里喝水吃电解质，补给点之后我们大概还要跑一英里才能折返。': "We finally reached the aid station at Mile 19.5. I saw many runners stopping to drink water and take electrolytes. After the station, we had to run about another mile before reaching the turnaround point.",
    '阳光越来越足，温度也越来越多高，十月底的纳什维尔，温度都快30摄氏度了，折返回去的路线还要面对着阳光，这让比赛变得更加艰难，我也开启跑跑走走模式。': "The sun got hotter and the temperature kept climbing. In late October, Nashville was pushing nearly 30°C (86°F). Running back meant facing the direct sunlight, making the race even more grueling. I eventually switched to a run-walk method.",
    '23英里处会有当地的居民给我们大冰块子水，既舒服又解暑，十分感谢。': "At Mile 23, local residents set up a station offering cups of ice-cold water, which was incredibly refreshing. I was extremely grateful.",
    '终于，终于，在24.5英里处，我终于回到了MetroCenter Levee Greenway入口处的补给点，沿河的暴晒大阳光路线终于要结束了，终点近在眼前。': 'Finally, at Mile 24.5, I made it back to the aid station at the entrance of the MetroCenter Levee Greenway. The sun-drenched river section was finally behind me, and the finish line was near.',
    '最后的路线，我穿过铁路隧道和比赛开始的大拱门，跑回位于纳什维尔之音（Nashville Sounds）的终点线，在穿过Start大拱门的时候还有一位完赛的选手主动说要给我拍几个照片，真的非常nice，这个比赛的摄影师确实太少了。': "For the final stretch, I ran through a railroad tunnel and back under the starting arch, finishing on the field of the Nashville Sounds baseball stadium. As I passed the start arch, a fellow finisher kindly offered to take a few photos of me. It was a very nice gesture, especially since there were hardly any official photographers on the course.",
    '纳什维尔之音是个棒球场，在跑过丹佛的里高橄榄球场之后，我又解锁了跑棒球场的成就。': "The Nashville Sounds play in a minor league baseball stadium. After running through Denver's Mile High football stadium, I have now checked off finishing in a baseball stadium.",
    'Siqi在终点处已经等候多时了，还拍下了我冲线的画面，挺帅的。这个天儿确实太热了，我满脸的大盐粒子。': "Siqi had been waiting for a while at the finish line and caught my final sprint on camera—pretty cool! The weather was so hot that my face was covered in salt crusts.",
    '但冲线的快感瞬间打散了跑马的疲惫，我迅速地找了一位热心的志愿者给我和Siqi拍合影，志愿者们真的都特别好。': "But the thrill of crossing the finish line instantly washed away the fatigue. I quickly found a helpful volunteer to take a photo of Siqi and me. The volunteers were truly wonderful.",
    '赛后还有完赛气泡水，不过这会儿都要收摊了，这次我跑了快5个小时20分钟，确实挺慢的，绝对今年的PW了。': "There was post-race sparkling water, though they were already packing up the booths. I finished in nearly 5 hours and 20 minutes—quite slow, and definitely my PW (personal worst) of the year.",
    '接着我和Siqi看到这个体育场里还有乒乓球桌和拍子，我俩没忍住打了两盘，结果没啥悬念，我2比0完胜，很轻松。': "Then Siqi and I noticed a ping-pong table and paddles inside the stadium. We couldn't resist playing two games. The outcome was predictable: I won 2-0 quite easily.",
    '接下来，我们找了个Planet Fitness洗澡，回家，3个小时的Driving不会觉得很累，我们听着乐队的夏天，在周六的晚间，顺利返程，很充实。': "Afterward, we found a Planet Fitness to shower, then headed home. The three-hour drive didn't feel tiring. We listened to 'The Big Band' on the way back, completing a very fulfilling Saturday.",
    '后记': 'Epilogue',
    '纳什维尔马拉松，确实挺难跑的，城市是多山的，比赛的爬升大概有844英尺（约257米），另外就是今年的天气确实有点反常，又晒又热；对于跑出了今年的最差成绩，我其实是可以心安理得的。': "The Nashville Marathon is indeed a tough race. The city is hilly, and the course had about 844 feet (257 meters) of elevation gain. Plus, the weather was unusually hot and sunny. Knowing that, I can easily come to terms with my worst time of the year.",
    '第二天去Cindy家做客，得知Ryan在同一天的印第安纳牦牛马拉松中跑出了和我差不多的成绩，这还只是他的第一个马拉松；从FB里还看到跑牦牛马的美国朋友们纷纷晒成绩，Raquel的第一全马就跑到了3小时40分钟 of 成绩，还有Todd，之前我们一起训练，他总是跑一会就没劲了，后来他训练得很认真，也跑到三个半小时；更别提朋友圈里的国内朋友们，纷纷破4又3的。': "Visiting Cindy's house the next day, I learned that Ryan finished the Indiana Yak Marathon on the same day with a time close to mine—and that was his very first marathon! On Facebook, American friends who ran the Yak Marathon were posting their times: Raquel finished her first marathon in 3:40, and Todd, who used to lose steam quickly during our training runs, had trained hard and finished in 3:50. Not to mention friends on WeChat who were breaking 4 hours or even 3 hours left and right.",
    '第二天去Cindy家做客，得知Ryan在同一天的印第安纳牦牛马拉松中跑出了和我差不多的成绩，这还只是他的第一个马拉松；从FB里还看到跑牦牛马的美国朋友们纷纷晒成绩，Raquel的第一全马就跑到了3小时40分钟的成绩，还有Todd，之前我们一起训练，他总是跑一会就没劲了，后来他训练得很认真，也跑到三个半小时；更别提朋友圈里的国内朋友们，纷纷破4又3的。': "Visiting Cindy's house the next day, I learned that Ryan finished the Indiana Yak Marathon on the same day with a time close to mine—and that was his very first marathon! On Facebook, American friends who ran the Yak Marathon were posting their times: Raquel finished her first marathon in 3:40, and Todd, who used to lose steam quickly during our training runs, had trained hard and finished in 3:50. Not to mention friends on WeChat who were breaking 4 hours or even 3 hours left and right.",
    '我是有点受触动的，就觉得跑马还是要有点目标的，要不总觉有那么点不够劲，不够通透，不够牛逼。': "I was indeed a bit inspired. I felt that running marathons needs some goals; otherwise, it lacks that extra drive, clarity, and sense of achievement.",
    '怎么说传奇跑者还要有点传奇的样子的，要不多心虚，所以，我决定下次跑得认真一点，拿我这双菜脚亮亮剑。': "After all, a 'legendary' runner should look the part, or else it feels like a sham! So, I've decided to run seriously next time and show what these beginner feet can do.",
    '- 本文完 -': '- The end -',
    '文字丨Arsenan': 'Words | Arsenan',
    '摄影丨Arsenan': 'Photos | Arsenan',
    '设计丨Arsenan': 'Design | Arsenan',
    '- Nashiville Marathon -': '- Nashville Marathon -',
    '美国乡村音乐之都': 'Capital of American Country Music',
    '2023-PW': '2023 PW',
    '# 乡村音乐之都，纳什维尔': '# Capital of Country Music: Nashville',
    '# 周五下午的纳什维尔': '# Nashville on Friday Afternoon',
    '# 纳什维尔马拉松': '# Nashville Marathon',
    '🎸 Nashiville, Tennessee': '🎸 Nashville, Tennessee',
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


def clean_caption_typos(txt: str) -> str:
    txt = txt.replace("Nashiville", "Nashville")
    txt = txt.replace("Recording Angle", "Recording Angel")
    txt = txt.replace("《You belong with me》", '"You Belong with Me"')
    return txt


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
            src = f"{img_prefix}img-{img_idx:03d}.webp"
            caption = ""
            for next_idx in range(indexed.index((idx, event)) + 1, len(indexed)):
                next_event = indexed[next_idx][1]
                if next_event["type"] == "text":
                    if is_caption(next_event["text"]):
                        txt = next_event["text"]
                        if not is_zh:
                            txt = clean_caption_typos(txt)
                        caption = txt
                    break
                elif next_event["type"] == "img":
                    break
            
            blocks.append(f'''      <figure>
        <img src="{src}" alt="Tennessee Marathon image {img_idx}" loading="lazy" decoding="async">''')
            if caption:
                blocks.append(f'        <figcaption>{escape(caption)}</figcaption>')
            blocks.append('      </figure>')
        
        elif event["type"] == "text":
            txt = event["text"]
            if not is_zh:
                if txt in TRANSLATIONS_MAP:
                    txt = TRANSLATIONS_MAP[txt]
                else:
                    txt = clean_caption_typos(txt)
            
            if is_caption(event["text"]) or should_skip_text(event["text"]):
                continue
            
            if txt.startswith("丨"):
                continue
            elif txt.startswith("# "):
                blocks.append(f'      <h2 class="section-label">{escape(txt[2:])}</h2>')
            elif txt.startswith("## "):
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
      --paper: #FAF5FF;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #dde5ec;
      --river: #0b67c2;
      --brick: #7c3aed;
      --gold: #d97706;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #F5EEFD 0, var(--paper) 320px);
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
      border-left: 4px solid var(--brick);
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
      --soft: #faf5ff;
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
    title = "Run50 #第12州｜田纳西：纳什维尔马拉松｜音乐之城的慢悠跑者，十月艳阳下的最慢跑" if is_zh else "Run50 #12 | Tennessee: Nashville Marathon"
    short = "Run50 #12 | Nashville Marathon"
    desc = (
      "十月底的音乐之都纳什维尔，在万圣节前夕跑过坎伯兰河与行人天桥，在极其炎热与暴晒的艳阳下，跑出了本年最慢的PW成绩，并在纳什维尔之音棒球场冲线！"
      if is_zh
      else "Race date: October 28, 2023. Running U.S. State 12: Nashville Marathon (Run Nash) in Tennessee, featuring the Cumberland River, the John Seigenthaler Pedestrian Bridge, a minor league baseball stadium finish, and completing the warmest and slowest race of the year."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
      f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
      if is_zh
      else f'<a href="./index.html">← English Stories</a><a href="{other}">Chinese Original</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    kicker = "Run50 #第12州 · 田纳西" if is_zh else "Run50 #12 · Tennessee"
    footer = "© 2023-2026 ArsenanZZ. Built with love."
    locale = "zh-CN" if is_zh else "en"
    key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    mount = f"supabase-comments-nashville-zh" if is_zh else f"supabase-comments-nashville-en"
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
  <meta property="og:image:alt" content="Tennessee Marathon cover with Cumberland River, John Seigenthaler Pedestrian Bridge, and a country music acoustic guitar.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-10-28T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav" aria-label="{"页面导航" if is_zh else "Page navigation"}">
    {nav}
  </nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">
      <span>By Arsenan</span>
      <span>Race: October 28, 2023</span>
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
    title = "I ran the Nashville Marathon under an unusually scorching October sun, crossing the line inside a baseball stadium for my slowest race of the year"
    desc = "Race date: October 28, 2023. Running U.S. State 12: Nashville Marathon (Run Nash) in Tennessee, featuring the Cumberland River, the John Seigenthaler Pedestrian Bridge, a minor league baseball stadium finish, and completing the warmest and slowest race of the year."
    canonical = f"{SITE}/run50/facebook/{SLUG}.html"
    key = f"run50-{SLUG}-facebook-en"
    mount = f"supabase-comments-nashville-facebook-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nashville Marathon | Run50 Facebook</title>
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
  <meta property="og:image:alt" content="Tennessee Marathon cover with Cumberland River, John Seigenthaler Pedestrian Bridge, and a country music acoustic guitar.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-10-28T07:00:00-05:00">
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
      <span>Race date: October 28, 2023</span>
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
        <span>Race: October 28, 2023</span>
        <span>Nashville, TN</span>
        <span>Run50 #12</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="Icon-style Nashville Marathon cover"><figcaption>Tennessee icon cover with Cumberland River, John Seigenthaler Pedestrian Bridge, and a country music acoustic guitar.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Nashville Marathon (Run Nash), Run50 State 12.</dd></div><div><dt>Course</dt><dd>Downtown Nashville, John Seigenthaler Pedestrian Bridge, East Nashville, Shelby Bottoms Greenway, MetroCenter Levee Greenway, and finishing on the field of the Nashville Sounds baseball stadium.</dd></div><div><dt>What stayed with me</dt><dd>Country music vibe on Broadway, walking on the historic pedestrian bridge, a Visually Impaired runner with their guide, running in scorching 30°C heat, and finishing the slowest run of the year with salt-crusted skin.</dd></div></dl></section>
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
<title id="title">Tennessee Nashville Marathon icon cover</title>
<desc id="desc">Icon style cover with Tennessee title, Run50 badge, John Seigenthaler Pedestrian Bridge, Cumberland River, and a country music acoustic guitar.</desc>
<rect width="1200" height="750" fill="#faf5ff"/>
<circle cx="580" cy="300" r="70" fill="#fcd34d" opacity="0.9"/>
<circle cx="580" cy="300" r="90" fill="none" stroke="#fef08a" stroke-width="4" stroke-dasharray="15 10" opacity="0.6"/>
<path d="M0 500 L80 500 L80 430 L120 430 L120 460 L180 460 L180 400 L210 400 L210 500 L300 500 L300 420 L350 420 L350 500 L500 500 L500 450 L560 450 L560 500 L1200 500 L1200 750 L0 750 Z" fill="#eddffa" opacity="0.5"/>
<g stroke="#7c3aed" stroke-width="5" fill="none" opacity="0.7">
  <line x1="0" y1="520" x2="1200" y2="520" stroke-width="8"/>
  <line x1="150" y1="520" x2="150" y2="580" stroke-width="10"/>
  <line x1="450" y1="520" x2="450" y2="580" stroke-width="10"/>
  <line x1="750" y1="520" x2="750" y2="580" stroke-width="10"/>
  <line x1="1050" y1="520" x2="1050" y2="580" stroke-width="10"/>
  <path d="M 0 520 A 150 150 0 0 1 300 520"/>
  <path d="M 10 520 A 140 140 0 0 1 290 520" stroke-dasharray="10 5"/>
  <path d="M 300 520 A 150 150 0 0 1 600 520"/>
  <path d="M 310 520 A 140 140 0 0 1 590 520" stroke-dasharray="10 5"/>
  <path d="M 600 520 A 150 150 0 0 1 900 520"/>
  <path d="M 610 520 A 140 140 0 0 1 890 520" stroke-dasharray="10 5"/>
  <path d="M 900 520 A 150 150 0 0 1 1200 520"/>
  <path d="M 910 520 A 140 140 0 0 1 1190 520" stroke-dasharray="10 5"/>
  <line x1="75" y1="460" x2="75" y2="520" stroke-width="3"/>
  <line x1="150" y1="440" x2="150" y2="520" stroke-width="3"/>
  <line x1="225" y1="460" x2="225" y2="520" stroke-width="3"/>
  <line x1="375" y1="460" x2="375" y2="520" stroke-width="3"/>
  <line x1="450" y1="440" x2="450" y2="520" stroke-width="3"/>
  <line x1="525" y1="460" x2="525" y2="520" stroke-width="3"/>
  <line x1="675" y1="460" x2="675" y2="520" stroke-width="3"/>
  <line x1="750" y1="440" x2="750" y2="520" stroke-width="3"/>
  <line x1="825" y1="460" x2="825" y2="520" stroke-width="3"/>
  <line x1="975" y1="460" x2="975" y2="520" stroke-width="3"/>
  <line x1="1050" y1="440" x2="1050" y2="520" stroke-width="3"/>
  <line x1="1125" y1="460" x2="1125" y2="520" stroke-width="3"/>
</g>
<path d="M0 580 Q300 530 600 580 T1200 580 L1200 750 L0 750 Z" fill="#2dd4bf" opacity="0.8"/>
<path d="M0 620 Q400 580 800 630 T1200 610 L1200 750 L0 750 Z" fill="#0d9488" opacity="0.9"/>
<path d="M0 660 Q300 630 600 680 T1200 660 L1200 750 L0 750 Z" fill="#115e59"/>
<path d="M0 630 Q250 640 400 750 L0 750 Z" fill="#a78bfa" stroke="#20242b" stroke-width="4"/>
<g transform="translate(260, 620) rotate(-25)">
  <ellipse cx="50" cy="50" rx="90" ry="75" fill="#d97706" stroke="#20242b" stroke-width="6"/>
  <ellipse cx="-20" cy="50" rx="70" ry="55" fill="#d97706" stroke="#20242b" stroke-width="6"/>
  <path d="M -60 8 Q -20 25 30 10 L 30 90 Q -20 75 -60 90 Z" fill="#d97706"/>
  <path d="M -60 8 Q -20 25 30 10 M 30 90 Q -20 75 -60 90" fill="none" stroke="#20242b" stroke-width="6"/>
  <circle cx="5" cy="50" r="28" fill="#1e1b4b" stroke="#f59e0b" stroke-width="4"/>
  <rect x="-220" y="40" width="160" height="20" fill="#78350f" stroke="#20242b" stroke-width="4"/>
  <line x1="-200" y1="40" x2="-200" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-180" y1="40" x2="-180" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-160" y1="40" x2="-160" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-140" y1="40" x2="-140" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-120" y1="40" x2="-120" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-100" y1="40" x2="-100" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <line x1="-80" y1="40" x2="-80" y2="60" stroke="#d1d5db" stroke-width="2"/>
  <path d="M -260 35 L -220 40 L -220 60 L -260 65 Z" fill="#78350f" stroke="#20242b" stroke-width="4"/>
  <circle cx="-250" cy="30" r="6" fill="#9ca3af" stroke="#20242b" stroke-width="2"/>
  <circle cx="-235" cy="30" r="6" fill="#9ca3af" stroke="#20242b" stroke-width="2"/>
  <circle cx="-250" cy="70" r="6" fill="#9ca3af" stroke="#20242b" stroke-width="2"/>
  <circle cx="-235" cy="70" r="6" fill="#9ca3af" stroke="#20242b" stroke-width="2"/>
  <rect x="70" y="38" width="12" height="24" rx="3" fill="#1e1b4b" stroke="#20242b" stroke-width="2"/>
  <line x1="-220" y1="44" x2="70" y2="44" stroke="#e5e7eb" stroke-width="1.5"/>
  <line x1="-220" y1="47" x2="70" y2="47" stroke="#e5e7eb" stroke-width="1.5"/>
  <line x1="-220" y1="50" x2="70" y2="50" stroke="#e5e7eb" stroke-width="1.5"/>
  <line x1="-220" y1="53" x2="70" y2="53" stroke="#e5e7eb" stroke-width="1.5"/>
  <line x1="-220" y1="56" x2="70" y2="56" stroke="#e5e7eb" stroke-width="1.5"/>
</g>
<g transform="translate(70 104)">
  <text x="0" y="0" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">TENNESSEE</text>
  <text x="0" y="46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#0b67c2">MUSIC CITY · CUMBERLAND RIVER · GUITAR</text>
</g>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #12</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">TENNESSEE</text>
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
    image = Image.new("RGB", (1200, 630), "#faf5ff")
    draw = ImageDraw.Draw(image)
    text_color = "#20242b"
    blue = "#0b67c2"
    purple = "#7c3aed"
    
    # Sun
    draw.ellipse((510, 230, 650, 370), fill="#fcd34d")
    
    # Far background skyline silhouettes
    draw.polygon([(0, 630), (0, 500), (80, 500), (80, 430), (120, 430), (120, 460), (180, 460), (180, 400), (210, 400), (210, 500), (300, 500), (300, 420), (350, 420), (350, 500), (500, 500), (500, 450), (560, 450), (560, 500), (1200, 500), (1200, 630)], fill="#eddffa")
    
    # Title
    draw.text((64, 64), "TENNESSEE", font=font(66, True), fill=text_color)
    draw.text((66, 136), "MUSIC CITY · CUMBERLAND RIVER · GUITAR", font=font(26, True), fill=blue)
    
    # Badge Box
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text_color, width=7)
    draw.text((790, 112), "Run50 #12", font=font(40, True), fill=text_color)
    draw.text((790, 166), "TENNESSEE", font=font(50, True), fill=blue)
    
    # Bridge Structure (Simple representation in PIL)
    # Bridge deck line
    draw.line([(0, 520), (1200, 520)], fill=purple, width=8)
    # Piers
    for px in (150, 450, 750, 1050):
        draw.line([(px, 520), (px, 580)], fill=purple, width=10)
    # Arches using chord / curves approximation or arcs
    # We can draw chord lines for simple geometry in PIL
    for bx in (0, 300, 600, 900):
        draw.arc((bx, 420, bx + 300, 620), 180, 360, fill=purple, width=5)
    
    # Cumberland River
    draw.polygon([(0, 630), (0, 550), (300, 530), (600, 550), (900, 530), (1200, 550), (1200, 630)], fill="#2dd4bf")
    draw.polygon([(0, 630), (0, 580), (400, 560), (800, 580), (1200, 570), (1200, 630)], fill="#0d9488")
    draw.polygon([(0, 630), (0, 610), (300, 590), (600, 610), (1200, 600), (1200, 630)], fill="#115e59")
    
    # Riverbank land
    draw.polygon([(0, 630), (0, 530), (250, 540), (400, 630)], fill="#a78bfa")
    
    # Acoustic Guitar
    fb_img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    fb_draw = ImageDraw.Draw(fb_img)
    # Guitar center is at (200, 200) inside fb_img
    # lower bout
    fb_draw.ellipse((160, 125, 340, 275), fill="#d97706", outline="#20242b", width=6)
    # upper bout
    fb_draw.ellipse((90, 145, 230, 255), fill="#d97706", outline="#20242b", width=6)
    # Waist connector and curves
    fb_draw.rectangle((120, 160, 200, 240), fill="#d97706")
    fb_draw.line((120, 160, 200, 150), fill="#20242b", width=6)
    fb_draw.line((120, 240, 200, 250), fill="#20242b", width=6)
    
    # Soundhole
    fb_draw.ellipse((140, 172, 196, 228), fill="#1e1b4b", outline="#f59e0b", width=4)
    # Neck
    fb_draw.rectangle((0, 190, 110, 210), fill="#78350f", outline="#20242b", width=4)
    # Frets
    for fx in range(10, 110, 15):
        fb_draw.line((fx, 190, fx, 210), fill="#d1d5db", width=2)
    # Headstock
    fb_draw.polygon([(0, 185), (-40, 185), (-40, 215), (0, 215)], fill="#78350f", outline="#20242b", width=4)
    # Pegs
    for px in (-30, -15):
        fb_draw.ellipse((px - 3, 177, px + 3, 183), fill="#9ca3af", outline="#20242b", width=2)
        fb_draw.ellipse((px - 3, 217, px + 3, 223), fill="#9ca3af", outline="#20242b", width=2)
    # Bridge
    fb_draw.rectangle((240, 188, 252, 212), fill="#1e1b4b", outline="#20242b", width=2)
    # Strings
    for sy in (194, 197, 200, 203, 206):
        fb_draw.line((0, sy, 240, sy), fill="#e5e7eb", width=2)
        
    # Rotate by -25 degrees
    rotated_fb = fb_img.rotate(-25, resample=Image.Resampling.BICUBIC)
    # Paste onto canvas
    image.paste(rotated_fb, (160, 320), rotated_fb)
    
    image.save(REPO / "assets" / f"og-run50-{SLUG}-icons.png", "PNG")


def update_indexes():
    new_card_zh = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="田纳西马城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">田纳西纳什维尔 · 2023.10.28</p>
          <h2 class="story-title">Run50 #第12州｜纳什维尔马拉松</h2>
          <p class="story-desc">十月底的音乐之都纳什维尔，在万圣节前夕跑过坎伯兰河与行人天桥，在极其炎热与暴晒的艳阳下，跑出了本年最慢的PW成绩，并在纳什维尔之音棒球场冲线！</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
    </section>'''

    new_card_en = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon cover for Nashville Marathon" />
        <div class="story-card-content">
          <div class="meta">Tennessee · Nashville · 2023.10.28</div>
          <h2>Nashville Marathon: running in the music city under autumn sunshine</h2>
          <p>Running U.S. State 12 quest in the Capital of Country Music, crossing the John Seigenthaler Pedestrian Bridge on a hot October day, and completing my slowest marathon of the year inside the baseball stadium.</p>
        </div>
      </a>
    </section>'''

    new_card_fb = f'''    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Scorching October sun gave me my slowest marathon of the year in Music City</h2>
        <p>Race date: October 28, 2023. Running U.S. State 12 at Nashville, TN. A hot city greenway run with a minor league baseball stadium finish, crossing the Cumberland River, and surviving a PW.</p>
        <div class="meta">
          <span>Nashville, TN</span>
          <span>slowest run survived</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon-style Nashville Marathon cover">
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
    zh_article = render_article(indexed_story, "zh", f"Run50-Nashville-Marathon-clean_files/")
    write_clean(zh_path, normal_page("zh", zh_article))

    print("Rendering English Page...")
    en_article = render_article(indexed_story, "en", f"../chinese/Run50-Nashville-Marathon-clean_files/")
    write_clean(en_path, normal_page("en", en_article))

    print("Rendering Facebook Page...")
    fb_article = render_article(indexed_story, "en", f"../stories/chinese/Run50-Nashville-Marathon-clean_files/")
    write_clean(fb_path, facebook_page(fb_article))

    print("Generating SVG Thumbnail Cover...")
    write_svg()

    print("Generating PNG OpenGraph Cover...")
    write_png()

    print("Registering cards on Listing Indexes...")
    update_indexes()

    print("Done! Tennessee Marathon story successfully published.")


if __name__ == "__main__":
    main()
