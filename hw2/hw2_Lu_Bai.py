import sys
from math import *
from numpy import *
from pylab import *

print 'Please input the elastic modulus:'
input_line = sys.stdin.readline()
E = float(input_line)

print 'Please input the density:'
input_line1 = sys.stdin.readline()
D = float(input_line1)

print 'Please input the second area moment of the cross-section:'
input_line2 = sys.stdin.readline()
I = float (input_line2)

print 'Please input the area of the cross-section:'
input_line3 = sys.stdin.readline()
A = float (input_line3)

print 'Please input the length of the beam:'
input_line4 = sys.stdin.readline()
L = float (input_line4)

print 'Please input the number of vibration modes to caculate:'
input_line5 = sys.stdin.readline()
N = int (input_line5)


for n in range ( 1, N+1) :
    l = (n+0.5) * pi
    while True:
        f = cos(l) - 1/cosh(l)
        df = -sin(l) + sinh(l)/cosh(l)**2.
        dl = -f/df
        l = l+dl
        if abs(dl) < 1e-8:
            break
    Wn =  sqrt (E*I/D/A) * L * L/l**2.
    outfile = open ('mode_%d.txt'%n, 'w')
    outfile.write( '%.10e\n'%Wn )
    npts = 20*n-9
    m = cos(l/2.)/cosh(l/2.)
    
    for i in range (0, npts):
        if n%2==0:
            even = sin(l*(i/(npts-1.)-0.5))-m*sinh(l*(i/(npts-1.)-0.5))
            outfile.write('%.10e\n'%even)
        else:
            odd = cos(l*(i/(npts-1.)-0.5))-m*cosh(l*(i/(npts-1.)-0.5))
            outfile.write('%.10e\n'%odd)
    outfile.close()
    filename = 'mode_%d.txt' %n
    modedata = loadtxt (filename, skiprows=1)

    figure()
    plot(modedata)
    grid(True)
    title('Mode shape of mode %d' %n)
    show()