"""Basic watcher module.

The :mod:`grigori` module contains two classes:

- :class:`grigori.Change`
- :class:`grigori.Watcher`

You can use the :class:`grigori.Watcher` class to create a watcher instance. Then you have the choice if you want to
use callbacks or a for loop. To use callbacks, use the :func:`grigori.Watcher.wait` method. To use the for loop, use the
:func:`grigori.Watcher.watch` method.
"""

from .watcher import Change
from .watcher import Watcher
