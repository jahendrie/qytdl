from __future__ import unicode_literals
import sys, os
import youtube_dl
from youtube_dl.utils import DownloadError

import internal_ydl
from internal_ydl.utils import DownloadError

##  Globals
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800



def system_install_path():
    return( "/usr/share/qytdl" )


def get_data_dir():

    ##  If they're on windows
    if sys.platform == "win32" or sys.platform == "win64":
        dataDir = "%s\\data" % (
                os.path.abspath( "%s\\.." % os.path.dirname( sys.argv[0] )) )

    ##  Otherwise, we assume linux / unix
    else:
        dataDir = "%s/data" % (
                os.path.abspath( "%s/.." % os.path.dirname( sys.argv[0] )) )

    return( dataDir )


def icon_path( filename = "", systemInstall = False ):

    if systemInstall:
        return( "/usr/share/qytdl/data/icons" )

    ##  Check for Windows
    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\icons\\%s" % ( get_data_dir(), filename ))

    ##  Otherwise, we assume linux / unix
    else:
        return( "%s/icons/%s" % ( get_data_dir(), filename ))


def image_path( filename = "" ):

    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\images\\%s" % ( get_data_dir(), filename ))

    else:
        return( "%s/images/%s" % ( get_data_dir(), filename ))


def downloads_path():


    home = os.getenv( "HOME" )
    winPaths = ( "%s\\Downloads" % home, "%s\\downloads" % home )
    linPaths = ( "%s/Downloads" % home, "%s/downloads" % home )


    if sys.platform == "win32" or sys.platform == "win64":
        return( sys_downloads_path( winPaths ))

    else:
        return( sys_downloads_path( linPaths ))


def sys_downloads_path( paths ):
        for p in paths:
            if os.path.exists( p ):
                return( p )
        return( home )


def get_free_space( path ):
    """Return folder/drive free space (in MiB)."""

    try:
        mib = 0
        if sys.platform == "win32" or sys.platform == "win64":
            freeBytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW( ctypes.c_wchar_p( path),
                    None, None, ctypes.pointer( freeBytes ))
            mib = freeBytes.value / 1024.0 / 1024.0
        else:
            st = os.statvfs( path )
            mib = st.f_bavail * st.f_frsize / 1024.0 / 1024.0

        if mib > 1024:
            return( "%.02lf GiB" % ( mib / 1024.0 ) )
        else:
            return( "%d MiB" % mib )

    except ( PermissionError, FileNotFoundError, AttributeError ):
        return( "UNKNOWN MiB" )


def old_get_free_space( path ):

    try:
        s = os.statvfs( path )
    except ( PermissionError, FileNotFoundError, AttributeError ):
        return( "UNKNOWN" )

    suffices = ( 'bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB' )
    suffix = 0
    freeSpace = s.f_frsize * s.f_bavail

    ##  Get it down to a sane number
    while( freeSpace > 1024 ):
        freeSpace /= 1024
        suffix += 1

    ##  Just to be safe, I guess
    if suffix >= len( suffices ):
        freeSpace = s.f_frsize * s.f_bavail
        suffix = 0

    if suffix > 0:
        freeSpaceStr = "%.02f %s" % ( freeSpace, suffices[ suffix ] )
    else:
        freeSpaceStr = "%d bytes" % freeSpace

    return( freeSpaceStr )
