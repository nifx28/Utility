#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, sys, os, re
from operator import itemgetter
from getpass import getpass

class Cfg:
    def __init__(self, props):
        for k, v in props.iteritems():
            self.__dict__[k] = v

    def __setattr__(self, *_): pass

    def __str__(self):
        str = []
        for k, v in self.__dict__.iteritems():
            qstr = '"' if isinstance(v, basestring) else ''
            str.append('"%s" = %s%s%s' % (k, qstr, v, qstr))
        return os.linesep.join(str)

cfg = Cfg({
    'logFile':	'%s\SpaceEngineers\SpaceEngineers.log' % os.getenv('APPDATA'),
    'wsURI':	'http://steamcommunity.com/sharedfiles/filedetails/?id=%s'
})

class Mods:
    def __init__(self):
        self.mod = []

        try:
            self.f = open(cfg.logFile, 'rU')
        except IOError as e:
            print '%s: %s' % (e.strerror, e.filename)

    def __del__(self):
        if self.f:
            self.f.close()

    def get(self):
        if self.f:
            for line in iter(self.f.readline, ''):
                kvd = self.parse(line)

                if kvd:
                    self.mod.append(kvd)

            return self.mod

    def parse(self, line):
        m = re.match(r'^.+ Obtained details: (.+)', line)

        if not m or len(m.groups()) < 1:
            return

        s = m.group(1).split('; ', 4)

        if len(s) < 4:
            return

        kvd = {}

        for kv in s:
            kvs = kv.split('=', 2)
            if len(kvs) == 2:
                kvd[kvs[0]] = kvs[1]

        return kvd

if (__name__ == '__main__'):
    pause = False
    notes = False

    if len(sys.argv) > 1:
        if sys.argv[1] == 'version':
            print 'Python v%s' % platform.python_version()
        elif sys.argv[1] == 'showcfg':
            print cfg

        if sys.argv[1] == 'pause':
            pause = True
        elif sys.argv[1] == 'notes':
            notes = True
        else:
            sys.exit()

    mods = Mods().get()
    mods.sort(cmp = lambda a, b: cmp(int(a['Id']), int(b['Id'])))

    if pause:
        for mod in mods:
            print '\'%s\': %s' % (mod['Id'], mod['title'])

        sys.stdout.write(u'請按任意鍵繼續 . . . ')
        sys.stdout.flush()
        getpass('')
    elif notes:
        link = '<a href="' + cfg.wsURI + '">%s</a> %s Mod category: %s'

        for mod in mods:
            t1 = mod['title']
            m = re.match(r'^\'(.+)\'$', t1)

            if m and len(m.groups()) == 1:
                t1 = m.group(1)

            t2 = ''
            t3 = mod['tags']
            m = re.match(r'^\'(.+)\'$', t3)

            if m and len(m.groups()) == 1:
                t3 = m.group(1)

            t3 = t3.split(',')
            ti = 0

            for t in t3:
                if t == 'mod':
                    t2 = 'Type: Mod,'
                    break

                ti += 1

            if len(t2) > 0:
                del t3[ti]

            t3 = ', '.join(t3)
            print link % (mod['Id'], t1, t2, t3)
    else:
        for mod in mods:
            print mod['Id']
