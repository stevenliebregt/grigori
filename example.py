import grigori
import os

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
file_pattern=r".+\.rst"
w = grigori.Watcher(directory, polling_interval=2000, recursive=True)

for changes in w.watch():
    for change in changes:
        print("file '%s' has been changed in the following way: '%s'" % (change["path"], change["type"]))
