
# jm_time
# =======

# https://www.epochconverter.com/
# https://cplusplus.com/reference/ctime/
# https://docs.python.org/fr/3/library/_time.html
# https://docs.python.org/3/library/_time.html#_time.time
# https://docs.python.org/3/library/_time.html#_time.struct_time

from Arduino import *

import time as _time
if python_detected: import calendar as _calendar

TIME_ONE_SEC    = 1 # time_t 1 second
TIME_ONE_MIN    = 60 # time_t 1 minute
TIME_ONE_HOUR   = 60 # time_t 1 hour
TIME_ONE_DAY    = 86400 # time_t 1 day

TIME_ILLEGAL    = -1 # time_t illegal value
TIME_YR_1970    = 0 # time_t Thursday January 01, 1970 00:00:00 UTC
TIME_YR_2000    = 946684800 # time_t Saturday January 01, 2000 00:00:00 UTC
TIME_MAX        = 2147483647 # time_t Tuesday January 19, 2038 03:14:07 UTC

TZO_CET         = 60 # Central European Time
TZO_CEST        = 120 # Central European Summer Time

if python_detected:
    if _time.gmtime(0)[0]!=1970: raise Exception("Python epoch doesn't match year 1970!")
    TIME_EPOCH = 1970
    TIME_OFFSET = 0
else:
    if _time.gmtime(0)[0]!=2000: raise Exception("Microython epoch doesn't match year 2000!")
    TIME_EPOCH = 2000
    TIME_OFFSET = TIME_YR_2000

_time_corr = 0

#def time():
#    return time_get()

def time(timer=None): # return time
    if timer==None:
        return time_get()
    else:
        return time_set(timer)

def time_get():
    if python_detected:
        return TIME_OFFSET + int(_time.time()) + _time_corr
    else:
        return TIME_OFFSET + _time.time() + _time_corr

def time_set(timer): # return time
    global _time_corr
    _time_corr = _time_corr + timer - time_get()
    return timer

def time_ns():
    return TIME_OFFSET*1000000000 + _time.time_ns() +_time_corr*1000000000

def sleep(s):
    _time.sleep(s)

# ---------------------------------------------------------------------

def gmtime(timer=None): # return tm
    if timer==None: timer=time_get()
    if python_detected:
        return _time.gmtime(timer - TIME_OFFSET)[0:8] + ((-1,))
    else:
        return _time.gmtime(timer - TIME_OFFSET) + ((-1,))

