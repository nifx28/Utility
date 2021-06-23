#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, msvcrt, ctypes, codecs

class Reveal:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.f = open(self.filename, 'r')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.f:
            del self.f

    def run(self):
        print('輸入檔案： "{}"\n'.format(self.filename))

        if self.f:
            i = 0

            for line in self.f:
                i += 1
                print('{0: >2}. {1}'.format(i, line.strip()))

            self.f.seek(0)
            print('\n文字轉碼 \'{}\' => \'{}\'\n'.format('mbcs', 'gb2312'))
            i = 0

            for line in self.f:
                i += 1
                print('{0: >2}. {1}'.format(i,
                    codecs.decode(
                        line.strip().encode('mbcs'),
                        encoding='gb2312')))

            print()

if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW(sys.implementation.name + ' ' + sys.version)

    with Reveal('中国語.txt') as r:
        r.run()

    print('請按任意鍵繼續 . . . ', end='', flush=True)
    msvcrt.getch()
