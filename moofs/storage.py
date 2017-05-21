#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

from sys import argv, exit
from time import time
import gevent
from gevent import monkey
monkey.patch_all()
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy

from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit

from fuse import  FuseOSError


class SFTPStorage(objects):
    '''
    A simple SFTP filesystem. Requires paramiko: http://www.lag.net/paramiko/
    You need to be able to login to remote host without entering a password.
    '''

    def __init__(self, hosts,  remote_path='.'):
	self.sftps =[]
	for host in set(hosts):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(host, key_filename="RBCEast.pem
        self.sftps.append(client.open_sftp())
    self.root = remote_path

    def execute(self, action, *args, **kwargs):
        quorum = kwargs.get("quorum", 1)
        jobs = [gevent.spawn(action, *[sftp]+args) for sftp in self.sftps]
        results = gevent.wait(jobs, count=min(len(jobs), quorum))
        return results.value

    def chmod(self, path, mode):
        def _chmod(sftp, path, mode):
            return sftp.chmod(path, mode)
        return self.execute(_chmod, path, mode)

    def chown(self, path, uid, gid):
        def _chown(sftp, path, mode):
            return sftp.chown(path, uid, gid)
        return self.execute(_chown, path, uid, gid)

    def create(self, path, mode):
        def _create(sftp, path, mode):
            f = sftp.open(path, 'w')
            f.chmod(mode)
            f.close()
            return 0
        return self.execute(_create, path, mode)

    def destroy(self, path):
        def _destroy(sftp):
            return sftp.close()
        return self.execute(_destroy)


    def getattr(self, path, fh=None):
        def _getattr(sftp, path, fh):
            try:
                st = self.sftps[0].lstat(path)
                return dict((key, getattr(st, key)) for key in ('st_atime', 'st_gid',
                                                                'st_mode', 'st_mtime', 'st_size', 'st_uid'))
            except IOError:
                raise FuseOSError(ENOENT)
        return self.execute(_getattr, path, fh)

    def mkdir(self, path, mode):
        def _mkdir(sftp, path, mode):
            return sftp.mkdir(path, mode)
        return self.execute(_mkdir, path, mode)

    def read(self, path, size, offset, fh):
        def  _read(sftp, path, size, offset, fh):
            f = self.sftps[0].open(path)
            f.seek(offset, 0)
            buf = f.read(size)
            f.close()
            return buf
        return self.execute(_read, path, size, offset, fh)

    def readdir(self, path, fh):
        def _readdir(sftps, path, fh):
            return ['.', '..'] + [name.encode('utf-8')
                                  for name in sftps.listdir(path)]
        return self.execute(_readdir, path, fh)

    def readlink(self, path):
        def _readlink(sftp, path):
            return sftp.readlink(path)
        return self.execute(_readlink, path)

    def rename(self, old, new):
        def _rename(sftp, old, new):
            return sftp.rename(old, self.root + new)
        return self.execute(_rename, old, new)

    def rmdir(self, path):
        def _rmdir(sftp, path):
            return sftp.rmdir(path)
        return self.execute(_rmdir, path)

    def symlink(self, target, source):
        def _symlink(sftp, target, source):
            return sftp.symlink(source, target)
        return self.execute(_symlink, source, target)

    def truncate(self, path, length, fh=None):
        def _truncate(sftp, path, length, fh=None):
            return sftp.truncate(path, length)
        return self.execute(_truncate, path, length, fh)

    def unlink(self, path):
        def _unlink(sftp, path):
            return sftp.unlink(path)
        return self.execute(_unlink, path)

    def utimens(self, path, times=None):
        def _utimens(sftp, path, times=None)
            return sftp.utime(path, times)
        return self.execute(_utimens, path, times)

    def write(self, path, data, offset, fh):
        def _write(sftp, path, data, offset, fh):
            f = sftp.open(path, 'r+')
            f.seek(offset, 0)
            f.write(data)
            f.close()
            return len(data)
        return self.execute(_write, path, data, offset, fh)


if __name__ == '__main__':
    if len(argv) != 3:
        print('usage: %s <host> <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(SFTP(argv[2:]), argv[1], foreground=True, nothreads=True)
