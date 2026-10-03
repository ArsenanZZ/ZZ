from pathlib import Path
import subprocess,tempfile
r=Path.cwd()
with tempfile.TemporaryDirectory() as td:
 for i,key in enumerate(['RI-009','RI-006','RI-025-1','RI-022','RI-002']):
  vf='scale=900:900:force_original_aspect_ratio=increase,crop=900:900:0:0' if key in ['RI-009','RI-022'] else 'scale=900:900:force_original_aspect_ratio=increase,crop=900:900'
  if False:vf='scale=900:900:force_original_aspect_ratio=decrease,pad=900:900:(ow-iw)/2:(oh-ih)/2:color=0xf5f1e6'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(r/f'assets/rhode-island-editorial/{key}.jpg'),'-vf',vf,'-frames:v','1',str(Path(td)/f'{i:02}.png')],check=True)
 from shutil import copyfile
 copyfile(Path(td)/'00.png',r/'assets/rhode-island-editorial/hero-still.png')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(Path(td)/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(r/'assets/rhode-island-editorial/hero.gif')],check=True)
