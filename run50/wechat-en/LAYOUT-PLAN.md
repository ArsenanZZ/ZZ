# Run50 wechat-en 版式分配方案（Design Bible v1）

> 2026-07-06 制定。默认暗色（现有 `html{color-scheme:dark}` + `.theme-toggle` 一键切亮色，保留不动）。
> 原则：**品牌统一（字体/导航/页脚/分享/暗色系）+ 每篇版式按故事性格分配**。

## 全站不变的设计系统

- 背景：`#0b1020`（暗）/ `#f5f7fb`（亮），正文 `#dbe7f6` / `#17212b`
- 标题字体 Georgia serif，正文 Inter，行高 1.9 左右
- 顶部导航、theme-toggle、"One more mile saved for the story." 结尾卡、上一篇/下一篇、分享按钮 —— 全站一致
- 每篇一个 **Accent Color**（按州/城市气质），只用于：强调色、Quote 边线、章节标题左边线、finish-line 卡、链接 hover

## 六种版式

| 代号 | 名字 | 参考 | 结构骨架 | 适合 |
|---|---|---|---|---|
| A | Journey | Apple Stories / Airbnb | 全屏Hero → 一句Hook → Day Timeline → 正文+图交替 → 地图 → Reflection | 旅行叙事、城市漫游 |
| B | Documentary | National Geographic | Hero → 大Quote → 正文 → 全宽图 → Quote → Gallery → Ending | 历史/文化/人物厚重的长篇 |
| C | Race Report | Strava / ESPN / Nike | Hero → 大成绩数字 → Stats卡 → 赛道图+海拔 → Mile分段 → 冲线 → Result | PB、夺冠、破四、特殊赛制 |
| D | Visual Story | Instagram / Apple图片流 | 大图 → 一句话 → 大图 → 一句话，文字极少 | 照片多、文字少、节日感 |
| E | Magazine | Medium / NYT Magazine | 标题 → Summary → 长正文 → Quote → Highlight → Ending | 思考、回忆、文字驱动 |
| F | Adventure | Patagonia / BBC Earth | Hero → 地图 → 海拔/天气卡 → 故事 → Gallery → Reflection | 越野、山地、极端环境 |

## 分配总表（61 篇）

图/字 = 图片数/英文词数，作为版式判断依据。

### Layout A — Journey（16 篇）

| 文件 | 故事 | 图/字 | Accent | Hero 建议 |
|---|---|---|---|---|
| cleveland | OH 从黑夜跑到天亮 | 65/2356 | 湖蓝 #38bdf8 | 湖畔清晨大图 |
| san-francisco | CA 雾中金门 | 77/2755 | 雾灰橙 #fb923c | 金门大桥雾景 |
| atlanta | GA 奥运五环 | 61/2344 | 金 #fbbf24 | 奥运公园 |
| denver-colfax | CO 一英里高城 | 148/4472 | 祖母绿 #34d399 | 落基山天际线 |
| north-carolina-oak-island | NC 海岛 | 98/3510 | 海蓝 #22d3ee | 海滩日出 |
| little-rock | AR | 92/3465 | 紫红 #e879f9 | 大奖牌特写 |
| new-hampshire-clarence-demar | NH 新英格兰 | 120/3731 | 枫叶红 #f87171 | 秋色公路 |
| fargo | ND | 77/3258 | 麦金 #fde047 | 平原地平线 |
| mad-marathon | VT 绿山（Apple 风格代表作） | 87/4071 | 绿 #4ade80 | 山谷全屏+一句话 |
| rocket-city | AL 火箭城 | 114/3298 | 火箭橙 #f97316 | 土星五号火箭 |
| hong-kong | 香港街马 | 102/3843 | 霓虹粉 #f472b6 | 夜景街道 |
| haikou | 海口 诗和星海 | 90/3672 | 星夜蓝 #818cf8 | 海边夜景 |
| west-lake-half | 西湖偶遇 | 52/2159 | 龙井绿 #86efac | 西湖晨雾 |
| ningbo-dongqian-lake | 宁波东钱湖 | 56/2488 | 湖绿 #2dd4bf | 湖面 |
| bangkok | 曼谷日与夜（用 Day/Night 双段 Timeline） | 102/4254 | 金橙 #fbbf24 | 夜市灯光 |
| pisa | 意大利比萨 | 110/3415 | 托斯卡纳黄 #facc15 | 斜塔 |

