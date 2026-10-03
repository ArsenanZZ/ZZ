from pathlib import Path
import subprocess,tempfile
r=Path.cwd()
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['MA-50-1','MA-27-1','MA-49-1','MA-37-3','MA-48']):
  vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900:0:0' if key in ['MA-50-1'] else 'scale=900:900:force_original_aspect_ratio=increase,crop=900:900'
  if key=='MA-49-1':vf='scale=900:900:force_original_aspect_ratio=decrease,pad=900:900:(ow-iw)/2:(oh-ih)/2:color=0xf5f1e6'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/massachusetts-editorial/{key}.jpg'),'-vf',vf,'-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 from shutil import copyfile
 copyfile(Path(td)/'00.png',r/'assets/massachusetts-editorial/hero-still.png')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/massachusetts-editorial/hero.gif')],check=True)
