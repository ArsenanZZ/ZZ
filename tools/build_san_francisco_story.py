from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import re
import shutil


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2022-State-04-CA"
)
CITY_HTML = SOURCE_BASE / "旧金山，流雾之下.html"
RACE_HTML = SOURCE_BASE / "我去跑旧金山马拉松，没有偶遇谷爱凌.html"

SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "san-francisco-marathon"
VERSION = "20260615-4"
ENGAGEMENT_VERSION = "20260615"

OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-SanFrancisco-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-san-francisco-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-san-francisco-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-ca.jpg"

TITLE_ZH = "Run50 #第4州｜加州：旧金山马拉松｜流雾之下的金门大桥"
TITLE_EN = "Run50 #4 | California: San Francisco Marathon Under the Rolling Fog"
TITLE_FB = "San Francisco turned 26.2 miles into fog, bridge wind, hills and bay light"
DATE_ZH = "2022.07.24"
DATE_EN = "Jul 24, 2022"
RACE_NAME = "45th San Francisco Marathon"


CITY_EN_TSV = r"""
1	| SF |
2	Preface
3	San Francisco has a huge reputation. In movies, the Golden Gate Bridge has been destroyed countless times. It seems to be an alien spacecraft's favorite piece of infrastructure. I had always wanted to take a look before the end of the world and see what the bridge looked like while it was still intact.
4	San Francisco also has a lot of fog, and the fog even has its own name: Karl. Karl is known as the city's most mysterious resident, and on social media she has 360,000 followers, sharing her moods with everyone day by day.
5	▲ Karl @Google
6	I had actually heard plenty about San Francisco's beauty before. When I chatted with Xiaofei from Taiwan, she told me she loved San Francisco and even showed me photos her photographer husband had taken there. Even through the screen, I could feel all that happiness.
7	▲ SF Poster @Google
8	So my expectations for San Francisco were completely maxed out. Finally, in July 2022, the chance came. 47 and I set out from Louisville and headed west toward California. After flying over Colorado's high mountains and canyons and Nevada's endless desert, we finally arrived at the destination of this trip: San Francisco.
9	▲ From Flight @Arsenan
10	01
11	Union Square
12	After leaving the airport, we took BART straight to Union Square, because our hotel was booked nearby.
13	Union Square is almost every visitor's first stop in San Francisco. It has the densest cluster of hotels, restaurants, shops and supermarkets, and it quickly sketches out the outline of the city.
14	▲ Union Square @Arsenan
15	It is also the most convenient transportation hub. Whether by foot, train, subway or bus, you can get almost anywhere in San Francisco from here. 47 was smart enough to book our hotel in this area, and she deserves a huge thumbs-up for that.
16	The moment we came out of the subway station, we were stunned. San Francisco's slopes are ridiculously steep. As locals say, it is very hilly. 47 and I, two such skinny little people, had to climb several hills just to reach the hotel entrance. It nearly took our lives.
17	Still, tired or not, my first impression of San Francisco felt fresh and fun, especially the cable cars. Every so often one passed by us, and the crisp bell sound was so pleasant it felt like a breeze brushing past.
18	▲ Cable Car @Arsenan
19	San Francisco's cable cars began operating in 1873. They have been around for more than 150 years and are the world's only manually operated cable car system still in service.
20	I imagined myself sitting on a cable car, listening to the bright bells along the way, looking at the unique buildings along the street, and feeling the charm that belongs only to this city. Somehow, even pushing our luggage did not feel quite as exhausting.
21	02
22	California Academy of Sciences
23	For two people like 47 and me, who love learning new things, the first stop had to be the California Academy of Sciences.
24	The famous California Academy of Sciences was founded in 1853. Today it is one of the largest natural history museums in the world. This place is impressive, covering everything from the sky to the earth.
25	▲ California Academy of Sciences @Arsenan
26	The California Academy of Sciences sits inside Golden Gate Park and has three main areas: an aquarium, a planetarium, and a natural history museum.
27	The planetarium impressed me the most. Inside there is a 75-foot dome that plays roughly 30-minute films about the universe at set times, with a different theme each time.
28	We watched two shows. The one that stayed with me most was about the scale of the universe. The film started from the tiny point of Earth and expanded outward into the vast cosmos. It was stunning.
29	It made me think of the worldview in The Three-Body Problem and Marvel's parallel universes. I think anyone who likes adventure probably carries some urge to look far away. For souls used to being boxed in, the sky overhead feels like a doorway to parallel universes, while the crowded city and noisy people below suddenly seem less important.
30	03
31	Golden Gate Bridge
32	After the California Academy of Sciences, we went with 47's good friend Anastasia for Korean hot pot buffet. The house-made drinks were unlimited and delicious. The place was small, but very popular.
33	▲ Anastasia @Arsenan
34	▲ 47 and Arsenan @Anastasia
35	We ate until we were full, then decided to go for a walk. Since Anastasia's apartment was right near the Golden Gate Bridge and she often posted Instagram photos that were clearly taken there, we figured we might as well go. As a semi-local, Anastasia became our guide and drove us to a small hillside by the bridge.
36	▲ Sunset @Arsenan
37	The wind beside the bridge was really strong. Anastasia clearly knew what she was doing: her car had all kinds of warm gear, and she very kindly lent me a red blanket. With proper equipment, the photos immediately looked better.
38	▲ Golden Gate Bridge @47
39	The Golden Gate Bridge is unbelievably famous. Many classic movie scenes were filmed here, including San Andreas, Rise of the Planet of the Apes, X-Men and more. It has been destroyed on screen again and again. The bridge is 2.7 kilometers long, about 120,000 cars cross it every day, and people can also walk or bike across it.
40	▲ Golden Gate Bridge @Arsenan
41	▲ 47 @Arsenan
42	We were very lucky. Karl was probably asleep at that moment, because the weather was unexpectedly good. Anastasia was surprised too and said it had been foggy recently. We really were lucky.
43	▲ Proposal @Arsenan
44	By the bridge, some people were proposing and others were simply taking in the view. We felt the strong sea wind, looked out at the Golden Gate Bridge in the sunset, watched a few birds pass by, and stayed until night fell, enjoying a rare easy and peaceful moment.
45	04
46	San Francisco Chinatown
47	As one of the oldest Chinatowns in the world, San Francisco's Chinatown is probably the largest Chinatown in the American West, even comparable to New York's Chinatown. In the San Francisco Bay Area, with a total population of more than seven million, there are over 700,000 Chinese people.
48	▲ Foggy @Arsenan
49	Our hotel happened to be right next to Chinatown, so breakfast the next morning was planned there: preserved egg and lean pork congee, big buns, char siu. Just thinking about it made me happy.
50	▲ SF Chinatown @Arsenan
51	47 and I wandered through San Francisco Chinatown under the flowing fog. With Karl around, this finally felt like the base color of the city.
52	Suozhang also left me a message saying San Francisco's summer was the coldest winter he had ever experienced. I went around in circles trying to understand that line, and I guess he meant San Francisco summers are very cold.
53	And yes, the fog-covered streets were much cooler. But when we walked into the Chinatown market, it was full of everyday warmth and human energy.
54	It felt like time travel, a little old and behind the times, but maybe that is also a snapshot of an era for the older Chinese immigrants who crossed the ocean back then. The shops and signs were all in Chinese. Uncles and aunties bought groceries along the street, and it felt no different from a market in a second- or third-tier city in China.
55	We bought congee and buns at a breakfast shop, but there was no dine-in, so we carried the food to the nearby Italian neighborhood, ordered a hot coffee, and paired it with preserved egg and lean pork congee plus char siu buns. It was a little mismatched, but somehow also kind of perfect.
56	▲ Italian Brunch @Arsenan
57	05
58	Lombard Street
59	After leaving the Italian neighborhood, we climbed a few more slopes and arrived at the world's most crooked street, Lombard Street. It is famous and has become one of San Francisco's most attractive streets.
60	▲ Italian Street @Arsenan
61	In the 1920s, Lombard Street was designed and built this way to ease traffic pressure. As a very short block between two streets, it has eight hairpin turns. Because the slope reaches about 40 degrees and curves like a Z, cars can only drive downhill one way.
62	▲ Lombard Street @Arsenan
63	▲ Lombard Street @47
64	To help prevent traffic accidents, San Franciscans built many flowerbeds on both sides of the winding roadway, allowing cars to spiral around them. Residents along the street also planted trees and flowers in front of their homes, adding color to the street. Today, flowers and plants line the whole block, with something blooming in every season.
65	Travel guides say that when you climb to the top of the street, you can look back over the view, then drive downward from the top, watching cars snake one after another while enjoying the layered, colorful flowers and this one-of-a-kind scene. But we did not rent a car, so we missed this chance to improve our driving skills.
66	06
67	Bike the City
68	I really like biking. Back in China, I often rode shared bikes all over the place.
69	I had long heard that San Francisco has a special love for bikes. Almost every main road has bike lanes, and after just a turn, you can find bike rental spots on nearly every corner. Cyclists can be seen moving through the city's streets and alleys everywhere.
70	
71	▲ SF Cycling Vlog @Arsenan
72	But we went one step further and booked a bike tour directly. Not only would a guide plan the route, the bikes were electric. In a city this hilly, an e-bike is the best possible answer.
73	The bike tour started near Fisherman's Wharf. Because we went the wrong way, we were quite late. I thought the guide definitely would not wait for us, but somehow we caught the last chance to join. We did delay everyone quite a bit, though, and I felt bad about it.
74	▲ SF Cycling @Arsenan
75	When traveling, biking is the mode of transportation that gets you closest to the corners of a city. Led by the guide, we rode through traffic, and at some stops he would pause to explain the city's history. He said he really liked this job because he loved San Francisco so much. No matter how many times he told the stories, he never got tired of them.
76	Before we knew it, we had reached Rincon Park near the San Francisco-Oakland Bay Bridge. The bridge was spectacular, forming an enormous open scene together with the blue sky and ocean.
77	▲ San Francisco-Oakland Bay Bridge @Arsenan
78	After leaving the park, we headed south, passing Oracle Park and the Warriors' Chase Center. Unfortunately, there was no time for me to make a pilgrimage, so I had to follow the group to Mezli Mediterranean for lunch. It was a great food stand, though of course not as good as Chinatown.
79	▲ Oracle Park @Arsenan
80	▲ Chase Center @Arsenan
81	▲ Mezli Mediterranean @Arsenan
82	After a break, we set off again. Then a small incident happened: 47's bike broke. We had to change bikes, but we really did not want to delay everyone any longer, so we talked with the guide and decided to leave the group. Once the replacement bike arrived, we would move freely on our own.
83	▲ Bike Replacement @Arsenan
84	▲Go @Arsenan
85	The rescue car arrived quickly, the bike swap worked, and we arranged the rest of the route ourselves.
86	We first went to Mission Dolores Park. It is a perfect place to enjoy a sunny afternoon, with wide lawns for playing and resting, and a beautiful view of the city. The golden tower of Mission High School especially caught my eye.
87	▲ Mission Dolores Park @Arsenan
88	Next was Alamo Square. Across from the square are the colorful houses known as the Painted Ladies, also called the Six Sisters. They have become a San Francisco landmark.
89	Even if you know nothing about design, you can still feel the beauty in the ornate roofs, stained glass and bay windows. Actually, when these buildings were first built, they were white. It was not until the 1960s that color designer Butch Kardum turned them into the artwork they are today.
90	▲ The Painted Ladies @Arsenan
91	Then we kept going and reached San Francisco City Hall, built in the Beaux-Arts style. It has the fifth-largest dome in the world, and many couples choose to register their marriages there.
92	▲ City Hall @Arsenan
93	We passed through San Francisco's Japantown. Japantown Peace Plaza looked special, with lively song-and-dance performances and plenty of people gathered to watch.
94	▲ Japantown Peace Plaza @Arsenan
95	On the way back to return the bikes, we deliberately stopped at Coit Tower, which looks a bit like a fire hose nozzle. It is said to commemorate Lillie Hitchcock Coit, who bravely helped firefighters and dedicated her life to the development of the city's fire services.
96	▲ Coit Tower @Arsenan
97	Standing on Telegraph Hill in Pioneer Park, we could see one of San Francisco's famous sights in the distance: Alcatraz Island, the legendary prison island.
98	▲ Alcatraz Island @Arsenan
99	This used to be San Francisco's most notorious federal prison, holding troublemakers from other prisons, mostly bank robbers and murderers, even gang leaders. Nicolas Cage filmed The Rock here, telling a story that takes place between Alcatraz and the Bay Area.
100	We circled around San Francisco and finally returned to Fisherman's Wharf. It was super lively and also the end point for returning the bikes.
101	Fisherman's Wharf was originally a fishing harbor where Italian fishermen gathered. In the 1960s, as the catch declined, it gradually became a tourist attraction. Today it is full of shopping centers, crab sellers line the road one after another, and street musicians and artists perform one after another. It is incredibly lively.
102	▲ Fisherman's Wharf @Arsenan
103	We had planned to wait at Pier 39 for the last boat out to see the Golden Gate Bridge, but the fog came in and Karl wrapped the whole bridge up. The wind was strong too, so we decided to take the boat later. Better to go to Chinatown first for some Chinese food and recover.
104	▲ SF Street @Arsenan
105	We walked from Fisherman's Wharf to Chinatown and ate at a Chinese restaurant Eric Tsang had once visited. The setup was still as simple as ever, very much the feeling of an American Chinatown.
106	▲ Chinatown Food @Arsenan
107	Postscript
108	When we came out of the Chinese restaurant, the flowing fog had spread from the west, where the Golden Gate Bridge sits, across the entire downtown area. It felt a little chilly, so we picked up our pace.
109	Thinking back on this full and tightly packed day, I thought of San Francisco, the theme song from Forrest Gump. What the song says felt exactly like my mood in that moment.
110	For those who come to San Francisco
111	For those going to San Francisco
112	be sure to wear some flowers in your hair
113	remember to wear some flowers in your hair
114	If you come to San Francisco
115	if you go to San Francisco
116	summertime will be a loving there
117	there will be beautiful times in the summer
118	- End -
119	Words | Arsenan
120	Photos | Arsenan
121	Design | Arsenan
"""


