# -*- coding: utf-8 -*-

#%%
"""
Packages
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from tkinter import *
from tkinter import filedialog
import pandas as pd
import peak


import plotly
import plotly.plotly as py
from plotly.graph_objs import *
plotly.tools.set_credentials_file(username='victorpimenta', api_key='znZcYtEF4Mq7VqMhgRiy')

"""
Variables
"""

threshold = 0.05 # Changes according to standards (ISO 2372)
Noise_Percentage = 0 # Expected Noise amplitude / Peak Amplitude

#%%
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



################ findNearest ######################

# Given a number and an array, finds the index of the nearest value inside the array
def findNearest(value, array):

    index = np.abs(array - value).argmin()
    return index


############### freqZoom #######################

# Given 2 frequency values, creates a plot of the FFT in the interval
# delimited by them
def freqZoom(yf, xf, lowFreq, highFreq, noisePct = 0, threshold = False):

    lowFreqIndex = findNearest(lowFreq, xf)
    highFreqIndex = findNearest(highFreq, xf)
    ax = plt.figure().add_subplot(111)
    ax.plot(xf[lowFreqIndex:highFreqIndex], yf[lowFreqIndex:highFreqIndex])
    ax.grid()
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude')
    peakAmp = np.max(yf[lowFreqIndex:highFreqIndex])
    ax.set_ylim([peakAmp*noisePct, peakAmp])
    message = "NO DANGER"
    if threshold != False:
        ax.hlines(threshold, int(lowFreq), int(highFreq), color = 'r')
        if peakAmp >= threshold:
            message = "DANGER"
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
T = t[1]-t[0] 	# sample frequency
Fs = 1/T
print("# Samples:", N)

#%%
"""
FFT and Peak Detection
"""

yf = np.fft.fft(signal)
xf = np.fft.fftfreq(t.shape[-1], T)
xf = xf[0:np.int(N/2)]
yf = 2.0/N * np.abs(yf[0:np.int(N/2)])

max_index = xf[yf.argmax()]
min_dist = findNearest(max_index, xf)

# Threshold normalizes values to a number between 0 and 1
# Minimum distance between peaks will be adopted as 60% of the biggest amplitude (other peaks probably will be its harmonics)
peaks = peak.indexes(yf, thres = 0.25, min_dist = min_dist)

# Assuming the rotational speed to be expressed by the frequency with maximum amplitude
omega = 60*max_index # Conversion from Hz to RPM
maxAmp = max(yf)
maxHarmAmp = sorted(yf[peaks])[-2]


#%%
"""
Storage of processed data into data frames for easier handling
"""

time_table = pd.DataFrame({'i':t, 'signal':signal})

freq_table = pd.DataFrame({'Information' : ['Maximum amplitude', 'Rotational speed', 'Maximum amplitude @ harmonics'],
                           'Value' : [maxAmp, omega, maxHarmAmp],
                           'Unit' : ['mm/s', 'RPM', 'mm/s']})
freq_table = freq_table.set_index('Information')
freq_table.index.name = None
freq_table = freq_table[['Value', 'Unit']]


#%%
"""
Plots
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
plt.savefig('img/time.png')
plt.clf()

#FFT
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(xf, yf)
ax2.plot(xf[peaks], yf[peaks], 'r+', ms = 5, mew = 2, label ='{} peaks'.format(len(peaks)))
ax2.legend()
ax2.grid()
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Amplitude')
ax2.set_title("Frequency Domain")
plt.savefig('img/freq.png')

#freqZoom(yf,xf,0,1500, 0.8)
freqZoom(yf,xf,0,2000, Noise_Percentage, threshold)

plt.show()

    #%%
"""
Plotly Dynamic Plot
"""

#data1 = Scattergl(x = t, y = signal, name = '<b>Time-domain signal</b>')
#data2 = Bar(x = xf, y = yplot, name = '<b>FFT</b> Spectrogram')
#data = [data2]
#fig = dict(data = data)
##time_url = py.plot_mpl(fig2, filename='time-domain')


