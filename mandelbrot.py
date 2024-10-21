# https://preshing.com/20110926/high-resolution-mandelbrot-in-obfuscated-python/
import struct
from math import log, log2

g = 3  # sub-grid size
i = 255  # max iterations
w, h = 1200, 800  # width & height
P = struct.pack  # pack function alias
M = open('M.bmp', 'wb')  # output file


def Y(c):  # accepts complex number to use in Mandelbrot function
    # returns fraction of remaining iterations to reach solution
    z = 0
    n = i
    while (abs(z) < 6):
        z = z*z + c
        if not (n := n - 1):  # check for maximum iterations
            return n  # use zero to signify member of set
    return (2 + n - 4*abs(z)**-0.4)/i  # smooth out bands


def T(t):  # accepts fraction in range 0.0 to ~1.0
    # returns RGB colour as tuple of 8-bit values
    r = t*80 + 255*t**9 - 950*t**99
    g = t*70 - 880*t**18 + 701*t**9
    b = t*255**(1 - 2*t**45)
    return int(b), int(g), int(r) # intentionally not RGB


# BITMAPINFOHEADER (RGB24)
M.write(b'BM' + P('<QIIHHHH',  # id field
                  w*h*3+26,  # file size (data + header)
                  26,  # header size
                  12,  # data offset
                  w,  # bitmap width
                  h,  # bitmap height
                  1,  # colour planes
                  24))  # bits per pixel

#p = 0  # for original sub-grid position
p = g//2  # offset for sub-grid position
for y in range(h):  # -1.25j to +1.25j
    print("%.2f%%\r" % (100*y/h), end="")
    for x in range(w):  # -2.70 to +1.05
        s = 0.0  # fraction of remaining iterations
        for a in range(-p, g - p):
            for b in range(-p, g - p):
                z = complex(3.75*(x + a/float(g))/w - 2.70,
                            2.50*(y + b/float(g))/h - 1.25)
                s += Y(z)**2  # mean squared value
        M.write(P('BBB', *T(s/g**2)))
