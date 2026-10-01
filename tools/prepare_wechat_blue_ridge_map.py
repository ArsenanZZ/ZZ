"""Prepare the established Run50 SVG for the NH editorial renderer."""
from pathlib import Path
import build_wechat_michigan_assets as base
base.RUN50_FIRST_21 = [*base.RUN50_FIRST_21, 'NH', 'LA', 'VA']
base.COLORS['NH']='#e89838'
base.COLORS['LA']='#b2cb36'
base.COLORS['VA']='#70ad67'
base.CITY_DOTS=[*base.CITY_DOTS, ('NH','Keene',42.9337,-72.2781), ('LA','Baton Rouge',30.4515,-91.1871), ('VA','Roanoke',37.27097,-79.94143)]
markup=base.build_html().replace('STATE_PATHS.MI','STATE_PATHS.VA').replace('if (abbr === "MI")','if (abbr === "VA")')
markup=markup.replace('"NY:New York City":','"NH:Keene": { x: 1510, y: 320 }, "NY:New York City":')
(base.ROOT/'tmp').mkdir(exist_ok=True)
(base.ROOT/'tmp/wechat-blue-ridge-editorial-map.html').write_text(markup,encoding='utf-8')
