"""Prepare the established Run50 SVG for the NH editorial renderer."""
from pathlib import Path
import build_wechat_michigan_assets as base
base.RUN50_FIRST_21 = [*base.RUN50_FIRST_21, 'NH']
base.COLORS['NH']='#e89838'
base.CITY_DOTS=[*base.CITY_DOTS, ('NH','Keene',42.9337,-72.2781)]
markup=base.build_html().replace('STATE_PATHS.MI','STATE_PATHS.NH').replace('if (abbr === "MI")','if (abbr === "NH")')
markup=markup.replace('"NY:New York City":','"NH:Keene": { x: 1510, y: 320 }, "NY:New York City":')
(base.ROOT/'tmp').mkdir(exist_ok=True)
(base.ROOT/'tmp/wechat-new-hampshire-editorial-map.html').write_text(markup,encoding='utf-8')
