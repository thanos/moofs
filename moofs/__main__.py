#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
moofs.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``moofs`` (if installed)
or ``python -m moofs`` (no install required).
"""
from __future__ import absolute_import, unicode_literals
import logging
from sys import argv, exit

from fuse import FUSE

from moofs.operations import  FuseOperations
from moofs.storage import  SFTPStorage

from moofs.log import configure_stream

logger = logging.getLogger(__name__)


def cli():
    """Add some useful functionality here or import from a submodule."""
    # configure root logger to print to STDERR
    if len(argv) < 3:
        print('usage: %s <host> <mountpoint>' % argv[0])
        return 1
    configure_stream(level='DEBUG')

    # launch the command line interface
    logger.debug('Booting up command line interface')
    fuse = FUSE(FuseOperations(SFTPStorage(argv[2:]), argv[1]), foreground=True, nothreads=True)
    return 0

if __name__ == '__main__':
    # exit using whatever exit code the CLI returned
    exit(cli())
