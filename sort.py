import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

font_path = "sarasa-term-sc-nerd-regular.ttf"
font_size = 16

char_grayscale_values = {}
ascii_chars = ''.join(chr(i) for i in range(32, 127))
image = Image.new("L", (font_size*len(ascii_chars), font_size), color="black")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font_path, font_size)
    
for i in range(len(ascii_chars)):
    char = ascii_chars[i]
    x = i*font_size
    y = 0
    
    # 在图像上绘制字符
    draw.text((x, y), char, font=font, fill="white")
    
    # 截取字符图像
    char_image = image.crop((x, y, x + font_size, y + font_size))
    # 计算字符的平均灰度值
    grayscale_value = sum(char_image.getdata()) / (font_size * font_size) # type: ignore
    char_grayscale_values[char] = grayscale_value

sorted_chars = sorted(char_grayscale_values.items(), key=lambda x: x[1])
sorted_chars.reverse()
for char, grayscale_value in sorted_chars:
    print(char, end='')