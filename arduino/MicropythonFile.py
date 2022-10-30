
# MicropythonFile
# ===============

from Arduino_defines import *

# ===================

FILE_READ = "rb"
FILE_WRITE = "ab"

from Stream import *

class MicropythonFile(Stream):

    def os_path_isdir(path):
        try:
            return _os.stat(path)[0]==0x4000
        except:
            return False

    def os_path_isfile(path):
        try:
            return _os.stat(path)[0]==0x8000
        except:
            return False

    def __init__(self):
        super(MicropythonFile, self).__init__()
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
            #self._si.close()
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
        return (self._rootpath + self._dirpath + self._filepath)

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
        return _os.stat(self.fullpath())[6]

    def open(self, rootpath, dirpath, filepath, mode=FILE_READ): # return File

        if self.isopen(): self._close()
        self._init(rootpath, dirpath, filepath, mode)

        if MicropythonFile.os_path_isdir(self.fullpath()):
            try:
                self._si = _os.ilistdir(self.fullpath())
            except:
                pass
        elif MicropythonFile.os_path_isfile(self.fullpath()):
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
        if not self.isdir(): return MicropythonFile()
        try:
            name = next(self._si)[0]
        except:
            return MicropythonFile()
        return MicropythonFile().open(self._rootpath, self._dirpath + self._filepath, ('/' + name) if name else '')

    def rewindDirectory(self): # return OK
        if not self.isdir(): return False
        self._si = _os.ilistdir(self.fullpath())
        return True

    def read_char(self):
        if not self.isfile(): return -1
        c = self._fd.read(1)
        c = -1 if (c==None or c==b'') else c[0]
        return c

    def write_char(self, c):
        if not self.isfile(): return 0
        return self._fd.write(bytes((c,)))

