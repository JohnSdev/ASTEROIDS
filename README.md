README
Detta är Asteroids spelet med IOT Hub implementerad

Se exempel på en enkel implemtentering i egen app Både som standalone eller class

https://docs.microsoft.com/sv-se/azure/iot-hub/iot-hub-python-getstarted

Alt 1: iot_standalone.py är filen från tutorialn. Den kan köras standalone eller importeras i Asteroids och sedan via funktion
skicka meddelanden. (Obj endast Alt 2 är implementerad för tillfället)

Alt2:
iot.py är samma program dock ändrad till en class. I Asteroids.py importeras klassen och sedan skapas det ett objekt med IOT() Rad 40. 

På Rad 327, GameOver så aktiveras funtionen för att skicka meddelandet och score parametern skickas med. 
Denna metod är mest lämplig om man ska skapa flera olika IOT objekt, eftersom IOT.py är en device simulator så skulle det passa
Alt 1 ovan är enklare då man inte behöver göra en klass.
