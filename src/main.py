#!/usr/bin/env python3
#===============================================================================
#   qytdl   |   version 0.9     |   GPL v3      |   2017-12-22
#   James Hendrie               |   hendrie.james@gmail.com
#
#   PyQt5 front-end to Youtube-DL.
#
#   ---------------------------------------------------------------------------
#
#    Copyright (C) 2017 James Hendrie
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
from mainWindow import MainWindow

from PyQt5.QtGui import QIcon
from icons import Icons


def print_usage():
    print( "qytdl [OPTION] [URLS]" )


def print_help():
    print_usage()
    print( "\nThis program is a minimal frontend to Youtube-DL.  With it, you" )
    print( "can build a queue of URLs for Youtube-DL to download to a specified" )
    print( "directory." )


def main():

    urls = []
    if len( sys.argv ) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            return( 0 )
        else:
            for arg in sys.argv[1:]:
                urls.append( arg )


    app = QApplication( sys.argv )

    app.setWindowIcon( Icons().get_icon( "application-icon", True ))

    win = MainWindow()

    if len( urls ) > 0:
        win.load_urls( urls )

    sys.exit( app.exec_() )


if __name__ == "__main__":
    main()
