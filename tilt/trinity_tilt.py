from time import sleep

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#Hardware SPI Configuration
SPI_PORT=0
SPI_DEVICE=0
mcp=Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

print('Reading MCP3008 values, press Ctrl-C to quit...')

Tilt_Channel_No=0
V_REF=3.3
while True:
        # The read_adc function will get the value of the specified channel (0-7).
        digital_result= mcp.read_adc(Tilt_Channel_No)
        analog_result=digital_result/1024*V_REF*1000
        result=float("{0:.4g}".format(analog_result))
        print (result)
        sleep(5)
