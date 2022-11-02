from __future__ import unicode_literals
import sys, os
import youtube_dl
from youtube_dl.utils import DownloadError

####    RE-ENABLE if you want to enable possible internal YDL
#import internal_ydl
#from internal_ydl.utils import DownloadError

if sys.platform == "win32" or sys.platform == "win64":
    import ctypes

##  Globals
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800


def qytdl_version():
    return( "1.6" )

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

    iconPath = os.path.join( get_data_dir(), "icons" )

    if systemInstall:
        return( "/usr/share/qytdl/data/icons" )

    if filename != "":
        return( os.path.join( iconPath, filename ))
    else:
        return( iconPath )

def image_path( filename = "" ):

    imagePath = os.path.join( get_data_dir(), "images" )

    if filename != "":
        return( os.path.join( imagePath, filename ))
    else:
        return( imagePath )


def stylesheets_path( filename = "" ):
    ssPath = os.path.join( get_data_dir(), "stylesheets" )

    if filename != "":
        return( os.path.join( ssPath, filename ))
    else:
        return( ssPath )


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


def generate_dirname( cwd, path ):

    ##  We'll need a mutable string I guess
    baseDirName = path
    dirName = baseDirName

    ##  If needed, increment until we get a useful directory name
    num = 0
    while os.path.exists( os.path.join( cwd, dirName )):
        dirName = "%s.%d" % ( baseDirName, num )
        num += 1

    return( os.path.join( cwd, dirName) )


def boolify( B ):
    b = B.lower()
    if b == "true" or b == "yes" or b == "1":
        return( True )
    elif b == "false" or b == "no" or b == "0":
        return( False )
    else:
        return( B )
