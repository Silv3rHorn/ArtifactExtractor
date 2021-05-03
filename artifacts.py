LOC_RECENT = u'/AppData/Roaming/Microsoft/Windows/Recent/'
LOC_REG = u'/Windows/System32/config/'
LOC_WINEVT = LOC_REG
LOC_WINEVTX = u'/Windows/System32/winevt/logs/'
LOC_AMCACHE = u'/Windows/AppCompat/Programs/'

SYSTEM_FILE = [  # [artifact, src_path, dest_dir]
    # registry hives
    ['regb', LOC_REG + u'RegBack/SAM', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SECURITY', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SOFTWARE', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SYSTEM', u'/Registry/RegBack/'],
    ['regb_xp', LOC_REG + u'Repair/SAM', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/SECURITY', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/software', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/system', u'/Registry/Repair/'],

    # system logs
    ['evtl_xp', LOC_WINEVT + u'AppEvent.evt', u'/OSLogs/evtl/'],
    ['evtl_xp', LOC_WINEVT + u'SecEvent.evt', u'/OSLogs/evtl'],
    ['evtl_xp', LOC_WINEVT + u'SysEvent.evt', u'/OSLogs/evtl'],
    ['setupapi', u'/Windows/Inf/setupapi.dev.log', u'/Registry/'],
    ['setupapi_xp', u'/Windows/setupapi.log', u'/Registry/'],

    # mru
    ['amcache', LOC_AMCACHE + u'RecentFileCache.bcf', u'/MRU/Prog/recentfilecache/'],

    # persistence
    ['sch_xp', u'/Windows/SchedLgU.txt', u'/Autoruns/sch_tsks/'],

    # etl
    ['etl', u'/ProgramData/Microsoft/Windows/Power Efficiency Diagnostics/energy-ntkl.etl', u'/Misc/etl/'],
    ['etl', u'/ProgramData/Microsoft/Windows/Power Efficiency Diagnostics/energy-trace.etl', u'/Misc/etl/'],
    ['etl', u'/Windows/System32/LogFiles/WMI/LwtNetLog.etl', u'/Misc/etl/'],
    ['etl', u'/Windows/System32/LogFiles/WMI/Wifi.etl', u'/Misc/etl/'],

    # file system
    ['logfile', u'/$LogFile', u'/Filesystem/'],
    ['mft', u'/$MFT', u'/Filesystem/'],

    # others
    ['bits', u'/ProgramData/Microsoft/Network/Downloader/qmgr.dat', u'/Misc/bits/'],
    ['pagefile', u'/pagefile.sys', u'/Memory/pagefile/']
]

SYSTEM_DIR = [  # [artifact, src_path, dest_dir, isRecursive, stringToMatch]
    # registry hives
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SAM'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SECURITY'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SOFTWARE'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SYSTEM'],

    # system logs
    ['antimalware', u'/ProgramData/Microsoft/Microsoft Antimalware/Support', u'/Virus Scans/', False, u'MPLog'],
    ['defender', u'/ProgramData/Microsoft/Windows Defender/Support', u'/Virus Scans/', False, u'MPLog'],
    ['evtl', LOC_WINEVTX[:-1], u'/OSLogs/evtl', False, None],
    ['ual', u'/Windows/System32/LogFiles/SUM', u'/OSLogs/ual', False, u'.mdb'],

    # mru
    ['amcache', LOC_AMCACHE[:-1], u'/MRU/Prog/amcache/', False, u'Amcache'],
    ['prefetch', u'/Windows/Prefetch', u'/MRU/Prog/prefetch/', False, u'.pf'],
    ['sccm', u'/Windows/System32/wbem/Repository', u'/MRU/Prog/sccm/', False, None],
    ['srum', u'/Windows/System32/sru', u'/MRU/Prog/srum/', False, None],
    ['sqm', u'/ProgramData/Microsoft/Windows/Sqm/Upload', u'/MRU/Prog/sqm/', False, u'.sqm'],
    ['syscache', u'/System Volume Information', u'/MRU/Prog/syscache/', False, u'Syscache'],

    # persistence
    ['sch_job', u'/Windows/Tasks', u'/Autoruns/sch_tsks/', False, u'.job'],
    ['sch_xml', u'/Windows/System32/Tasks', u'/Autoruns/sch_tsks/', True, None],
    ['startupinfo', u'/Windows/System32/wdi/LogFiles/StartupInfo', u'/Autoruns/startupinfo/', False, u'StartupInfo'],

    # etl
    ['etl', u'/Windows/System32/WDI/LogFiles', u'/Misc/etl/', False, u'.etl'],

    # others
    ['certutil', u'/Windows/System32/config/systemprofile/AppData/LocalLow/Microsoft/CryptnetUrlCache/MetaData',
     u'/Misc/certutil/', False, None],
    ['recycle', u'/$Recycle.Bin', u'/Recycle/', True, None],
    ['recycle_xp', u'/RECYCLER', u'/Recycle/', True, None],
    ['sig_ctlg', u'/Windows/System32/CatRoot', u'/Misc/signatures/', True, None],
    ['wer', u'/ProgramData/Microsoft/Windows/WER', u'/Misc/wer/', True, None]
]

USER_FILE = [  # [artifact, src_path, dest_dir]
    # etl
    ['etl', u'/AppData/Local/Microsoft/Windows/Explorer/ExplorerStartupLog.etl', u'/Misc/etl/'],
    ['etl', u'/AppData/Local/Microsoft/Windows/Explorer/ExplorerStartupLog_RunOnce.etl', u'/Misc/etl/'],
    ['etl', u'/AppData/Local/Packages/Microsoft.Windows.Cortana_cw5n1h2txyewy/TempState/Traces/CortanaTrace1.etl',
     u'/Misc/etl/'],

    # system logs
    ['pshist', u'/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt', u'/OSLogs/pshist/']
]

USER_DIR = [  # [artifact, src_path, dest_dir, isRecursive, stringToMatch]
    # registry hives
    ['ntuser', u'/', u'/Registry/', False, u'NTUSER'],
    ['usrclass', u'/AppData/Local/Microsoft/Windows/', u'/Registry/', False, u'UsrClass'],
    ['usrclass_xp', u'/Local Settings/Application Data/Microsoft/Windows/', u'/Registry/', False, u'UsrClass'],

    # mru
    ['iehist', u'/AppData/Local/Microsoft/Windows/WebCache', u'/MRU/Files/iehist/', False, None],
    ['iehist_xp', u'/Local Settings/History/History.IE5', u'/MRU/Files/iehist/', True, None],
    ['jmp', LOC_RECENT + u'AutomaticDestinations', u'/MRU/Files/jmp/', False, None],
    ['jmp', LOC_RECENT + u'CustomDestinations', u'/MRU/Files/jmp/', False, None],
    ['lnk', LOC_RECENT, u'MRU/Files/lnk', False, None],
    ['lnk_xp', u'/Recent/', u'MRU/Files/lnk', False, None],
    ['thumbcache', u'/AppData/Local/Microsoft/Windows/Explorer', u'/MRU/thumbcache/', False, u'thumbcache_'],
    ['timeline', u'/AppData/Local/ConnectedDevicesPlatform', u'/MRU/timeline/', True, None],

    # others
    ['certutil', u'/AppData/LocalLow/Microsoft/CryptnetUrlCache/MetaData', u'/Misc/certutil/', False, None],
    ['rdpcache', u'/AppData/Local/Microsoft/Terminal Server Client/Cache', u'/Misc/rdpcache/', False, None],
    ['rdpcache_xp', u'/Local Settings/Application Data/Microsoft/Terminal Server Client/Cache', u'/Misc/rdpcache/',
     False, None]
]

FILE_ADS = [  # [artifact, src_path, dest_dir, ads_name]
    # file system
    ['usnjrnl', u'/$Extend/$UsnJrnl', u'/Filesystem/', u'$J']
]
