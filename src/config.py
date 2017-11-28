import sys, os


def default_opts():
    opts = {
            "downloadDir" : os.getenv( "HOME" ),
            "format" : "22"
            }
    
    return( opts )

def config_path():
    if sys.platform == "win32" or sys.platform == "win64":
        path = "%s/qytdl" % os.getenv( "APPDATA" )
    else:
        path = "%s/.config/qytdl" % os.getenv( "HOME" )

    if not os.path.exists( path ):
        try:
            os.makedirs( path )
            return( path )

        except PermissionError:
            print( "ERROR:  Cannot create directory '%s'." % path )
            print( "Unable to save settings." )
            return( "" )
    else:
        return( path )


def config_file():

    if sys.platform == "win32" or sys.platform == "win64":
        cfg = "%s\\config.txt" % config_path()
    else:
        cfg = "%s/config.txt" % config_path()

    return( cfg )


def create_config( path, opts ):

    try:
        fp = open( path, "w" )

        ##  Download directory
        fp.write( "# Path to directory where videos are saved\n\n" )
        fp.write( "download_dir=%s\n\n" % opts[ "downloadDir" ] )

        ##  Format code
        fp.write("# Desired format code " )
        fp.write( "(use youtube-dl -F $URL to see format codes)\n")
        fp.write( "# default is 0 (autodetect best)\n" )
        fp.write( "# 22 = 720p mp4\n\n" )
        fp.write( "format=%s\n\n" % opts[ "format" ] )

        fp.close()

    except PermissionError:
        print( "ERROR:  Cannot write to '%s'." % path )
        print( "Unable to create settings file, cannot save preferences." )



def get_option( line ):
    s = line.partition( '=' )[2].partition( '\n' )[0]
    s = s.replace( '"', '' )

    return( s )


def read_options( fp, opts ):

    lines = fp.readlines()
    for line in lines:
        if line[0] == '#':
            continue

        if "download_dir=" in line:
            dDir = get_option( line )
            opts[ "downloadDir" ] = dDir

        if "format=" in line:
            fmt = get_option( line )
            opts[ "format" ] = fmt


def read_config():

    opts = default_opts()
    cfg = config_file()

    try:
        fp = open( cfg, "r" )
        read_options( fp, opts )
        fp.close()

    except FileNotFoundError:
        create_config( path, opts )

    except PermissionError:
        print( "ERROR:  Cannot read from '%s'." % path )
        print( "Unable to restore settings" )


    return( opts )



def write_config( opts ):

    cfg = config_file()
    create_config( cfg, opts )
