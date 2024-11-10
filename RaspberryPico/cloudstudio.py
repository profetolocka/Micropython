import dht, time, ujson, gc
from machine import Pin, ADC
import network, urequests
from time import sleep

sensorTH = dht.DHT22 (Pin(15))  #Conectado a pin 20 (GP15)

sensor_temp = ADC(4)
factor_conversion = 3.3 / (65535)

#Datos de la red Wifi
red ="LosToloNetwork"
password ="performance15"

#Token de acceso a Cloud Studio
accessToken = "c98b4c0a-bccf-4405-91fc-6fa0d76f1db5"

#Endpoints de las tres variables
endPointTPico   = 121894
endPointTSensor = 121895
endPointHSensor = 121896

#URLs de las variables
tempURL = 'https://gear.cloud.studio/services/gear/DeviceIntegrationService.svc/UpdateTemperatureSensorStatus'
humURL  = 'https://gear.cloud.studio/services/gear/DeviceIntegrationService.svc/UpdateHumiditySensorStatus'

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

def enviarDatos():
    
    # Realizo la lectura correspondiente a cada sensor
    sensorTH.measure ()  #Mide
    
    tempSensor = sensorTH.temperature()
    humSensor = sensorTH.humidity ()
    
    temp2040 = sensor_temp.read_u16() * factor_conversion
    tempInterna = 27 - (temp2040 - 0.706) / 0.001721
    
    # Armas los payloads de las variables
    
    payloadTempInterna = {
        'accessToken': accessToken,  # Se repite en todos los payloads que realicemos
        'endpointID': endPointTPico, # Es un numero entero y se modifica de acuerdo al sensor que utilicemos
        'temperatureCelsius': tempInterna 
    }
    print('Temperatura del sensor interno', payloadTempInterna['temperatureCelsius'])
    print()

    payloadTempSensor = {
        'accessToken': accessToken,  # Se repite en todos los payloads que realicemos
        'endpointID': endPointTSensor, # Es un numero entero y se modifica de acuerdo al sensor que utilicemos
        'temperatureCelsius': tempSensor
    }
    print('Temperatura del sensor DHT22', payloadTempSensor['temperatureCelsius'])
    print()

    payloadHumSensor = {
        'accessToken': accessToken,  # Se repite en todos los payloads que realicemos
        'endpointID': endPointHSensor, # Es un numero entero y se modifica de acuerdo al sensor que utilicemos
        'humidityPercentage': humSensor
    }
    print('Humedad del sensor DHT22', payloadHumSensor['humidityPercentage'])
    print()

    #Enviar datos al servidor
    
    response = urequests.post(tempURL, json = payloadTempInterna)
    print('Respuesta del servidor: ', response.status_code)
    response.close()

    response = urequests.post(tempURL, json = payloadTempSensor)
    print('Respuesta del servidor: ', response.status_code)
    response.close()

    response = urequests.post(humURL, json = payloadHumSensor)
    print('Respuesta del servidor: ', response.status_code)
    response.close()

while (1):

    try:
        conectaWiFi (red, password)
                    
        enviarDatos()
        sleep (5)
        
        gc.collect ()

    except Exception as err:    
        print ("Error:",err)
        #machine.reset ()
        