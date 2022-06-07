import numpy as np
import math
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit

def lorentzian (x, x0, a, gam):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def generate_data(noi = 1,scale = 1):
    '''
    Genetaring lorentzian type signal with noise

    Parameters
    ----------
    noi : float, optional
        amplitude of noise. The default is 1.
    scale : float, optional
        scaling result. The default is 1.

    Returns
    -------
    1d array
        returns lorentzian signal with noise.

    '''
    size = 2000
    x = np.linspace(-size//2,size//2,size)
    
    spect = lorentzian(
        x, np.random.randint(-400,400,1)[0], 
        np.random.randint(10,60,1)[0], 
        np.random.randint(60,200,1)[0])
    
    noise = 0
    for _ in range(3):
        noise = noise+(np.random.randn(size)*noi)-(noi/2)
    noise = noise/3
    data = spect+noise
    data = data-(np.mean(data[:5]))
    return data*scale
    
def lorentzian_wave(x, x0, a, gam ,a2,freq,dc,phase,a3,freq2,dc2,phase2):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)+\
        (a2*np.sin(2*np.pi*(x)*freq/len(x)+math.radians(phase))+dc)+\
            (a3*np.cos(2*np.pi*(x)*freq2/len(x)+math.radians(phase2))+dc2)
           
def wave(x,a,freq,dc,phase,a2,freq2,dc2,phase2):
    return (a*np.sin(2*np.pi*(x)*freq/len(x)+math.radians(phase))+dc)+\
        (a2*np.cos(2*np.pi*(x)*freq2/len(x)+math.radians(phase2))+dc2)
### Params to fit
scale = 1
pause = 0.5 
x0 = [300,1700] 
lor_amp = [3,200]
gam = [10,300]
wave_amp = [0.5,100]
freq = [0.01,1.2]
dc = [-100,100]
phase = [0,360]
### Params to generate lorentz
gen_amp = [0.5, 3]
gen_scale = [0.3,2]
### Params to generate baseline
rand_amp = [3,6]
rand_freq = [0.5, 1.3]
rand_ph = [20,340]
rand_dc = [-20,20]
### Creating baseline, fitting, removing baseline, results on plot in loop     
plt.figure(figsize = (12,4))
while True:
    ### Generate lorentz
    data = generate_data(random.uniform(gen_amp[0],gen_amp[1]),random.uniform(gen_scale[0], gen_scale[1]))
    x = np.arange(len(data))
    ### Generate baseline with sin and cos
    baseline = random.uniform(rand_amp[0],rand_amp[1])*np.sin(2*np.pi*(x)*\
            random.uniform(rand_freq[0],rand_freq[1])/len(x)+\
                math.radians(random.uniform(rand_ph[0],rand_ph[1])))+random.uniform(rand_dc[0],rand_dc[1])+\
        random.uniform(rand_amp[0],rand_amp[1])*np.cos(2*np.pi*(x)*\
            random.uniform(rand_freq[0],rand_freq[1])/len(x)+\
                math.radians(random.uniform(rand_ph[0],rand_ph[1])))+random.uniform(rand_dc[0],rand_dc[1])
    ### Adding baseline to data
    data_bl = data+baseline*scale
    ### Fit to data with baseline
    fit,p = curve_fit(lorentzian_wave, x, data_bl,
                    bounds=([x0[0],lor_amp[0],gam[0],
                             wave_amp[0],freq[0],dc[0],phase[0],
                             wave_amp[0],freq[0],dc[0],phase[0]],
                            [x0[1],lor_amp[1],gam[1],
                             wave_amp[1],freq[1],dc[1],phase[1],
                             wave_amp[1],freq[1],dc[1],phase[1]]))
    ### Baseline based on previous fit
    bl_rem = wave(x,*fit[-8:])
    ### Baseline removing
    bl = bl_rem+(np.mean(data_bl[:5])-np.mean(bl_rem[:5]))
    rem = data_bl-(bl_rem+(np.mean(data_bl[:5])-np.mean(bl_rem[:5])))
    ### Calulating mse
    mse = np.mean((data-rem)**2)
    ### Plot displaying
    plt.clf()
    plt.suptitle('BASELINE REMOVING')
    plt.subplot(1,2,1)
    plt.plot(data_bl,label = 'data with baseline')
    plt.plot(bl,label = 'fit baseline')
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(data,label = 'real data')
    plt.plot(rem,label = 'data after \nbaseline removing \nMSE: '+ str(np.round(mse,2)))
    plt.legend()
    plt.pause(pause)