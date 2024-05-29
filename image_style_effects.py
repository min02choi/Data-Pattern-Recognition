from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import cv2
import numpy as np


class TextStyles:
    def __init__(self, img_dir_path, bg_color):
        self.img_dir_path = img_dir_path
        self.bg_color = bg_color

    # 랜덤 색상을 생성
    def get_random_color(self, color_range=(0, 255)):
        y = np.random.randint(color_range[0], color_range[1])
        cr = np.random.randint(0, 255)
        cb = np.random.randint(0, 255)

        ycrcb = np.uint8([[[y, cr, cb]]])
        rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)

        return tuple(rgb[0][0])

    # 없음(none)
    def create_none(self, font_name, font_path, text):
        img = Image.new(mode='RGBA', size=(256, 256), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        x = img.width//2
        y = img.height//2

        fill_color = self.get_random_color()
        font_size = np.random.randint(100, 140)

        font = ImageFont.truetype(font_path, font_size)

        draw.text((x, y), text, font=font, anchor='mm', fill=fill_color,)

        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_none.png'
        img.save(img_path, format='PNG')

    # 테두리(str)
    def create_stroke(self, font_name, font_path, text):

        # 색 간 모호함을 제거하기 위해 색의 구간을 지정
        color_list = [
            ('black', 'white'),
            ('white', 'black'),
            ('black', self.get_random_color((180, 256))),
            ('white', self.get_random_color((0, 100))),
            (self.get_random_color((0, 100)), self.get_random_color((180, 256))),
            (self.get_random_color((180, 256)), self.get_random_color((0, 100)))
        ]

        img = Image.new(mode='RGBA', size=(256, 256), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        x = img.width//2
        y = img.height//2

        fill_color, stroke_color = random.choice(color_list)
        stroke_size = np.random.randint(3, 7)
        font_size = np.random.randint(100, 140)

        font = ImageFont.truetype(font_path, font_size)

        draw.text((x, y), text, font=font, anchor='mm', fill=fill_color,
                stroke_width=stroke_size, stroke_fill=stroke_color)

        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_str.png'
        img.save(img_path, format='PNG')

    # 번짐(glow)
    def create_glow(self, font_name, font_path, text):
        color_list = [
            (self.get_random_color((20, 150)), self.get_random_color((200, 256))),
            ('white', self.get_random_color((150, 256)))
        ]
        image_size = (256, 256)

        original_img = Image.new('RGBA', image_size, self.bg_color)
        border_img = Image.new('RGBA', image_size, self.bg_color)

        font_size = np.random.randint(100, 140)

        font = ImageFont.truetype(font_path, font_size)

        # 텍스트 배치 위치
        x = original_img.width // 2
        y = original_img.height // 2

        fill_color, blur_color = random.choice(color_list)

        border_draw = ImageDraw.Draw(border_img)
        border_draw.text((x, y), text, font=font, fill=blur_color, anchor='mm')

        scale_factor = 10

        # 이미지 축소 및 확장으로 블러 효과 생성
        for _ in range(7):
            small_img = border_img.resize((int(image_size[0] / scale_factor), int(image_size[1] / scale_factor)), resample=Image.BILINEAR)
            blurred_border = small_img.resize(image_size, resample=Image.BILINEAR)

        draw = ImageDraw.Draw(original_img)
        draw.text((x, y), text, font=font, fill=fill_color, anchor='mm')

        # 블러 테두리와 본문 텍스트 이미지 합성
        blurred_border.paste(original_img, (0, 0), original_img)

        # 이미지 저장
        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_glow.png'
        blurred_border.save(img_path, format='PNG')

    # 테두리, 번짐(str+glow)
    def create_strglow(self, font_name, font_path, text):
        color_list = [
            ('black', 'white', self.get_random_color((30, 120))),
            ('white', 'black', self.get_random_color((180, 256))),
            (self.get_random_color((200, 256)), self.get_random_color((20, 150)), self.get_random_color((180, 256))),
            (self.get_random_color((20, 150)), self.get_random_color((200, 256)), self.get_random_color((200, 256))),
        ]

        image_size = (256, 256)

        original_img = Image.new('RGBA', image_size, self.bg_color)
        border_img = Image.new('RGBA', image_size, self.bg_color)

        font_size = np.random.randint(100, 140)
        stroke_size = np.random.randint(3, 5)

        font = ImageFont.truetype(font_path, font_size)

        x = original_img.width // 2
        y = original_img.height // 2

        fill_color, stroke_color, blur_color = random.choice(color_list)
        border_draw = ImageDraw.Draw(border_img)
        border_draw.text((x, y), text, font=font, fill=blur_color, anchor='mm')

        scale_factor = 10

        # 이미지 축소 및 확장으로 블러 효과 생성
        for _ in range(7):
            small_img = border_img.resize((int(image_size[0] / scale_factor), int(image_size[1] / scale_factor)),
                                      resample=Image.BILINEAR)
            blurred_border = small_img.resize(image_size, resample=Image.BILINEAR)

        # 본문 텍스트 그리기
        draw = ImageDraw.Draw(original_img)
        draw.text((x, y), text, font=font, fill=fill_color, anchor='mm', stroke_width=stroke_size, stroke_fill=stroke_color)

        # 블러 테두리와 본문 텍스트 이미지 합성
        blurred_border.paste(original_img, (0, 0), original_img)

        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_strglow.png'
        blurred_border.save(img_path, format='PNG')

    # 이중 테두리(str+str)
    def create_strstr(self, font_name, font_path, text):

        color_list = [
            ('black', 'white', 'black'),
            ('white', 'black', 'white'),
            ('black', self.get_random_color((180, 256)), self.get_random_color((180, 256))),
            ('white', self.get_random_color((0, 100)), self.get_random_color((0, 100)))
        ]

        img = Image.new(mode='RGBA', size=(256, 256), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        x = img.width//2
        y = img.height//2

        fill_color, inline_stroke_color, outline_stroke_color = random.choice(color_list)

        # 스타일 수치 설정
        inline_stroke_size = np.random.randint(3, 7)
        outline_stroke_size = round(inline_stroke_size * np.random.uniform(1.5, 3))

        font_size = np.random.randint(100, 140)
        font = ImageFont.truetype(font_path, font_size)

        # 테두리 그리기
        # 두꺼운 선
        draw.text((x, y), text, font=font, anchor='mm', fill=fill_color, 
                stroke_width=outline_stroke_size, stroke_fill=outline_stroke_color)

        # 얇은 선
        draw.text((x, y), text, font=font, anchor='mm', fill=fill_color,
                stroke_width=inline_stroke_size, stroke_fill=inline_stroke_color)

        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_strstr.png'
        img.save(img_path, format='PNG')

    # 그림자(shadow)
    def create_shadow(self, font_name, font_path, text):

        color_list = [
            (self.get_random_color((20, 150)), self.get_random_color((200, 256))),
            ('white', self.get_random_color((150, 256)))
        ]

        img = Image.new(mode='RGBA', size=(256, 256), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        x = img.width // 2
        y = img.height // 2

        fill_color, shadow_color = random.choice(color_list)

        font_size = np.random.randint(100, 140)
        font = ImageFont.truetype(font_path, font_size)

        shadow_offset = np.random.randint(3, 6)
        shadow_position = (x + shadow_offset, y + shadow_offset)

        draw.text(shadow_position, text, font=font, anchor='mm', fill=shadow_color)
        draw.text((x, y), text, font=font, anchor='mm', fill=fill_color)

        img_path = f'{self.img_dir_path}/{font_name}_{text}_{font_size}_shadow.png'
        img.save(img_path, format='PNG')
