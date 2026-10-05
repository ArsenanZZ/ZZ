"""Five source photographs, square opening with a matching reduced-motion still."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
PHOTO=ROOT/'run50/stories/chinese/Run50-Louisville-Marathon-2024-clean_files'
def build():
    frames=[]
    for n in [82,53,91,92,57]:
        with Image.open(PHOTO/f'img-{n:03}.webp') as im:
            frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=(0 if n==57 else .5,.15 if n==82 else .5)))
    frames[0].save(ROOT/'assets/louisville-wechat-hero-paper-era-still.png')
    frames[0].save(ROOT/'assets/louisville-wechat-hero-paper-era.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)
    sheet=Image.new('RGB',(1500,300))
    for i,im in enumerate(frames):sheet.paste(im.resize((300,300)),(i*300,0))
    (ROOT/'tmp').mkdir(exist_ok=True);sheet.save(ROOT/'tmp/louisville-paper-hero-check.jpg')
if __name__=='__main__':build()
