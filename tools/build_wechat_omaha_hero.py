from pathlib import Path
import json,subprocess,tempfile
from PIL import Image,ImageOps
import pillow_heif
pillow_heif.register_heif_opener()
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['P195','P196','P181','P211','P203']):
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/omaha-2026/{key}.jpg'),'-vf','scale=900:820:force_original_aspect_ratio=increase,crop=900:820:0:0' if key in ['P195','P196','P203'] else 'scale=900:820:force_original_aspect_ratio=increase,crop=900:820','-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/omaha-2026/hero.gif')],check=True)
