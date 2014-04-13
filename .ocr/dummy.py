import numpy as np 
import pylab
from scipy.interpolate import UnivariateSpline
from matplotlib.ticker import FuncFormatter as ff
import matplotlib 
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

def m2hm(x, i):
    h = int(x)
    m = 100*(x - int(x)) % 60
    return '%(h)01d:%(m)02d' % {'h':h,'m':m}

matplotlib.rc('font', **font)

t = np.arange(0,2,0.001)

x=[0,0.5,0.75,1,1.5,1.75,1.9,2]
y=[2.5, 1.8, 2, 2, 2, 2, 1.9, 1.5]
s = UnivariateSpline(x, y, k=5)

yy = s(t) - 0.2

mn = [yy[:i].mean() for i in xrange(len(yy))]

x2 = [0, 0.3, 0.5, 0.75, 1, 1.25,1.5,1.75, 2]
y2 =[2.75, 2., 2.1,2.2,2.3,2.4,2.5, 2.6, 2.7]
s2 = UnivariateSpline(x2, y2, k=5)
yy2 = s2(t) 

mn2 = [yy2[:i].mean() for i in xrange(len(yy2))]

n = len(yy)
k=0
for i in xrange(1, n-1, 10):
    pylab.figure()
    pylab.plot(t[:i+1], yy[:i+1], 'g-', linewidth=4)
    pylab.plot(t[:i+1], mn[:i+1], 'g--', linewidth=4)


    pylab.plot(t[:i+1], yy2[:i+1], 'r-', linewidth=4)
    pylab.plot(t[:i+1], mn2[:i+1], 'r--', linewidth=4)

     
    pylab.gca().yaxis.set_major_formatter(ff(m2hm))
    pylab.ylabel("500m Split", fontsize=15, weight="bold")
    pylab.xlabel("Km", fontsize=15, weight="bold")
    pylab.xlim(0,2)
    pylab.ylim(1,3)

    pylab.gcf().savefig("plotframes/plot_%04d.png" % k)
    k+=1

# pylab.show()