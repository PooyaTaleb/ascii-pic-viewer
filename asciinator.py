
# N.T.S:
#   ImageFile = convert should be commented out and moved into the else/except section

from os.path import isfile
from time import sleep
from PIL import Image
import numpy as np
import sys

density = ("Ñ@#W$9876543210?!abc;:+=-,._                    ", "Ñ@#W$9876543210?!abc;:+=-,._ ", "  _.,-=+:;cba!?0123456789$W#@Ñ", "           _.,-=+:;cba!?0123456789$W#@Ñ", "        _.,-=+:;cba!?0123456789$W#@Ñ", "Ñ@#W$9876543210?!abc;:+=-,._  ", '       .:-i|=+%O#@', '        .:░▒▓█')
ditherPat = (
    (3/48, 5/48, 7/48, 5/48, 3/48), 
    (1/48, 3/48, 5/48, 3/48, 1/48))


endlessReplay = True
density = density[2]
autoRotate = True
color = True
size=240,66


l = len(density)
if (len(sys.argv) == 0 or not isfile(sys.argv[1])):
    raise Exception('please enter a valid file')
ImageFile = Image.open(sys.argv[1], 'r')
if(sys.argv[1][-4:] == '.gif'): # it's gifing time
# try: # it's gifing time
    # gif all over them
    ImageFile.seek(1)

    resString = []
    curFrame = 0
    flag = False
    if(autoRotate and ImageFile.size[1]>ImageFile.size[0]):
        flag = True

    while True:
        try:
            ImageFile.seek(curFrame)
        except EOFError:
            break
        curFrame += 1
        im = ImageFile.convert('YCbCr')
        if(flag):
            im = im.rotate(90, expand=True)
        tempSize = im.size[0],int(im.size[1]*0.5)
        im = im.resize(tempSize)
        im.thumbnail(size)
        im = im.convert('YCbCr')
        ycbcr = np.array(im)[:,:,0]
        res=''
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

            for i in range(len(ycbcr)):
                for j in range(len(ycbcr[0])):
                    if(r[i][j]):
                        if(g[i][j]):
                            if(b[i][j]):
                                res+=("\u001b[37m")
                            else:
                                res+=("\u001b[33;1m")
                        else:
                            if(b[i][j]):
                                res+=("\u001b[35;1m")
                            else:
                                res+=("\u001b[31;1m")
                    else:
                        if(g[i][j]):
                            if(b[i][j]):
                                res+=("\u001b[36;1m")
                            else:
                                res+=("\u001b[32;1m")
                        else:
                            if(b[i][j]):
                                res+=("\u001b[34;1m")
                            else:
                                res+=("\u001b[37m")
                    res+=(density[(l*ycbcr[i][j])//256])
                res+=('\n')
            res+=("\u001b[0m")
        else:
            for i in ycbcr:
                for j in i:
                    res+=(density[(l*j)//256])
                res+=('\n')
        resString.append(res)
    t = ImageFile.info['duration'] / 1000
    while True:
        for i in resString:
            print("\u001b[0;0H", end='')
            print(i)
            sleep(t)
        if(not endlessReplay):
            break
else:
# except EOFError:
    ImageFile = ImageFile.convert('YCbCr')
    if(autoRotate and ImageFile.size[1]>ImageFile.size[0]):
        ImageFile = ImageFile.rotate(90, expand=True)
    tempSize = ImageFile.size[0],int(ImageFile.size[1]*0.5)
    im = ImageFile.resize(tempSize)
    im.thumbnail(size)
    im = im.convert('YCbCr')
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

        for i in range(len(ycbcr)):
            for j in range(len(ycbcr[0])):
                if(r[i][j]):
                    if(g[i][j]):
                        if(b[i][j]):
                            print("\u001b[37m",end='')
                        else:
                            print("\u001b[33;1m",end='')
                    else:
                        if(b[i][j]):
                            print("\u001b[35;1m",end='')
                        else:
                            print("\u001b[31;1m",end='')
                else:
                    if(g[i][j]):
                        if(b[i][j]):
                            print("\u001b[36;1m",end='')
                        else:
                            print("\u001b[32;1m",end='')
                    else:
                        if(b[i][j]):
                            print("\u001b[34;1m",end='')
                        else:
                            print("\u001b[37m",end='')
                print(density[(l*ycbcr[i][j])//256],end='')
            print()
        print("\u001b[0m",end='')
    else:
        for i in ycbcr:
            for j in i:
                print(density[(l*j)//256],end='')
            print()
