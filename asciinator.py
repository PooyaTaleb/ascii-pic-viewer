from os.path import isfile
from PIL import Image
import numpy as np
import sys

density = ("Ñ@#W$9876543210?!abc;:+=-,._                    ", "Ñ@#W$9876543210?!abc;:+=-,._ ", "  _.,-=+:;cba!?0123456789$W#@Ñ", "           _.,-=+:;cba!?0123456789$W#@Ñ", "        _.,-=+:;cba!?0123456789$W#@Ñ", "Ñ@#W$9876543210?!abc;:+=-,._  ", '       .:-i|=+%O#@', '        .:░▒▓█')
ditherPat = (
    (3/48, 5/48, 7/48, 5/48, 3/48), 
    (1/48, 3/48, 5/48, 3/48, 1/48))

# settings
autoRotate = True       # automatically rotate the images to make them horizontal
color = True            # try to recreate the color with dithering (1 bit color)
density = density[2]    # which density pattern to use


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

if (color):

    im = im.convert('RGB')
    r = np.pad(np.array(im,dtype = int)[:,:,0] , [(0,2),(2,2)], mode = 'constant', constant_values = 0)
    g = np.pad(np.array(im,dtype = int)[:,:,1] , [(0,2),(2,2)], mode = 'constant', constant_values = 0)
    b = np.pad(np.array(im,dtype = int)[:,:,2] , [(0,2),(2,2)], mode = 'constant', constant_values = 0)

    for i in range(r.shape[0] - 2):
        for j in range(2, r.shape[1] - 2):
            if(r[i][j] > 127):
                rError = r[i][j] - 255
                r[i][j] = 255
            else:
                rError = r[i][j] 
                r[i][j] = 0
            if(g[i][j] > 127):
                gError = g[i][j] - 255
                g[i][j] = 255
            else:
                gError = g[i][j] 
                g[i][j] = 0
            if(b[i][j] > 127):
                bError = b[i][j] - 255
                b[i][j] = 255
            else:
                bError = b[i][j] 
                b[i][j] = 0
            r[i][j+1] += int(rError * 7 / 48)
            r[i][j+2] += int(rError * 5 / 48)
            g[i][j+1] += int(gError * 7 / 48)
            g[i][j+2] += int(gError * 5 / 48)
            b[i][j+1] += int(bError * 7 / 48)
            b[i][j+2] += int(bError * 5 / 48)
            for k in range(5):
                r[i+1][j+k-2] += int(rError * ditherPat[0][k])
                r[i+2][j+k-2] += int(rError * ditherPat[1][k])
            for k in range(5):
                g[i+1][j+k-2] += int(gError * ditherPat[0][k])
                g[i+2][j+k-2] += int(gError * ditherPat[1][k])
            for k in range(5):
                b[i+1][j+k-2] += int(bError * ditherPat[0][k])
                b[i+2][j+k-2] += int(bError * ditherPat[1][k])

    r = r[0:-2, 2:-2]
    g = g[0:-2, 2:-2]
    b = b[0:-2, 2:-2]

    print(ycbcr.shape)
    print(r.shape)
    print(g.shape)
    print(b.shape)
    lastColor=0
    for i in range(len(ycbcr)):
        for j in range(len(ycbcr[0])):
            if(r[i][j]):
                if(g[i][j]):
                    if(b[i][j]):
                        if(lastColor != 7):
                            lastColor = 7
                            print("\u001b[37m",end='')
                    else:
                        if(lastColor != 3):
                            lastColor = 3
                            print("\u001b[33;1m",end='')
                else:
                    if(b[i][j]):
                        if(lastColor != 5):
                            lastColor = 5
                            print("\u001b[35;1m",end='')
                    else:
                        if(lastColor != 1):
                            lastColor = 1
                            print("\u001b[31;1m",end='')
            else:
                if(g[i][j]):
                    if(b[i][j]):
                        if(lastColor != 6):
                            lastColor = 6
                            print("\u001b[36;1m",end='')
                    else:
                        if(lastColor != 2):
                            lastColor = 2
                            print("\u001b[32;1m",end='')
                else:
                    if(b[i][j]):
                        if(lastColor != 4):
                            lastColor = 4
                            print("\u001b[34;1m",end='')
                    else:
                        if(lastColor != 7):
                            lastColor = 7
                            print("\u001b[37m",end='')
            print(density[(l*ycbcr[i][j])//256],end='')
        print()
    print("\u001b[0m",end='')
else: # no color
    for i in ycbcr:
        for j in i:
            print(density[(l*j)//256],end='')
        print()
