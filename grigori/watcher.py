import logging
import sys
import time


logger = logging.getLogger(__name__)


class Watcher:

    _polling_interval = 1000  # The time between polls, in milliseconds.

    def __init__(self, polling_interval: int = _polling_interval):
        if type(polling_interval) == int:  # TODO: add proper check and error if not.
            self._polling_interval = polling_interval

    def watch(self):
        logger.info("start watching")

        try:
            while True:
                yield self._poll()
                time.sleep(self._polling_interval / 1000)
        except KeyboardInterrupt:
            logger.warning("stopped watching due to KeyboardInterrupt")

    def _poll(self):
        changes = []

        changes.append({
            "type": "ADDED",
            "path": "/test/test.py",
        })

        return changes