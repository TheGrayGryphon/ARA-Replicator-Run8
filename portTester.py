import argparse
import serial
import serial.tools.list_ports
import time

parser = argparse.ArgumentParser(description='Python script to serve as miniRD daemon',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-p', '--port', help='Serial (COM) port the MiniRD is connected to (optional). \n'
                                         'If left blank, this tool will poll all available serial ports.',
                    default=None, type=str)
parser.add_argument('-v', '--verbosity', help=f'Verbosity level 0 (silent) to 3 (most verbose).',
                    type=int, default=0)
args = parser.parse_args()
valid_port = args.port
verbosity = args.verbosity

retries = 0
s_port = serial.Serial(port=valid_port, baudrate=9600, timeout=5)
print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Serial port object opened: {s_port}')
print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Sending "I" request for ID')
s_port.write(b'I\r\n')
in_line = s_port.readline()
while len(in_line) < 1:
    print(f'[{time.strftime("%H:%M:%S", time.localtime())}] no response - backing off [{retries}]')
    time.sleep(1)
    retries += 1
    #print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Sending "I" request for ID')
    #s_port.write(b'I\r\n')
    in_line = s_port.readline()
# Successful response
print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Raw response: {in_line}')
print(f'[{time.strftime("%H:%M:%S", time.localtime())}] ASCII response: {in_line.strip().decode("utf-8").split(",")}')
print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Sending "r" request for control read')

while True:
    retries = 0
    s_port.write(b'r\r\n')
    in_line = s_port.readline()
    while len(in_line) < 1:
        print(f'[{time.strftime("%H:%M:%S", time.localtime())}] no response - backing off [{retries}]')
        time.sleep(1)
        retries += 1
        #print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Sending "r" request for control read')
        #s_port.write(b'r\r\n')
        in_line = s_port.readline()
    print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Raw response: {in_line}')
    print(f'[{time.strftime("%H:%M:%S", time.localtime())}] ASCII response: {in_line.strip().decode("utf-8").split(",")}')
    print(f'[{time.strftime("%H:%M:%S", time.localtime())}] Sending "r" request for control read')
