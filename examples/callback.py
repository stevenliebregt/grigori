#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from grigori import Change
from grigori import Watcher


def on_added(change: dict) -> None:
    print("file '%s' was added" % change["file"])


def on_modified(change: dict) -> None:
    print("file '%s' was modified" % change["file"])


def on_deleted(change: dict) -> None:
    print("file '%s' was deleted" % change["file"])


directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")

w = Watcher(directory)


# Bind the callbacks.
w.on(Change.ADDED, on_added)
w.on(Change.MODIFIED, on_modified)
w.on(Change.DELETED, on_deleted)

w.wait()  # Start watching the files.
