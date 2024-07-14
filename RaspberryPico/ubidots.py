import dht, time, ujson
from machine import Pin
import network, urequests

sensorTH = dht.DHT22 (Pin(15))  #Conectado a pin 20 (GP15)

red ="LosToloNetwork"
password ="performance15"
token = "BBUS-NWc2yFh4ZOXuAtQI5lo5ubQjtKX8IW"

def conectaWiFi (red, password): 
    global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():
        miRed.active(True)
        miRed.connect(red, password)
        print('Conectando la red', red +"...")
        timeout = time.time ()
        while not miRed.isconnected():
            #wdt.feed ()
            if (time.ticks_diff (time.time (), timeout) > 10):
                return False
    return True

while (1):

    sensorTH.measure ()  #Mide
    
    temp = sensorTH.temperature()
    hum = sensorTH.humidity ()
    
    print (temp,"grados")
    print (hum,"%")
    time.sleep (300)
 
    #try:
    conectaWiFi (red, password)
    
    url = "https://industrial.api.ubidots.com/api/v1.6/devices/raspberry-pico/"
    
    payload = {
        "Temperatura": temp,
        "Humedad": hum
    }
    
    respuesta = urequests.post(url, headers = {'content-type': 'application/json', 'X-Auth-Token':token}, data=ujson.dumps(payload))
        
    print(respuesta.text)
    print (respuesta.status_code)
    respuesta.close ()

    #except:
            
        #print ("Error!")
        #machine.reset ()
        