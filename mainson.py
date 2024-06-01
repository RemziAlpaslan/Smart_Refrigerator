from machine import Pin, I2C, ADC
import utime as time
from dht import DHT11, InvalidChecksum
from pico_i2c_lcd import I2cLcd

pin = Pin(22, Pin.OUT, Pin.PULL_DOWN)
pin2 = Pin(10, Pin.OUT, Pin.PULL_DOWN)

relay1 = Pin(18, Pin.OUT)
relay2 = Pin(19, Pin.OUT)
relay3 = Pin(20, Pin.OUT)
relay4 = Pin(21, Pin.OUT)

i2c = I2C(id=1,scl=Pin(27),sda=Pin(26),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

adc = ADC(Pin(28, mode=Pin.IN))

temp=0.0
setTemp  = 0.0
temp1=0.0
temp2=0.0
pelt_sayac=0
gpio_pin = machine.Pin(1, machine.Pin.IN)
while True:
    
    try:
        sensor = DHT11(pin)
        temp1= (sensor.temperature)
        sensor2 = DHT11(pin2)
        temp2= (sensor2.temperature)
        
    except:
          pass

    setTemp=round((adc.read_u16()/65535)*25-2.5,1)
    
    if temp1>setTemp and pelt_sayac != 400:
        pelt_sayac=pelt_sayac+1
    if temp1<setTemp and pelt_sayac != 0:
        pelt_sayac=pelt_sayac-1
    if pelt_sayac>350:
        relay1.value(0)
        relay2.value(0)
        relay3.value(0)
        relay4.value(0)
        
    elif pelt_sayac>300:
        relay1.value(1)
        relay2.value(0)
        relay3.value(0)
        relay4.value(0)
        
    elif pelt_sayac>200:
        relay1.value(1)
        relay2.value(1)
        relay3.value(0)
        relay4.value(0)
        
    elif pelt_sayac>100:
        relay1.value(1)
        relay2.value(1)
        relay3.value(1)
        relay4.value(0)
    else:
        relay1.value(1)
        relay2.value(1)
        relay3.value(1)
        relay4.value(1)
    if len(str(temp2))==3:
        temp21=str(temp2)+' '
    else:
        temp21=str(temp2)
    if len(str(temp1))==3:
        temp11=str(temp1)+' '
    else:
        temp11=str(temp1)
    setTemp=int(setTemp)
    if len(str(int(setTemp)))==1:
        setTemp1=str(int(setTemp))+' '
    else:
        setTemp1=str(int(setTemp))
    print(len(str(setTemp)))
    time.sleep(0.01)
    try:
        lcd.move_to(0,0)
        lcd.putstr('Ic:'+str(temp11)+"C")
        lcd.move_to(11,0)
        lcd.putstr('Ayar:')
        lcd.move_to(0,1)
        lcd.putstr('Dis:'+str(temp21)+"C")
        lcd.move_to(13,1)
        lcd.putstr(str(setTemp1)+"C")

    except:
        pass