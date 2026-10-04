from pathlib import Path
import subprocess,tempfile
r=Path.cwd()
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['ME-33-2','ME-47','ME-41-1','ME-37-1','ME-44']):
  vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900:0:0' if key in ['ME-33-2','ME-37-1'] else 'scale=900:900:force_original_aspect_ratio=increase,crop=900:900'
  if key in ['ME-41-1','ME-44','ME-47']:vf='scale=900:900:force_original_aspect_ratio=decrease,pad=900:900:(ow-iw)/2:(oh-ih)/2:color=0xf5f1e6'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/maine-editorial/{key}.jpg'),'-vf',vf,'-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 from shutil import copyfile
 copyfile(Path(td)/'00.png',r/'assets/maine-editorial/hero-still.png')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/maine-editorial/hero.gif')],check=True)
