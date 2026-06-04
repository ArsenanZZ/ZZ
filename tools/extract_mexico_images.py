import re
import os

zh_path = r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-zh-standalone.html"
en_path = r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-en-standalone.html"
fb_path = r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-fb-standalone.html"

def count_images(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all base64 images
    matches = re.findall(r'src="data:image/[^;]+;base64,([^"]+)"', content)
    print(f"{os.path.basename(path)} has {len(matches)} base64 images")
    return len(matches)

count_images(zh_path)
count_images(en_path)
count_images(fb_path)
