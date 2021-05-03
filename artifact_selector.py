import argparse
import os.path

import artifacts

from argparse import RawTextHelpFormatter


def _parse_selection(options):
    selection_raw = options.artifact

    std_7 = {'reg', 'regb', 'ntuser', 'usrclass', 'antimalware', 'defender', 'evtl', 'pshist', 'setupapi', 'amcache',
             'iehist', 'jmp', 'lnk', 'prefetch', 'rdpcache', 'sccm', 'sqm', 'srum', 'syscache', 'thumbcache', 'timeline',
             'wer', 'sch_job', 'sch_xml', 'startupinfo', 'ual'}
    std_xp = {'reg', 'regb_xp', 'ntuser', 'usrclass_xp', 'antimalware', 'defender', 'evtl_xp', 'setupapi_xp',
              'iehist_xp', 'lnk_xp', 'prefetch', 'rdpcache_xp', 'sch_job', 'sch_xp'}
    all_7 = std_7 | {'recycle', 'mft', 'usnjrnl', 'logfile', 'pagefile', 'sig_ctlg'}
    all_xp = std_xp | {'recycle_xp', 'mft', 'usnjrnl', 'logfile', 'pagefile', 'sig_ctlg'}
    supported = all_7 | all_xp | {'std', 'std_xp', 'all', 'all_xp'}

    selection = selection_raw.split(',')
    selection = set(selection)

    # remove unsupported artifacts
    unsupported = set()
    for selected in selection:
        if selected not in supported:
            print("{} artifact is not supported.\n".format(selected))
            unsupported.add(selected)
    selection = selection - unsupported

    # expand std, std_xp, all, all_xp
    if 'std' in selection:
        selection = selection | std_7
    if 'std_xp' in selection:
        selection = selection | std_xp
    if 'all' in selection:
        selection = selection | all_7
    if 'all_xp' in selection:
        selection = selection | all_xp

    # remove std, std_xp, all_7, all_xp
    selection = selection - {'std', 'std_xp', 'all', 'all_xp'}

    if len(selection) == 0:
        selection = None

    return selection


def _parse_unsupported(file_path, dir_path):
    if file_path:
        artifacts.SYSTEM_FILE.append(['unsupported', file_path, u'/Others/'])
    if dir_path:
        artifacts.SYSTEM_DIR.append(['unsupported', dir_path, u'/Others/', False, None])


