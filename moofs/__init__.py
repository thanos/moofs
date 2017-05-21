# -*- coding: utf-8 -*-
"""
moofs
~~~~~~~~~~~~~~~~~~~

A simple fFUSE based filesystem that pass through all commoands and replicates all writes to a list of servers using sfp.

:copyright: (c) 2015 by thanos vassilakis
:licence: MIT, see LICENCE for more details
"""
from __future__ import absolute_import, unicode_literals
import logging

# Generate your own AsciiArt at:
# patorjk.com/software/taag/#f=Calvin%20S&t=moofs
__banner__ = r"""
╦  ╦┌─┐┌┐┌┌─┐┬ ┬┌─┐┬─┐┌┬┐
╚╗╔╝├─┤││││ ┬│ │├─┤├┬┘ ││  by thanos vassilakis
 ╚╝ ┴ ┴┘└┘└─┘└─┘┴ ┴┴└──┴┘
"""

__title__ = 'moofs'
__summary__ = 'A simple fFUSE based filesystem that pass through all commoands and replicates all writes to a list of servers using sfp.'
__uri__ = 'https://github.com/thanos/moofs'

__version__ = '0.0.1'

__author__ = 'thanos vassilakis'
__email__ = 'thanosv2gmail.com'

__license__ = 'MIT'
__copyright__ = 'Copyright 2015 thanos vassilakis'

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
