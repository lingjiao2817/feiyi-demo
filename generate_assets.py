from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('assets', exist_ok=True)

texts = {
    'standard.png': '标准动作\n(待替换)',
    'step1.png': '第1步\n预备握槌',
    'step2.png': '第2步\n内旋启动',
    'step3.png': '第3步\n水平控槌',
    'step4.png': '第4步\n还原定型',
}

for filename, text in texts.items():
    img = Image.new('RGB', (400, 300), color=(248, 236, 224))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 380, 280], outline=(200, 16, 46), width=3)
    draw.text((200, 130), text, fill=(200, 16, 46), anchor='mm')
    img.save(f'assets/{filename}')
    print(f'已生成: assets/{filename}')
