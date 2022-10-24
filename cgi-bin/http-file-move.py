#!/usr/bin/python3

"""\
@ECHO OFF

REM https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/more
REM https://ss64.com/nt/more.html
REM https://stackoverflow.com/questions/23729430/how-to-convert-get-method-to-post-method-in-a-bat-file-while-i-am-using-it-unde/23731072#23731072
REM https://www.hanselman.com/blog/forgotten-but-awesome-windows-command-prompt-features

REM set >>t.txt

MOVE /Y "%PATH_TRANSLATED%" ".%QUERY_STRING%"
rem MOVE /Y ".%QUERY_STRING%" "%PATH_TRANSLATED%"

ECHO.Content-Type: text/plain
ECHO.
IF NOT ERRORLEVEL 1 (
ECHO.=OK=
) ELSE (
ECHO.#ER#
)
"""

import sys
import os

print("Content-Type: text/plain", end="\r\n")
print("", end="\r\n")

#print(os.environ)
#for env in os.environ:
#    print(env + '=' + os.environ[env])

#print(os.environ["PATH_TRANSLATED"])
#print(os.environ["QUERY_STRING"])

try:
    src = open(os.environ["PATH_TRANSLATED"], "r")
    text = src.read()
    src.close()
    dst = open('.' + os.environ["QUERY_STRING"], "w")
    dst.write(text)
    dst.close()
    os.remove(os.environ["PATH_TRANSLATED"])
except:
    print("#ER#")
else:
    print("=OK=")

