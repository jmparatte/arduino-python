
# Arduino class Print
# ===================

class Print:

    def __init__(self):
        #print("Print.8")
        pass

    def __del__(self):
        #print("Print.12")
        pass

    def availableForWrite(self):
        return 1

    def write_char(self, c):
        #return c&0 # 0 (it's to use <c> parameter)
        _ = c
        return 0

    def write_bstr(self, b):
        l = 0
        for c1 in b:
            l1 = self.write_char(c1)
            if l1==0: break;
            l += l1
        return l

    def write_str(self, s):
        return self.write_bstr(s.encode())

    def write(self, v):
        if isinstance(v, int):
            return self.write_char(v)
        elif isinstance(v, (bytes, bytearray)):
            return self.write_bstr(v)
        else:
            return self.write_str(v)

    def print(self, v):
        if isinstance(v, str):
            return self.write_str(v)
        elif isinstance(v, (bytes, bytearray)):
            return self.write_bstr(v)
        else:
            return self.write_str(str(v))

    def println(self, v=b''):
        return (self.print(v) + self.write_bstr(b'\r\n'))

    def flush(self):
        pass
