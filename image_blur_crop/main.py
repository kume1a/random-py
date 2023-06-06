from PIL import Image, ImageFilter
import os


os.chdir('')
# for image in os.listdir():
#     os.rename(image, image.replace("_blur", ""))

basewidth = 500

for image in filter(lambda e: e.endswith('.jpg'), os.listdir()):
    im = Image.open(image)

    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im1 = im.resize((basewidth,hsize), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(12))

    image_name = image.split('.')[0]
    im1.save(image_name + '_blur' + '.jpg', optimize=True, quality=70)