#%%
"""
HTML Report
"""

sample = time_table.head(10)
time_table_html = sample.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling

freq_table_html = freq_table.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')

html_string = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Group 2 | Dashboard</title>
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.6 -->
  <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
  <!-- Ionicons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css">
  <!-- Theme style -->
  <link rel="stylesheet" href="dist/css/AdminLTE.min.css">
  <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
  <link rel="stylesheet" href="dist/css/skins/_all-skins.min.css">
  <!-- iCheck -->
  <link rel="stylesheet" href="plugins/iCheck/flat/blue.css">
  <!-- Morris chart -->
  <link rel="stylesheet" href="plugins/morris/morris.css">
  <!-- jvectormap -->
  <link rel="stylesheet" href="plugins/jvectormap/jquery-jvectormap-1.2.2.css">
  <!-- Date Picker -->
  <link rel="stylesheet" href="plugins/datepicker/datepicker3.css">
  <!-- Daterange picker -->
  <link rel="stylesheet" href="plugins/daterangepicker/daterangepicker.css">
  <!-- bootstrap wysihtml5 - text editor -->
  <link rel="stylesheet" href="plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css">

  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
</head>
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">

  <header class="main-header">
    <!-- Logo -->
    <a href="index2.html" class="logo">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><b>G</b>2</span>
      <!-- logo for regular state and mobile devices -->
      <span class="logo-lg"><b>Group 2</b> | Dashboard</span>
    </a>
    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>

      <div class="navbar-custom-menu">
        <ul class="nav navbar-nav">

          <!-- Control Sidebar Toggle Button -->
          <li>
            <a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
  <!-- Left side column. contains the logo and sidebar -->
  <aside class="main-sidebar">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <!-- Sidebar user panel -->
      <div class="user-panel">
        <div class="pull-left image">
          <img src="dist/img/victor.png" class="img-circle" alt="User Image">
        </div>
        <div class="pull-left info">
          <p>Victor Pimenta</p>
          <a href="#"><i class="fa fa-circle text-success"></i> Online</a>
        </div>
      </div>
      <!-- search form -->
      <form action="#" method="get" class="sidebar-form">
        <div class="input-group">
          <input type="text" name="q" class="form-control" placeholder="Search...">
              <span class="input-group-btn">
                <button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i>
                </button>
              </span>
        </div>
      </form>
      <!-- /.search form -->
      <!-- sidebar menu: : style can be found in sidebar.less -->
      <ul class="sidebar-menu">
        <li class="header">MAIN NAVIGATION</li>
        <li class="active treeview">
          <a href="#">
            <i class="fa fa-link"></i> <span>Dashboard</span>
            <span class="pull-right-container">
            </span>
          </a>
          </li>
        <li class="treeview">
          <a href="#">
            <i class="fa fa-pie-chart"></i>
            <span>Charts</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
          </a>
          <ul class="treeview-menu">
            <li><a href="pages/charts/chartjs.html"><i class="fa fa-circle-o"></i> Time Domain</a></li>
            <li><a href="pages/charts/morris.html"><i class="fa fa-circle-o"></i> FFT</a></li>
            <li><a href="pages/charts/flot.html"><i class="fa fa-circle-o"></i> Hilbert Transform</a></li>
          </ul>
        </li>
      </ul>
    </section>
    <!-- /.sidebar -->
  </aside>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Dashboard
        <small>Control panel</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
        <li class="active">Dashboard</li>
      </ol>
    </section>

    <!-- Main content -->
    <section class="content">
      <!-- Small boxes (Stat box) -->
      <div class="row">
        <div class="col-lg-3 col-xs-6">
          <!-- small box -->
          <div class="small-box bg-aqua">
            <div class="inner">

              <p>Maximum peak amplitude</p>
            </div>
            <div class="icon">
              <i class="ion-arrow-graph-up-right"></i>
            </div>
            <a href="#" class="small-box-footer">More info <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
        <!-- ./col -->
        <div class="col-lg-3 col-xs-6">
          <!-- small box -->
          <div class="small-box bg-green">
            <div class="inner">

              <p>Maximum harmonics amplitude</p>
            </div>
            <div class="icon">
              <i class="ion-qr-scanner"></i>
            </div>
            <a href="#" class="small-box-footer">More info <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
        <!-- ./col -->
        <div class="col-lg-3 col-xs-6">
          <!-- small box -->
          <div class="small-box bg-yellow">
            <div class="inner">

              <p>Rotational speed</p>
            </div>
            <div class="icon">
              <i class="ion-ios-gear-outline"></i>
            </div>
            <a href="#" class="small-box-footer">More info <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
        <!-- ./col -->
        <div class="col-lg-3 col-xs-6">
          <!-- small box -->
          <div class="small-box bg-red">
            <div class="inner">

              <p>Sampling rate</p>
            </div>
            <div class="icon">
              <i class="ion-ios-reload"></i>
            </div>
            <a href="#" class="small-box-footer">More info <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
        <!-- ./col -->
      </div>
      <!-- /.row -->
      <!-- Main row -->
      <div class="row">
        <!-- Left col -->
        <section class="col-lg-12 connectedSortable">
          <!-- Custom tabs (Charts with tabs)-->
          
          <img class="img-responsive" src="img/time.png" alt="FFT" style="width:50%" align="left">
          <img class="img-responsive" src="img/freq.png" alt="FFT" style="width:50%" align="right">
          
        </section>
        <!-- /.Left col -->
        <!-- right col (We are only adding the ID to make the widgets sortable)-->
         <!-- right col -->
      </div>
      <!-- /.row (main row) -->

    </section>
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->
  <footer class="main-footer">
    <div class="pull-right hidden-xs">
      <b>Version</b> 1.0.0, Adapted.
    </div>
    <strong>Copyright &copy; 2014-2016 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights
    reserved.
  </footer>

  <!-- Control Sidebar -->

  <!-- /.control-sidebar -->
  <!-- Add the sidebar's background. This div must be placed
       immediately after the control sidebar -->
  <div class="control-sidebar-bg"></div>
