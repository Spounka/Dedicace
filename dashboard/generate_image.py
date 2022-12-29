from PIL import ImageFont, Image, ImageDraw


def create_img():
    IMG_WIDTH, IMG_HEIGHT = (70, 70)
    img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), 'purple')

    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('./fira.ttf', IMG_WIDTH // 3)
    size = fnt.getbbox('A.Y')
    text_x = IMG_WIDTH // 2 - size[2] // 2
    text_y = IMG_HEIGHT // 2 - size[3] // 2
    d.text((text_x, text_y), 'A.Y', font=fnt, fill=(255, 255, 255))

    img.save('img.png')


if __name__ == "__main__":
    create_img()
