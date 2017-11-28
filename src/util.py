import sys, os

##  Globals
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800



def system_install_path():
    return( "/opt/qytdl" )


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
