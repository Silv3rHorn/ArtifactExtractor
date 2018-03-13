LOC_REG = u'/Windows/System32/config/'
LOC_WINEVT = LOC_REG
LOC_WINEVTX = u'/Windows/System32/winevt/logs/'
LOC_AMCACHE = u'/Windows/AppCompat/Programs/'
LOC_RECENT = u'/AppData/Roaming/Microsoft/Windows/Recent/'

SYSTEM_FILE = [  # [artifact, src_path, dest_dir]
    ['regb', LOC_REG + u'RegBack/SAM', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SECURITY', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SOFTWARE', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SYSTEM', u'/Registry/RegBack/'],

    ['regb_xp', LOC_REG + u'Repair/SAM', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/SECURITY', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/software', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/system', u'/Registry/Repair/'],

    ['evtl', LOC_WINEVTX + u'Application.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Security.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Setup.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'System.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-PowerShell%4Operational.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-TaskScheduler%4Operational.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx', u'/OSLogs/'],
    ['evtl', LOC_WINEVTX + u'Microsoft-Windows-Windows Firewall With Advanced Security%4Firewall.evtx', u'/OSLogs/'],

    ['evtl_xp', LOC_WINEVT + u'AppEvent.evt', u'/OSLogs/'],
    ['evtl_xp', LOC_WINEVT + u'SecEvent.evt', u'/OSLogs/'],
    ['evtl_xp', LOC_WINEVT + u'SysEvent.evt', u'/OSLogs/'],

    ['amcache', LOC_AMCACHE + u'RecentFileCache.bcf', u'/MRU/Prog/'],

    ['setupapi', u'/Windows/Inf/setupapi.dev.log', u'/Registry/'],
    ['setupapi_xp', u'/Windows/setupapi.log', u'/Registry/'],

    ['mft', u'/$MFT', u'/Filesystem/'],
    ['logfile', u'/$LogFile', u'/Filesystem/']
]

SYSTEM_DIR = [  # [artifact, src_path, dest_dir, isRecursive, stringToMatch]
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SAM'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SECURITY'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SOFTWARE'],
    ['reg', LOC_REG[:-1], u'/Registry/', False, u'SYSTEM'],

    ['amcache', LOC_AMCACHE[:-1], u'/MRU/Prog/', False, u'Amcache'],
    ['prefetch', u'/Windows/Prefetch', u'/MRU/Prog/prefetch/', False, u'.pf'],
    ['srum', u'/Windows/System32/sru', u'/MRU/Prog/srum/', False, None],
    ['sccm', u'/Windows/System32/wbem/Repository', u'/MRU/Prog/sccm/', False, None],

    ['recycle', u'/$Recycle.Bin', u'/Recycle/', True, None],
    ['recycle_xp', u'/RECYCLER', u'/Recycle/', True, None]
]

USER_FILE = [  # [artifact, src_path, dest_dir]

]

USER_DIR = [  # [artifact, src_path, dest_dir, isRecursive, stringToMatch]
    ['ntuser', u'/', u'/Registry/', False, u'NTUSER'],
    ['usrclass', u'/AppData/Local/Microsoft/Windows/', u'/Registry/', False, u'UsrClass'],
    ['usrclass_xp', u'/Local Settings/Application Data/Microsoft/Windows/', u'/Registry/', False, u'UsrClass'],

    ['lnk', LOC_RECENT, u'MRU/Files/lnk/', False, None],
    ['lnk_xp', u'/Recent/', u'MRU/Files/lnk/', False, None],
    ['jmp', LOC_RECENT + u'AutomaticDestinations', u'/MRU/Files/jmp/', False, None],
    ['jmp', LOC_RECENT + u'CustomDestinations', u'/MRU/Files/jmp/', False, None],
    ['iehist', u'/AppData/Local/Microsoft/Windows/WebCache', u'/MRU/Files/iehist/', False, None],
    ['iehist_xp', u'/Local Settings/History/History.IE5', u'/MRU/Files/iehist/', True, None]
]

FILE_ADS = [  # [artifact, src_path, dest_dir, ads_name]
    ['usnjrnl', u'/$Extend/$UsnJrnl', u'/Filesystem/', u'$J']
]
