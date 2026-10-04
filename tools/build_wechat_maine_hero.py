from pathlib import Path
import subprocess,tempfile
r=Path.cwd()
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['ME-33-2','ME-08','ME-25-1','ME-40','ME-41-1','ME-37-1','ME-44','ME-43-1']):
  # Every frame is a real square crop, with no padded borders.
  vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900'
  if key=='ME-37-1':vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900:0:ih-900'
  if key=='ME-43-1':vf='crop=1080:1080:0:180,scale=900:900'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/maine-editorial/{key}.jpg'),'-vf',vf,'-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 from shutil import copyfile
 copyfile(Path(td)/'00.png',r/'assets/maine-editorial/hero-still.png')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/maine-editorial/hero.gif')],check=True)
