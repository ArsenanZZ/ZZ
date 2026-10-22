"""Validate the published RunCN map references and historical cutoffs."""
import json
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'tools/data/runcn-map-timeline.json').read_text(encoding='utf8'))
assert [x['station'] for x in data['stations']]==list(range(1,31))
for n,absent in [(27,{'cn_yunnan','cn_tibet','cn_qinghai'}),(28,{'cn_tibet','cn_qinghai'}),(29,{'cn_qinghai'})]:
    visited={s['province'] for s in data['stations'] if s['station']<=n}
    assert not visited&absent,(n,visited&absent)
assert 'cn_anhui' in {s['province'] for s in data['stations'] if s['station']<=6}
for c in data['pages']:
    src='/assets/runcn-article-maps-20261022/'+c['slug']+'.jpg'
    with Image.open(ROOT/src.lstrip('/')) as im:assert im.size==(1800,1290),src
    for suffix in ['editorial','modern-rail']:
        p=ROOT/'run50/wechat'/f'{c["slug"]}-{suffix}.html'
        soup=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
        image=soup.select_one('.map-poster img,.location-poster img')
        assert image['src']==src,p
        assert image['width']=='1800' and image['height']=='1290',p
        assert 'padding:0!important' in soup.style.get_text(),p
print('23 historical maps / 46 article URLs: references, dimensions and milestone cutoffs passed.')
