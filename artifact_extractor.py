#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to extract common Windows artifacts from source image and its shadow copies."""

from __future__ import print_function
import argparse
import hashlib
import itertools
import logging
import os
import sys
import artifacts
import vsm

from datetime import datetime as dt
from dfvfs.lib import definitions
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
        """ Checks if file of the same hash has been previously extracted"""

        if file_entry.path_spec.location in self._extracted:
            if md5 in self._extracted[file_entry.path_spec.location]:
                return False
            else:
                self._extracted[file_entry.path_spec.location].append(md5)
                return True
        else:
            self._extracted[file_entry.path_spec.location] = [md5]
            return True

    def export_file(self, file_entry, output_path, recursive=False):
        """ Outputs a path specification to the specified path"""

        md5_obj = hashlib.md5()
        if file_entry.IsDirectory():
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            for sub_file_entry in file_entry.sub_file_entries:
                if recursive and sub_file_entry.IsDirectory():
                    self.export_file(sub_file_entry, os.path.join(output_path, sub_file_entry.name), True)
                elif not sub_file_entry.IsDirectory():
                    self.export_file(sub_file_entry, os.path.join(output_path, sub_file_entry.name))
        elif file_entry.IsFile():
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            try:
                in_file = file_entry.GetFileObject()
                output = open(output_path, "wb")

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
                    logging.info("Duplicate:\t{}\t{}".format(output_path, md5_obj.hexdigest()))
                else:
                    self._preserve_timestamps(file_entry, output_path)
                    logging.info("Extracted:\t{}\t{}".format(output_path, md5_obj.hexdigest()))
            except IOError:
                logging.error("IOError:\t{}".format(output_path))
                pass

    @staticmethod
    def _get_file_entry(base_path_spec, artifact_location, data_stream=None):
        path_spec = base_path_spec
        path_spec.location = artifact_location
        path_spec.data_stream = data_stream
        file_entry = resolver.Resolver.OpenFileEntry(path_spec)
        if file_entry:
            return file_entry
        else:
            logging.error("Missing:\t{}".format(artifact_location))
            return None

    @staticmethod
    def _get_output_path(output_base_dir, artifact_output_path):
        elements = artifact_output_path.split('/')
        output_path = output_base_dir
        for element in elements:
            output_path = os.path.join(output_path, element)
        return output_path

    @staticmethod
    def _get_vsc_ctime(base_path_spec):
        return vsm.VSS_CREATION_TIMESTAMPS[base_path_spec.parent.store_index + 1]

    def extract_artifacts(self, base_path_specs, output_base_dir):
        # Move non-vsc to front of list to be processed first
        for base_path_spec in base_path_specs:
            if base_path_spec.parent.type_indicator != 'VSHADOW':
                base_path_specs.insert(0, base_path_specs.pop(base_path_specs.index(base_path_spec)))

        for base_path_spec in base_path_specs:
            try:
                file_entry = resolver.Resolver.OpenFileEntry(base_path_spec)
            except RuntimeError as e:
                print(e)
                file_entry = None
            if file_entry is None:
                logging.warning(u'Unable to open base path specification:\n{0:s}'.format(base_path_spec.comparable))
                continue

            vsc_dir = ''
            if base_path_spec.parent.type_indicator == 'VSHADOW':
                print(u"Processing " + base_path_spec.parent.type_indicator + u' (' +
                      self._get_vsc_ctime(base_path_spec) + u')...')
                vsc_dir = self._get_vsc_ctime(base_path_spec).replace(':', '').replace(' ', '@')
            else:
                print(u"Processing " + base_path_spec.parent.type_indicator + u'...')

            for artifact in itertools.chain(artifacts.SYSTEM_FILE, artifacts.SYSTEM_DIR, artifacts.FILE_ADS):
                if len(artifact) == 3 and artifact in artifacts.FILE_ADS:  # extract ADS (artifacts.FILE_ADS)
                    file_entry = self._get_file_entry(base_path_spec, artifact[0], artifact[2])
                else:
                    file_entry = self._get_file_entry(base_path_spec, artifact[0], None)
                if file_entry is None:
                    continue

                output_path = self._get_output_path(output_base_dir, artifact[1])
                if base_path_spec.parent.type_indicator == 'VSHADOW':
                    if file_entry.IsFile():  # artifacts.SYSTEM_FILE
                        self.export_file(file_entry, os.path.join(output_path, vsc_dir, artifact[0].split('/')[-1]))
                    elif file_entry.IsDirectory():    # artifacts.SYSTEM_DIR
                        self.export_file(file_entry, os.path.join(output_path, vsc_dir), artifact[2])
                else:
                    if file_entry.IsFile():  # artifacts.SYSTEM_FILE
                        output_path = os.path.join(output_path, artifact[0].split('/')[-1])
                        self.export_file(file_entry, output_path)
                    elif file_entry.IsDirectory():  # artifacts.SYSTEM_DIR
                        self.export_file(file_entry, output_path, artifact[2])

            users_file_entry = self._get_file_entry(base_path_spec, '/Users', None)
            if users_file_entry is None:
                continue
            for user_file_entry in users_file_entry.sub_file_entries:
                stat_object = user_file_entry.GetStat()
                if stat_object.type == definitions.FILE_ENTRY_TYPE_DIRECTORY:
                    dir_name = user_file_entry.path_spec.location.split('/')[-1]
                    if dir_name not in ['All Users', 'Default', 'Default User', 'Default.migrated', 'Public']:

                        for artifact in artifacts.USER_FILE:
                            artifact_location = user_file_entry.path_spec.location + artifact[0]
                            file_entry = self._get_file_entry(base_path_spec, artifact_location, None)
                            if file_entry is None:
                                continue
                            output_path = self._get_output_path(output_base_dir, artifact[1])

                            if base_path_spec.parent.type_indicator == 'VSHADOW':
                                output_path = os.path.join(output_path, vsc_dir, 'Users', dir_name,
                                                           artifact[0].split('/')[-1])
                                self.export_file(file_entry, output_path)
                            else:
                                output_path = os.path.join(output_path, 'Users', dir_name, artifact[0].split('/')[-1])
                                self.export_file(file_entry, output_path)

                        for artifact in artifacts.USER_DIR:
                            artifact_location = user_file_entry.path_spec.location + artifact[0]
                            file_entry = self._get_file_entry(base_path_spec, artifact_location, None)
                            if file_entry is None:
                                continue
                            output_path = os.path.join(self._get_output_path(output_base_dir, artifact[1]), dir_name)

                            if base_path_spec.parent.type_indicator == 'VSHADOW':
                                self.export_file(file_entry, os.path.join(output_path, vsc_dir), artifact[2])
                            else:
                                self.export_file(file_entry, output_path, artifact[2])


def main():
    """ The main program function.
    Returns:
        A boolean containing True if successful or False if not.
    """
    argument_parser = argparse.ArgumentParser(description=(
        u'Extracts common Windows artifacts from source (including Volume Shadow Copies).'))
    argument_parser.add_argument(u'source', nargs=u'?', action=u'store', metavar=u'image.raw', default=None, help=(
        u'path of the directory or filename of a storage media image containing the file.'))
    argument_parser.add_argument(u'dest', nargs=u'?', action=u'store', metavar=u'destination', default=None, help=(
        u'destination directory where the output will be stored.'))
    options = argument_parser.parse_args()

    if not options.source or not options.dest:
        print(u'One or more arguments is missing.\n')
        argument_parser.print_help()
        print(u'')
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
            print(u'No supported file system found in source.\n')
            return False

        if os.path.exists(options.dest):
            print(u'')
            artifact_extractor.extract_artifacts(base_path_specs, options.dest)
        else:
            print(u'Cannot find destination directory.\n')
            return False
    except KeyboardInterrupt:
        print(u'\nAborted by user.')
        return False

    print(u'\nCompleted.')
    return True


if __name__ == '__main__':
    if not main():
        sys.exit(1)
    else:
        sys.exit(0)
