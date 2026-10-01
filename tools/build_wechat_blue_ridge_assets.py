"""Prepare original-photo GIF and clipboard assets for Blue Ridge."""
from pathlib import Path
import json,shutil,subprocess,tempfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PHOTO=ROOT/'assets/blue-ridge-marathon-magazine-photos-v2'
COPY=ROOT/'assets/blue-ridge-wechat-copy';COPY.mkdir(exist_ok=True)
data=json.loads((ROOT/'tools/data/blue-ridge-wechat-editorial.json').read_text(encoding='utf-8'))
for b in data['blocks']:
 for im in b.get('images',[b]):
  if 'src' not in im:continue
  p=ROOT/im['src'].lstrip('/');out=COPY/(p.stem+'.jpg')
  pic=Image.open(p).convert('RGB');pic.thumbnail((1080,2000));pic.save(out,quality=88)
for n in range(1,10):shutil.copy2(ROOT/f'assets/new-hampshire-wechat-copy/number-{n:02}-universal.png',COPY)
for theme in ['light','dark']:shutil.copy2(ROOT/f'assets/louisiana-wechat-copy/arrows-{theme}.png',COPY)
for src,name in [('assets/cn-article-maps/us-light-cc00be9f9ec484c8.png','map'),('assets/wechat-blue-ridge-poster.png','poster')]:
 pic=Image.open(ROOT/src).convert('RGB');pic.thumbnail((1400,2000));pic.save(COPY/(name+'.jpg'),quality=90)
with tempfile.TemporaryDirectory() as directory:
 folder=Path(directory)
 for i,n in enumerate(['va-062-2','va-039','va-025','va-066-1','va-066']):
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(PHOTO/(n+'.webp')),'-vf','scale=900:820:force_original_aspect_ratio=increase,crop=900:820:0:0' if i==0 else 'scale=900:820:force_original_aspect_ratio=increase,crop=900:820','-frames:v','1',str(folder/f'{i:02}.png')],check=True)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(folder/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(ROOT/'assets/blue-ridge-wechat-hero.gif')],check=True)
