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

#loglog(ps)

def entropy(powerSpectrum,q):
    q = float(q)
    
    powerSpectrum = np.array(powerSpectrum)
        
    if not q ==1:
        S = 1/(q-1)*(1-np.sum(powerSpectrum**q))
    else:
        S = - np.sum(powerSpectrum*np.log2(powerSpectrum))
        
    return S




'''
takes an array of power spectra and makes an evaluation for each point specified in xOutput. Note that I am not using the binning function anymore. The output is an array of evaluations for each powerspectrum at each time point.
'''

def powerSpectraArray (pspectra,xOutput):
    '''Computes an average power spectrum
    from multiple power spectra, and returns 
    (interpolated) evaluations for xOutput values '''
    
    l = len(pspectra)
    array = np.zeros([l,len(xOutput)])
    # S = []
    
    for i,ps in enumerate(pspectra):
        #print i
        # s = entropy(ps/np.sum(ps),1)
        # S.append(s)
        
        x = np.arange(1,len(ps)+1)
        f = interp1d(x,ps/np.sum(ps))
        # try:
        array[i] = f(x)
        # except:
        #     array[i,0]=-1
        #     continue
        
    index = np.argwhere(array[:,0]==-1)
    array = np.delete(array,index,0)
    #S = np.delete(S,index,0)
    return array#,S

# take all values for now
def getXOutput(spectrumSize, vectorSize):
    return range(1, spectrumSize+1)
    # return np.logspace(1, spectrumSize+1, num=vectorSize, dtype=int)

'''

The get the average and the confidence intervals you need to process the array output as the following:

a,s = avgPowerSpectrum(pspectra,xOutput)
p = 1 #(confidence interval parameter, here 1%-99%)
pDown = np.percentile(a,p,axis=0)
pUp = np.percentile(a,100-p,axis=0)
avg = np.mean(a,0)
std = np.std(a,0)
'''

def avgPowerSpectrum (powerSpectra, xOutput):
    spectra = powerSpectraArray(powerSpectra,xOutput)
    return np.mean(spectra, 0)

# confidenceIntervalParameter of 1 is 1%-99% 
def avgPercentileUp (powerSpectra, xOutput, confidenceIntervalParameter):
    spectra = powerSpectraArray(powerSpectra,xOutput)
    return np.percentile(spectra,100-confidenceIntervalParameter,axis=0)

def avgPercentileDown (powerSpectra, xOutput, confidenceIntervalParameter):
    spectra = powerSpectraArray(powerSpectra,xOutput)
    return np.percentile(spectra,confidenceIntervalParameter,axis=0)
