# Grigori

Grigori is a small Python 3 module that watches over your files and notifies you of changes.

## Usage

There are currently 2 ways you can use Grigori, with a for loop, or with callbacks.

**For loops**

For the complete example, see `/examples/basic.py`.

```python
w = Watcher(directory)

for changes in w.watch():
    for change in changes:
        print("file '%s' has been changed in the following way: '%s'" % (change["file"], change["type"]))
```

**Callbacks**

For the complete example, see `/examples/callbacks.py`.

```python
w = Watcher("./directory/to/watch")

# Bind the callbacks.
w.on(Change.ADDED, on_added)
w.on(Change.MODIFIED, on_modified)
w.on(Change.DELETED, on_deleted)

w.wait()  # Start watching the files.
```

## To Do

Allow for watching multiple top-level directories, which will be each watched in threads using a thread pool.

Add `inotify` support.

Add Handler classes that can be used instead of for loops or callbacks.
