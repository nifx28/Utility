#!/usr/bin/env python
# coding: utf-8

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

        return '\n'.join(str)

argv0 = os.path.abspath(__file__)
dirname = os.path.dirname(argv0)
basename = os.path.splitext(os.path.basename(argv0))[0]
appdata = os.getenv('APPDATA')

cfg = Cfg({ # 配置變數預設值。
    'logFile':		r'%s\SpaceEngineers.log' % dirname,
    'serverPath':	r'%s\SpaceEngineersDedicated\Mods' % appdata,
    'clientPath':	r'%s\SpaceEngineers\Mods' % appdata,
    'gameLogFile':	r'%s\SpaceEngineers\SpaceEngineers.log' % appdata,
    'wsURI':		'http://steamcommunity.com/sharedfiles/filedetails/?id=%s',
    'batchFile':	r'%s\%s.cmd' % (dirname, basename)
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

class ModsId:
    def __init__(self, syncDate):
        self.f = None
        self.mod = []

        try:
            self.f = open(r'%s\%s.log' % (dirname, syncDate), 'r') # Id 紀錄檔。
        except IOError as e:
            print '%s: %s' % (e.strerror, e.filename)

    def __del__(self):
        if self.f:
            self.f.close() # 關閉檔案。

    def get(self): # 取得 Mod 資訊。
        if self.f:
            for line in iter(self.f.readline, ''): # 讀出每一行記錄。
                self.mod.append({'Id': line[:-1]}) # 設定欄位變數值。

            return self.mod

class Cli: # 命令列功能。
    @staticmethod
    def verbose(): # 若使用捷徑執行則暫停。
        for mod in mods:
            print ('\'%s\': %s' % (mod['Id'], mod['title'])).decode('utf-8')

        sys.stdout.write(u'請按任意鍵繼續 . . . ') # 已知問題：Unicode 輸出，重新導向會異常。
        sys.stdout.flush()
        getpass('')

    @staticmethod
    def notes(showDesc=False): # 產生網頁超連結。
        link = '%2d. <a href="' + cfg.wsURI + '">%s</a>'
        desc = ' %s Mod category: %s'
        str = []
        strN = 0

        for mod in mods:
            strN += 1
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
                str.append((link + desc) % (strN, mod['Id'], t1, t2, t3))
            else:
                str.append(link % (strN, mod['Id'], t1))

        return str

    @staticmethod
    def notesFB(showDesc=False): # 產生臉書網誌。
        print '''\
伺服器安裝MOD表({:%m/%d})

工作坊列表：

{!s}

伺服器 Mods 輸入欄位：

{!s}

此文件使用 Python v{ver.major}.{ver.minor} 程式 <a href="https://github.com/nifx28/Utility/blob/master/SpaceEngineers/Mods.py">Mods.py</a> 讀取 <b>C:\\Users\\使用者\\AppData\\Roaming\\SpaceEngineers\\SpaceEngineers.log</b> 產生。\
'''.format(date.today(), '\n'.join(Cli.notes(showDesc)), '\n'.join(Cli.get()), ver=sys.version_info)

    @staticmethod
    def batch(src=cfg.clientPath, dst=cfg.serverPath): # 產生 Mods 資料夾同步批次檔。
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

    @staticmethod
    def get(): # 伺服器 Mods 輸入欄位。
        str = []

        for mod in mods:
            str.append(mod['Id'])

        return str

if (__name__ == '__main__'): # 從命令列執行。
    verbose = False
    notes = False
    notesFB = False
    notesDesc = False
    batch = False
    batchSrc = None
    batchDst = None
    sync = False
    syncDate = None

    if len(sys.argv) > 1:
        if sys.argv[1] == 'usage': # 顯示使用說明。
            print 'Mods.py [verbose|usage|help|version|cfg|notes|facebook|batch|sync] args...'
        elif sys.argv[1] == 'help': # 顯示求助說明。
            print '''\
Mods.py
Mods.py verbose
Mods.py usage
Mods.py help
Mods.py version
Mods.py cfg
Mods.py > {0}.log
Mods.py notes yes > {0}_notes.log
Mods.py facebook yes > {0}_facebook.log
Mods.py batch
Mods.py sync {0}\
'''.format(date.today())
        elif sys.argv[1] == 'version': # 顯示版本。
            print 'Python v%s' % platform.python_version()
        elif sys.argv[1] == 'cfg': # 列出配置變數。
            print cfg

        if sys.argv[1] == 'verbose': # 若使用捷徑執行則暫停。
            verbose = True
        elif sys.argv[1] == 'notes': # 產生網頁超連結。
            notes = True
        elif sys.argv[1] == 'facebook': # 產生臉書網誌。
            notesFB = True
        elif sys.argv[1] == 'batch': # 產生 Mods 資料夾同步批次檔。
            batch = True
        elif sys.argv[1] == 'sync': # 產生 Mods 資料夾同步批次檔。
            batch = True
            sync = True
        else:
            sys.exit() # 資訊顯示。

    if len(sys.argv) > 2:
        if (notes or notesFB) and sys.argv[2] == 'yes': # 新增 Mod 描述。
            notesDesc = True
        elif sync: # Id 紀錄檔來源。
            syncDate = sys.argv[2]
        elif batch: # Mods 資料夾同步來源。
            batchSrc = sys.argv[2]

    if sync and not syncDate:
        sys.exit() # 未指定同步日期。

    if len(sys.argv) > 3:
        if sync: # Mods 資料夾同步來源。
            batchSrc = sys.argv[3]
        elif batch: # Mods 資料夾同步目的。
            batchDst = sys.argv[3]

    if len(sys.argv) > 4:
        if sync: # Mods 資料夾同步目的。
            batchDst = sys.argv[4]

    if not sync:
        mods = Mods().get() # 從遊戲紀錄檔取得 Mod 列表。
        mods.sort(cmp = lambda a, b: cmp(int(a['Id']), int(b['Id']))) # 排序 Mod 列表，Id 由小到大。
    else:
        mods = ModsId(syncDate).get() # 從 Id 紀錄檔取得 Mod 列表。

    if verbose:
        Cli.verbose()							# Mods.py verbose
    elif notes:
        print '\n'.join(Cli.notes(notesDesc))	# Mods.py notes [yes]
    elif notesFB:
        Cli.notesFB(notesDesc)					# Mods.py facebook [yes]
    elif batch:
        if batchSrc and batchDst:
            Cli.batch(batchSrc, batchDst)		# Mods.py {batch|sync} [src] [dst]
        else:
            Cli.batch()							# Mods.py {batch|sync}
    else:
        print '\n'.join(Cli.get())				# Mods.py
