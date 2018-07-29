import logging
import os
import re
import sys
import time


logger = logging.getLogger(__name__)


class Watcher:

    _directory = os.getcwd()  # The root directory to watch.
    _recursive = False
    _polling_interval = 1000  # The time between polls, in milliseconds.
    _file_pattern = r".+"  # The file pattern to match entries that are files.
    _directory_pattern = r".+"  # The directory pattern to match entries that are directories.

    _files = {}

    def __init__(self, directory: str, recursive: bool = _recursive, polling_interval: int = _polling_interval,
                 file_pattern: str = _file_pattern, directory_pattern: str = _directory_pattern):
        self._directory = directory
        self._recursive = recursive
        self._polling_interval = polling_interval
        self._file_pattern = file_pattern
        self._directory_pattern = directory_pattern

    def watch(self):
        logger.info("start watching")
        try:
            while True:
                yield self._poll()
                time.sleep(self._polling_interval / 1000)
        except KeyboardInterrupt:
            logger.warning("stopped watching due to KeyboardInterrupt")

    def _poll(self):
        changes = {}
        files = {}

        self._walk(self._directory, changes, files)

        print(self._files)

        return changes

    def _walk(self, directory: str, changes: dict, files: dict):
        with os.scandir(directory) as scanner:
            for entry in scanner:
                if entry.is_dir():
                    if self._recursive and re.match(self._directory_pattern, entry.name):
                        self._walk(entry.path, changes, files)
                else:
                    if re.match(self._file_pattern, entry.name):
                        files[entry.path] = entry.stat().st_mtime  # Save in new list, so we can compare for deleted.
                        # if entry.path in self._files:
                        #     # print("modified: " + entry.path)
                        #     self._files[entry.path] = entry.stat().st_mtime
                        # else:
                        #     # print("added: " + entry.path)
                        #     self._files[entry.path] = entry.stat().st_mtime
