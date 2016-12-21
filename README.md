Broadlink RM/RM2/RM Pro/RM3/BlackBean Web server with REST API.

Uses https://github.com/mjg59/python-broadlink 
Based and inspired by https://github.com/davorf/BlackBeanControl

Usage:

1) Edit settings.ini

2) Start python server.py

3) In your browser:

http://localhost:8080/learnCommand/lampon   #learn command with name lampon
http://localhost:8080/sendCommand/lampon   #send command with name lampon

4) Added get temperature from supported devices (like RM2/Pro):

http://localhost:8080/getStatus/temp

Returns:

{
    "temperature": 22.2
}

* required JSON format suites homebridge-http-temperature plugin.

5) Added support for A1 sensors (temperature, lights and etc..)

http://localhost:8080/a1/temperature
http://localhost:8080/a1/lights
http://localhost:8080/a1/noise
and etc..


