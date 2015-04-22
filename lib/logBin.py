import numpy as np

def binning(x,y,bins,log_10=False,confinter=5):

    # local imports
    from numpy import log10,linspace,logspace,mean,median,append,std,array
    from scipy.stats import scoreatpercentile


    if isinstance(bins,int) or isinstance(bins,float):
        if log_10:
            bins = logspace(np.log10(min(x))*0.9,np.log10(max(x))*1.1,bins)
        else:
            bins = linspace(min(x)*0.9,max(x)*1.1,bins)


    if log_10:
        c = x > 0
        x = x[c]
        y = y[c]
        bins = np.log10(bins)
        x = np.log10(x)
        y = np.log10(y)

    Tbins =[]
    Median =[]
    Sigma =[]
    Perc_Up =[]
    Perc_Down = []
    Points=[]

    for i,ix in enumerate(bins):

        if i+2>len(bins):
            break

        c1 = x >= ix
        c2 = x < bins[i+1]
        c=c1*c2

        if len(y[c])>0:
            Tbins = append(Tbins,median(x[c]))
            Median =  append(Median,median(y[c]))
            Sigma = append(Sigma,std(y[c]))
            Perc_Down = append(Perc_Down,scoreatpercentile(y[c],confinter))
            Perc_Up = append(Perc_Up,scoreatpercentile(y[c],100-confinter))
            Points = append(Points,len(y[c]))

        Perc_Up = array(Perc_Up)
        Perc_Down = array(Perc_Down)
        
        return Tbins,Median,Sigma,Perc_Down,Perc_Up,Points

def percentile(pSpec,binNum): #, tmin=-1, tmax=-1):

    #m = []

    pdf = np.array(map(float, pSpec))
    d = 0

    m = np.reshape(pdf,[len(pdf)/1024,1024])
    perc = np.median(m,0)

    # take a range of samples from the power spectrum, arranged linearly on logarithmic scale 
    # idea here is to sample more from the lower end of the spectrum than from the tail.
    xt = np.logspace(np.log10(0.24),np.log10(1025),binNum)
    x = np.arange(0.25,256.25,0.25)

    # this is where the binning happens
    #try:
    B = binning(x,perc,xt,log_10=True)
        # TODO: is ommiting 'x' really a good idea?
        #return {'x' : list(B[0]),'y' : list(B[1])} 
    return list(B) #list(B[1])
    #except:
    #    print '??'
    #    return 0