RACE_EN_TSV = r"""
1	Course | SF |
2	Preface
3	I had wanted to run a marathon in San Francisco for a long time. I wanted to go a year earlier, but I missed the early-bird price and could not quite bring myself to register. And honestly, California really was far away.
4	This year, the San Francisco Marathon entered its 45th year, roughly the same age as the Chicago Marathon. I like races with that kind of commemorative meaning, so I did not hesitate and signed up right away.
5	Running a marathon seems to have become the main reason I travel, almost a habit. Once the marathon was on the calendar, California suddenly did not feel so far away.
6	I like San Francisco because it is so special. Whether you call it Saint Francis, Jiu Jin Shan, or San Faan Si, all those names point to this small city of less than 130 square kilometers on the northwestern edge of the Bay.
7	The Gold Rush made it a cradle for adventurers, and hippie culture gave it an untamed spirit. Pacific fog, West Coast tides, the blend of history and modern life, the collision of East and West: all of it gives the city a color unlike anywhere else in America.
8	But the San Francisco Marathon is another story. Unlike flat, steady city road races, San Francisco's course is intimidating, with relentless ups and downs that are hard enough to make even serious runners nervous.
9	For more than forty years, San Francisco has held a firm place as the 15th hardest race in the world...
10	As The Wall Street Journal put it, this is a race even marathoners fear.
11	Still, on this loop, there are busy city scenes and unexpectedly simple, beautiful views.
12	I was willing to accept that challenge, and I looked forward to measuring the Golden Gate Bridge with my own feet, with a runner's stubbornness and pride.
13	▲ Run San Fancisco @FinisherPix
14	01
15	Packet pickup at the expo
16	The day before the race, we went to Festival Pavilion to pick up our gear. I was still doing the full marathon, and 47 had signed up for the half.
17	▲ SF Expo @Arsenan
18	The surprise was that this year's San Francisco Marathon had two medals: one before the race and one after. Maybe it was to celebrate the special 45th anniversary. The pre-race medal was definitely not as grand as the finisher medal, so I was still looking forward to the post-race one more.
19	▲ Pre-race Medal @Arsenan
20	As we were leaving, I saw old marathon shirts for sale near the entrance, 10 dollars each, which felt like a good deal. I bought two long-sleeve shirts. The green one would end up going with me for half of the race.
21	▲ SF Course Map @Google
22	▲ My SF Marathon Course @Relive
23	02
24	The 45th San Francisco Marathon begins
25	On July 24, the 45th San Francisco Marathon was finally about to start. All of us runners gathered near the start by the Ferry Building.
26	▲ Ferry Building @Arsenan
27	The sky was still deep blue and the night had not fully faded, but the streets were already full of people. The start line in the distance was especially lively. Because of the wave start, some of the faster runners had already set off.
28	I squeezed into my corral with the crowd, told 47 I would see her at the finish, and headed out. The half-marathon runners would not start until an hour later.
29	At the beginning I was pretty excited, following the big crowd through Fisherman's Wharf and Fort Mason toward the Presidio of San Francisco, where the Golden Gate Bridge stands.
30	▲ Fisherman's Wharf @Arsenan
31	At that point I still could not really see the bridge. I just felt that running into the morning fog with the sea wind in my face was very comfortable.
32	▲ Run in Presidio @Arsenan
33	Around mile five, we turned a corner and the Golden Gate Bridge suddenly appeared right in front of us, coming straight toward us.
34	▲ Golden Gate Bridge @Arsenan
35	Half of the bridge was still hiding in the clouds and fog, but all of us were thrilled. We immediately pulled out phones, cameras, pagers, whatever we had, and started taking photos.
36	I joined the photo-taking army too, wildly absorbing bridge pictures.
37	▲ Run with Golden Gate Bridge @FinisherPix
38	When we ran underneath the bridge, there was a turnaround followed by a big climb that felt a little like trail running. It was tiring, but the excitement outweighed the fatigue, because we were about to get onto the Golden Gate Bridge.
39	▲ Run into Golden Gate Bridge @Arsenan
40	Before getting on the bridge, I ran to the roadside to take more photos. Other runners would come over and ask whether I needed help taking a picture. Of course I happily accepted. The best thank-you was to help them take a few photos with the bridge too.
41	▲ Golden Gate Bridge @Runner
42	After coming to the U.S., the biggest lesson I feel I have learned is to actively accept help from others, and then give back when someone needs it. No one can walk alone.
43	Finally, we were getting onto the bridge. The wind was truly strong, roaring beside my ears. Thick fog mixed with rain hit my face. It was a little cold.
44	▲ Run in Golden Gate Bridge @Arsenan
45	Europeans and Americans really are resistant to cold. Some people were running shirtless, which honestly made my jaw drop.
46	But when I looked down at the sea below, the wind was pushing boats across the water and pulling out long ripples. It was spectacular. Overhead, the bridge appeared and disappeared inside the clouds and fog, like we were flying through some palace above the clouds. If this race had been only for this view, I think it still would have been worth it.
47	The bridge is long, about 2.7 kilometers. The freshness of running it for the first time kept me from feeling that this stretch was too hard. Aside from being a bit cold, everything was fine.
48	▲ Downhill @Arsenan
49	▲ Downhill @FinisherPix
50	Then we reached the north side of the bridge and ran downhill. There were lots of photographers here too, and I happily leaned into the cameras, collecting some excellent running photos. I looked festive, so I must have been running happily.
51	▲ Golden Gate Bridge @Inidan Friend
52	By the water, I helped a few Indian friends take bridge photos from different angles, and they helped freeze my own condition in that moment too.
53	▲ Run near Sea @FinisherPix
54	By then we were around mile 12. It was uphill all the way, and we had to cross the bridge again. The near-halfway distance plus the wet weather made me feel even colder, so I quickly pulled my long sleeves down.
55	▲ Cold @FinisherPix
56	The return stretch across the bridge was difficult for me. This time the sea wind was especially strong, and the rain seemed to be getting heavier. Add the earlier uphill effort, and I could no longer run well. I stopped and started walking slowly.
57	▲ Uphill @Arsenan
58	▲ Windy @Arsenan
59	Those 2.7 kilometers of bridge felt like a very long distance to me.
60	In that moment, I truly realized that maybe only when you run on the Golden Gate Bridge can you understand that the core brains of Silicon Valley and the legendary geniuses of business have not only unimaginable mental power, but also astonishing physical stamina.
61	My thoughts started wandering. What if the person running next to me right now was Zuckerberg or Bill Gates? I could not let the big shots laugh at me.
62	A foreign girl beside me kept pushing me too, telling me to start running, keep my body temperature up, and follow behind her.
63	That was how I slowly survived the hardest part of the race. I still failed to keep up with her in the end, but I was grateful for her guidance.
64	Once I came off the bridge, I came back to life. It was downhill, and there was an aid station. I adjusted and got ready for the second half of the marathon.
65	▲ 14 mile @Arsenan
66	Starting around mile 15, we ran through a stretch of neighborhoods. There, I took a sweet snack from a child. It tasted good and helped with energy.
67	▲ Cute @Arsenan
68	▲ Downtown @Arsenan
69	▲ Good Energy @Arsenan
70	After crossing the city, Golden Gate Park was ahead, and on the left was the finish for the first half marathon.
71	▲ Half @Arsenan
72	▲ Half @FinisherPix
73	I was sure 47 had not finished yet, so I did not look much and kept going.
74	Ahead was Slow Lake, green and beautiful, with wild ducks in the water and a Chinese-style pavilion. It felt comfortable. Since this was Slow Lake, I decided there was no need to rush either, so I stopped and walked slowly for a while.
75	▲ Slow Lake @Arsenan
76	After leaving Golden Gate Park, I guess we had also left the weather zone controlled by the Golden Gate Bridge. The sun suddenly got strong and hot. One city, two climates. It was pretty magical.
77	▲ Back to Downtown @FinisherPix
78	In the end I was so hot that I had to take off the green battle shirt that had served with distinction and toss it by the roadside.
79	▲ Too Hot @Arsenan
80	The downtown scenery in the second half did not disappoint. The buildings all had character.
81	The sky was very blue too, and running under it put me in a good mood.
82	Especially at this point, the second-half marathon runners also joined the course. The most obvious feeling was that the aid stations became richer, and the course became lively again.
83	Eileen Gu was in this group. I did see a tall, thin girl run ahead of me, but she disappeared quickly. I still do not know whether it was her.
84	Later there was a special stretch where beer was available. The owner said it was Hope Beer, free only today.
85	▲ Hope Beer @Arsenan
86	After Hope Beer, a turn brought us to Chase Center, home of the NBA's Golden State Warriors. It happened to be the NBA offseason, and I thought I definitely had to come watch Curry play here someday.
87	▲ Chase Center @Arsenan
88	▲ Chase Center @FinisherPix
89	After mile 24, we finally returned to SF Bay. The ocean was healing, and running felt energetic again.
90	▲ SF Giants @Arsenan
91	At mile 25, we reached the home of the MLB San Francisco Giants. The stadium was magnificent and felt even more impressive than the Warriors' arena.
92	▲ SF Bay @Arsenan
93	In the final mile, the sunlight was especially fierce. Not far away was the magnificent Bay Bridge, and the finish line was hidden behind it.
94	▲ Bay Bridge @Arsenan
95	I did not care too much about the time. A little over five hours, I guess, and I crossed the finish.
96	▲ Almost done @FinisherPix
97	▲ Done @FinisherPix
98	▲ Finish @FinisherPix
99	The medal was all right: square and tidy, very engineering-school.
100	I immediately practiced the correct way to take photos by pairing the medal with San Francisco scenery.
101	▲ Medal @Arsenan
102	I called 47 at the finish and learned that she had finished too. She and Anastasia were driving over to pick me up. That was honestly so nice.
103	03
104	Post-race relaxing
105	At noon we ordered a big delivery meal. Since it was still early, we went to walk around the aquarium.
106	▲ Aquarium of the Bay @Arsenan
107	Then we went to Pier 39 for a boat tour, conveniently unlocking the world-famous image of medal plus bridge.
108	▲ Pier 39 @Arsenan
109	▲ Alcatraz Island @Arsenan
110	▲ Boat Tour @Arsenan
111	The wind on the boat was strong. Seeing downtown San Francisco from the water felt special too. Our boat went from the sunny Pier 39 toward the Golden Gate Bridge, which was still wrapped in heavy fog.
112	▲ Medal with Golden Gate Bridge @Arsenan
113	The scenery was good. I took some photos of the medal with the bridge and successfully completed the mission, adding a lot of precious inventory. That also included 47's grand-mage-under-the-bridge photo.
114	▲Archmage47 @Arsenan
115	Postscript
116	Everything looked good. Next, it was time to go home.
117	We waited a long time at the airport. The flight was delayed several times. During the wait, I bought the race photos from San Francisco. They cost roughly half the registration fee, and there were dozens of them. The photos were expensive, but they felt even more precious.
118	In the end, the flight was canceled, so we had to return the next day and gained an extra half day of San Francisco time.
119	▲ SFO airport @Arsenan
120	I did not run into Eileen Gu during the San Francisco Marathon. But compared with the domestic news frenzy over her 1:40 result and second place among women under 19, what I saw more often over those 26.2 miles was simple, ordinary love.
121	This year, the San Francisco Marathon partnered with sponsor Degree to form a special team made up of athletes with disabilities.
122	Zamperla, a participant from Philadelphia, said, "I was diagnosed with eye degeneration in third grade... and by age 30 I was completely blind." Zamperla was grouped with a woman from Houston who has multiple sclerosis, and on Sunday they completed their first marathon together.
123	The race also designed a 1,000-meter family lollipop run especially for children. A mother who participated with her four-year-old daughter said, "I think it is really good to get kids involved. It is especially important for physical health."
124	This year's San Francisco Marathon was also the first race in California history with men's, women's and non-binary divisions, and rainbow flags could be seen flying everywhere along the way.
125	▲ Welcome to San Fracisco "Again" @Arsenan
126	Norris, a participant from Houston, said, "We work so hard just to do basic things, so doing something extra, like a marathon, is very difficult, but very worthwhile."
127	- End -
128	Words | Arsenan
129	Photos | Arsenan
130	Design | Arsenan
"""


