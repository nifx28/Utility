#!/usr/bin/env python3
# coding: utf-8
import sys, os, serial, csv

class GPSParser:
    def __init__(self, log, port='COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE): # 9600,8,N,1
        self.log = log
        self.com = serial.Serial(port, baudrate, bytesize, parity, stopbits)
        print('Serial port: {} ({},{},{},{})'.format(self.com.name, baudrate, bytesize, parity, stopbits))
        self.gga = 0
        self.gsa = 0
        self.gsv = 0
        self.rmc = 0
        self.vtg = 0

    def __del__(self):
        if self.com:
            self.com.close()

    def start(self, amount=5):
        name, ext = os.path.splitext(self.log)

        with open(name + ext, 'w') as logOut:
            logOut.write('{\n')

            for i in range(amount):
                print('.', end='')
                line = []

                for c in self.com.readline():
                    if c > 31 and c < 127:
                        line.append(chr(c))
                    elif c != 10 and c != 13:
                        line.append('%{:02X}'.format(c))

                key = ''.join(line).replace('"', '\\"')
                logOut.write('\t"{}": [\n'.format(key))

                if len(key) > 0:
                    logOut.write('{}{}\n'.format(self.proc(line), ',' if i + 1 < amount else ''))

            logOut.write('}\n')

        print('\nGGA: {}, GSA: {}, GSV: {}, RMC: {}, VTG: {}'.format(self.gga, self.gsa, self.gsv, self.rmc, self.vtg))

    def proc(self, line):
        data = csv.reader(line, quoting=csv.QUOTE_NONE)
        list = []

        for row in data:
            list.append('\n'.join(row))

        list = ''.join(list).split('\n')
        listLen = len(list)
        fields = []

        for i in range(listLen):
            fields.append('\t\t"{}"{}\n'.format(list[i], ',' if i + 1 < listLen else ''))

            if i == 0:
                if list[i] == '$GPGGA':
                    self.gga += 1
                elif list[i] == '$GPGSA':
                    self.gsa += 1
                elif list[i] == '$GPGSV':
                    self.gsv += 1
                elif list[i] == '$GPRMC':
                    self.rmc += 1
                elif list[i] == '$GPVTG':
                    self.vtg += 1

        return '{}\t]'.format(''.join(fields))

if __name__ == '__main__':
    gps = None

    if len(sys.argv) > 1:
        gps = GPSParser(sys.argv[1])

    if gps and len(sys.argv) > 2:
        gps.start(int(sys.argv[2]))
    else:
        gps.start()
