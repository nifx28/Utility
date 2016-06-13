#!/usr/bin/env python3
# coding: utf-8
import sys, os
from array import *

class Serialize:
    @classmethod
    def parse(cls, txt):
        name, ext = os.path.splitext(txt)

        with open(name + '_tmp' + ext, 'wb') as binOut:
            count = 0

            with open(txt, 'r') as txtIn:
                for line in txtIn:
                    line = line.rstrip('\n')
                    arr = array('B')
                    arr.append(len(line))
                    arr.tofile(binOut)
                    binOut.write(bytearray(line, 'utf-8'))
                    arr = array('B')
                    arr.append(0)
                    arr.tofile(binOut)
                    count += 1

        with open(name + '_bin' + ext, 'wb') as binOut:
            arr = array('B')
            arr.append(count)
            arr.append(0)
            arr.tofile(binOut)

            with open(name + '_tmp' + ext, 'rb') as binIn:
                while True:
                    chunk = binIn.read(1024)

                    if chunk:
                        binOut.write(chunk)
                    else:
                        break

        os.remove(name + '_tmp' + ext)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        Serialize.parse(sys.argv[1])
