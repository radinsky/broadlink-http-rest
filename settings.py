import configparser
from os import path

applicationDir = path.dirname(path.abspath(__file__))
BlackBeanControlSettings = path.join(applicationDir, 'settings.ini')

settings = configparser.ConfigParser()
settings.read(BlackBeanControlSettings)

IPAddress = settings.get('General', 'IPAddress')
Port = settings.get('General', 'Port')
MACAddress = settings.get('General', 'MACAddress')
Timeout = settings.get('General', 'Timeout')
