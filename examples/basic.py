#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from grigori import Watcher

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")

w = Watcher(directory)

for changes in w.watch():
    for change in changes:
        print("file '%s' has been changed in the following way: '%s'" % (change["file"], change["type"]))
