import configparser
import netaddr
from os import path
from collections import defaultdict

applicationDir = path.dirname(path.abspath(__file__))
settingsINI = path.join(applicationDir, 'settings.ini')

settings = configparser.ConfigParser()
settings.read(settingsINI)

if settings.has_option('General', 'Timeout'):
    Timeout = settings.get('General', 'Timeout')
else:
    Timeout = 5

DevList = []
Dev = defaultdict(dict)
for section in settings.sections():
    if section == 'General' or 'Commands' in section or 'Status' in section:
        continue
    print ("Reading device configuration for %s" % section)
    Dev[section,'IPAddress'] = settings.get(section,'IPAddress').strip()
    Dev[section,'MACAddress'] = netaddr.EUI(settings.get(section, 'MACAddress'))
    if settings.has_option(section,'Timeout'):
        Dev[section,'Timeout'] = int(settings.get(section, 'Timeout').strip())
    else:
        Dev[section,'Timeout'] = 8
    if settings.has_option(section,'Device'):
        Dev[section,'Device'] = int(settings.get(section, 'Device').strip(),16)
    else:
        Dev[section,'Device'] = None
    if settings.has_option(section,'Type'):
        Dev[section,'Type'] = settings.get(section,'Type').strip()
    else:
        Dev[section,'Type'] = section.strip()[-2:]
    DevList.append(section.strip())

