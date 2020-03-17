Update @Types header in CHAT files
==================================

|Build Status|

What it does
------------

``update_chat_types`` looks at CHAT files and updates the ``@Types``
header if needed, based on the existence of ``0types.txt`` in a file's
immediate directory. If no header currently exists, it is inserted
before the first utterance.

Prerequisites
-------------

Make sure to have Python 3 installed, e.g., on macOS, you can use
Homebrew with

::

    $ brew install python3

Install
-------

Clone this repo and ``cd`` into it, then run

::

    $ python3 setup.py install

to install the executable ``update_chat_types``.

Usage
-----


::

    Options:
      --chatdir TEXT  CHAT root dir  [required]
      --help          Show this message and exit.

e.g.

::

    $ update_chat_types --chatdir /path/to/childes-data

.. |Build Status| image:: https://travis-ci.org/TalkBank/update_chat_types.png
   :target: https://travis-ci.org/TalkBank/update_chat_types
