import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

font_path = "sarasa-term-sc-nerd-regular.ttf"
font_size = 8
image = Image.new("L", (font_size * 16, font_size * 16), color="white")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font_path, font_size)
char_grayscale_values = {}
字符串='1234567890-=`qwertyuiop[]asdfghjkl;\'\\zxcvbnm,./!~@#$%^&*()_+}{:"|?><QAWSZEXDCRVFBTGYHNUMJKILOP'
print(len(字符串))
for i in range(len(字符串)):
    char = 字符串[i]
    x = i % 16 * font_size
    y = i // 16 * font_size
    draw.text((x, y), char, font=font, fill="black")
    char_image = image.crop((x, y, x + font_size, y + font_size))
    grayscale_value = sum(char_image.getdata()) // (font_size * font_size) #type:ignore
    char_grayscale_values[char] = grayscale_value

sorted_chars = sorted(char_grayscale_values.items(), key=lambda x: x[1], reverse=False)
for char, grayscale_value in sorted_chars:
    print(char, end='')