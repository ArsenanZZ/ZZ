from pathlib import Path
import subprocess,tempfile
r=Path.cwd()
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['CT-50','CT-59','CT-42','CT-55-1','CT-57']):
  vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900:0:0' if key in ['CT-50','CT-42'] else 'scale=900:900:force_original_aspect_ratio=increase,crop=900:900'
  if key=='CT-55-1':vf='scale=900:900:force_original_aspect_ratio=decrease,pad=900:900:(ow-iw)/2:(oh-ih)/2:color=0xf5f1e6'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/connecticut-editorial/{key}.jpg'),'-vf',vf,'-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/connecticut-editorial/hero.gif')],check=True)
