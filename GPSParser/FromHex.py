#!/usr/bin/env python3
# coding: utf-8
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        line = bytes.fromhex(sys.argv[1]).decode('ascii', 'ignore')
        print(line)
        print(''.join('{:02X}'.format(ord(i)) for i in line))