SKIP_TEXTS = {"0/0", "继续观看", "★"}
KICKER_TEXTS = {"丨SF丨", "Course丨SF丨"}


def parse_tsv(raw: str) -> dict[int, str]:
    data = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        index, text = line.split("\t", 1)
        data[int(index)] = text
    return data


EN_BY_INDEX = {
    "city": parse_tsv(CITY_EN_TSV),
    "race": parse_tsv(RACE_EN_TSV),
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1700


def has_text_ancestor(el) -> bool:
    return any(parent.tag in ("p", "section") for parent in el.iterancestors())


def extract_article(path: Path, article: str):
    doc = html.fromstring(path.read_text(encoding="utf-8", errors="replace"))
    root = (doc.xpath('//*[@id="js_content"]') or [doc])[0]
    events = []
    seen_text = set()
    text_index = 0
    for el in root.iter():
        if el.tag == "img":
            src = el.get("src") or ""
            if re.search(r"_files/640(\(|$)", src):
                source = (path.parent / src.replace("./", "")).resolve()
                events.append({"type": "image", "source": source, "article": article})
            continue

        if el.tag not in ("p", "section", "span", "strong", "em", "h1", "h2", "h3"):
            continue
        if has_text_ancestor(el):
            continue
        text = norm("".join(el.itertext()))
        if not text or text in SKIP_TEXTS or is_styleish(text):
            continue
        if text in seen_text:
            continue
        seen_text.add(text)
        text_index += 1

        if text.startswith("已关注 Follow"):
            if "My SF Marathon Course @Relive" in text:
                text = "▲ My SF Marathon Course @Relive"
            else:
                continue

        events.append({"type": "text", "text": text, "article": article, "index": text_index})

    end = len(events)
    for idx, event in enumerate(events):
        if event["type"] == "text" and event["text"] == "设计丨Arsenan":
            end = idx + 1
            break
    return events[:end]


def extract_story():
    city_events = extract_article(CITY_HTML, "city")
    race_events = extract_article(RACE_HTML, "race")
    for event in city_events + race_events:
        if event["type"] != "text":
            continue
        if event["index"] not in EN_BY_INDEX[event["article"]]:
            raise RuntimeError(f"Missing translation for {event['article']} #{event['index']}: {event['text']}")
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


def translated(event) -> str:
    return EN_BY_INDEX[event["article"]][event["index"]]


def clean_zh_heading(text: str) -> str:
    text = text[2:].strip() if text.startswith("# ") else text
    text = re.sub(r"[🎨📍].*$", "", text).strip()
    return text


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def fix_caption_typos(text: str) -> str:
    return (
        text.replace("Fancisco", "Francisco")
        .replace("Fracisco", "Francisco")
        .replace("Inidan", "Indian")
        .replace("The Painted Ladiesk", "The Painted Ladies")
        .replace("Ciot Tower", "Coit Tower")
    )


def render_text(event, lang: str) -> str:
    original = event["text"]
    text = clean_zh_heading(original) if lang == "zh" else translated(event)
    text = fix_caption_typos(text)
    if re.fullmatch(r"\d{2}", original):
        return f"<h3>{escape(text)}</h3>"
    if original.startswith("# ") or original in {"前言", "后记"}:
        return f"<h2>{escape(text)}</h2>"
    if original in KICKER_TEXTS:
        return f'<p class="story-kicker-line">{escape(text)}</p>'
    if original == "- 本文完 -":
        return f'<p class="end-mark">{escape(text)}</p>'
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
        text = original if lang == "zh" else translated(event)
        if is_caption(original):
            caption = escape(fix_caption_typos(text))
            if output and output[-1].endswith("</figure>") and "<figcaption>" not in output[-1]:
                output[-1] = output[-1].replace("</figure>", f"<figcaption>{caption}</figcaption></figure>")
            else:
                output.append(f'<p class="caption-line">{caption}</p>')
            continue
        output.append(render_text(event, lang))
    return "\n".join(output)


def engagement_block(lang: str) -> str:
    page_key = f"run50-{SLUG}-zh" if lang == "zh" else f"run50-{SLUG}-en"
    comments_id = "supabase-comments-san-francisco-zh" if lang == "zh" else "supabase-comments-san-francisco-en"
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
        <div id="{comments_id}" data-zz-supabase-comments></div>
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
        <div id="{comments_id}" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
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
        <div id="supabase-comments-san-francisco-fb" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def story_page(lang: str, city_article: str, race_article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    desc = (
        "Run50第4州加州旧金山：流雾、联合广场、金门大桥、唐人街、单车游城，以及2022年7月24日第45届旧金山马拉松。"
        if is_zh
        else "Run50 State 4 in California: San Francisco fog, Union Square, Golden Gate Bridge, Chinatown, a bike tour, and the 45th San Francisco Marathon on July 24, 2022."
    )
    nav_back = "中文故事" if is_zh else "English Stories"
    other = "English" if is_zh else "中文"
    other_href = f"../english/{SLUG}.html" if is_zh else f"../chinese/{SLUG}.html"
    lang_attr = "zh-Hans" if is_zh else "en"
    eyebrow = "Run50 #第4州 · 加州" if is_zh else "Run50 #4 · California"
    deck = desc
    city_label = "城市篇 | 旧金山，流雾之下" if is_zh else "City Story | San Francisco under the rolling fog"
    race_label = "比赛篇 | 第45届旧金山马拉松" if is_zh else "Race Story | The 45th San Francisco Marathon"
    meta_city = "旧金山，加州" if is_zh else "San Francisco, California"
    meta_date = DATE_ZH if is_zh else DATE_EN
    city_alt = "旧金山图标封面" if is_zh else "San Francisco Marathon icon cover"
    return f"""<!doctype html>
<html lang="{lang_attr}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}">
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
    h1 {{ margin:0; font-family:Georgia, "Times New Roman", "Microsoft YaHei", serif; font-size:clamp(34px,5vw,64px); line-height:1.05; letter-spacing:0; }}
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
  <nav class="nav"><a href="./index.html">← {escape(nav_back)}</a><a href="{other_href}">{escape(other)}</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a></nav>
  <header class="hero">
    <div class="hero-card">
      <div>
        <p class="eyebrow">{escape(eyebrow)}</p>
        <h1>{escape(title)}</h1>
        <p class="dek">{escape(deck)}</p>
        <div class="meta-row"><span>{escape(meta_city)}</span><span>{escape(meta_date)}</span><span>Run50 #4</span><span>{escape(RACE_NAME)}</span></div>
      </div>
      <img class="cover" src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="{escape(city_alt)}">
    </div>
  </header>
  <main>
    <p class="part-label">{escape(city_label)}</p>
    <article>
{city_article}
    </article>
    <p class="part-label">{escape(race_label)}</p>
    <article>
{race_article}
    </article>
  </main>
{engagement_block(lang)}
</body>
</html>
"""


def facebook_page(race_article: str, city_article: str) -> str:
    desc = (
        "The July 24, 2022 San Francisco Marathon first: Golden Gate fog, bridge wind, hills, downtown heat and bay light, followed by the full city weekend behind the run."
    )
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
  <meta property="og:image" content="{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}">
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
        <p class="dek">On July 24, 2022, Run50 State 4 took me to the 45th San Francisco Marathon: a hard, beautiful course built from fog, Golden Gate wind, rolling hills, downtown sun and the kind of ordinary kindness that stays with you.</p>
        <div class="meta-row"><span>San Francisco, CA</span><span>{DATE_EN}</span><span>Run50 #4</span><span>Golden Gate course</span></div>
      </div>
      <img src="../../assets/{THUMB_PATH.name}?v={VERSION}" alt="San Francisco Marathon icon cover">
    </div>
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race day</p>
      <p>The San Francisco Marathon is not a flat city cruise. It asks runners to climb, freeze, sweat, and cross one of the most famous bridges in the world. That is why this story starts with the race itself.</p>
{race_article}
      <p class="transition">The marathon gave the trip its shape, but San Francisco had already been working on me before race morning: Karl the fog, Union Square hills, Chinatown breakfast, the Golden Gate at sunset, and a bike ride that looped through the city's many moods.</p>
      <p class="section-label">The city around the race</p>
{city_article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{RACE_NAME}</dd></div>
          <div><dt>Date</dt><dd>{DATE_EN}</dd></div>
          <div><dt>State</dt><dd>California · Run50 #4</dd></div>
          <div><dt>Route memory</dt><dd>Ferry Building start, Presidio fog, Golden Gate Bridge, Golden Gate Park, Chase Center, SF Giants and Bay Bridge sunlight.</dd></div>
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
    draw.text((x + 30, y + 48), "Run50 #04", fill="#20242b", font=font(38, True))
    draw.text((x + 30, y + 113), "CALIFORNIA", fill="#0b67c2", font=font(42, True))


def draw_sf_scene(draw, height: int):
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    sky = "#cfe9f4"
    fog = "#f3f7f9"
    bay = "#74c7d5"
    bridge = "#d85b3f"
    bridge_dark = "#9f3a2d"
    hill = "#8cc96b"
    road = "#4b5563"
    draw.rectangle((0, 0, int(1200 * scale), height), fill=sky)
    draw.ellipse((p(895, 112), p(990, 207)), fill="#f7bc3b")
    draw.polygon([p(0, 430), p(340, 365), p(760, 420), p(1200, 350), p(1200, 630), p(0, 630)], fill=bay)
    draw.polygon([p(0, 420), p(280, 350), p(580, 390), p(900, 345), p(1200, 390), p(1200, 630), p(0, 630)], fill=hill)
    draw.polygon([p(0, 470), p(500, 425), p(1200, 455), p(1200, 630), p(0, 630)], fill="#69b35d")
    for y in (255, 290, 325):
        draw.rounded_rectangle((p(70, y), p(715, y + 34)), radius=int(17 * scale), fill=fog)
    for x in (260, 625):
        draw.rectangle((p(x, 300), p(x + 44, 535)), fill=bridge_dark)
        draw.rectangle((p(x + 8, 300), p(x + 36, 535)), fill=bridge)
        draw.line((p(x + 22, 300), p(x + 22, 250)), fill=bridge_dark, width=max(3, int(5 * scale)))
    draw.line((p(180, 330), p(330, 252)), fill=bridge_dark, width=max(4, int(6 * scale)))
    draw.line((p(330, 252), p(650, 252)), fill=bridge_dark, width=max(4, int(6 * scale)))
    draw.line((p(650, 252), p(760, 340)), fill=bridge_dark, width=max(4, int(6 * scale)))
    draw.line((p(165, 358), p(770, 358)), fill=bridge, width=max(12, int(18 * scale)))
    for x in range(220, 730, 42):
        draw.line((p(x, 270), p(x - 18, 358)), fill=bridge_dark, width=max(2, int(3 * scale)))
    draw.rectangle((p(165, 382), p(770, 415)), fill=road)
    draw.line((p(165, 398), p(770, 398)), fill="#f5d66c", width=max(2, int(3 * scale)))

    # Cable car
    draw.rounded_rectangle((p(820, 425), p(1010, 545)), radius=int(12 * scale), fill="#f7d05a", outline="#20242b", width=max(3, int(5 * scale)))
    draw.rectangle((p(845, 392), p(985, 430)), fill="#e94b35", outline="#20242b", width=max(3, int(4 * scale)))
    for x in (850, 900, 950):
        draw.rectangle((p(x, 448), p(x + 34, 492)), fill="#bde6f3")
    draw.rectangle((p(815, 510), p(1015, 548)), fill="#2f9f72")
    draw.ellipse((p(855, 532), p(900, 577)), fill="#20242b")
    draw.ellipse((p(940, 532), p(985, 577)), fill="#20242b")
    draw.line((p(900, 392), p(780, 270)), fill="#20242b", width=max(2, int(3 * scale)))
    draw.text(p(883, 405), "SF", fill="#20242b", font=font(max(18, int(26 * scale)), True))

    # Runner
    x, y = 555, 485
    draw.ellipse((p(x, y), p(x + 26, y + 26)), fill="#0b67c2")
    draw.line((p(x + 13, y + 26), p(x + 10, y + 70)), fill="#20242b", width=max(3, int(5 * scale)))
    draw.line((p(x + 11, y + 42), p(x - 18, y + 58)), fill="#20242b", width=max(3, int(5 * scale)))
    draw.line((p(x + 12, y + 70), p(x - 8, y + 105)), fill="#20242b", width=max(3, int(5 * scale)))
    draw.line((p(x + 12, y + 70), p(x + 45, y + 94)), fill="#20242b", width=max(3, int(5 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#cfe9f4")
    draw = ImageDraw.Draw(image)
    draw_sf_scene(draw, 630)
    draw.text((64, 64), "SAN FRANCISCO", fill="#20242b", font=font(66, True))
    draw.text((66, 136), "GOLDEN GATE · FOG · HILLS", fill="#667085", font=font(26, True))
    draw_badge(draw, 760, 64, 362, 164)
    image.save(OG_PATH)


def generate_cover_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <rect width="1200" height="750" fill="#cfe9f4"/>
  <circle cx="935" cy="134" r="58" fill="#f7bc3b"/>
  <path d="M0 512 L340 440 L760 510 L1200 430 L1200 750 L0 750Z" fill="#74c7d5"/>
  <path d="M0 500 L280 420 L580 470 L900 415 L1200 465 L1200 750 L0 750Z" fill="#8cc96b"/>
  <path d="M0 560 L500 515 L1200 545 L1200 750 L0 750Z" fill="#69b35d"/>
  <g fill="#f3f7f9">
    <rect x="70" y="305" width="645" height="40" rx="20"/>
    <rect x="45" y="350" width="670" height="40" rx="20"/>
    <rect x="90" y="395" width="610" height="40" rx="20"/>
  </g>
  <g>
    <rect x="260" y="360" width="44" height="280" fill="#9f3a2d"/>
    <rect x="268" y="360" width="28" height="280" fill="#d85b3f"/>
    <rect x="625" y="360" width="44" height="280" fill="#9f3a2d"/>
    <rect x="633" y="360" width="28" height="280" fill="#d85b3f"/>
    <path d="M180 395 L330 300 L650 300 L760 405" fill="none" stroke="#9f3a2d" stroke-width="8"/>
    <line x1="165" y1="428" x2="770" y2="428" stroke="#d85b3f" stroke-width="22"/>
    <rect x="165" y="458" width="605" height="40" fill="#4b5563"/>
    <line x1="165" y1="478" x2="770" y2="478" stroke="#f5d66c" stroke-width="4"/>
    <g stroke="#9f3a2d" stroke-width="4">
      <line x1="220" y1="322" x2="202" y2="428"/><line x1="262" y1="315" x2="244" y2="428"/>
      <line x1="304" y1="307" x2="286" y2="428"/><line x1="346" y1="300" x2="328" y2="428"/>
      <line x1="388" y1="300" x2="370" y2="428"/><line x1="430" y1="300" x2="412" y2="428"/>
      <line x1="472" y1="300" x2="454" y2="428"/><line x1="514" y1="300" x2="496" y2="428"/>
      <line x1="556" y1="300" x2="538" y2="428"/><line x1="598" y1="300" x2="580" y2="428"/>
      <line x1="640" y1="303" x2="622" y2="428"/><line x1="682" y1="333" x2="664" y2="428"/>
    </g>
  </g>
  <g>
    <rect x="820" y="505" width="190" height="120" rx="12" fill="#f7d05a" stroke="#20242b" stroke-width="5"/>
    <rect x="845" y="465" width="140" height="45" fill="#e94b35" stroke="#20242b" stroke-width="4"/>
    <rect x="850" y="535" width="34" height="44" fill="#bde6f3"/>
    <rect x="900" y="535" width="34" height="44" fill="#bde6f3"/>
    <rect x="950" y="535" width="34" height="44" fill="#bde6f3"/>
    <rect x="815" y="600" width="200" height="38" fill="#2f9f72"/>
    <circle cx="878" cy="640" r="23" fill="#20242b"/><circle cx="963" cy="640" r="23" fill="#20242b"/>
    <line x1="900" y1="465" x2="780" y2="320" stroke="#20242b" stroke-width="4"/>
    <text x="883" y="492" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="900" fill="#20242b">SF</text>
  </g>
  <g stroke="#20242b" stroke-width="6" fill="none">
    <circle cx="568" cy="578" r="14" fill="#0b67c2" stroke="none"/>
    <line x1="568" y1="592" x2="565" y2="644"/>
    <line x1="565" y1="612" x2="538" y2="630"/>
    <line x1="565" y1="644" x2="545" y2="690"/>
    <line x1="565" y1="644" x2="600" y2="680"/>
  </g>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">SAN FRANCISCO</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">GOLDEN GATE · FOG · HILLS</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #04</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="43" font-weight="900" fill="#0b67c2">CALIFORNIA</text>
</svg>
'''
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source = RACE_HTML.parent / f"{RACE_HTML.stem}_files" / "640(71)"
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        bg = ImageOps.fit(image, (1200, 750), method=Image.LANCZOS, centering=(0.5, 0.5))
        bg = bg.filter(ImageFilter.GaussianBlur(18))
        overlay = Image.new("RGB", (1200, 750), "#edf3f7")
        bg = Image.blend(bg, overlay, 0.18)
        fg = image.copy()
        fg.thumbnail((1080, 700), Image.LANCZOS)
        x = (1200 - fg.width) // 2
        y = (750 - fg.height) // 2
        bg.paste(fg, (x, y))
        bg.save(MEDAL_COVER_PATH, quality=92)


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>', re.S)
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
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="旧金山马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">加州旧金山 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第4州｜旧金山马拉松</h2>
          <p class="story-desc">城市篇与比赛篇合并：流雾Karl、联合广场、金门大桥、唐人街、单车游城，以及45届旧金山马拉松的桥风、山坡和湾区阳光。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for San Francisco Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">California · San Francisco · {DATE_ZH}</div>
          <h2>San Francisco Marathon: Golden Gate fog, hills and bay light</h2>
          <p>A two-part San Francisco weekend: Karl the fog, Chinatown breakfast, Golden Gate sunset, biking the city, then a hard beautiful marathon across the bridge.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>San Francisco turned 26.2 miles into fog, bridge wind, hills and bay light</h2>
        <p>Race date: July 24, 2022. State 4 of Run50 crossed the Golden Gate Bridge, ran through fog and sudden sun, and ended with a medal beside the bay.</p>
        <div class="meta"><span>San Francisco, CA</span><span>Run50 #4</span><span>Golden Gate course</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style San Francisco Marathon cover">
    </a>
"""

    text = remove_existing_card(zh_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./new-york-city-marathon.html", zh_card, '<section class="story-grid"')
    text = re.sub(r"\s*'CA-旧金山': 'san-francisco-marathon.html',?\n", "\n", text)
    text = text.replace(
        "'NY-纽约市': 'new-york-city-marathon.html'",
        "'NY-纽约市': 'new-york-city-marathon.html',\n      'CA-旧金山': 'san-francisco-marathon.html'",
        1,
    )
    zh_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(en_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./new-york-city-marathon.html", en_card, '<section class="story-grid"')
    text = re.sub(r"\s*'CA-San Francisco': 'san-francisco-marathon.html',?\n", "\n", text)
    text = text.replace(
        "'NY-New York City': 'new-york-city-marathon.html'",
        "'NY-New York City': 'new-york-city-marathon.html',\n      'CA-San Francisco': 'san-francisco-marathon.html'",
        1,
    )
    en_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./new-york-city-marathon.html", fb_card, '<main class="shell">')
    fb_path.write_text(clean_text(text), encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- San Francisco Run50 story -->.*?<!-- /San Francisco Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- San Francisco Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="{escape(TITLE_FB)}">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style San Francisco Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">{escape(TITLE_FB)}</a>
            <p class="video-sub">San Francisco, CA &middot; Jul 24, 2022</p>
          </div>
        </div>
      </article>
      <!-- /San Francisco Run50 story -->
"""
    text = text.replace("      <!-- /New York Run50 story -->\n", "      <!-- /New York Run50 story -->\n" + card, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    if "'San Francisco':{lat:37.7749,lon:-122.4194}" not in text:
        text = text.replace(
            "'New York City':{lat:40.7128,lon:-74.0060},'Cincinnati'",
            "'New York City':{lat:40.7128,lon:-74.0060},'San Francisco':{lat:37.7749,lon:-122.4194},'Cincinnati'",
            1,
        )
    text = re.sub(r"^\s*'CA':\[\{city:'San Francisco'.*?\}\],\n", "", text, flags=re.M)
    text = text.replace(
        "  'NY':[{city:'New York City',date:'Nov 7, 2021',story:'stories/english/new-york-city-marathon.html',fb:'facebook/new-york-city-marathon.html'}],",
        "  'NY':[{city:'New York City',date:'Nov 7, 2021',story:'stories/english/new-york-city-marathon.html',fb:'facebook/new-york-city-marathon.html'}],\n"
        "  'CA':[{city:'San Francisco',date:'Jul 24, 2022',story:'stories/english/san-francisco-marathon.html',fb:'facebook/san-francisco-marathon.html'}],",
        1,
    )
    text = re.sub(
        r"\n\s*<!-- California San Francisco story dot -->.*?<!-- /California San Francisco story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    dot = """
    <!-- California San Francisco story dot -->
    <circle cx="183" cy="137" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="183" cy="137" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="San Francisco, CA" data-date="Jul 24, 2022" data-story="stories/english/san-francisco-marathon.html"/>
    <!-- /California San Francisco story dot -->
"""
    text = text.replace("    <!-- /New York City story dot -->\n", "    <!-- /New York City story dot -->\n" + dot, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 15 stories", " 16 stories")
    text = text.replace("<strong>15</strong> stories", "<strong>16</strong> stories")
    path.write_text(clean_text(text), encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        f"run50-{SLUG}-facebook-en",
        f"run50-{SLUG}-en",
        f"run50-{SLUG}-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-new-york-city-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(clean_text(text), encoding="utf-8")


def main():
    city_events, race_events = extract_story()
    all_events = city_events + race_events
    image_count = copy_story_images(all_events)
    city_zh = render_events(city_events, "zh", "Run50-SanFrancisco-Marathon-clean_files/", "旧金山照片")
    race_zh = render_events(race_events, "zh", "Run50-SanFrancisco-Marathon-clean_files/", "旧金山马拉松照片")
    city_en = render_events(city_events, "en", "../chinese/Run50-SanFrancisco-Marathon-clean_files/", "San Francisco photo")
    race_en = render_events(race_events, "en", "../chinese/Run50-SanFrancisco-Marathon-clean_files/", "San Francisco Marathon photo")
    city_fb = render_events(city_events, "en", "../stories/chinese/Run50-SanFrancisco-Marathon-clean_files/", "San Francisco photo")
    race_fb = render_events(race_events, "en", "../stories/chinese/Run50-SanFrancisco-Marathon-clean_files/", "San Francisco Marathon photo")

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
    shutil.copyfile(THUMB_PATH, FB_THUMB_PATH)
    generate_medal_cover()
    update_story_indexes()
    update_root_home()
    update_hub()
    update_landing_counts()
    update_supabase_sql()
    print(f"Built {SLUG}: {image_count} images, {len(city_events)} city events, {len(race_events)} race events")


if __name__ == "__main__":
    main()
