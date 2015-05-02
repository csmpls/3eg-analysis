import numpy as np
from scipy import stats
from scipy.interpolate import interp1d

'''Here all functions related to the analysis of EEG signal, 
using methods based on the power spectrum'''


def pSpectrum(vector):
    
    A = np.fft.fft(vector)
    ps = np.abs(A)**2
    ps = ps[:len(ps)/2]
        
    return ps

#ps = pSpectrum(test[500:600])
#loglog(ps)

def entropy(power_spectrum,q):
    q = float(q)
    
    power_spectrum = np.array(power_spectrum)
        
    if not q ==1:
        S = 1/(q-1)*(1-np.sum(power_spectrum**q))
    else:
        S = - np.sum(power_spectrum*np.log2(power_spectrum))
        
    return S

def entropySeries(time,rawData,q,windowSize=1,normalize=True):
    
    
    #t = tSeries['rawTime']
    #raw = tSeries['rawValue']
    
    t = np.array(time)
    raw = np.array(rawData)
    
    intervales = np.arange(np.trunc(min(t)+1),np.trunc(max(t)+1),windowSize)

    T = []
    S = [] 
    spectra = []
    
    for i,ix in enumerate(intervales[:-1]):
        #print i,ix
        
        c = (t>=ix)*(t<intervales[i+1])
        
        vector = raw[c]
        ps = np.array(pSpectrum(vector)) # Power Spectrum
        
        try:
            spectra += [ps]
        except:
            spectra = [ps]

        
        
        #if normalize:
        ps = ps/np.sum(ps)
        
        s = entropy(ps,q) #Compute Entropy
        S.append(s)
        T.append(i)

    S = np.array(S)
    T = np.array(T)
    
    if normalize:
        S = (S-np.mean(S))/np.std(S)
        
    return {'time' : list(intervales[:-1]), 'S': list(S),'spectra':spectra}


def avgPowerSpectrum(pspectra,xOutput):
    '''Computes an average power spectrum
    from multiple power spectra, and returns 
    (interpolated) evaluations for xOutput values '''
    
    if isinstance(pspectra,dict):
        pspectra = pspectra.values()
    
    l = len(pspectra)
    array = np.zeros([l,len(xOutput)])
    S = []
    
    for i,ps in enumerate(pspectra):
        #print i
        s = entropy(ps/np.sum(ps),1)
        S.append(s)
        
        x = np.arange(1,len(ps)+1)
        f = interp1d(x,ps/np.sum(ps))
        try:
            array[i] = f(xOutput)
        except:
            array[i,0]=-1
            continue
        
    index =np.argwhere(array[:,0]==-1)
    array = np.delete(array,index,0)
    S = np.delete(S,index,0)
    return array,S
