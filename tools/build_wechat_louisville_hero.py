"""Seven-photo opening: Siqi first, race, both parents' groups and medal."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
PHOTO=ROOT/'run50/stories/chinese/Run50-Louisville-Marathon-2024-clean_files'
with tempfile.TemporaryDirectory() as directory:
 folder=Path(directory)
 for i,n in enumerate([82,53,16,44,91,92,57]):
  crop='crop=900:820:(iw-900)/2:0' if n==82 else 'crop=900:820'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(PHOTO/f'img-{n:03}.webp'),'-vf','scale=900:820:force_original_aspect_ratio=increase,'+crop,'-frames:v','1',str(folder/f'{i:02}.png')],check=True)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','1/3','-i',str(folder/'%02d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(ROOT/'assets/louisville-wechat-hero.gif')],check=True)
