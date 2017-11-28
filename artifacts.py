LOC_REG = u'/Windows/System32/config/'
LOC_WINEVT = u'/Windows/System32/winevt/logs/'
LOC_AMCACHE = u'/Windows/AppCompat/Programs/'
LOC_RECENT = u'/AppData/Roaming/Microsoft/Windows/Recent/'

SYSTEM_FILE = [  # [artifact_path, destination_directory]
    [LOC_REG + u'SAM', u'/Registry/'],
    [LOC_REG + u'SECURITY', u'/Registry/'],
    [LOC_REG + u'SOFTWARE', u'/Registry/'],
    [LOC_REG + u'SYSTEM', u'/Registry/'],

    [LOC_REG + u'RegBack/SAM', u'/Registry/RegBack/'],
    [LOC_REG + u'RegBack/SECURITY', u'/Registry/RegBack/'],
    [LOC_REG + u'RegBack/SOFTWARE', u'/Registry/RegBack/'],
    [LOC_REG + u'RegBack/SYSTEM', u'/Registry/RegBack/'],

    [LOC_WINEVT + u'Application.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Security.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Setup.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'System.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-PowerShell%4Operational.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-TaskScheduler%4Operational.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx', u'/OSLogs/'],
    [LOC_WINEVT + u'Microsoft-Windows-Windows Firewall With Advanced Security%4Firewall.evtx', u'/OSLogs/'],

    [LOC_AMCACHE + u'Amcache.hve', u'/MRU/Prog/'],
    [LOC_AMCACHE + u'RecentFileCache.bcf', u'/MRU/Prog/'],

    [u'/Windows/Inf/setupapi.dev.log', u'/Registry/']
]

SYSTEM_DIR = [  # [artifact_path, destination_directory, isRecursive]
    # [u'/$Recycle.Bin', u'/Recycle/', True],
    [u'/Windows/Prefetch', u'/MRU/Prog/prefetch/', False],
    [u'/Windows/System32/sru', u'/MRU/Prog/srum/', False],
    [u'/Windows/System32/wbem/Repository', u'/MRU/Prog/sccm/', False]
]

USER_FILE = [  # [artifact_path, destination_directory]
    [u'/NTUSER.DAT', u'/Registry/'],
    [u'/AppData/Local/Microsoft/Windows/UsrClass.dat', u'/Registry/']
]

USER_DIR = [  # [artifact_path, destination_directory, isRecursive]
    [LOC_RECENT, u'MRU/Files/lnk/', False],
    [LOC_RECENT + u'AutomaticDestinations', u'/MRU/Files/jmp/', False],
    [LOC_RECENT + u'CustomDestinations', u'/MRU/Files/jmp/', False],
    [u'/AppData/Local/Microsoft/Windows/WebCache', u'/MRU/Files/webcache/', False]
]

FILE_ADS = [  # [artifact_path, destination_directory, ADS Name]
    # [u'/$Extend/$UsnJrnl', u'/filesystem/', u'$J']
]
