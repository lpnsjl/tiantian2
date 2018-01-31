# -*- coding: UTF-8 -*
"""
1 生成验证码
2 sha1加密
3 生成seeion_id的随机字符串
"""
from PIL import ImageDraw,Image,ImageFont
import random,string,os
from datetime import datetime
from django.core.cache import cache
from dailyfresh import settings
from hashlib import sha1

# 1111111111111111111111111
# 图片的背景色
backcolor = (random.randint(0,100),random.randint(0,100),255)
# 图片的宽高
width = 100
height = 30
#字体的颜色
fontcolor = (100,100,255)

# 生成验证码文本
def get_text():
    text_list = list(string.ascii_letters)
    for i in range(10):
        text_list.append(str(i))

    text = ''.join(random.sample(text_list,4))
    return text.lower()

# 绘制干扰点
def draw_point(draw):
    for i in range(100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        draw.point(xy,fill)

def get_verify_code(path,filename):
    image = Image.new('RGB',(width,height),backcolor)
    draw = ImageDraw.Draw(image)
    draw_point(draw)
    font = ImageFont.truetype('arial.ttf', 25)

    text = get_text()
    draw.text((5, 2), text=text[0], fill=fontcolor,font=font)
    draw.text((30, 2), text=text[1], fill=fontcolor, font=font)
    draw.text((55, 2), text=text[2], fill=fontcolor, font=font)
    draw.text((80, 2), text=text[3], fill=fontcolor, font=font)

    del draw

    image.save('%s/%s.png'% (path,filename))
    return text

def cache_verify_code():
    verify_code_path = os.path.join(settings.BASE_DIR, 'static/code_image')
    now = datetime.now()
    t = now.timestamp()
    filename = ''.join(str(t).split('.'))
    verify_code = get_verify_code(verify_code_path, filename)
    # 将验证码存入缓存中
    cache.set(filename, verify_code, 30)
    return filename

# 2222222222222222222222222222222222222
# sha1加密
def encrypte(text):
    s = sha1()
    s.update(text.encode('utf-8'))
    new_text = s.hexdigest()
    return new_text

def get_seesion_id():
    text_list = list(string.ascii_letters)
    for i in range(50):
        text_list.append(str(i))
    text = ''.join(random.sample(text_list,10))
    session_id = encrypte(text)
    return session_id

if __name__ == '__main__':
    get_verify_code('C:/Users/佘俊林/Desktop','aa')