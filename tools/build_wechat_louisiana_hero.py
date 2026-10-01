"""Five-photo opening: race, Siqi selfie, LSU tiger, mile 20 and Baton Rouge."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
PHOTO=ROOT/'run50/stories/chinese/Run50-Louisiana-Marathon-clean_files'
with tempfile.TemporaryDirectory() as directory:
 folder=Path(directory)
 for i,n in enumerate(['img-042','la-052-1','img-067','la-067-3','la-067-1']):
  crop='crop=900:820:0:0' if n=='la-067-1' else 'crop=900:820'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str((PHOTO if n.startswith('img-') else ROOT/'assets/louisiana-magazine-photos')/(n+'.webp')),'-vf','scale=900:820:force_original_aspect_ratio=increase,'+crop,'-frames:v','1',str(folder/f'{i:02}.png')],check=True)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(folder/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(ROOT/'assets/louisiana-wechat-hero.gif')],check=True)
