import sys, os
import configparser


def default_opts():
    """
    Return a dict filled with default options for the program.
    """
    opts = {
            "downloadPath" : os.getenv( "HOME" ),
            "profile" : "auto",
            "fallback" : ["auto"],
            "duplicates" : False,
            "mode" : "system",
            "externalPath" : "none",
            }
    
    return( opts )

def config_data_path():
    """
    Returns the full path (str) to the program's configuration data directory.
    """
    if sys.platform == "win32" or sys.platform == "win64":
        path = "%s/qytdl" % os.environ[ "APPDATA" ]
    else:
        path = "%s/.config/qytdl" % os.path.expanduser( '~' )

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


def config_path():
    """
    Returns full path (str) to the program's configuration file.
    """

    if sys.platform == "win32" or sys.platform == "win64":
        cfg = "%s\\qytdl.cfg" % config_data_path()
    else:
        cfg = "%s/qytdl.cfg" % config_data_path()

    return( cfg )


def write_config( opts ):


    try:
        cfg = configparser.ConfigParser( allow_no_value = True )
        cfg.read( config_path() )

        userPath = os.path.expanduser( '~' )


        ##  Download directory
        cfg[ "DEFAULT" ] = {
                "# Absolute path to directory where downloads are saved" : None,
                "download_path" : opts.get( "downloadPath", userPath ),
                "\n# Absolute path to youtube-dl executable, if needed" : None,
                "external_path" : opts.get( "externalPath", "none" ),
                "\n# Allow duplicate URLs to be inserted into queue" : None,
                "allow_duplicates" : opts.get( "allowDuplicates", False ),
                "\n# Mode used to call youtube-dl (overriden by profiles)" : None,
                "# system: use libraries called from program (default)" : None,
                "# internal: use libraries distributed with program" : None,
                "# external: use external youtube-dl executable" : None,
                "mode" : opts.get( "mode", "system" )
                }

        #   Build the fallbacks string
        fbStr = ""
        if len( opts[ "fallback" ] ) > 0:
            if len( opts[ "fallback" ] ) == 1:
                fbStr = opts[ "fallback" ][0]
            else:
                for fb in opts[ "fallback" ][:-1]:
                    fbStr += ( "%s " % fb )
                fbStr += opts[ "fallback" ][-1]
        else:
            fbStr = "auto"


        cfg[ "Profiles" ] = {
                "# Default profile" : None,
                "profile" : opts.get( "profile", "auto" ),
                "\n# Fallback profiles (profile IDs separated by spaces)" : None,
                "fallback" : fbStr
                }

        ##  Write it to disk
        fp = open( config_path(), 'w' )
        cfg.write( fp )
        fp.close()

    except PermissionError:
        print( "ERROR:  Cannot write to '%s'." % config_path() )
        print( "Unable to create settings file, cannot save preferences." )



def get_option( line ):
    s = line.partition( '=' )[2].partition( '\n' )[0]
    s = s.replace( '"', '' )

    return( s )


def read_options( opts ):

    cfg = configparser.ConfigParser( allow_no_value = True )
    cfg.read( config_path() )

    userPath = os.path.expanduser( '~' )

    ##  Default section
    section = cfg[ "DEFAULT" ]
    opts[ "downloadPath" ] = section.get( "download_path", userPath )
    opts[ "externalPath" ] = section.get( "external_path", "none" )
    opts[ "duplicates" ] = section.get( "allow_duplicates", False )
    opts[ "mode" ] = section.get( "mode", "system" )

    ##  Profiles section
    section = cfg[ "Profiles" ]
    opts[ "profile" ] = section.get( "profile", "auto" )
    opts[ "fallback" ] = []

    fbStr = section.get( "fallback", "auto" )
    fbStr.replace( ',', '', -1 )
    for fb in fbStr.split():
        opts[ "fallback" ].append( fb )



def read_config():

    opts = default_opts()

    if not os.path.exists( config_path() ):
        write_config( opts )

    try:
        read_options( opts )

    except FileNotFoundError:
        write_config( opts )

    except PermissionError:
        print( "ERROR:  Cannot read from '%s'." % config_path() )
        print( "Unable to restore settings" )


    return( opts )
