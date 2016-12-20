from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import broadlink, configparser
import sys, getopt
import time, binascii
import netaddr
import settings
from os import path
from Crypto.Cipher import AES

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):

        if 'favicon' in self.path:
            return False

        self._set_headers()

        if 'learnCommand' in self.path:
            commandName = self.path.split('/')[2] 
            result = learnCommand(commandName)
            if result == False:
                self.wfile.write("Failed: No command learned")
            else:
                self.wfile.write("Learned: %s" % commandName)

        
        elif 'sendCommand' in self.path:
            commandName = self.path.split('/')[2]
            result = sendCommand(commandName)
            if result == False:
                self.wfile.write("Failed: Unknonwn command")
            else:
                self.wfile.write("Sent: %s" % commandName)

        elif 'getStatus' in self.path:
            if 'temp' in self.path:
                result = getTempRM()
                if result == False:
                    self.wfile.write("Failed: Can not get temperature")
                else:
                    self.wfile.write('''{
    "temperature": %s
}''' % result)
            else:
                self.wfile.write("Failed: Unknonwn command")

        else:
            self.wfile.write("Failed")


def sendCommand(commandName):
    device = broadlink.rm((realIPAddress, realPort), realMACAddress)
    device.auth()

    deviceKey = device.key
    deviceIV = device.iv

    if settingsFile.has_option('Commands', commandName):
        commandFromSettings = settingsFile.get('Commands', commandName)
    else:
        return False

    if commandFromSettings.strip() != '':
        decodedCommand = binascii.unhexlify(commandFromSettings)
        AESEncryption = AES.new(str(deviceKey), AES.MODE_CBC, str(deviceIV))
        encodedCommand = AESEncryption.encrypt(str(decodedCommand))
        
        finalCommand = encodedCommand[0x04:]    
        device.send_data(finalCommand)
        return True

def learnCommand(commandName):
    device = broadlink.rm((realIPAddress, realPort), realMACAddress)
    device.auth()

    deviceKey = device.key
    deviceIV = device.iv

    device.enter_learning()
    time.sleep(RealTimeout)
    LearnedCommand = device.check_data()

    if LearnedCommand is None:
        print('Command not received')
        return False

    AdditionalData = bytearray([0x00, 0x00, 0x00, 0x00])    
    finalCommand = AdditionalData + LearnedCommand

    AESEncryption = AES.new(str(deviceKey), AES.MODE_CBC, str(deviceIV))
    decodedCommand = binascii.hexlify(AESEncryption.decrypt(str(finalCommand)))

    BlackBeanControlIniFile = open(path.join(settings.applicationDir, 'settings.ini'), 'w')    
    settingsFile.set('Commands', commandName, decodedCommand)
    settingsFile.write(BlackBeanControlIniFile)
    BlackBeanControlIniFile.close()
    return True

def getTempRM():
    device = broadlink.rm((realIPAddress, realPort), realMACAddress)
    device.auth()
    temperature = device.check_temperature()
    if temperature:
        return temperature
    return False 

        
def start(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting broadlink-rest server on port %s ...' % port
    httpd.serve_forever()

if __name__ == "__main__":

    settingsFile = configparser.ConfigParser()
    settingsFile.optionxform = str
    settingsFile.read(settings.BlackBeanControlSettings)

    commandName = ''
    deviceName=''
    deviceIPAddress = ''
    devicePort = ''
    deviceMACAddres = ''
    deviceTimeout = ''
    alternativeIPAddress = ''
    alternativePort = ''
    alternativeMACAddress = ''
    alternativeTimeout = ''

    if (deviceName.strip() != '') and ((alternativeIPAddress.strip() != '') or (alternativePort.strip() != '') or (alternativeMACAddress.strip() != '') or (alternativeTimeout != '')):
        print('Device name parameter can not be used in conjunction with IP Address/Port/MAC Address/Timeout parameters')
        sys.exit(2)

    if (((alternativeIPAddress.strip() != '') or (alternativePort.strip() != '') or (alternativeMACAddress.strip() != '') or (alternativeTimeout.strip() != '')) and ((alternativeIPAddress.strip() == '') or (alternativePort.strip() == '') or (alternativeMACAddress.strip() == '') or (alternativeTimeout.strip() == ''))):
        print('IP Address, Port, MAC Address and Timeout parameters can not be used separately')
        sys.exit(2)

    if deviceName.strip() != '':
        if settingsFile.has_section(deviceName.strip()):
            if settingsFile.has_option(deviceName.strip(), 'IPAddress'):
                deviceIPAddress = settingsFile.get(deviceName.strip(), 'IPAddress')
            else:
                deviceIPAddress = ''

            if settingsFile.has_option(deviceName.strip(), 'Port'):
                devicePort = settingsFile.get(deviceName.strip(), 'Port')
            else:
                devicePort = ''

            if settingsFile.has_option(deviceName.strip(), 'MACAddress'):
                deviceMACAddress = settingsFile.get(deviceName.strip(), 'MACAddress')
            else:
                deviceMACAddress = ''

            if settingsFile.has_option(deviceName.strip(), 'Timeout'):
                deviceTimeout = settingsFile.get(deviceName.strip(), 'Timeout')
            else:
                deviceTimeout = ''        
        else:
            print('Device does not exist in settings.ini')
            sys.exit(2)

    if (deviceName.strip() != '') and (deviceIPAddress.strip() == ''):
        print('IP address must exist in settings.ini for the selected device')
        sys.exit(2)

    if (deviceName.strip() != '') and (devicePort.strip() == ''):
        print('Port must exist in settings.ini for the selected device')
        sys.exit(2)

    if (deviceName.strip() != '') and (deviceMACAddress.strip() == ''):
        print('MAC address must exist in settings.ini for the selected device')
        sys.exit(2)

    if (deviceName.strip() != '') and (deviceTimeout.strip() == ''):
        print('Timeout must exist in settings.ini for the selected device')
        sys.exit(2)    

    realIPAddress = settings.IPAddress
    if realIPAddress.strip() == '':
        print('IP address must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)

    realPort = settings.Port
    if realPort.strip() == '':
        print('Port must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        realPort = int(realPort.strip())

    realMACAddress = settings.MACAddress
    if realMACAddress.strip() == '':
        print('MAC address must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        realMACAddress = netaddr.EUI(realMACAddress)

    RealTimeout = settings.Timeout
    if RealTimeout.strip() == '':
        print('Timeout must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        RealTimeout = int(RealTimeout.strip())    

    start()