from pathlib import Path
import build_wechat_michigan_assets as base
extra=[('NH','Keene',42.9337,-72.2781,'#e89838'),('LA','Baton Rouge',30.4515,-91.1871,'#98c038'),('VA','Roanoke',37.271,-79.9414,'#5ca860'),('ND','Fargo',46.8772,-96.7898,'#5ca860'),('KS','El Dorado',37.8172,-96.8623,'#3898a8'),('VT','Warren',44.1206,-72.8556,'#98c038'),('AL','Huntsville',34.7304,-86.5861,'#98c038'),('AZ','Buckeye',33.3703,-112.5838,'#e89838'),('DE','Wilmington',39.7391,-75.5398,'#e89838'),('MN','Rochester',44.0121,-92.4802,'#e89838'),('CT','Simsbury',41.8759,-72.8012,'#9068c0'),('RI','Woonsocket',42.0029,-71.5148,'#d4614a'),('MA','Holyoke',42.2043,-72.6162,'#3898a8'),('ME','Sanford',43.4392,-70.7742,'#d4614a'),('NE','Omaha',41.2565,-95.9345,'#3898a8')]
extra=extra[:11]
base.RUN50_FIRST_21 += [x[0] for x in extra]
base.COLORS.update({x[0]:x[4] for x in extra});base.CITY_DOTS += [x[:4] for x in extra]
markup=base.build_html().replace('STATE_PATHS.MI','STATE_PATHS.CT').replace('if (abbr === "MI")','if (abbr === "CT")')
markup=markup.replace('"NY:New York City":','"NH:Keene": {x:1510,y:320}, "VT:Warren": {x:1466,y:270}, "CT:Simsbury": {x:1488,y:380}, "RI:Woonsocket": {x:1488,y:376}, "NY:New York City":')
(base.ROOT/'tmp/wechat-connecticut-editorial-map.html').write_text(markup,encoding='utf-8')
