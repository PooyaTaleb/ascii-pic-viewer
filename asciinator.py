# note : some options are not implemented yet these include:
#   queue & camera

from os.path import isfile, splitext    # checks for file existance and splits file names
from time import sleep                  # to display gifs (adds delay between frames)
from PIL import Image                   # to handle image manipulation
import numpy as np                      # used for some calculations
import cv2                              # used for taking pictures
import sys                              # used for reading commandline arguments
import os                               # used for capturing screenshots (for output)

density = ("Ñ@#W$9876543210?!abc;:+=-,._                    ", "Ñ@#W$9876543210?!abc;:+=-,._ ", "  _.,-=+:;cba!?0123456789$W#@Ñ", "           _.,-=+:;cba!?0123456789$W#@Ñ", "        _.,-=+:;cba!?0123456789$W#@Ñ", "Ñ@#W$9876543210?!abc;:+=-,._  ", '       .:-i|=+%O#@', '        .:░▒▓█')
ditherPat = (
    (3/48, 5/48, 7/48, 5/48, 3/48), 
    (1/48, 3/48, 5/48, 3/48, 1/48))


# settings
endlessReplay = True    # endlessly replay gifs or not
density = density[2]    # which density pattern to use
autoRotate = True       # automatically rotate the images to make them horizontal
output = False          # create an image showing the output
color = True            # try to recreate the color with dithering (1 bit color)
queue = True            # show all files in some folder
size=240,66             


if (len(sys.argv) >= 2 and (not isfile(sys.argv[1])) and sys.argv[1][0] != '-'):
    raise Exception('please enter a valid file')
if (len(sys.argv) >= 2 and sys.argv[-1][0] == '-'): # you can use these to change options for this time only
    if ('m' in sys.argv[-1]): # monochrome mode
        color = False
    if ('r' in sys.argv[-1]): # autoRotate off
        autoRotate = False
    if ('e' in sys.argv[-1]): # looped animation off (only show animated files once)
        endlessReplay = False
    if ('o' in sys.argv[-1]): # output the results as a file
        output = True
        endlessReplay = False
    if ('q' in sys.argv[-1]): # show all images in a queue (not implemented yet)
        queue = True
        output = False
        endlessReplay = False


l = len(density)
if (len(sys.argv) > 2):                                                         # open image if image address is given
    ImageFile = Image.open(sys.argv[1], 'r')
else:                                                                           # otherwise use camera
    result, ImageFile = cv2.VideoCapture(0) .read() 
    ImageFile = Image.fromarray(cv2.cvtColor(ImageFile, cv2.COLOR_BGR2RGB))
    print(result)

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

        lastColor=0
        for i in range(len(ycbcr)):
            for j in range(len(ycbcr[0])):
                if(r[i][j]):
                    if(g[i][j]):
                        if(b[i][j]):
                            if(lastColor != 7):
                                lastColor = 7
                                res += ("\u001b[37m")
                        else:
                            if(lastColor != 3):
                                lastColor = 3
                                res += ("\u001b[33;1m")
                    else:
                        if(b[i][j]):
                            if(lastColor != 5):
                                lastColor = 5
                                res += ("\u001b[35;1m")
                        else:
                            if(lastColor != 1):
                                lastColor = 1
                                res += ("\u001b[31;1m")
                else:
                    if(g[i][j]):
                        if(b[i][j]):
                            if(lastColor != 6):
                                lastColor = 6
                                res += ("\u001b[36;1m")
                        else:
                            if(lastColor != 2):
                                lastColor = 2
                                res += ("\u001b[32;1m")
                    else:
                        if(b[i][j]):
                            if(lastColor != 4):
                                lastColor = 4
                                res += ("\u001b[34;1m")
                        else:
                            if(lastColor != 7):
                                lastColor = 7
                                res += ("\u001b[37m")
                res+=(density[(l*ycbcr[i][j])//256])
            res+=('\n')
        res+=("\u001b[0m")
    else:
        for i in ycbcr:
            for j in i:
                res+=(density[(l*j)//256])
            res+=('\n')
    resString.append(res)
flag = False
try:
    ImageFile.seek(1)
    flag = True
except EOFError:
    pass
if(flag):
    t = ImageFile.info['duration'] / 1000
    if(output):
        ims = []
        os.system("sudo echo ") # starts the internal sudo timer
    frame = 0
    while True:
        for i in resString:
            print("\u001b[0;0H", end='')
            print(i, end='')
            if(output):
                os.system("sudo fbcat > .temp"+str(frame)+".ppm")  
                ims.append(Image.open('.temp'+str(frame)+'.ppm', 'r'))
                frame+=1
            else:
                sleep(t)
        if(not endlessReplay):
            break
    if(output):
        if(isfile(splitext(sys.argv[1])[0]+"-asciified.gif")):
            name = input('automaticly generated name taken. please enter name manually')
            if(name == ''):
                name = splitext(sys.argv[1])[0]+"-asciified.gif"
            while(isfile(name)):
                if(input('name taken. overwrite it? (y/n)): ').lower()=='y'):
                    break
                name = input('enter new name:')
        else:
            name = splitext(sys.argv[1])[0]+"-asciified.gif"
        ims[0].save(name, save_all=True, append_images=ims[1:], duration=t, loop = 0)
        os.system("rm .temp*")  
else:
    print(resString[0])
