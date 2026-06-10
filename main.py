# A rough frequency counter.

import time, machine, esp32, micropython

# The pin with the signal we want to measure the frequency of.
SIGNAL_PIN = 13
signal_pin = machine.Pin(SIGNAL_PIN, machine.Pin.IN)

# The Pulse Counter to use.
PULSE_COUNTER_UNIT = 0

# Filter out signal glitches that are shorter than this value.
FILTER_NS = 10

# The number of samples to collect. Larger N will be slower but more accurate.
N = micropython.const(50)

counter_start_time_us = time.ticks_us()
ONE_SECOND_IN_US = micropython.const(1000000)
N_TIMES_ONE_SECOND_IN_US = micropython.const(N * ONE_SECOND_IN_US)  # Precalculate for speed.

def calculate_frequency(args):
    # We know N and the start and end times. Calculate the average frequency of this sample, in Hz.
    start_time, end_time = args
    frequency = N_TIMES_ONE_SECOND_IN_US / time.ticks_diff(end_time, start_time)
    print(f"{frequency}Hz")

def counter_max_callback(_):
    # Note the time. Schedule the frequency calculation, providing the start and end times.
    now = time.ticks_us()
    global counter_start_time_us

    micropython.schedule(calculate_frequency, (counter_start_time_us, now))
    counter_start_time_us = now

# Set up the Pulse Counter to count to N. On N, reset the count and raise an interrupt.
counter = esp32.PCNT(PULSE_COUNTER_UNIT, pin=signal_pin, rising=esp32.PCNT.INCREMENT, max=N, filter=FILTER_NS)  # filter is important!
counter.irq(handler=counter_max_callback, trigger=esp32.PCNT.IRQ_MAX)
counter.start()

try:
    while True:
        print("Sampling signal...")
        time.sleep(1)
except KeyboardInterrupt as e:
    counter.stop()
    raise e

