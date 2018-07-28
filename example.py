import grigori

w = grigori.Watcher(polling_interval=400)

for changes in w.watch():
    for change in changes:
        print("file '%s' has been changed in the following way: '%s'" % (change["path"], change["type"]))
