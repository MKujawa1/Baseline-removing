import numpy as np
import math
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit

def lorentzian_gen( x, x0, a, gam ):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def generate_data(noi=1,scale = 1):
    
    l = 2000
    
    x2 = np.linspace(-l//2,l//2,l)


    end_lor = lorentzian_gen(
        x2, np.random.randint(-400,400,1)[0], 
        np.random.randint(10,60,1)[0], 
        np.random.randint(60,200,1)[0])
        
   
    wave = end_lor
   
    end_noi = 0
    for v in range(3):
        end_noi = end_noi+ np.random.randn(l)*noi
    end_noi = end_noi/3
   
    data = wave+end_noi
    data = data-(np.mean(data[:5]))
    return data*scale
    

def lorentzian_gen3( x, x0, a, gam ,a2,freq,dc,phase,a3,freq2,dc2,phase2):

    return a * gam**2 / ( gam**2 + ( x - x0 )**2)+\
        (a2*np.sin(2*np.pi*(x)*freq/len(x)+math.radians(phase))+dc)+\
            (a3*np.cos(2*np.pi*(x)*freq2/len(x)+math.radians(phase2))+dc2)
           

def lorentzian_gen2( x, x0, a, gam):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def wave(x,a2,freq,dc,phase,
         a3,freq2,dc2,phase2):
    return (a2*np.sin(2*np.pi*(x)*freq/len(x)+math.radians(phase))+dc)+\
        (a3*np.cos(2*np.pi*(x)*freq2/len(x)+math.radians(phase2))+dc2)
       

plt.figure(figsize = (12,4))
while True:
    data = generate_data(2,0.5)
    
    x = np.arange(len(data))
    d = random.uniform(4, 6)*np.sin(2*np.pi*(x)*random.uniform(0.5, 1.3)/len(x)+math.radians(random.uniform(0, 360)))+random.uniform(-10, 10)+\
        (random.uniform(4, 6)*np.sin(2*np.pi*(x)*random.uniform(0.5, 1.3)/len(x)+math.radians(random.uniform(0, 360)))+random.uniform(-10, 10))
    
    data_bl = data+d*1
    
    
    f3,p3 = curve_fit(lorentzian_gen3, x, data_bl,
                    bounds=([300,3,10,
                             0.5,0.01,-100,0,
                             0.5,0.01,-100,0],
                            [1700,200,300,
                             100,1.2,100,360,
                             100,1.2,100,360]))
    
    
    fun3 = lorentzian_gen3(x,*f3)
    
    # plt.plot(data_bl)
    # plt.plot(fun3)
    plt.clf()
    w = wave(x,*f3[-8:])
    plt.subplot(1,2,1)
    plt.plot(data_bl)
    plt.plot((w+(np.mean(data_bl[:5])-np.mean(w[:5]))))
    
    
    plt.subplot(1,2,2)
    
    plt.plot(data)
    plt.plot(data_bl-(w+(np.mean(data_bl[:5])-np.mean(w[:5]))))
    
    # l = lorentzian_gen2(x,f3[0],f3[1],f3[2])
    
    # bl = fun3-l
    
    # # plt.plot(data_bl)
    # # plt.plot(bl+(data_bl[0]-bl[0]))
    # plt.clf()
    
    # plt.subplot(2,2,1)
    # plt.title('BL_DATA AND FIT_DATA')
    # plt.plot(data_bl)
    # plt.plot(fun3)
    # plt.subplot(2,2,2)
    # plt.title('BL_DATA AND FIT-LORENTZ')
    # plt.plot(data_bl)
    # plt.plot(bl+(data_bl[0]-bl[0]))
    # plt.subplot(2,2,3)
    # plt.title('BL_REMOVED')
    # plt.plot(data_bl-(bl+(np.mean(data_bl[:5])-np.mean(bl[:5]))))
    # plt.subplot(2,2,4)
    # plt.title('ORG AND BL_REMOVED')
    # plt.plot(data)
    # plt.plot(data_bl-(bl+(np.mean(data_bl[:5])-np.mean(bl[:5]))))
    
    plt.pause(0.5)
