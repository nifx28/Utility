#!/usr/bin/env python3
# coding: utf-8
import sys
from urllib.request import *
from shutil import *
from base64 import *
from hashlib import *

class Integrity:
    @classmethod
    def parse(cls, hash, file=None, url=None):
        alg = None

        if hash[:7] == 'sha256-' or hash[:7] == 'sha384-' or hash[:7] == 'sha512-':
            alg = hash[3:6]
            hash = b64decode(hash[7:]).hex()

            if file and url:
                with urlopen(url) as r, open(file, 'wb') as bf:
                    copyfileobj(r, bf)
        else:
            alg = '256' if len(hash) == 64 else alg
            alg = '384' if len(hash) == 96 else alg
            alg = '512' if len(hash) == 128 else alg

            if not file:
                hash = b64encode(bytes.fromhex(hash)).decode('ascii')

        if file:
            m = None
            m = sha256() if alg == '256' else m
            m = sha384() if alg == '384' else m
            m = sha512() if alg == '512' else m

            with open(file, 'rb') as bf:
                while True:
                    buf = bf.read(1024)

                    if buf:
                        m.update(buf)
                    else:
                        break

            m = m.hexdigest()

            if m == hash:
                print('sha{}-{}'.format(alg, m))
            else:
                print('Base64: {}'.format(b64encode(bytes.fromhex(m)).decode('ascii')))
                print('SHA{}: {}'.format(alg, m))
        else:
            print('sha{}-{}'.format(alg, hash))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        Integrity.parse(sys.argv[1])
    elif len(sys.argv) == 3:
        Integrity.parse(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        Integrity.parse(sys.argv[1], sys.argv[2], sys.argv[3])
