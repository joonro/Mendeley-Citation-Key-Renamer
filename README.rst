=============================
Mendeley-Citation-Key-Renamer
=============================

Automatically renames citation keys for `Mendeley <http://www.mendeley.com/>`_ reference manager. It will automatically generate citation keys by ``author-year-journal-abbreviation`` format. For example, for the following citation:

   Porter, R. H. (1981). A study of cartel stability : the Joint Executive Committee , 1880-1886. Bell Journal of Economics, (November), 1880–1886.

it will generate the following citation keys::

   porter-1981-bell-j-econ

and update the sqlite database for Mendeley. It will use pre-defined rules to generate Journal abbreviation.

Usage
=====

* Change the path to the Mendeley database:

   .. code-block:: python

       sqlite = 'joonhyoung.ro@gmail.com@www.mendeley.com.sqlite'  # change
       if os.name == 'nt':
           path_db = r'\Users\joon\AppData\Local\Mendeley Ltd\Mendeley Desktop\{}'.format(sqlite)
       else:
           path_db = '/home/joon/.local/share/data/Mendeley Ltd./Mendeley Desktop/'.format(sqlite)

* Also, to maintain the same `localURL` across Windows and GNU/Linux, I have a
  junction at `C:\home` which points at `C:\Users`. You can either make the
  junction or modify the source code before running this script.

* To use, with Mendeley closed, run it with ``python``::
   
   python /path/to/mendeley-rename-citation-key.py

* You can add more words by adding them to the ``abbr_rule`` dict

Installation
============

Dependencies
------------

* `APSW <http://rogerbinns.github.io/apsw/download.html>`_

Download
--------

.. code-block:: sh

    git clone https://github.com/joonro/Mendeley-Citation-Key-Renamer.git
