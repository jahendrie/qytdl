#!/usr/bin/env python3
#===============================================================================
#   qytdl   |   version 1.4     |   GPL v3      |   2021-10-25
#   James Hendrie               |   hendrie.james@gmail.com
#
#   PyQt5 front-end to Youtube-DL.
#
#   ---------------------------------------------------------------------------
#
#    Copyright (C) 2017-2020 James Hendrie
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#===============================================================================

import sys, os
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

from PyQt5.QtGui import QIcon
from icons import Icons

from util import qytdl_version


def print_version():
    print( "qytdl, version %s" % qytdl_version() )
    print( "James Hendrie <hendrie.james@gmail.com>" )

def print_usage():
    print( "qytdl [OPTION/URLs]" )


def print_help():
    print_usage()
    print( "\nThis program is a minimal frontend to Youtube-DL.  With it, you" )
    print( "can build a queue of URLs for Youtube-DL to download to a specified" )
    print( "directory." )
    print( "" )
    print( "Options:" )
    print( " -h or --help\t\tThis help text" )
    print( " -V or --version\tVersion and author info" )
    print( " -d or --debug\t\tEnable debug mode (verbose output)" )
    print( " - or --stdin\t\tRead URLs from stdin" )


def main():

    urls = []
    debug = False

    if len( sys.argv ) > 1:

        ##  If they want help
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            return( 0 )

        elif sys.argv[1] == "-V" or sys.argv[1] == "--version":
            print_version()
            return( 0 )

        ##  If they're reading URLs from stdin
        elif sys.argv[1] == '-' or sys.argv[1] == "--stdin":
            rawUrls = sys.stdin.readlines()
            for r in rawUrls:
                urls.append( r.replace( ' ', '\n', -1 ).strip() )

        ##  If they're trying to use debug mode
        elif sys.argv[1] == "-d" or sys.argv[1] == "--debug":
            debug = True

        ##  If they're importing URLs
        elif os.path.exists( sys.argv[1] ):
            try:

                fin = open( sys.argv[1], "r" )
                rawUrls = fin.readlines()
                fin.close()

                for r in rawUrls:
                    urls.append( r.strip() )


            except ( OSError, PermissionError, FileNotFoundError ):
                print( "ERROR:  Cannot read from '%s'!  Aborting." %
                        sys.argv[1] )
                sys.exit( 1 )

        ##  Running a bunch of URLs as args
        else:
            for arg in sys.argv[1:]:
                urls.append( arg )


    app = QApplication( sys.argv )

    sysInstall = ( os.path.expanduser( '~' ) in sys.argv[0] )
    app.setWindowIcon( Icons().get_icon( "application-icon", sysInstall ))


    win = MainWindow( debug )
    if debug:
        print( "(Debug mode)" )

    if len( urls ) > 0:
        win.load_urls( urls )

    sys.exit( app.exec_() )


if __name__ == "__main__":
    main()
