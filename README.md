Broadlink Web server with REST API
==================================
Supported devices: RM/RM2/RM Pro/RM3/BlackBean/A1
-------------------------------------------------

Uses [python-broadlink](https://github.com/mjg59/python-broadlink)

Based and inspired by [BlackBeanControl](https://github.com/davorf/BlackBeanControl)

Example usage
-------------

1) Update settings.ini with your configuration

2) Start python server.py

3) In your browser:
```
http://localhost:8080/learnCommand/lampon   #learn command with name lampon
http://localhost:8080/sendCommand/lampon    #send command with name lampon
```
4) Added get temperature from supported devices (like RM2/Pro):
```
http://localhost:8080/getStatus/temperature
```
Returns:
```
{ "temperature": 22.2 } 
```
*required JSON format suites [homebridge-http-temperature](https://github.com/metbosch/homebridge-http-temperature) plugin.

5) Added support for A1 sensors (temperature, lights and etc..)
```
http://localhost:8080/a1/temperature
http://localhost:8080/a1/lights
http://localhost:8080/a1/noise
and etc..
```
Returns:
```
{ "temperature": 22.2 } 
{ "lights": dark } 
{ "noise": low } 
and etc..
```
*required JSON format suites [homebridge-http-temperature](https://github.com/metbosch/homebridge-http-temperature) plugin.
