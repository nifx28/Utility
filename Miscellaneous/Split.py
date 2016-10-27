#!/usr/bin/env python3
# coding: utf-8
import sys, os
from PIL import Image

class Split:
    def __init__(self, height, file):
        self.height = height
        self.file = file

    def proc(self):
        try:
            height = int(self.height)
        except ValueError:
            return

        name, ext = os.path.splitext(self.file)

        img = Image.open(self.file)
        w = img.width;
        h = img.height;
        crop = int(h / height)
        last = h - crop * height
        total = crop + (1 if last > 0 else 0)

        print('Image Size: {} x {}'.format(w, h))
        print('Crop At: {} * {} + {}\n'.format(height, crop, last))

        for i in range(total):
            num = i + 1
            pos = i * height
            print('{:>3}: {:>6} x {:>6}'.format(num, w, height if i < crop else last), end='')
            print('    Box: [{:>6}, {:>6}, {:>6}, {:>6}]'.format(0, pos, w, pos + (height if i < crop else last)))
            raster = Image.new('RGBA', (w, height if i < crop else last))
            raster.paste(img.crop((0, pos, w, pos + (height if i < crop else last))))
            raster.save('{}{}{}'.format(name, num, ext), ext[1:])

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Split(sys.argv[1], sys.argv[2]).proc()
