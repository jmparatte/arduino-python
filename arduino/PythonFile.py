
# PythonFile
# ==========

from Arduino_defines import *

# ===================

FILE_READ = "rb"
FILE_WRITE = "ab"

from Stream import *

class PythonFile(Stream):

    def os_path_isdir(path):
        return _os.path.isdir(path)

    def os_path_isfile(path):
        return _os.path.isfile(path)

    def __init__(self):
        super(PythonFile, self).__init__()
        self._init("", "", "", FILE_READ)

    def __del__(self):
        self._close()

    def __bool__(self):
        return self.isopen()

    def _init(self, rootpath, dirpath, filepath, mode):
        # save arguments...
        self._rootpath = rootpath
        self._dirpath = dirpath
        self._filepath = filepath
        self._mode = mode
        # init variables...
        self._fd = None # file descriptor
        self._si = None # scandir iterator

    def _close(self):
        if self.isdir():
            self._si.close()
            self._si = None
        elif self.isfile():
            self._fd.close()
            self._fd = None
        else:
            pass

    def rootpath(self):
        return self._rootpath

    def dirpath(self):
        return self._dirpath

    def filepath(self):
        return self._filepath

    def fullpath(self):
        return (self._rootpath + self._dirpath + self._filepath) #.replace('/', '\\')

    def isdir(self):
        return bool(self._si)

    def isfile(self):
        return bool(self._fd)

    def isopen(self):
        return self.isdir() or self.isfile()

    def name(self):
        return self._filepath[1:]

    def size(self):
        if not self.isfile(): return -1
        return _os.stat(self.fullpath()).st_size

    def open(self, rootpath, dirpath, filepath, mode=FILE_READ): # return File

        if self.isopen(): self._close()
        self._init(rootpath, dirpath, filepath, mode)

        if PythonFile.os_path_isdir(self.fullpath()):
            try:
                self._si = iter(_os.scandir(self.fullpath()))
            except:
                pass
        elif PythonFile.os_path_isfile(self.fullpath()):
            try:
                self._fd = open(self.fullpath(), self._mode)
            except:
                pass
        else:
            pass
        return self

    def close(self): # return OK
        if not self.isopen(): return False
        self._close()
        return True

    def isDirectory(self): # return True if opened file is a directory
        return self.isdir()

    def openNextFile(self): # return File
        # https://www.arduino.cc/reference/en/libraries/sd/opennextfile/
        if not self.isdir(): return PythonFile()
        try:
            name = next(self._si).name
        except:
            return PythonFile()
        return PythonFile().open(self._rootpath, self._dirpath + self._filepath, ('/' + name) if name else '')

    def rewindDirectory(self): # return OK
        if not self.isdir(): return False
        self._si = iter(_os.scandir(self.fullpath()))
        return True

    def read_char(self):
        if not self.isfile(): return -1
        c = self._fd.read(1)
        c = -1 if (c==None or c==b'') else c[0]
        return c

    def write_char(self, c):
        if not self.isfile(): return 0
        return self._fd.write(bytes((c,)))

