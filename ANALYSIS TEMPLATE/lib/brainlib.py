import numpy as np
from scipy import stats
from scipy.interpolate import interp1d


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





def powerSpectraArray (pspectra,xOutput):

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
