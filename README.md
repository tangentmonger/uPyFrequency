uPyFrequency
============

A rough frequency counter in MicroPython for the ESP32.

1. Set up a periodic Timer and also the Pulse Counter. Start them at the same time.
2. In the timer interrupt callback, get the number of pulses the Pulse Counter has seen, and also reset it to zero. Schedule more processing.
3. In the scheduled function, do maths to find the frequency, given the period and the number of pulses.

Pulse Counter filter is important if the signal is noisy.

The timing will be affected by MicroPython overheads so it's not the most accurate, but depending on your application this might be good enough.

A better approach would be to use the RMT peripheral to very accurately set the sampling period (as demonstrated in e.g. https://github.com/DavidAntliff/esp32-freqcount). At time of writing MicroPython doesn't have this support for the RMT.

Tested with a 1kHz signal and period=50ms on an ESP32-S3, giving typical results:
* frequency: 1000.0Hz
* frequency: 1000.0Hz
* frequency: 980.0Hz
* frequency: 1000.0Hz
* frequency: 1000.0Hz
* frequency: 1000.0Hz
* frequency: 1000.0Hz
