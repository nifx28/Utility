#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, sys, os, re
from datetime import date
from operator import itemgetter
from getpass import getpass

class Cfg:
    def __init__(self, props): # 初始化配置變數。
        for k, v in props.iteritems():
            self.__dict__[k] = v

    def __setattr__(self, *_): pass # 配置變數為常數。

    def __str__(self): # 列出配置變數。
        str = []

        for k, v in self.__dict__.iteritems():
            qstr = '"' if isinstance(v, basestring) else '' # 字串配置變數加上雙引號。
            str.append('"%s" = %s%s%s' % (k, qstr, v, qstr))

        return os.linesep.join(str)

argv0 = os.path.abspath(__file__)

cfg = Cfg({ # 配置變數預設值。
    'logFile':		'%s\SpaceEngineers.log' % os.path.dirname(argv0),
    'serverPath':	'%s\SpaceEngineersDedicated\Mods' % os.getenv('APPDATA'),
    'clientPath':	'%s\SpaceEngineers\Mods' % os.getenv('APPDATA'),
    'gameLogFile':	'%s\SpaceEngineers\SpaceEngineers.log' % os.getenv('APPDATA'),
    'wsURI':		'http://steamcommunity.com/sharedfiles/filedetails/?id=%s',
    'batchFile':	'%s\%s.cmd' % (os.path.dirname(argv0), os.path.splitext(os.path.basename(argv0))[0])
})

class Mods:
    def __init__(self):
        self.f = []
        self.mod = []

        try:
            self.f.append(open(cfg.logFile, 'w'))		# 擷取出來的記錄檔。
            self.f.append(open(cfg.gameLogFile, 'rU'))	# 太空工程師遊戲記錄檔。
        except IOError as e:
            print '%s: %s' % (e.strerror, e.filename)

    def __del__(self):
        for f in self.f:
            if f:
                f.close() # 關閉檔案。

    def get(self): # 取得 Mod 資訊。
        if self.f[1]:
            for line in iter(self.f[1].readline, ''): # 讀出每一行記錄。
                kvd = self.parse(line)

                if kvd:
                    self.mod.append(kvd)

            return self.mod

    def parse(self, line): # 剖析記錄檔。
        m = re.match(r'^.+ Obtained details: (.+)', line) # 比對特徵。

        if not m or len(m.groups()) < 1:
            return
        else:
            if self.f[0]:
                self.f[0].write(line) # 列出比對到的行。

        s = m.group(1).split('; ', 4) # 取出欄位。

        if len(s) < 4:
            return

        kvd = {}

        for kv in s:
            kvs = kv.split('=', 2)

            if len(kvs) == 2:
                kvd[kvs[0]] = kvs[1] # 設定欄位變數值。

        return kvd

class Cli: # 命令列功能。
    def pause(self): # 若使用捷徑執行則暫停。
        for mod in mods:
            print '\'%s\': %s' % (mod['Id'], mod['title'])

        sys.stdout.write(u'請按任意鍵繼續 . . . ')
        sys.stdout.flush()
        getpass('')

    def notes(self, showDesc=False): # 產生網頁超連結。
        link = '<a href="' + cfg.wsURI + '">%s</a>'
        desc = ' %s Mod category: %s'
        str = []

        for mod in mods:
            t1 = mod['title']
            m = re.match(r'^\'(.+)\'$', t1) # 比對特徵。

            if m and len(m.groups()) == 1:
                t1 = m.group(1) # 去掉單引號。

            if showDesc: # 新增 Mod 描述。
                t2 = ''
                t3 = mod['tags']
                m = re.match(r'^\'(.+)\'$', t3)

                if m and len(m.groups()) == 1:
                    t3 = m.group(1)

                t3 = t3.split(',')
                ti = 0

                for t in t3:
                    if t == 'mod':
                        t2 = 'Type: Mod.'
                        break

                    ti += 1

                if len(t2) > 0:
                    del t3[ti]

                t3 = ', '.join(t3)
                str.append((link + desc) % (mod['Id'], t1, t2, t3))
            else:
                str.append(link % (mod['Id'], t1))

        return str

    def notesFB(self, showDesc=False): # 產生臉書網誌。
        print u'''\
伺服器安裝MOD表({:%m/%d})

使用 Python v{ver.major}.{ver.minor} 程式 <a href="https://github.com/nifx28/Utility/blob/master/SpaceEngineers/Mods.py">Mods.py</a> 讀取 <b>C:\\Users\\使用者\\AppData\\Roaming\\SpaceEngineers\\SpaceEngineers.log</b> 產生。

Workshop 列表：

{!s}

伺服器 Mods 輸入欄位：

{!s}
'''.format(date.today(), os.linesep.join(self.notes(showDesc)), os.linesep.join(self.get()), ver=sys.version_info)

    def batch(self, src=cfg.clientPath, dst=cfg.serverPath): # 產生 Mods 資料夾同步批次檔。
        try:
            f = open(cfg.batchFile, 'w')
        except IOError as e:
            print '%s: %s' % (e.strerror, e.filename)

        if f:
            f.write('''\
@echo off
title Space Engineers (%d)
''' % len(mods))

            for mod in mods:
                f.write('copy /v /y /b "%s\%s.sbm" "%s"\n' % (src, mod['Id'], dst))

            f.close()

    def get(self): # 伺服器 Mods 輸入欄位。
        str = []

        for mod in mods:
            str.append(mod['Id'])

        return str

if (__name__ == '__main__'): # 從命令列執行。
    pause = False
    notes = False
    notesFB = False
    notesDesc = False
    batch = False
    batchSrc = None
    batchDst = None

    if len(sys.argv) > 1:
        if sys.argv[1] == 'version': # 顯示版本。
            print 'Python v%s' % platform.python_version()
        elif sys.argv[1] == 'showcfg': # 列出配置變數。
            print cfg

        if sys.argv[1] == 'pause': # 若使用捷徑執行則暫停。
            pause = True
        elif sys.argv[1] == 'notes': # 產生網頁超連結。
            notes = True
        elif sys.argv[1] == 'facebook': # 產生臉書網誌。
            notesFB = True
        elif sys.argv[1] == 'batch': # 產生 Mods 資料夾同步批次檔。
            batch = True
        else:
            sys.exit() # 資訊顯示。

    if len(sys.argv) > 2:
        if (notes or notesFB) and sys.argv[2] == 'yes': # 新增 Mod 描述。
            notesDesc = True
        elif batch: # Mods 資料夾同步來源。
            batchSrc = sys.argv[2]

    if len(sys.argv) > 3:
        if batch: # Mods 資料夾同步目的。
            batchDst = sys.argv[3]

    mods = Mods().get() # 從遊戲紀錄檔取得 Mod 列表。
    mods.sort(cmp = lambda a, b: cmp(int(a['Id']), int(b['Id']))) # 排序 Mod 列表，Id 由小到大。
    cli = Cli() # 命令列功能。

    if pause:
        cli.pause()										# Mods.py pause
    elif notes:
        print os.linesep.join(cli.notes(notesDesc))		# Mods.py notes [yes]
    elif notesFB:
        cli.notesFB(notesDesc)							# Mods.py facebook [yes]
    elif batch:
        if batchSrc and batchDst:
            cli.batch(batchSrc, batchDst)				# Mods.py batch [src] [dst]
        else:
            cli.batch()									# Mods.py batch
    else:
        print os.linesep.join(cli.get())				# Mods.py
