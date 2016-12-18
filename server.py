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

        else:
            self.wfile.write("Failed")

def sendCommand(commandName):
    RM3Device = broadlink.rm((RealIPAddress, RealPort), RealMACAddress)
    RM3Device.auth()

    RM3Key = RM3Device.key
    RM3IV = RM3Device.iv

    if SettingsFile.has_option('Commands', commandName):
        CommandFromSettings = SettingsFile.get('Commands', commandName)
    else:
        return False

    if CommandFromSettings.strip() != '':
        DecodedCommand = binascii.unhexlify(CommandFromSettings)
        AESEncryption = AES.new(str(RM3Key), AES.MODE_CBC, str(RM3IV))
        EncodedCommand = AESEncryption.encrypt(str(DecodedCommand))
        
        FinalCommand = EncodedCommand[0x04:]    
        RM3Device.send_data(FinalCommand)

def learnCommand(commandName):
    RM3Device = broadlink.rm((RealIPAddress, RealPort), RealMACAddress)
    RM3Device.auth()

    RM3Key = RM3Device.key
    RM3IV = RM3Device.iv

    RM3Device.enter_learning()
    time.sleep(RealTimeout)
    LearnedCommand = RM3Device.check_data()

    if LearnedCommand is None:
        print('Command not received')
        return False

    AdditionalData = bytearray([0x00, 0x00, 0x00, 0x00])    
    FinalCommand = AdditionalData + LearnedCommand

    AESEncryption = AES.new(str(RM3Key), AES.MODE_CBC, str(RM3IV))
    DecodedCommand = binascii.hexlify(AESEncryption.decrypt(str(FinalCommand)))

    BlackBeanControlIniFile = open(path.join(settings.ApplicationDir, 'settings.ini'), 'w')    
    SettingsFile.set('Commands', commandName, DecodedCommand)
    SettingsFile.write(BlackBeanControlIniFile)
    BlackBeanControlIniFile.close()

        
def start(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting broadlink-rest server on port %s ...' % port
    httpd.serve_forever()

if __name__ == "__main__":

    SettingsFile = configparser.ConfigParser()
    SettingsFile.optionxform = str
    SettingsFile.read(settings.BlackBeanControlSettings)

    commandName = ''
    DeviceName=''
    DeviceIPAddress = ''
    DevicePort = ''
    DeviceMACAddres = ''
    DeviceTimeout = ''
    AlternativeIPAddress = ''
    AlternativePort = ''
    AlternativeMACAddress = ''
    AlternativeTimeout = ''

    if (DeviceName.strip() != '') and ((AlternativeIPAddress.strip() != '') or (AlternativePort.strip() != '') or (AlternativeMACAddress.strip() != '') or (AlternativeTimeout != '')):
        print('Device name parameter can not be used in conjunction with IP Address/Port/MAC Address/Timeout parameters')
        sys.exit(2)

    if (((AlternativeIPAddress.strip() != '') or (AlternativePort.strip() != '') or (AlternativeMACAddress.strip() != '') or (AlternativeTimeout.strip() != '')) and ((AlternativeIPAddress.strip() == '') or (AlternativePort.strip() == '') or (AlternativeMACAddress.strip() == '') or (AlternativeTimeout.strip() == ''))):
        print('IP Address, Port, MAC Address and Timeout parameters can not be used separately')
        sys.exit(2)

    if DeviceName.strip() != '':
        if SettingsFile.has_section(DeviceName.strip()):
            if SettingsFile.has_option(DeviceName.strip(), 'IPAddress'):
                DeviceIPAddress = SettingsFile.get(DeviceName.strip(), 'IPAddress')
            else:
                DeviceIPAddress = ''

            if SettingsFile.has_option(DeviceName.strip(), 'Port'):
                DevicePort = SettingsFile.get(DeviceName.strip(), 'Port')
            else:
                DevicePort = ''

            if SettingsFile.has_option(DeviceName.strip(), 'MACAddress'):
                DeviceMACAddress = SettingsFile.get(DeviceName.strip(), 'MACAddress')
            else:
                DeviceMACAddress = ''

            if SettingsFile.has_option(DeviceName.strip(), 'Timeout'):
                DeviceTimeout = SettingsFile.get(DeviceName.strip(), 'Timeout')
            else:
                DeviceTimeout = ''        
        else:
            print('Device does not exist in settings.ini')
            sys.exit(2)

    if (DeviceName.strip() != '') and (DeviceIPAddress.strip() == ''):
        print('IP address must exist in settings.ini for the selected device')
        sys.exit(2)

    if (DeviceName.strip() != '') and (DevicePort.strip() == ''):
        print('Port must exist in settings.ini for the selected device')
        sys.exit(2)

    if (DeviceName.strip() != '') and (DeviceMACAddress.strip() == ''):
        print('MAC address must exist in settings.ini for the selected device')
        sys.exit(2)

    if (DeviceName.strip() != '') and (DeviceTimeout.strip() == ''):
        print('Timeout must exist in settings.ini for the selected device')
        sys.exit(2)    

    RealIPAddress = settings.IPAddress
    if RealIPAddress.strip() == '':
        print('IP address must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)

    RealPort = settings.Port
    if RealPort.strip() == '':
        print('Port must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        RealPort = int(RealPort.strip())

    RealMACAddress = settings.MACAddress
    if RealMACAddress.strip() == '':
        print('MAC address must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        RealMACAddress = netaddr.EUI(RealMACAddress)

    RealTimeout = settings.Timeout
    if RealTimeout.strip() == '':
        print('Timeout must exist in settings.ini or it should be entered as a command line parameter')
        sys.exit(2)
    else:
        RealTimeout = int(RealTimeout.strip())    

    start()