from typing import List, Tuple
import PIL.Image as Image


class AsciIt:
    def __init__(self, 字体: str = "sarasa-term-sc-nerd-regular.ttf", 字体大小: int = 8, 字符集: str = '@%#$?=1!+^|"~*-:.`_', 颜色: bool = False,控制台大小:Tuple[int,int]=(0,0)) -> None:
        self.队列: List[Tuple[str, str]] = []
        self.字体 = 字体
        self.字体大小 = 字体大小
        self.字符集 = 字符集
        self.是否彩色 = 颜色
        self.控制台大小=控制台大小

    def 添加入队列(self, 图片路径: str, 输出路径: str) -> None:
        self.队列.append((图片路径, 输出路径))

    def 处理(self, paths: Tuple[str, str]) -> None:
        图片路径, 输出路径 = paths
        image = Image.open(图片路径)
        控制台宽度, 控制台高度 = self.控制台大小
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
