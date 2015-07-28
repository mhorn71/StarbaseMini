__author__ = 'mark'

import utilities

message = b'8001'

response = utilities.staribus_status_b2str(message)
status_message = utilities.staribus_status_str2b('TIMEOUT')

print('Staribus Bytes to String : ' + response)
print('Staribus String to Bytes : ' + repr(status_message))

try:
    rgbcolour = utilities.hex2rgb('#FFFFFF')
    hexcolour = utilities.rgb2hex((255, 255, 255))
except ValueError as msg:
    print(msg)
else:
    print('Hex Colour to RGB : ' + repr(rgbcolour))
    print('RGB Colour to Hex : ' + repr(hexcolour))

if utilities.check_starinet_port('1205'):
    print('Starinet Port : valid')
else:
    print('Starinet Port : invalid')

if utilities.check_ip('192.168.1.1'):
    print('Starinet Address : valid')
else:
    print('Starinet Address : invalid')

serial_port = utilities.serial_port_scanner()

if serial_port is not None:
    print('Serial port found : ' + str(serial_port))
else:
    print('No serial ports found')
