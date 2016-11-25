# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from tkinter import *
from tkinter import filedialog
import pandas as pd
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

plotly.tools.set_credentials_file(username='victorpimenta', api_key='znZcYtEF4Mq7VqMhgRiy')


"""
functions space
"""

############### Signal Generator #################

#create a sin function signal with 3 base frequencies and its 3 first harmonics
def signalgenerator(frequencies, Fs, noise = True, signal = 0):
    
    for freq in frequencies:
        #base frequencies
        wave = (amplitude) * np.sin(2.0*np.pi*freq*t)
        
        #1st harmonics
        harmonic1 = (amplitude/2) * np.sin(2.0*np.pi*2*freq*t)
        
        signal += wave + harmonic1

    #creates noise
    # 0 is the mean of the normal distribution you are choosing from
    # 1 is the standard deviation of the normal distribution
    # last one is the number of elements you get in array noise
    
    noise = np.random.normal(0,1,Fs)
#TODO: create a method that generates more waves and maybe add noise

    signal += noise
    return signal


################### csv_data #####################

# Reads a .csv file and converts the data to a time vector t and a vector x
# with the measured values
def csv_data(file_path):
    return np.genfromtxt(file_path,delimiter=',', unpack=True)



################## freqZoom #######################

# Given 2 frequency values, creates a plot of the FFT in the interval
# delimited by them
def freqZoom(yf, xf, lowFreq, highFreq, limit = False):
    
    N = np.int(np.prod(yf.shape))
    Fs = 2*xf[-1]
    ax = plt.figure().add_subplot(111)  
    ax.plot(xf[int(lowFreq*N/Fs) : int(highFreq*N/Fs) + 1], 2.0/N * np.abs(yf[int(lowFreq*N/Fs):int(highFreq*N/Fs) + 1]))
    ax.grid()
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude')
    #ax.set_xlim([int(lowFreq), int(highFreq)])
    message = "Ok"
    if limit != False:     
        ax.hlines(limit, int(lowFreq), int(highFreq) + 1, color = 'r')
        if np.max(2.0/N * np.abs(yf[int(lowFreq*N/Fs):int(highFreq*N/Fs) + 1])) >= limit:
            message = "Danger"
    ax.set_title("%.1f Hz to %.1f Hz - %s"%(lowFreq,highFreq,message))

#TODO: add a feature that monitor the amplitudes within the interval of freqZoom




"""
values space
"""

###### If generating a signal ######
amplitude = 1.0

#in Hz
frequencies = [1000.0, 755.0, 355.0]

#t = np.arange(0.0,1,25e-6)  

####################################

###### If using a csv file #########

file_name = "car_engine.csv"


####################################

#TODO: whats the best step for t variable so that we can have a good measuement?(considering the amount of harmonics)
"""
process
"""


#signal = signalgenerator(freq1,freq2,freq3)
t, signal = csv_data("CSV_FILES/" + file_name)

## To include in the final version

#root = Tk()
#root.withdraw()
#t, signal = csv_data(filedialog.askopenfilename())
#root.destroy()

##

N = np.int(np.prod(t.shape))# list length
Fs = 1/(t[1]-t[0]) 	# sample frequency
T = 1/Fs;
print("# Samples:", N)


"""
plots
"""

#Plot xy
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(t, signal)
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Amplitude')
ax1.grid()
#ax1.axis([0.0,0.1,-10*amplitude,10*amplitude])
ax1.set_title("Time Domain")
plt.savefig('htmlreport/img/time.png')
plt.clf()

#FFT
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
yf = fft(signal)
yplot = 2.0/N * np.abs(yf[0:np.int(N/2)])
ax2.plot(xf, yplot)
ax2.grid()
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Amplitude')
ax2.set_title("Frequency Domain")
plt.savefig('htmlreport/img/freq.png')



#freqZoom(yf,xf,0,1500, 0.8)
freqZoom(yf,xf,0,2000,0.05)


plt.show()

#%% Plotly Dynamic Plot

#data1 = Scattergl(x = t, y = signal, name = '<b>Time-domain signal</b>')
#data2 = Bar(x = xf, y = yplot, name = '<b>FFT</b> Spectrogram')
#data = [data2]
#fig = dict(data = data)
##time_url = py.plot_mpl(fig2, filename='time-domain')

#%% HTML Report

df = pd.DataFrame({'i':t, 'rms':signal})
sample = df.head(10)
html_table = sample.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling

html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Vibrations Analysis Tool - Group 2 Inc.</h1>

        <!-- *** Section 1 *** --->
        <h2>Section 1: Time Domain Signal</h2>
        <img src="img/time.png" alt="Time Domain Signal" style="width:432px;height:288px;">
        <p>Include maximum value, average, etc</p>
        
        <!-- *** Section 2 *** --->
        <h2>Section 2: FFT Spectrogram (Fast Fourier Analysis)</h2>
        <<img src="img/time.png" alt="Time Domain Signal" style="width:432px;height:288px;">
        <p>Include maximum value, average, etc</p>
        
        <h3>Reference table: rms value</h3>
        ''' + html_table + '''
    </body>
</html>'''
    
f = open('htmlreport/report.html','w')
f.write(html_string)
f.close()

