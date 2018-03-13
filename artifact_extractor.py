#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to extract common Windows artifacts from source image and its shadow copies."""

from __future__ import print_function
import hashlib
import itertools
import logging
import os
import sys

import artifacts
import artifact_selector
import vsm

from datetime import datetime as dt
from dfvfs.helpers import volume_scanner
from dfvfs.resolver import resolver
from win32file import SetFileTime, CreateFileW, CloseHandle
from win32file import GENERIC_WRITE, FILE_SHARE_WRITE
from win32file import OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL

LOG_FILE = ''


class ArtifactExtractor(volume_scanner.VolumeScanner):
    """Class that extracts common Windows artifacts."""

    _READ_BUFFER_SIZE = 32768  # Class constant that defines the default read buffer size
    _extracted = {}

    @staticmethod
    def _preserve_timestamps(file_entry, output_path):
        """Obtain and set (to preserve) original timestamps of exported files."""

        accessed = created = modified = dt.now()
        stat_object = file_entry.GetStat()

        if stat_object.atime:
            if stat_object.atime_nano:
                accessed = dt.fromtimestamp((float(str(stat_object.atime) + '.' + str(stat_object.atime_nano))))
            else:
                accessed = dt.fromtimestamp(stat_object.atime)

        if stat_object.crtime:
            if stat_object.crtime_nano:
                created = dt.fromtimestamp((float(str(stat_object.crtime) + '.' + str(stat_object.crtime_nano))))
            else:
                created = dt.fromtimestamp(stat_object.crtime)

        if stat_object.mtime:
            if stat_object.mtime_nano:
                modified = dt.fromtimestamp((float(str(stat_object.mtime) + '.' + str(stat_object.mtime_nano))))
            else:
                modified = dt.fromtimestamp(stat_object.mtime)

        handle = CreateFileW(output_path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL,
                             None)
        SetFileTime(handle, created, accessed, modified)  # does not seem to preserve nano precision of timestamps
        CloseHandle(handle)

    def _check_unique(self, file_entry, md5):
        """Check if file of the same hash has been previously extracted."""

        if file_entry.path_spec.location in self._extracted:
            if md5 in self._extracted[file_entry.path_spec.location]:
                return False
            else:
                self._extracted[file_entry.path_spec.location].append(md5)
                return True
        else:
            self._extracted[file_entry.path_spec.location] = [md5]
            return True

    def export_file(self, file_entry, output_path, recursive=False, string_to_match=None):
        """Export file to specified output path."""

        md5_obj = hashlib.md5()

        if len(output_path) > 254:
            output_path = output_path[:251] + output_path[-4:]

        if file_entry.IsDirectory():
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            for sub_file in file_entry.sub_file_entries:
                if recursive and sub_file.IsDirectory():
                    self.export_file(sub_file, os.path.join(output_path, sub_file.name), True, string_to_match)
                elif not sub_file.IsDirectory():
                    self.export_file(sub_file, os.path.join(output_path, sub_file.name), False, string_to_match)
        elif file_entry.IsFile():
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            if string_to_match is not None and string_to_match.lower() not in file_entry.name.lower():
                return
            stat_object = file_entry.GetStat()
            if stat_object.size <= 0 and file_entry.path_spec.data_stream is None:  # empty file
                logging.info(u"Empty File:\t{}".format(file_entry.path_spec.location))
                return

            try:
                in_file = file_entry.GetFileObject()
                output = open(output_path, 'wb')

                data = in_file.read(self._READ_BUFFER_SIZE)
                while data:
                    md5_obj.update(data)
                    output.write(data)
                    data = in_file.read(self._READ_BUFFER_SIZE)

                if output:
                    output.close()
                if in_file:
                    in_file.close()

                if not self._check_unique(file_entry, md5_obj.hexdigest()):
                    os.remove(output_path)
                    logging.info(u"Duplicate:\t{}\t{}".format(file_entry.path_spec.location, md5_obj.hexdigest()))
                else:
                    self._preserve_timestamps(file_entry, output_path)
                    logging.info(u"Extracted:\t{}\t{}".format(file_entry.path_spec.location, md5_obj.hexdigest()))
            except IOError:
                logging.error(u"IOError:\t{}".format(file_entry.path_spec.location))
                pass

    @staticmethod
    def _get_file_entry(base_path_spec, artifact_location, data_stream=None):
        """Get file_entry object of specified path specification."""

        path_spec = base_path_spec
        path_spec.location = artifact_location
        path_spec.data_stream = data_stream
        file_entry = resolver.Resolver.OpenFileEntry(path_spec)
        if file_entry:
            return file_entry
        else:
            logging.error(u"Missing:\t{}".format(artifact_location))
            return None

    @staticmethod
    def _get_output_path(pp, partition_type, file_entry, artifact, output_part_dir, vsc_dir, username=''):
        output_path = output_part_dir
        filename = ''

        if pp:  # preserve path
            elements = file_entry.path_spec.location.split('/')
            if file_entry.IsFile():
                filename = elements[-1]
                elements = elements[:-1]
        else:
            elements = artifact[2].split('/')
            if file_entry.IsFile():
                filename = artifact[1].split('/')[-1]

        for element in elements:
            output_path = os.path.join(output_path, element)

        if not pp and artifact in artifacts.USER_DIR:
            output_path = os.path.join(output_path, username)

        if partition_type == 'VSHADOW':
            output_path = os.path.join(output_path, vsc_dir)

        if not pp and artifact in artifacts.USER_FILE:
            output_path = os.path.join(output_path, 'Users', username)

        if file_entry.IsFile():
            output_path = os.path.join(output_path, filename)

        return output_path

    @staticmethod
    def _get_vsc_ctime(base_path_spec):
        return vsm.VSS_CREATION_TIMESTAMPS[base_path_spec.parent.store_index + 1]

    def extract_artifacts(self, base_path_specs, output_base_dir, selection, pp):  # pp = preserve path
        # Move non-vsc to front of list to be processed first
        for base_path_spec in base_path_specs:
            if base_path_spec.parent.type_indicator != 'VSHADOW':
                base_path_specs.insert(0, base_path_specs.pop(base_path_specs.index(base_path_spec)))

        for base_path_spec in base_path_specs:
            try:
                resolver.Resolver.OpenFileEntry(base_path_spec)
            except RuntimeError:
                logging.warning(u'Unable to open base path specification:\n{0:s}'.format(base_path_spec.comparable))
                continue

            # get partition of base path spec
            partition = 'p1'  # default value
            partition_type = base_path_spec.parent.type_indicator
            try:
                if partition_type == 'VSHADOW':
                    if hasattr(base_path_spec.parent.parent, 'location'):
                        partition = base_path_spec.parent.parent.location[1:]
                else:
                    self._extracted = {}
                    partition = base_path_spec.parent.location[1:]
                logging.info('=' * 10 + " Extracting: " + base_path_spec.parent.location[1:] + ' ' + '=' * 10)
            except AttributeError:  # base_path_spec has no 'location' attribute
                logging.info('=' * 10 + " Extracting: " + partition + ' ' + '=' * 10)
            output_part_dir = os.path.join(output_base_dir, partition)  # output partition directory

            vsc_dir = ''
            if partition_type == 'VSHADOW':
                print("Processing " + partition_type + ' (' + self._get_vsc_ctime(base_path_spec) + ')...')
                vsc_dir = self._get_vsc_ctime(base_path_spec).replace(':', '').replace(' ', '@')
            else:
                print("Processing " + partition_type + '...')

            for artifact in itertools.chain(artifacts.SYSTEM_FILE, artifacts.SYSTEM_DIR, artifacts.FILE_ADS):
                if artifact[0] not in selection:
                    continue

                # Get file entry
                if artifact in artifacts.FILE_ADS:
                    file_entry = self._get_file_entry(base_path_spec, artifact[1], artifact[3])
                else:
                    file_entry = self._get_file_entry(base_path_spec, artifact[1], None)
                if file_entry is None:
                    continue

                output_path = self._get_output_path(pp, partition_type, file_entry, artifact, output_part_dir, vsc_dir)
                if file_entry.IsFile():  # artifacts.SYSTEM_FILE, artifacts.FILE_ADS
                    self.export_file(file_entry, output_path)
                elif file_entry.IsDirectory():  # artifacts.SYSTEM_DIR
                    self.export_file(file_entry, output_path, artifact[3], artifact[4])

            # artifacts.USER_FILE, artifacts.USER_DIR
            if any(x in ['lnk_xp', 'iehist_xp', 'usrclass_xp'] for x in selection):
                users_file_entry = self._get_file_entry(base_path_spec, '/Documents and Settings', None)
            else:
                users_file_entry = self._get_file_entry(base_path_spec, '/Users', None)
            if users_file_entry is None:
                continue
            for user_file_entry in users_file_entry.sub_file_entries:
                if not user_file_entry.IsDirectory():
                    continue

                dir_name = user_file_entry.path_spec.location.split('/')[-1]
                if dir_name in ['All Users', 'Default', 'Default User', 'Default.migrated', 'Public',
                                'LocalService', 'NetworkService']:
                    continue

                for artifact in itertools.chain(artifacts.USER_FILE, artifacts.USER_DIR):
                    if artifact[0] not in selection:
                        continue

                    artifact_location = user_file_entry.path_spec.location + artifact[1]
                    file_entry = self._get_file_entry(base_path_spec, artifact_location, None)
                    if file_entry is None:
                        continue

                    output_path = self._get_output_path(pp, partition_type, file_entry, artifact, output_part_dir,
                                                        vsc_dir, dir_name)
                    if file_entry.IsFile():
                        self.export_file(file_entry, output_path)
                    elif file_entry.IsDirectory():
                        self.export_file(file_entry, output_path, artifact[3], artifact[4])


def main():
    """ The main program function.
    Returns:
        A boolean containing True if successful or False if not.
    """

    options = artifact_selector.get_selection()
    if not options:
        return False

    date_timestamp = dt.now()
    global LOG_FILE
    LOG_FILE = os.path.join(options.dest, "_logfile.{}.txt".format(date_timestamp.strftime("%Y-%m-%d@%H%M%S")))
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=u'[%(levelname)s] %(message)s')

    mediator = vsm.VolumeScannerMediator()
    artifact_extractor = ArtifactExtractor(mediator=mediator)

    try:
        base_path_specs = artifact_extractor.GetBasePathSpecs(options.source)
        if not base_path_specs:
            print('No supported file system found in source.\n')
            return False

        if os.path.exists(options.dest):
            print('')
            artifact_extractor.extract_artifacts(base_path_specs, options.dest, options.artifact, options.pp)
        else:
            print('Cannot find destination directory.\n')
            return False
    except KeyboardInterrupt:
        print('\nAborted by user.')
        return False

    print('\nCompleted.')
    return True


if __name__ == '__main__':
    if not main():
        sys.exit(1)
    else:
        sys.exit(0)
