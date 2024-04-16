import argparse
from typing import List, Tuple
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from tqdm import tqdm


class AsciIt:
    def __init__(self) -> None:
        # 用于生成的ASCII字符
        self.ascii = list(
            '@WMwPmBQRK&DNGOoEHk%8#A9SUX$Zbdz60gpqCh45Vae2nsFu3xYTcyLv?7Jft=1<[]r{}>Iijl!+()^|/\\"~*\'-:;,.`_ ')
        # 用于生成的字体     影响ASCII字体排序,应调用self.resort()
        self.font = "arialbd.ttf"
        self.font_size = 8

        self.image_ascii: List[str] = []
        self.image_color: List[Tuple[int, int, int]] = []

    def add(self, image_path: str, scale: float) -> None:
        """
        参数:
            image_path:图片路径
            scale:缩放比例X
        """
        image = Image.open(image_path)
        width, height = image.size
        image = image.resize((int(width * scale), int(height * scale)))
        self.image: Image.Image = image
        self.width, self.height = image.size

    def asciit(self, output_path: str, color: bool = False) -> None:
        """
        参数:
            output_path:输出路径
            color:是否包含颜色
        """
        self.color = color
        self.generate_ascii()
        if self.color:
            self.generate_color()
        self.save_image(output_path)

    def generate_ascii(self) -> None:
        bar = tqdm(desc='生成ASCII字符中', total=self.height*self.width)
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                color = self.image.getpixel((x, y))
                gray_value = color[0]*0.30+color[1]*0.59+color[2]*0.11
                char_index = int(gray_value / 255 * (len(self.ascii) - 1))
                if char_index >= len(self.ascii):
                    char_index = len(self.ascii) - 1
                else:
                    row += self.ascii[char_index]
                self.image_ascii.append(self.ascii[char_index])
                bar.update(1)
        bar.close()

    def generate_color(self) -> None:
        bar = tqdm(desc='生成ASCII颜色中', total=self.height*self.width)
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                color = self.image.getpixel((x, y))
                gray_value = color[0]*0.30+color[1]*0.59+color[2]*0.11
                char_index = int(gray_value / 255 * (len(self.ascii) - 1))
                if char_index >= len(self.ascii):
                    char_index = len(self.ascii) - 1
                else:
                    row += self.ascii[char_index]
                self.image_color.append((color[0], color[1], color[2]))
                bar.update(1)
        bar.close()

    def save_image(self, output_path: str) -> None:
        bar = tqdm(desc='保存图片中     ', total=self.height*self.width)
        image = Image.new('RGB', ((self.width * self.font_size),
                          (self.height * self.font_size)), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font, self.font_size)
        for i in range(self.height):
            for j in range(self.width):
                if self.color:
                    draw.text((j * self.font_size, i * self.font_size),
                              self.image_ascii[i * self.width + j], font=font, fill=self.image_color[i * self.width + j])
                else:
                    draw.text((j * self.font_size, i * self.font_size),
                              self.image_ascii[i * self.width + j], font=font, fill='black')
                bar.update(1)
        image.save(output_path)
        bar.close()

    def resort(self) -> None:
        font_size = self.font_size
        image = Image.new("L", (font_size * 16, font_size * 16), color="white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font, font_size)
        char_grayscale_values = {}
        for i in range(32, 127):
            char = chr(i)
            draw.text(((i - 32) % 16 * font_size, (i - 32) // 16 *
                      font_size), char, font=font, fill="black")
        for i in range(32, 127):
            char = chr(i)
            char_image = image.crop(((i - 32) % 16 * font_size, (i - 32) // 16 * font_size, ((
                i - 32) % 16 + 1) * font_size, ((i - 32) // 16 + 1) * font_size))
            grayscale_value = sum(char_image.getdata(   # type: ignore
            )) // (font_size * font_size)
            char_grayscale_values[char] = grayscale_value
        sorted_chars = sorted(char_grayscale_values.items(),
                              key=lambda x: x[1], reverse=False)
        char_list = []
        for char, _ in sorted_chars:
            char_list.append(char)
        self.ascii = char_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符画生成')
    parser.add_argument('InputPath', help='图片路径')
    parser.add_argument('OutputPath', help='输出路径')
    parser.add_argument('scale', help='缩放比例', type=float)
    parser.add_argument('--color', help='是否使用颜色', action='store_true')
    args = parser.parse_args()

    a = AsciIt()
    a.add(args.InputPath, args.scale)
    a.asciit(args.OutputPath, args.color)
