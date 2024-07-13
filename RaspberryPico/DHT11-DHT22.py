import dht
from machine import Pin
from time import sleep

sensorTH = dht.DHT22 (Pin(15))  #Conectado a pin 20 (GP15)

while (1):
    sensorTH.measure ()  #Mide
    
    print (sensorTH.temperature(),"grados")
    print (sensorTH.humidity (),"%")
    sleep (2)
    