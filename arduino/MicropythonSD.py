
# MicropythonSD
# =============

from Arduino_defines import *

# ===================

# https://www.arduino.cc/reference/en/libraries/sd/

# https://docs.micropython.org/en/latest/library/_os.html

from MicropythonFile import *

class MicropythonSDClass():

    def __init__(self, rootname=''):
        self._rootname = rootname
        self._rootpath = self._rootname

    def rootname(self):
        return self._rootname

    def rootpath(self):
        return self._rootpath

    def normpath(self, path):
        path = path.replace('\\', '/')
        while path[0:1]=='/': path=path[1:]
        while path[-1:]=='/': path=path[:-1]
        if path: path = '/' + path
        return path

    def fullpath(self, path):
        return (self._rootpath + self.normpath(path))

    def isdir(self, path):
        try:
            return _os.stat(self.fullpath(path))[0]==0x4000
        except:
            return False

    def isfile(self, path):
        try:
            return _os.stat(self.fullpath(path))[0]==0x8000
        except:
            return False

    def exists(self, path): # return OK
        try:
            return bool(_os.stat(self.fullpath(path)))
        except:
            return False

    def remove(self, path): # return OK
        try:
            _os.remove(self.fullpath(path))
            return True
        except:
            return False

    def mkdir(self, path): # return OK
        try:
            _os.mkdir(self.fullpath(path))
            return True
        except:
            return False

    def rmdir(self, path): # return OK
        try:
            _os.rmdir(self.fullpath(path))
            return True
        except:
            return False

    def open(self, path, mode=FILE_READ): # return File
        # https://www.arduino.cc/reference/en/libraries/sd/open/
        return MicropythonFile().open(self._rootpath, "", self.normpath(path), mode)
