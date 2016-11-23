LAST UPDATE: 11/22/2016 10:50pm


Description:

signalgenerator(freq1, freq2, freq3)
	
	Generates a signal based on the frequencies provided. There is the addition of noise, which is still not the ideal representation.
	This function is used only for test purposes. In our application, the signal will probably be stored as a .csv file.
	The implementation of a .csv reader will be done soon.
	
csv_data(file_path):

	Given the path to a .csv file containing t and signal values, this function will read the file and create the vector to analyze
	th signal.
	
	
freqZoom(yf, xf, lowFreq, highFreq, limit)

	By providing an interval [lowFrew, highFreq], this function creates a plot of the FFT within the interval.
	If a limit value is provided, the function should monitor this interval.
	Right now, the monitoring is done by raising an alert if any amplitude value within the frequency interval
	exceeds the limit value.
	Of course this is probably not enough, but it is a start.
	It is important to use frequencies lower than half the sampling frequency. Otherwise, the function will raise an error.
	
This code is a test version. It's objective is to allow us to visualize the problem.
The definitive version would be more organized and user oriented.
Also, the definitive code structure should be adapted to the raspberryPi's interface.


IN PROGRESS:

1) Data is usually stored as a .csv file. Adding a feature to extract the signal from a csv file is the next step. (DONE)

2) Organize the code into separate files, each one responsible for a part of the program. Right now the code is very confusing as all of 
   it's content is compressed to the same file.
   (Example: Files - Main, Signal Generator, CSV Data Extraction, Frequency Band Analysis)

3) Some sensors might not have the capability to store time information. If it only provides the measured information,
   maybe the addition of the creation of the time vector based on the sampling frequency can be useful. However, the RaspberryPi
   is probably capable to do this.
   
4) Is the monitoring by creating an amplitude limit enough? Is there another monitoring option? RMS value?
   RMS value will be added soon.

5) Which sampling frequency would simulate a reasonable sensor?
   For test purposes.

6) Which version of Python is used by RaspberryPi: 2 or 3? Should the code be able to run on both?
   