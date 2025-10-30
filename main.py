from machine import *
import time
from NRF24L01 import *



SCK_PIN = 6
MOSI_PIN = 7
MISO_PIN = 4
CSN_PIN = 16   # Chip Select Not
CE_PIN = 17    # Chip Enable

IRQ_PIN_NUM = 18

# Initialize the SPI bus (SPI(0) is common)
# Baudrate should be relatively fast, 4MHz is usually safe.
spi = SPI(0, baudrate=4000000, polarity=0, phase=0,
          sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))

# Initialize the control pins as Pin objects
csn = Pin(CSN_PIN, Pin.OUT, value=1)
ce = Pin(CE_PIN, Pin.OUT, value=0)

irq_pin = Pin(IRQ_PIN_NUM, Pin.IN, Pin.PULL_UP)

# Initialize the radio object
# The library expects Pin objects for CSN and CE.
nrf = NRF24L01(spi, csn, ce, payload_size=16)
nrf.set_channel(76)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

volatile_data_ready = False
# 🔼 --- END NEW --- 🔼


# 🔽 --- NEW: Interrupt Service Routine (ISR) --- 🔽
# This function is called *automatically* when the IRQ_PIN goes from HIGH to LOW
def nrf_irq_handler(pin):
    global volatile_data_ready
    # We just set the flag. We do the *real* work in the main loop.
    # This keeps the ISR very fast.
    volatile_data_ready = True


def transmit():
    nrf.stop_listening()
    while True:
        data = b"Hello World"
        nrf.send(data)
        print(f"Sending data: {data}")
        time.sleep(1)

def receive():
    global volatile_data_ready
    nrf.start_listening()

    irq_pin.irq(trigger=Pin.IRQ_RISING, handler=nrf_irq_handler)
    while True:
        if volatile_data_ready:
            irq_pin.irq(handler=None)
            volatile_data_ready = False
            print("Irq detected!")
            if nrf.any():
                received_data = nrf.recv()
                print(f"Received data: {received_data}")
            time.sleep(1)
        irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=nrf_irq_handler)

transmit()
