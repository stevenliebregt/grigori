import json
import logging
import os
import re
import time
import types

from enum import IntEnum

logger = logging.getLogger(__name__)


class Change(IntEnum):
    """Simple Enum representing the different types of changes to a file."""

    ADDED = 1
    MODIFIED = 2
    DELETED = 3


class Watcher:
    """Class that starts watching your files."""

    _directory = os.getcwd()  # The root directory to watch.
    _recursive = False
    _polling_interval = 1000  # The time between polls, in milliseconds.
    _file_pattern = r".+"  # The file pattern to match entries that are files.
    _directory_pattern = r".+"  # The directory pattern to match entries that are directories.
    _cache = False  # If True, we create a '.grigori' file which stores the files on shutdown.

    _callback_added = None
    _callback_modified = None
    _callback_deleted = None

    _files = {}  # Contains the current file list after each poll.

    def __init__(self, directory: str, recursive: bool = _recursive, polling_interval: int = _polling_interval,
                 file_pattern: str = _file_pattern, directory_pattern: str = _directory_pattern, cache: bool = _cache):
        self._directory = directory
        self._recursive = recursive
        self._polling_interval = polling_interval
        self._file_pattern = file_pattern
        self._directory_pattern = directory_pattern
        self._cache = cache

        # Check if we should use cache.
        if self._cache:
            self._load_cache()

    def _load_cache(self) -> None:
        """Load a list of files from the cache file."""

        cache_file = os.path.join(self._directory, ".grigori")

        if not os.path.exists(self._directory):
            self._cache = False
            logger.warning("turned off caching for this session because the directory: '" + self._directory +
                           "' does not exist")

        if os.path.isfile(cache_file):
            with open(cache_file, "r") as fh:
                try:
                    self._files = json.load(fh)
                except json.JSONDecodeError:
                    logger.error("cache contains invalid JSON, it will not be used")

    def _save_cache(self) -> None:
        """Save the list of files to the cache file."""

        cache_file = os.path.join(self._directory, ".grigori")

        with open(cache_file, "w") as fh:
            json.dump(self._files, fh)

    def on(self, change_type: Change, callback: types.FunctionType) -> None:
        """Register a callback function for a type of change.

        :param change_type: The type of the change.
        :param callback: A function to call when a change of the given type occurs.
        """

        if change_type == Change.ADDED:
            self._callback_added = callback
        elif change_type == Change.MODIFIED:
            self._callback_modified = callback
        elif change_type == Change.DELETED:
            self._callback_deleted = callback

    def watch(self) -> types.GeneratorType:
        """Keep polling for file changes and yield them.

        :return: A generator that yields a list of changes.
        """

        try:
            while True:
                yield self._poll()
                time.sleep(self._polling_interval / 1000)
        except KeyboardInterrupt:
            if self._cache:
                self._save_cache()
            logger.warning("stopped watching due to KeyboardInterrupt")

    def _poll(self) -> list:
        """Look for changes, then look for deleted files.

        :return: A list of changes, key the keys 'type' and 'file'.
        """

        changes = []
        files = {}

        self._walk(self._directory, changes, files)

        # Compare the file lists, so we can find the deleted files.
        deleted_files = self._files.keys() - files.keys()
        if deleted_files:
            for file in deleted_files:
                change = {
                    "type": Change.DELETED,
                    "file": file
                }

                changes.append(change)

                if self._callback_deleted is not None:
                    self._callback_deleted(change)

        self._files = files

        return changes

    def _walk(self, directory: str, changes: list, files: dict) -> None:
        """Walk through a directory to find changes in files.

        :param directory: The directory to walk through.
        :param changes: A list that tracks the changes during the walks in a poll.
        :param files: A list of files that are found during this poll. Used to compare to the list from the previous
            poll to find deleted files.
        """

        if not os.path.isdir(directory):
            logger.warning("directory '" + directory + "' does not exist")
            return

        with os.scandir(directory) as scanner:
            for entry in scanner:
                if entry.name == ".grigori":  # Filter cache file
                    continue
                if self._is_temporary_file(entry.path):  # Filter out IDE temporary files.
                    continue
                if entry.is_dir():
                    if self._recursive and re.match(self._directory_pattern, entry.name):
                        self._walk(entry.path, changes, files)
                else:
                    if re.match(self._file_pattern, entry.name):
                        files[entry.path] = entry.stat().st_mtime  # Save in new list, so we can compare for deleted.
                        if entry.path in self._files:  # The file is already saved, so we modified it.
                            if entry.stat().st_mtime > self._files[entry.path]:
                                change = {
                                    "type": Change.MODIFIED,
                                    "file": entry.path,
                                }
                                changes.append(change)
                                if self._callback_modified is not None:
                                    self._callback_modified(change)
                        else:  # The file is not in the files list, so we added it.
                            change = {
                                "type": Change.ADDED,
                                "file": entry.path,
                            }
                            changes.append(change)
                            if self._callback_added is not None:
                                self._callback_added(change)

    def wait(self) -> None:
        """Hacky method to use the 'watch' method without a 'for loop'."""

        for changes in self.watch():
            pass

    @staticmethod
    def _is_temporary_file(file: str) -> bool:
        """Check if the file given is a temporary file.

        :param file: The file to check.
        :return: True if the file is temporary, False if not.
        """

        # JetBrains editors append ___jb_[tmp/old/bak]___ to temporary file names.
        if "___jb_tmp___" in file or "___jb_old___" in file or "___jb_bak___" in file:
            return True

        # VIM and more append ~ to temporary file names.
        if file[-1:] == "~":
            return True

        return False
