Broadlink HTTP server/proxy with REST API
==================================
Supported devices: RM/RM2/RM Pro/RM3/BlackBean/A1
-------------------------------------------------

Uses [python-broadlink](https://github.com/mjg59/python-broadlink)

Based and inspired by [BlackBeanControl](https://github.com/davorf/BlackBeanControl)

Example usage
-------------

1) Update settings.ini with your configuration

You can erase the section for specific devices to have the system auto-detect.
These settings will be rewritten to the settings.ini file so that it doesn't
need auto-detection for the next run.  If you add a device, you can force
autodetection by setting the "Autodetect" option to valid integer, the number
of seconds to timeout the autodetection process.  When no devices are found
and no Autodetect option is present, then Autodetection is forced with a
timeout of 5 seconds.

If you have more than one IP address, you can restrict serverAddress to an IP
Likewise, serverPort can be changed from the default of 8080

You may give multiple device sections with different names to organize your
commands by device.  The plain "Commands" section is used when a device is
not specified, and as a default should a command not be found in a device-
specific section.

2) Start python server.py

If no devices are in settings.ini, note the names of the devices found.  These
will be named by the hostname, so make sure the IP address resolves or enter
it in /etc/hosts

3) In your browser:
```
http://localhost:8080/learnCommand/lampon   #learn command with name lampon
http://localhost:8080/sendCommand/lampon    #send command with name lampon
```
If you have more than one device, use the alternate syntax
```
http://localhost:8080/deviceName/learnCommand/lampon   #learn command with name lampon
http://localhost:8080/deviceName/sendCommand/lampon    #send command with name lampon
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
Alternatively, see the new getSensor format below instead

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
Alternatively, use the new syntax
```
http://localhost:8080/SomeA1Device/getSensor/temperature
```
Where SomeA1Device is some valid A1 device.  You can also read the temperature from RM devices
with this syntax.  This is likely the preferred method.

6) Get and Set status of devices having COMMANDon and COMMANDoff abilities
```
http://localhost:8080/sendCommand/lampon #automaticly set status of "lamp" to "on"
http://localhost:8080/getStatus/lamp     #return lamp status as 0 or 1
```

