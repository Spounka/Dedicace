from PIL import Image, ImageDraw


def create_img():
    IMG_WIDTH, IMG_HEIGHT = (70, 70)
    img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), 'purple')

    d = ImageDraw.Draw(img)
    img.save('img.png')


if __name__ == "__main__":
    create_img()
