# A rough frequency counter.

import time, machine, esp32, micropython

SECONDS_IN_MS = machine.const(1000)


def calculate_frequency(pulses):
    frequency = pulses / TIMER_PERIOD_MS * SECONDS_IN_MS
    print(f"frequency: {frequency}Hz")


def timer_callback(_):
    micropython.schedule(calculate_frequency, counter.value(0))  # This also resets the pulse counter to zero.


SIGNAL_PIN = 13  # The pin with the signal we want to measure the frequency of.
signal_pin = machine.Pin(SIGNAL_PIN, machine.Pin.IN)

PULSE_COUNTER_UNIT = 0  # The Pulse Counter to use.
GLITCH_FILTER_NS = 10  # Filter out signal glitches that are shorter than this value.
counter = esp32.PCNT(PULSE_COUNTER_UNIT, pin=signal_pin, rising=esp32.PCNT.INCREMENT, filter=GLITCH_FILTER_NS)

TIMER_ID = 0  # The hardware timer to use.
TIMER_PERIOD_MS = 50  # The sampling period.
timer = machine.Timer(TIMER_ID, mode=machine.Timer.PERIODIC, period=TIMER_PERIOD_MS, callback=timer_callback)
counter.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    counter.stop()
    timer.deinit()
    raise e
