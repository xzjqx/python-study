# -*- coding:utf-8 -*-
# 第 0000 题：将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果
from PIL import Image, ImageDraw, ImageFont
def add_num(picture, num):
    img = Image.open(picture)
    x, y = img.size
    myfont = ImageFont.truetype('arial.ttf', x / 3)
    ImageDraw.Draw(img).text((4 * x / 5, -10), str(num), font = myfont, fill = 'red')
    img.save('face1_with_num.jpg')

if __name__ == '__main__':
    add_num('face1.gif', 9)
