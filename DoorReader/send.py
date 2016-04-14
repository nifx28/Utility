#!/usr/bin/env python3
import sys, platform, socket

class Socket:
    def __init__(self, host, port):
        print('Python {}'.format(platform.python_version()))
        self.soc = None
        self.host = host
        self.port = port

    def __del__(self):
        if self.soc:
            self.soc.close()

    def Connect(self):
        if self.soc:
            self.soc.close()

        print('Connect to {}:{} ...'.format(self.host, self.port))
        self.soc = socket.socket();
        self.soc.connect((self.host, int(self.port)))

    def Send(self, hex):
        if self.soc:
            print('Send: {}'.format(hex))
            payload = bytes.fromhex(hex)
            print('Decode: {}'.format(payload.decode(errors='ignore')))

    def Recv(self, bits):
        if self.soc:
            print('Recv: {}'.format(self.soc.recv(bits)))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        soc = Socket(sys.argv[1], sys.argv[2])
        soc.Connect()
        seq = [0x7E, 0x04, 0x01, 0x18, 0x00]
        seq.append(0xFF ^ seq[2] ^ 0x18)
        seq.append(seq[2] + seq[3] + seq[-1])
        soc.Send(''.join('{:02X} '.format(b) for b in seq))
        soc.Recv(1024)
    else:
        sys.exit(1)
