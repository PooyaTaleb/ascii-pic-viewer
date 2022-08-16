from os.path import isfile
from PIL import Image
import numpy as np
import sys

density = ("Ñ@#W$9876543210?!abc;:+=-,._                    ", "Ñ@#W$9876543210?!abc;:+=-,._ ", "  _.,-=+:;cba!?0123456789$W#@Ñ", "           _.,-=+:;cba!?0123456789$W#@Ñ", "        _.,-=+:;cba!?0123456789$W#@Ñ", "Ñ@#W$9876543210?!abc;:+=-,._  ", '       .:-i|=+%O#@', '        .:░▒▓█')

autoRotate = False

density = density[2]

l = len(density)

if (len(sys.argv) == 0 or not isfile(sys.argv[1])):
    raise Exception('please enter a valid file')
ImageFile = Image.open(sys.argv[1], 'r')
ImageFile = ImageFile.convert('YCbCr')

if(autoRotate and ImageFile.size[1]>ImageFile.size[0]):
    ImageFile = ImageFile.rotate(90, expand=True)
size = ImageFile.size[0],int(ImageFile.size[1]*0.5)
im = ImageFile.resize(size)

size=240,66

im.thumbnail(size)

ycbcr = np.array(im)[:,:,0]

for i in ycbcr:
    for j in i:
        print(density[(l*j)//256],end='')
    print()