</div>
<!-- ./wrapper -->

<!-- jQuery 2.2.3 -->
<script src="plugins/jQuery/jquery-2.2.3.min.js"></script>
<!-- jQuery UI 1.11.4 -->
<script src="https://code.jquery.com/ui/1.11.4/jquery-ui.min.js"></script>
<!-- Resolve conflict in jQuery UI tooltip with Bootstrap tooltip -->
<script>
  $.widget.bridge('uibutton', $.ui.button);
</script>
<!-- Bootstrap 3.3.6 -->
<script src="bootstrap/js/bootstrap.min.js"></script>
<!-- Morris.js charts -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
<script src="plugins/morris/morris.min.js"></script>
<!-- Sparkline -->
<script src="plugins/sparkline/jquery.sparkline.min.js"></script>
<!-- jvectormap -->
<script src="plugins/jvectormap/jquery-jvectormap-1.2.2.min.js"></script>
<script src="plugins/jvectormap/jquery-jvectormap-world-mill-en.js"></script>
<!-- jQuery Knob Chart -->
<script src="plugins/knob/jquery.knob.js"></script>
<!-- daterangepicker -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="plugins/datepicker/bootstrap-datepicker.js"></script>
<!-- Bootstrap WYSIHTML5 -->
<script src="plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js"></script>
<!-- Slimscroll -->
<script src="plugins/slimScroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="plugins/fastclick/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="dist/js/app.min.js"></script>
<!-- AdminLTE dashboard demo (This is only for demo purposes) -->
<script src="dist/js/pages/dashboard.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="dist/js/demo.js"></script>
</body>
</html>
'''

f = open('index.html','w')
f.write(html_string)
f.close()

