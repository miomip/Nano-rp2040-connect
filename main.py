from machine import *
import time
from NRF24L01 import *


SCK_PIN = 13    # 13 (D13)
MOSI_PIN = 11   # 11 (D11)
MISO_PIN = 12  # 12 (D12)
CSN_PIN = 16   # D0 (GPIO 16) is often free
CE_PIN = 17    # D1 (GPIO 17) is often free

# Initialize the SPI bus (SPI(0) is the default hardware bus)
# The specific GPIO numbers must match your board's configuration.
spi = SPI(0, baudrate=4000000, polarity=0, phase=0,
          sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))

# Initialize the radio object
cfg = {'spi': spi, 'cs': CSN_PIN, 'ce': CE_PIN}
nrf = NRF24L01(cfg['spi'], cfg['cs'], cfg['ce'], payload_size=32)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

def transmit():
    nrf.stop_listening()
    while True:
        data = b"Hello World"
        nrf.send(data)
        print(f"Sending data: {data}")
        time.sleep(1)

def receive():
    nrf.start_listening()
    while True:
        if nrf.any():
            received_data = nrf.recv()
            print(f"Received data: {received_data}")
        time.sleep(1)

