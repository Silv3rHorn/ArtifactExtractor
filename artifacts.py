LOC_REG = u'/Windows/System32/config/'
LOC_WINEVT = LOC_REG
LOC_WINEVTX = u'/Windows/System32/winevt/logs/'
LOC_AMCACHE = u'/Windows/AppCompat/Programs/'
LOC_RECENT = u'/AppData/Roaming/Microsoft/Windows/Recent/'

SYSTEM_FILE = [  # [artifact_path, destination_directory]
    ['reg', LOC_REG + u'SAM', u'/Registry/'],
    ['reg', LOC_REG + u'SECURITY', u'/Registry/'],
    ['reg', LOC_REG + u'SOFTWARE', u'/Registry/'],
    ['reg', LOC_REG + u'SYSTEM', u'/Registry/'],

    ['regb', LOC_REG + u'RegBack/SAM', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SECURITY', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SOFTWARE', u'/Registry/RegBack/'],
    ['regb', LOC_REG + u'RegBack/SYSTEM', u'/Registry/RegBack/'],

    ['regb_xp', LOC_REG + u'Repair/SAM', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/SECURITY', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/SOFTWARE', u'/Registry/Repair/'],
    ['regb_xp', LOC_REG + u'Repair/SYSTEM', u'/Registry/Repair/'],

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

    ['amcache', LOC_AMCACHE + u'Amcache.hve', u'/MRU/Prog/'],
    ['amcache', LOC_AMCACHE + u'RecentFileCache.bcf', u'/MRU/Prog/'],

    ['setupapi', u'/Windows/Inf/setupapi.dev.log', u'/Registry/'],
    ['setupapi_xp', u'/Windows/setupapi.log', u'/Registry/'],

    ['mft', u'/$MFT', u'/Filesystem/'],
    ['logfile', u'/$LogFile', u'/Filesystem/']
]

SYSTEM_DIR = [  # [artifact_path, destination_directory, isRecursive]
    ['recycle', u'/$Recycle.Bin', u'/Recycle/', True],
    ['recycle_xp', u'/RECYCLER', u'/Recycle/', True],
    ['prefetch', u'/Windows/Prefetch', u'/MRU/Prog/prefetch/', False],
    ['srum', u'/Windows/System32/sru', u'/MRU/Prog/srum/', False],
    ['sccm', u'/Windows/System32/wbem/Repository', u'/MRU/Prog/sccm/', False]
]

USER_FILE = [  # [artifact_path, destination_directory]
    ['ntuser', u'/NTUSER.DAT', u'/Registry/'],
    ['usrclass', u'/AppData/Local/Microsoft/Windows/UsrClass.dat', u'/Registry/'],
    ['usrclass_xp', u'/Local Settings/Application Data/Microsoft/Windows/UsrClass.dat', u'/Registry/']
]

USER_DIR = [  # [artifact_path, destination_directory, isRecursive]
    ['lnk', LOC_RECENT, u'MRU/Files/lnk/', False],
    ['lnk_xp', u'/Recent/', u'MRU/Files/lnk/', False],
    ['jmp', LOC_RECENT + u'AutomaticDestinations', u'/MRU/Files/jmp/', False],
    ['jmp', LOC_RECENT + u'CustomDestinations', u'/MRU/Files/jmp/', False],
    ['iehist', u'/AppData/Local/Microsoft/Windows/WebCache', u'/MRU/Files/iehist/', False],
    ['iehist_xp', u'/Local Settings/History/History.IE5', u'/MRU/Files/iehist/', True]
]

FILE_ADS = [  # [artifact_path, destination_directory, ADS Name]
    ['usnjrnl', u'/$Extend/$UsnJrnl', u'/Filesystem/', u'$J']
]