### Layout B — Documentary（16 篇）

| 文件 | 故事 | 图/字 | Accent | Hero 建议 |
|---|---|---|---|---|
| disney（旗舰长篇，可加章节目录） | FL Key West+Disney，386图/万词 | 386/10078 | 魔法紫 #c084fc | 城堡烟花，全屏 |
| honolulu | HI 两届火奴鲁鲁 | 248/7826 | 彩虹青 #22d3ee | 钻石头山航拍 |
| chicago | IL 第45届芝加哥大满贯 | 193/4103 | 城市蓝 #60a5fa | 摩天楼人海 |
| west-virginia | WV Marshall 大学(空难历史) | 196/3360 | 军绿 #84cc16 | 体育场，庄重 |
| san-antonio | TX 河滨步道 | 252/4959 | 辣椒红 #ef4444 | Riverwalk |
| st-joseph | MO 首届小镇马 | 139/3273 | 复古棕 #d4a669 | 小镇主街 |
| louisville-2024 | KY 博士毕业冲线 | 112/2987 | 学位金 #fde047 | 冲线+博士袍 |
| louisiana | LA 法式南方 | 71/3066 | 紫金绿(Mardi Gras) #a78bfa | 州府大楼 |
| arizona-phoenix | AZ 沙漠 | 88/3216 | 沙漠橙 #fb923c | 仙人掌日落 |
| guilin | 桂林山水 | 89/3128 | 山水青 #2dd4bf | 漓江群峰 |
| xian-city-wall | 西安城墙雨中 | 109/5409 | 古城灰金 #d4a669 | 雨中城墙 |
| lanzhou | 兰州河西走廊 | 137/4869 | 黄河土黄 #eab308 | 黄河铁桥 |
| wuhan-marathon-2018 | 武汉跨世纪 | 124/4781 | 长江蓝 #60a5fa | 长江大桥 |
| wuhan-wuxi | 樱花三城 | 118/4525 | 樱粉 #f9a8d4 | 樱花大道 |
| singapore-sundown | 新加坡十年重返 | 108/4559 | 赤道青 #2dd4bf | 夜跑灯海 |
| mexico | 墨西哥城高原 | 107/4335 | 玛雅绿红 #34d399 | 宪法广场 |

### Layout C — Race Report（6 篇）

| 文件 | 故事 | 图/字 | Accent | Hero 建议 |
|---|---|---|---|---|
| kentucky-derby（主场破四，Nike"Finally"式开场） | 巨大 "3:5X" 数字 | 85/3855 | 玫瑰金 #f8dc8a | 冲线照全屏+成绩 |
| kentucky-derby-2025 | 第50个马拉松里程碑 | 77/2326 | 冠军金 #fbbf24 | "50" 大数字 |
| hell-on-gravel | KS 碎石路夺冠(ESPN式) | 71/3987 | 冠军红 #ef4444 | 领奖照+CHAMPION |
| south-carolina | 冲BQ未果 "Too Slow for Boston" | 68/2621 | 波士顿蓝 #60a5fa | 配速表/表情 |
| michigan-meadows | 六圈公园(心理战) | 86/2701 | 湖蓝 #38bdf8 | 圈数图 |
| shanghai-vertical | 上海中心垂直马(楼层当里程) | 48/1814 | 天际银蓝 #94a3b8 | 上海中心仰拍 |

### Layout D — Visual Story（7 篇）

