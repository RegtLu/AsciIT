import os
from typing import List, Tuple
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from tqdm import tqdm
import shutil
from multiprocessing import Pool


class AsciIt:
    def __init__(self, 字体: str = "arialbd.ttf", 字体大小: int = 8, 字符集: str = '@WMwPmBQRK&DNGOoEHk%8#A9SUX$Zbdz60gpqCh45Vae2nsFu3xYTcyLv?7Jft=1<[]r{}>Iijl!+()^|/\\"~*\'-:;,.`_ ', 颜色: bool = False) -> None:
        self.队列: List[Tuple[str, str]] = []
        self.字体 = 字体
        self.字体大小 = 字体大小
        self.字符集 = self.生成排序后的ascii字符(字符集)
        self.是否彩色 = 颜色

    def 添加入队列(self, 图片路径: str, 输出路径: str) -> None:
        self.队列.append((图片路径, 输出路径))

    def 获取控制台大小(self) -> Tuple[int, int]:
        columns, lines = shutil.get_terminal_size()
        return columns, lines

    def 处理(self, paths: Tuple[str, str]) -> None:
        图片路径, 输出路径 = paths
        image = Image.open(图片路径)
        控制台宽度, 控制台高度 = self.获取控制台大小()
        宽, 高 = image.size
        缩放比例 = min(控制台宽度 / 宽, 控制台高度 / 高)
        image = image.resize((int(宽 * 缩放比例), int(高 * 缩放比例)))
        字符序列 = self.字符(image)
        self.保存图片(image, 字符序列, 输出路径)

    def 字符(self, Pillow对象: Image.Image) -> List[str]:
        宽, 高 = Pillow对象.size
        字符序列: List[str] = []
        for y in range(高):
            for x in range(宽):
                color = Pillow对象.getpixel((x, y))
                gray_value = 255-(color[0] * 0.30 + color[1] * 0.59 + color[2] * 0.11)
                char_index = int(gray_value / 255 * (len(self.字符集)))
                if char_index >= len(self.字符集):
                    char_index = len(self.字符集) - 1
                字符序列.append(self.字符集[char_index])
        return 字符序列

    def 保存图片(self, Pillow对象: Image.Image, 字符序列: List[str], 输出路径: str) -> None:
        宽, 高 = Pillow对象.size
        with open(输出路径, 'w') as f:
            for i in range(高):
                for j in range(宽):
                    f.write(字符序列[i * 宽 + j])
                f.write('\n')

    def 生成排序后的ascii字符(self, 字符集: str) -> List[str]:
        字体大小 = self.字体大小
        image = Image.new("L", (字体大小 * 16, 字体大小 * 16), color="white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.字体, 字体大小)
        char_grayscale_values = {}

        for i in range(len(字符集)):
            char = 字符集[i]
            draw.text((i % 16 * 字体大小, i // 16 * 字体大小), char, font=font, fill="black")
        
        for i in range(len(字符集)):
            char = 字符集[i]
            char_image = image.crop((i % 16 * 字体大小, i // 16 * 字体大小, (i % 16 + 1) * 字体大小, (i // 16 + 1) * 字体大小))
            grayscale_value = sum(char_image.getdata()) // (字体大小 * 字体大小) #type:ignore
            char_grayscale_values[char] = grayscale_value

        sorted_chars = sorted(char_grayscale_values.items(), key=lambda x: x[1], reverse=False)
        char_list: List[str] = [char for char, _ in sorted_chars]
        return char_list


if __name__ == "__main__":
    线程池 = Pool(8)
    a = AsciIt()

    for root, dirs, files in os.walk(r'./raw'):
        for file in files:
            if file.endswith('.jpg'):
                a.添加入队列(os.path.join(root, file), os.path.join('./new', file).replace('.jpg', '.txt'))

    list(tqdm(线程池.imap(a.处理, a.队列), total=len(a.队列), desc='进度'))
