
# PythonSD
# ========

from Arduino_defines import *

# ===================

# https://www.arduino.cc/reference/en/libraries/sd/

# https://docs.python.org/3/library/os.html

from PythonFile import *

class PythonSDClass():

    def __init__(self, rootname='.'):
        self._rootname = rootname
        self._rootpath = os.path.abspath(self._rootname)

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
        return os.path.isdir(self.fullpath(path))

    def isfile(self, path):
        return os.path.isfile(self.fullpath(path))

    def exists(self, path): # return OK
        return os.path.exists(self.fullpath(path))

    def remove(self, path): # return OK
        try:
            os.remove(self.fullpath(path))
            return True
        except:
            return False

    def mkdir(self, path): # return OK
        try:
            os.mkdir(self.fullpath(path))
            return True
        except:
            return False

    def rmdir(self, path): # return OK
        try:
            os.rmdir(self.fullpath(path))
            return True
        except:
            return False

    def open(self, path, mode=FILE_READ): # return File
        # https://www.arduino.cc/reference/en/libraries/sd/open/
        return PythonFile().open(self._rootpath, "", self.normpath(path), mode)
