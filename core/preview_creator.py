from PIL import (Image, ImageDraw, 
                 ImageFont, ImageEnhance, 
                 ImageFilter)

from enum import Enum
from dataclasses import dataclass

import textwrap
import re
import random
import os


@dataclass
class Color:
    r: int | float
    g: int | float
    b: int | float
    
    @property
    def tuple_color(self):
        return (self.r, 
                self.g, 
                self.b)


class Colors(Enum):
    LIGHT_PINK: Color = Color(205, 174, 174)
    LIGHT_YELLOW: Color = Color(225, 175, 154)
    LIGHT_GREEN: Color = Color(174, 225, 174)
    LIGHT_BLUE: Color = Color(190, 164, 205)
    LIGHT_PURPLE: Color = Color(205, 174, 205)
    LIGHT_BLACK: Color = Color(50, 50, 50)
    
    
def get_flags(text: str) -> tuple:
    """ Получение флагов из описания. """
    
    text_without_flags = re.sub(r'\/\w+\s\d+', '', text)

    # Извлекаем значения флагов в словарь
    flags = {}
    matches = re.findall(r'\/(\w+)\s(\d+)', text)
    for match in matches:
        try:
            flags[match[0]] = int(match[1])
        except TypeError:
            flags[match[0]] = match[1]
    return flags, text_without_flags


def add_random_color_to_colors(colors: list[Color]) -> list[Color]:
    """ 
        Генерация трёх случайных значений 
        между 100 и 255 для получения 
        пастельных цветов.
    """
    
    for i in range(20):
        r, g, b = tuple([random.randint(100, 225) for _ in range(3)])
        colors.append(Color(r, g, b))
        
    return colors


def get_smoothstep(start_color, 
                   end_color, 
                   position) -> Color:
        """ Получение smoothstep. """
        
        position = max(0.0, min(1.0, position))

        t = position * position * (3 - 2 * position)

        r, g, b = tuple([
            int(start_color.tuple_color[i] + t * 
                (end_color.tuple_color[i] - 
                 start_color.tuple_color[i])
                )
            for i in range(3)
        ])

        return Color(r, g, b)
    
    
def transform_gradient(gradient: Image, 
                       width: int, 
                       height: int, 
                       default_width: int, 
                       default_height: int
                       ) -> Image:
    """ Преобразовывает изображение градиента. """
    
    # Случайный угол поворота градиента на фоне
    angle = random.randint(0, 359)
    
    # Поворот изображения
    gradient = gradient.rotate(angle)

    step = int(width / 5)

    gradient = gradient.crop((step, step, 
                              width - step, height - step))
    gradient = gradient.resize((default_width, 
                                default_height))
    return gradient


def make_background_gradient(default_width: int, 
                             default_height: int
                             ) -> Image:
    """ Отрисовывает градиент. """
    
    # Список пастельных цветов
    colors = [i.value for i in Colors]
    colors = add_random_color_to_colors(colors=colors)

    width, height = (int(default_width * 1.5), 
                           int(default_width * 1.5))
    gradient = Image.new(mode='RGB', 
                         size=(width, height), 
                         color=colors[0].tuple_color)
    
    draw = ImageDraw.Draw(gradient)

    # Случайные начальный и конечный цвета
    start_color = random.choice(colors)
    end_color = random.choice(colors)

    # Рисование плавного градиента
    for y in range(height):
        t = y / height
        color = get_smoothstep(start_color, 
                           end_color, t)
        draw.line((0, y, 
                   width, y), 
                  fill=color.tuple_color)

    gradient = transform_gradient(gradient, 
                                  width, 
                                  height, 
                                  default_width, 
                                  default_height)

    return gradient


def get_optimal_font_size(text: str, 
                          font_path: str, 
                          max_size: int, 
                          image_width: int
                          ) -> ImageFont:
    """
       Возвращает оптимальный размер шрифта, 
       основанный на максимальном размере 
       и ширине изображения. 
    """
    
    font_size = 1
    font = ImageFont.truetype(font_path, 
                              font_size)
    
    while (font.getsize(text)[0] < image_width and 
           font_size < max_size):
        font_size += 1
        font = ImageFont.truetype(font_path, 
                                  font_size)
        
    font = ImageFont.truetype(font_path, 
                              font_size - 1)
    return font


def make_preview(title: str, 
                 description: str = "", 
                 background: bool = False, 
                 filename: str = "none"
                ) -> tuple[list[str], Image]:
    """ Рисует превью. """
    flags, description = get_flags(description)

    width, height = 3000, 1500

    if flags.get('sq', False):
        height = 3000

    img = make_background_gradient(width, height)

    if flags.get('bl', 0) != 0:
        # Блюр фона 
        
        img = img.filter(
            ImageFilter.GaussianBlur(
                radius=abs(flags.get('bl', 5))
            )
        )

    if flags.get('nbg', '0') == '0':
        # Затемнение фона
        
        flag = flags.get('bg', False)
        if flag:
            flag = abs(flag / 10)
        else:
            flag = 0.5
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(flag)

    draw = ImageDraw.Draw(img)
    size_x, size_y = img.size
    
    def draw_text(raw_text: str, 
                  font_size: int, 
                  line_width: int, 
                  offset: int = 0, 
                  raw_font='bold'
                  ) -> tuple[Image, Image]:
        """ Отрисовка текста на изображении. """
        
        raw_font = ImageFont.truetype('static/fonts/%s.ttf' % raw_font, size=font_size)
        line_width = line_width - raw_text.count(' ')
        raw_text = '\n'.join(textwrap.wrap(raw_text, width=line_width))

        # Draw quote text
        draw.text(
            (int(size_x / 2), 
             int(size_y / 2) + offset), 
            str(raw_text),
            anchor="mm",
            font=raw_font,
            fill='white'
        )

        return raw_font, raw_text

    font, text = draw_text(raw_text=title,
                           font_size=abs(flags.get('ts', 180)),
                           line_width=abs(flags.get('tlw', 30)),
                           offset=flags.get('to', 0),
                           raw_font=str(
                            flags.get('tf', 'bold'))
                           .replace('0', 'bold')
                           .replace('1', 'light'))
    
    draw_text(raw_text=description,
              font_size=abs(flags.get('ds', 100)),
              line_width=abs(flags.get('dlw', 50)),
              offset=250 + (100 * text.count("\n")),
              raw_font=str(flags.get('df', 'light'))
                           .replace('0', 'bold')
                           .replace('1', 'light'))
    
    img.save(f"media/{filename}.jpeg")
    