| 文件 | 故事 | 图/字 | Accent | Hero 建议 |
|---|---|---|---|---|
| nashville | TN 音乐城，图多 | 182/3496 | 霓虹紫 #c084fc | 百老汇霓虹 |
| green-bay | WI Lambeau 包装工 | 122/2276 | 包装工绿金 #4ade80 | Lambeau Field |
| kentucky-derby-2023 | 全城跑步派对 | 98/2936 | 派对粉 #f472b6 | 人群嘉年华 |
| cincinnati-flying-pig | 飞猪嘉年华 | 92/3261 | 小猪粉 #f9a8d4 | 飞猪装扮 |
| miami | 穿CR7球衣进梅西主场 | 102/3455 | 迈阿密青粉 #22d3ee | 球场/海滩 |
| indianapolis | IN 一日往返 | 56/1751 | 赛车灰 #94a3b8 | 纪念碑环岛 |
| wuhan-graduation | 凤凰岭夜跑+毕业相册 | 51/1076 | 毕业蓝 #818cf8 | 相册拼图 |

### Layout E — Magazine（10 篇）

| 文件 | 故事 | 图/字 | Accent | 备注 |
|---|---|---|---|---|
| louisville | KY 北美第一马(起点回忆) | 26/1525 | 蓝草蓝 #60a5fa | 系列的"序章"感 |
| kentucky-derby-2021 | 半年跑步日记 | 41/1427 | 日记灰蓝 #94a3b8 | 日记体排版 |
| new-york-city | 第50届NYC打卡(NYT风格) | 57/1985 | NYT黑白+金 #fde047 | 大标题serif |
| steel-tank-story | 钢罐的故事(跑步起源) | 26/2927 | 钢铁灰 #94a3b8 | 全系列精神原点，值得精排 |
| three-city-pilgrimage | 三城朝圣 | 15/2835 | 朱砂红 #f87171 | 文字驱动 |
| xiamen | 最难忘的中签 | 18/2920 | 鹭岛青 #2dd4bf | 文字驱动 |
| wuhan-han-marathon | 汉马私人记忆(最长情感文) | 115/5958 | 记忆暖黄 #fde68a | 图虽多但文字是主角 |
| harbin | 东北回家 | 57/2283 | 冰雪蓝 #7dd3fc | 乡愁散文 |
| hatfield-mccoy | ⚠️ 草稿(1图/946词) | 1/946 | 待定 | 先补内容再排版 |
| pittsburgh | ⚠️ 草稿(1图/992词) | 1/992 | 待定 | 先补内容再排版 |

### Layout F — Adventure（4 篇）

| 文件 | 故事 | 图/字 | Accent | Hero 建议 |
|---|---|---|---|---|
| anchorage | AK 阿拉斯加(BBC Earth 感) | 173/3182 | 冰蓝 #7dd3fc | 超宽雪山/冰川 |
| blue-ridge | VA 全美最难公路马 | 85/3934 | 山脊青黛 #818cf8 | 海拔剖面图开场 |
| guiyang-marathon-climb | 贵阳爬升 | 71/3911 | 喀斯特绿 #34d399 | 山城折线 |
| dalian-trail | 大连越野 | 50/3061 | 海崖蓝 #38bdf8 | 山海线航拍 |

## 实施顺序建议

1. **试点 3 篇**先做出效果再铺开：`mad-marathon`(A/Apple)、`hell-on-gravel`(C/夺冠)、`anchorage`(F/Alaska)
2. 每种版式做成一套可复制的 HTML section 骨架 + CSS class（`layout-a` … `layout-f`），accent 用 CSS 变量 `--accent` 每篇一行搞定
3. 暗/亮切换沿用现有 `data-theme` 机制，新版式所有颜色都写成暗色默认 + `[data-theme=light]` 覆盖
4. FB 分享：每篇补 `og:image`（用 Hero 图）、`og:description`（用一句 Hook）
