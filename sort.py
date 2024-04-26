import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

字体路径 = "sarasa-term-sc-nerd-regular.ttf"
字体大小 = 16

灰度列表 = {}
ascii列表 = ''.join(chr(i) for i in range(32, 127))
image = Image.new("L", (字体大小*len(ascii列表), 字体大小), color="black")
绘图 = ImageDraw.Draw(image)
字体 = ImageFont.truetype(字体路径, 字体大小)
    
for i in range(len(ascii列表)):
    字符 = ascii列表[i]
    x = i*字体大小
    y = 0
    
    # 在图像上绘制字符
    绘图.text((x, y), 字符, font=字体, fill="white")
    
    # 截取字符图像
    字符图像 = image.crop((x, y, x + 字体大小, y + 字体大小))
    # 计算字符的平均灰度值
    灰度值 = sum(字符图像.getdata()) / (字体大小 * 字体大小) # type: ignore
    灰度列表[字符] = 灰度值

字符表 = sorted(灰度列表.items(), key=lambda x: x[1])
字符表.reverse()
for char, 灰度值 in 字符表:
    print(char, end='')