def test_gmtime():
    print()
    print("test_gmtime():")
    t=946684800; gm=(2000, 1, 1, 0, 0, 0, 5, 1, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    print("test_gmtime():")
    t=1648342799; gm=(2022, 3, 27, 0, 59, 59, 6, 86, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    t=1648342800; gm=(2022, 3, 27, 1, 0, 0, 6, 86, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    t=1648342801; gm=(2022, 3, 27, 1, 0, 1, 6, 86, -1);  gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    print("test_gmtime():")
    t=1667091599; gm=(2022, 10, 30, 0, 59, 59, 6, 303, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    t=1667091600; gm=(2022, 10, 30, 1, 0, 0, 6, 303, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    t=1667091601; gm=(2022, 10, 30, 1, 0, 1, 6, 303, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)
    print("test_gmtime():")
    t=2147483647; gm=(2038, 1, 19, 3, 14, 7, 1, 19, -1); gm_=gmtime(t); print(t, gm, gm_, gm==gm_)

if __name__=="__main__": test_gmtime()

# ---------------------------------------------------------------------

def timegm(gm): # return time
    if python_detected:
        return TIME_OFFSET + _calendar.timegm(gm[0:6] + (0,0, -1,))
    else:
        return TIME_OFFSET + _time.mktime(gm[0:6] + (0,0, -1,))

def test_timegm():
    print()
    print("test_timegm():")
    gm=(2000, 1, 1, 0, 0, 0, 5, 1, -1); t=946684800; t_=timegm(gm); print(gm, t, t_, t==t_)
    print("test_timegm():")
    gm=(2022, 3, 27, 0, 59, 59, 6, 86, -1); t=1648342799; t_=timegm(gm); print(gm, t, t_, t==t_)
    gm=(2022, 3, 27, 1, 0, 0, 6, 86, -1); t=1648342800; t_=timegm(gm); print(gm, t, t_, t==t_)
    gm=(2022, 3, 27, 1, 0, 1, 6, 86, -1); t=1648342801; t_=timegm(gm); print(gm, t, t_, t==t_)
    print("test_timegm():")
    gm=(2022, 10, 30, 0, 59, 59, 6, 303, -1); t=1667091599; t_=timegm(gm); print(gm, t, t_, t==t_)
    gm=(2022, 10, 30, 1, 0, 0, 6, 303, -1); t=1667091600; t_=timegm(gm); print(gm, t, t_, t==t_)
    gm=(2022, 10, 30, 1, 0, 1, 6, 303, -1); t=1667091601; t_=timegm(gm); print(gm, t, t_, t==t_)
    print("test_timegm():")
    gm=(2038, 1, 19, 3, 14, 7, 1, 19, -1); t=2147483647; t_=timegm(gm); print(gm, t, t_, t==t_)

if __name__=="__main__": test_timegm()

# ---------------------------------------------------------------------

_tz_offsets = (
    TZO_CET,    # [0]: standard
    TZO_CEST    # [1]: daylight
)

_tz_table: tuple[tuple, ...] = ()

def _tz_last_sunday_of_month(gm0, isdst):
    # gm0: (year,month,mday, hour,min,sec, wday,yday, isdst)
    # isdst: start Daylight else Standard timezone
    mday0 = gm0[2] # last day of month, wday unknown
    time0 = timegm(gm0) # time of last day of month
    gm1 = gmtime(time0) # adjust/compute wday (and yday)
    wday1 = gm1[6] # wday of last day of month: 0..6 => monday..sunday
    mday2 = mday0 - (wday1 + 1)%7 # mday of last sunday of month
    gm2 = (gm0[0:2] + (mday2,) + gm0[3:6] + (0,0, -1,)) # incomplete gm tupple of last sunday of month
    time3 = timegm(gm2) # true time of start of timezone
    gm3 = gmtime(time3) # true gm tupple of start of timezone
    lm3 = gmtime(time3 + _tz_offsets[isdst]*60)[0:8] + ((isdst,)) # localtime of start of timezone
    return (time3, gm3, lm3)

def _tz_table_make():
    global _tz_table
    for year in range(2000, 2038): # not including 2038 !!!
        _tz_table += (_tz_last_sunday_of_month((year, 3,31, 1,0,0, 0,0, -1), 1),) # start Daylight
        _tz_table += (_tz_last_sunday_of_month((year,10,31, 1,0,0, 0,0, -1), 0),) # start Standard

_tz_table_make()

def view_tz_table():
    print()
    print("view_tz_table():")
    i = 0
    while i<len(_tz_table):
        row = _tz_table[i]
        print(row)
        i += 1

if __name__=="__main__": view_tz_table()

# ---------------------------------------------------------------------

def _localtime(timer):
    i = 0
    for t2 in _tz_table:
        if timer<t2[0]: break
        i += 1
    tm = gmtime(timer + _tz_offsets[i&1]*60)[0:8] + ((i&1,))
    return tm

def localtime(timer=None):
    if timer==None: timer=time_get()
    if python_detected:
        #return _localtime(timer)
        return _time.localtime(timer)[0:9]
    else:
        return _localtime(timer)

def test_localtime():
    print()
    print("test_localtime():")
    t=946684800; lt=(2000, 1, 1, 1, 0, 0, 5, 1, 0); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    print("test_localtime():")
    t=1648342799; lt=(2022, 3, 27, 1, 59, 59, 6, 86, 0); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    t=1648342800; lt=(2022, 3, 27, 3, 0, 0, 6, 86, 1); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    t=1648342801; lt=(2022, 3, 27, 3, 0, 1, 6, 86, 1); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    print("test_localtime():")
    t=1667091599; lt=(2022, 10, 30, 2, 59, 59, 6, 303, 1); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    t=1667091600; lt=(2022, 10, 30, 2, 0, 0, 6, 303, 0); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    t=1667091601; lt=(2022, 10, 30, 2, 0, 1, 6, 303, 0); lt_=localtime(t); print(t, lt, lt_, lt==lt_)
    print("test_localtime():")
    t=2147483647; lt=(2038, 1, 19, 4, 14, 7, 1, 19, 0); lt_=localtime(t); print(t, lt, lt_, lt==lt_)

if __name__=="__main__": test_localtime()

# ---------------------------------------------------------------------

def _mktime(lm):
    i = 0
    for row1 in _tz_table:
        lm1 = row1[2]
        if lm[0]<lm1[0] or (lm[0]==lm1[0] and (
           lm[1]<lm1[1] or (lm[1]==lm1[1] and (
           lm[2]<lm1[2] or (lm[2]==lm1[2] and (
           lm[3]<lm1[3] or (lm[3]==lm1[3] and (
           lm[4]<lm1[4] or (lm[4]==lm1[4] and
           lm[5]<lm1[5] ))))))))): break
        i += 1
    offset2 = (_tz_offsets[0] + (1 if lm[8]==1 else 0)*60)*60
    time2 = timegm(lm) - offset2
    return time2

def mktime(lm):
    if python_detected:
        #return _mktime(lm)
        return TIME_OFFSET + int(_time.mktime(lm))
    else:
        return _mktime(lm)

def test_mktime():
    print()
    print("test_mktime():")
    lm=(2000, 1, 1, 1, 0, 0, 5, 1, 0); t=946684800; t_=mktime(lm); print(lm, t, t_, t==t_)
    print("test_mktime:")
    lm=(2022, 3, 27, 1, 59, 59, 6, 86, 0); t=1648342799; t_=mktime(lm); print(lm, t, t_, t==t_)
    lm=(2022, 3, 27, 3, 0, 0, 6, 86, 1); t=1648342800; t_=mktime(lm); print(lm, t, t_, t==t_)
    lm=(2022, 3, 27, 3, 0, 1, 6, 86, 1); t=1648342801; t_=mktime(lm); print(lm, t, t_, t==t_)
    print("test_mktime():")
    lm=(2022, 10, 30, 2, 59, 59, 6, 303, 1); t=1667091599; t_=mktime(lm); print(lm, t, t_, t==t_)
    lm=(2022, 10, 30, 2, 0, 0, 6, 303, 0); t=1667091600; t_=mktime(lm); print(lm, t, t_, t==t_)
    lm=(2022, 10, 30, 2, 0, 1, 6, 303, 0); t=1667091601; t_=mktime(lm); print(lm, t, t_, t==t_)
    print("test_mktime():")
    lm=(2038, 1, 19, 4, 14, 7, 1, 19, 0); t=2147483647; t_=mktime(lm); print(lm, t, t_, t==t_)

if __name__=="__main__": test_mktime()
