uPyFrequency
============

A rough frequency counter in MicroPython.

Approach: time how long it takes for the Pulse Counter peripheral to count N rising edges on the signal pin, and use that to calculate the frequency.

A higher value for N will give higher accuracy at the cost of speed.

As the frequency slows, so will the rate of frequency updates provided by this code.

The timing will be affected by MicroPython overheads so it's not the most accurate, but depending on your application this might be good enough.

A better approach would be to use the RMT peripheral to very accurately set the sampling period (as demonstrated in e.g. https://github.com/DavidAntliff/esp32-freqcount). At time of writing MicroPython doesn't have this support for the RMT.

Tested with a 1kHz signal and N=50, giving typical results:
* 999.84Hz
* 1000.16Hz
* 999.84Hz
* 1000.06Hz
* 1000.02Hz
* 1000.08Hz
* 999.84Hz
* 1000.16Hz
* 999.84Hz

