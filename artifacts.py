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
    ['evtl_xp', LOC_WINEVT + u'AppEvent.evt', u'/OSLogs/'],
    ['evtl_xp', LOC_WINEVT + u'SecEvent.evt', u'/OSLogs/'],
    ['evtl_xp', LOC_WINEVT + u'SysEvent.evt', u'/OSLogs/'],
    ['setupapi', u'/Windows/Inf/setupapi.dev.log', u'/Registry/'],
    ['setupapi_xp', u'/Windows/setupapi.log', u'/Registry/'],

    # mru
    ['amcache', LOC_AMCACHE + u'RecentFileCache.bcf', u'/MRU/Prog/recentfilecache/'],

    # persistence
    ['sch_xp', u'/Windows/SchedLgU.txt', u'/Autoruns/sch_tsks/'],

    # file system
    ['logfile', u'/$LogFile', u'/Filesystem/'],
    ['mft', u'/$MFT', u'/Filesystem/'],

    # others
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

    # others
    ['recycle', u'/$Recycle.Bin', u'/Recycle/', True, None],
    ['recycle_xp', u'/RECYCLER', u'/Recycle/', True, None],
    ['sig_ctlg', u'/Windows/System32/CatRoot', u'/Signatures/', True, None],
    ['wer', u'/ProgramData/Microsoft/Windows/WER', u'/MRU/Prog/wer/', True, None]
]

USER_FILE = [  # [artifact, src_path, dest_dir]
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
    ['rdpcache', u'/AppData/Local/Microsoft/Terminal Server Client/Cache', u'/MRU/rdpcache/', False, None],
    ['rdpcache_xp', u'/Local Settings/Application Data/Microsoft/Terminal Server Client/Cache', u'/MRU/rdpcache/',
     False, None]
]

FILE_ADS = [  # [artifact, src_path, dest_dir, ads_name]
    # file system
    ['usnjrnl', u'/$Extend/$UsnJrnl', u'/Filesystem/', u'$J']
]