def get_selection():
    argument_parser = argparse.ArgumentParser(description=(
        'ArtifactExtractor extracts selected Windows artifacts from forensic images and VSCs.\n'
        'It utilises various libraries and example code written by Joachim Metz.\n\n'

        'Supported Artifacts: \n'
        '\t std \t\t reg, regb, ntuser, usrclass, antimalware, defender, evtl, pshist, setupapi, amcache, iehist, jmp, '
        'lnk, prefetch, rdpcache, sccm, srum, syscache, thumbcache, timeline, wer, sch_job, sch_xml, startupinfo\n'
        '\t std_xp \t reg, regb_xp, ntuser, usrclass_xp, antimalware, defender, evtl_xp, setupapi_xp, iehist_xp, '
        'lnk_xp, prefetch, rdpcache_xp, sch_job, sch_xp\n'
        '\t all \t\t all (Windows 7+) - WARNING: SLOW!\n'
        '\t all_xp \t all (Windows XP) - WARNING: SLOW!\n'

        '\t\t ===== Registry Hives ======\n'
        '\t reg \t\t registry hives\n'
        '\t regb \t\t backup registry hives (Windows 7+)\n'
        '\t regb_xp \t backup registry hives (Windows XP)\n'
        '\t ntuser \t users\' ntuser hive\n'
        '\t usrclass \t users\' usrclass hive (Windows 7+)\n'
        '\t usrclass_xp \t users\' usrclass hive (Windows XP)\n'

        '\t\t ===== System Logs ======\n'
        '\t antimalware \t microsoft antimalware mplogs\n'
        '\t defender \t windows defender mplogs\n'
        '\t evtl \t\t event logs (Windows 7+)\n'
        '\t evtl_xp \t event logs (Windows XP)\n'
        '\t pshist \t powershell command history\n'
        '\t setupapi \t setupapi log (Windows 7+)\n'
        '\t setupapi_xp \t setupapi log (Windows XP)\n'
        '\t ual \t\t user access logs\n'

        '\t\t ===== Most Recently Used ======\n'
        '\t amcache \t amcache and/or recentfilecache.bcf\n'
        '\t iehist \t users\' ie history (Windows 7+)\n'
        '\t iehist_xp \t users\' ie history (Windows XP)\n'
        '\t jmp \t\t users\' jmp lists\n'
        '\t lnk \t\t users\' lnk files (Windows 7+)\n'
        '\t lnk_xp \t users\' lnk files (Windows XP)\n'
        '\t prefetch \t prefetch\n'
        '\t sccm \t\t system center configuration manager software metering\n'
        '\t srum \t\t system resource usage monitor\n'
        '\t sqm \t\t software qauality metrices\n'
        '\t syscache \t syscache hive (Windows 7)\n'
        '\t thumbcache \t thumbcache files (Windows 7+)\n'
        '\t timeline \t timeline activity history\n'

        '\t\t ===== Persistence ======\n'
        '\t sch_job \t scheduled task job files\n'
        '\t sch_xml \t scheduled task xml files (Windows 7+)\n'
        '\t sch_xp \t scheduled task info log (Windows XP)\n'
        '\t startupinfo \t startupinfo xml files\n'

        '\t\t ===== File System ======\n'
        '\t mft \t\t ntfs mft\n'
        '\t logfile \t ntfs logfile\n'
        '\t usnjrnl \t ntfs usnjurnl - WARNING: SLOW!\n'

        '\t\t ===== Others ======\n'
        '\t pagefile \t pagefile - WARNING: SLOW!\n'
        '\t rdpcache \t rdp cache files (Windows 7+)\n'
        '\t rdpcache_xp \t rdp cache files (Windows XP)\n'
        '\t recycle \t users\' recycle bin files (Windows 7+) - does not provide owner or original file name\n'
        '\t recycle_xp \t users\' recycle bin files (Windows XP) - does not provide owner\n'
        '\t wer \t\t windows error reporting reports\n'
        '\t sig_ctlg \t users\' signature catalog files\n\n'

        'Usage: \n'
        '\t Extract essential (in developer\'s opinion) artifacts\n'
        '\t artifact_extractor <forensic image> <dest> -a std\n\n'

        '\t Extract essential (in developer\'s opinion) artifacts + $MFT\n'
        '\t artifact_extractor <forensic image> <dest> -a std,mft\n\n'

        '\t Extract unsupported file\n'
        '\t artifact_extractor <forensic image> <dest> --cf <path to unsupported file e.g. /Windows/hiberfil.sys>]>\n\n'

        '\t Extract unsupported directory\n'
        '\t artifact_extractor <forensic image> <dest> --cd <path to unsupported dir e.g. /Windows/Temp>\n\n'
    ), formatter_class=RawTextHelpFormatter)

    argument_parser.add_argument('source', nargs='?', metavar='image.raw', default=None, help=(
        'path of the directory or filename of a storage media image containing the file.'))
    argument_parser.add_argument('dest', nargs='?', metavar='destination', default=None, help=(
        'destination directory where the output will be stored.'))
    argument_parser.add_argument('-a', '--artifact', default='std', help=(
        'artifacts to extract. See above for list of supported artifacts.'))
    argument_parser.add_argument('--uf', default=None, help='path of unsupported file to extract.')
    argument_parser.add_argument('--ud', default=None, help='path of unsupported directory to extract.')
    argument_parser.add_argument('--pp', action='store_true', help='preserve path of extracted artifacts in output.')
    argument_parser.add_argument('--old', action='store_true', help='extract from Windows.old directory as well.')

    options = argument_parser.parse_args()
    options.source = os.path.abspath(options.source)
    options.dest = os.path.abspath(options.dest)

    if not options.source or not options.dest:
        print('One or more arguments is missing.\n')
        argument_parser.print_help()
        print('')
        return False

    if (not options.uf) and (not options.ud):
        options.artifact = _parse_selection(options)
    else:
        options.artifact = {'unsupported'}
        _parse_unsupported(options.uf, options.ud)

    if options.artifact is None:
        return False
    else:
        return options
