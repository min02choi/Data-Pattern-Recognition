"""
### 생성 스타일
1. none: 효과없음
2. str: 테두리
3. glow: 번짐
4. strglow: 테두리, 번짐
5. strstr: 이중테두리
6. shadow: 그림자
"""

import os
from image_style_effects import TextStyles


# 경로 지정
IMG_DIR_PATH = './images'
FONT_DIR_PATH = './fonts'

# 배경 색상 설정
# IMAGE_BG_COLOR = 0xD9D9D9
IMAGE_BG_COLOR = (0, 0, 0, 0)

# 폰트 저장할 리스트
font_res = []

"""
# 생성할 단어
words = [
    '쾅', '헉', '깡', '슝', '앗', 
    '챙', '꽝', '쓱', '싹', '탁',
    '띵', '후', '딱', '쿵', '꺅', 
    '탓', '꺄', '삐', '퍽', '푹',
    '슥', '척', '앙', '멍', '꽥', 
    '땡', '쑥', '쏙', '짝', '쪽',
    '끽', '띡', '덜', '쿨', '활', 
    '쌩', '윙', '힉', '빽', '질',
    '죽', '탕', '펑', '웅', '냠', 
    '응', '동', '둥', '슬', '통',
    '긁적', '깜짝', '덜덜', '두근', '딸랑', 
    '멈칫', '서걱', '씨익', '우웅', '움찔',
    '저벅', '촤악', '쿨럭', '쿠웅', '피식',
    '휘잉', '펄럭', '크르', '에엑', '쌔앵',
    '꽈당', '히익', '퍼엉', '스슥', '뭐야',
    '벌컥', '주륵', '슈슉', '털썩', '띠링',
    '터벅', '덜컥', '빠앙', '두둥', '찰싹',
    '북북', '흠칫', '꽈악', '달칵', '찰칵',
    '깜박', '팔짝', '오물', '아차', '영차',
    '허걱', '허억', '하하', '싱긋', '꾸깃',
]
"""

words = [
    '하', "쾅", "덜덜", "쿠궁",
]

# 반복 횟수
ITERATE = 2

# 생성하는 이미지를 저장할 폴더 만들기
def create_img_dir():
    try:
        if not os.path.exists(IMG_DIR_PATH):
            print('이미지를 저장할 디렉토리 생성')
            os.makedirs(IMG_DIR_PATH)
    except OSError:
        print('Error: Creating directory. ' + IMG_DIR_PATH)

# font 리스트에 저장
def get_fonts():
    for path in os.listdir(FONT_DIR_PATH):
        if os.path.isfile(os.path.join(FONT_DIR_PATH, path)) and path != '.DS_Store':
            font_res.append(path)

def main():
    webtoonStyles = TextStyles(IMG_DIR_PATH, IMAGE_BG_COLOR)

    create_img_dir()
    get_fonts()

    img_cnt = 0
    # 사용할 글자 선택
    for text in words:
        print(f"단어: {text}")

        # 폰트 선택
        for font_name_with_ex in font_res:

            font_name = os.path.splitext(font_name_with_ex)[0]
            font_path = f'{FONT_DIR_PATH}/{font_name_with_ex}'

            # 스타일 적용한 이미지 생성
            count = 0
            while ITERATE > count:
                webtoonStyles.create_none(font_name, font_path, text)
                webtoonStyles.create_stroke(font_name, font_path, text)
                webtoonStyles.create_glow(font_name, font_path, text)
                webtoonStyles.create_strglow(font_name, font_path, text)
                webtoonStyles.create_strstr(font_name, font_path, text)
                webtoonStyles.create_shadow(font_name, font_path, text)
                count += 1
                img_cnt += 5
        
        # file_count = sum([len(files) for r, d, files in os.walk(IMG_DIR_PATH)])
        # print(f'생성한 image 개수: {file_count}장')
        print(f'생성한 image 개수: {img_cnt}장')

    file_count = sum([len(files) for r, d, files in os.walk(IMG_DIR_PATH)])
    print(f'===============')
    print('이미지 생성 완료')
    print(f'===============')
    print(f'사용한 단어: {words}')
    print(f'단어 개수: {len(words)}개')
    print(f'font 경로: {FONT_DIR_PATH}')
    print(f'font 개수: {len(font_res)}개')
    print(f'image 생성 경로: {IMG_DIR_PATH}')

    file_count = sum([len(files) for r, d, files in os.walk(IMG_DIR_PATH)])
    print(f'총 생성한 image 개수: {file_count}장')
    print('================')


if __name__ == "__main__":
    main()
