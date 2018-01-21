from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, qApp, QMessageBox )
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QAction

from mainWidget import MainWidget
#from aboutWidget import AboutWidget

from util import *
from icons import Icons
from config import *


class MainWindow( QMainWindow ):

    opts = read_config()
    urls = []

    def __init__( self ):
        super().__init__()

        self.init_UI()


    def init_UI( self ):
        self.mainWidget = MainWidget( self )

        self.statusBar()
        self.build_menu_bar()

        self.setCentralWidget( self.mainWidget )

        self.resize( WINDOW_WIDTH, WINDOW_HEIGHT )
        self.center_window()
        self.setWindowTitle( "qYoutube-DL" )
        self.show()


    def center_window( self ):
        f = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        f.moveCenter( center )
        self.move( f.topLeft() )

    
    def build_menu_bar( self ):

        get_icon = Icons().get_icon

        ########  Actions

        ##  Save
        saveAction = QAction( QIcon( get_icon( "document-save" )), "&Save",self)
        saveAction.setShortcut( "Ctrl+S" )
        saveAction.setStatusTip( "Save current settings" )
        saveAction.triggered.connect( self.save_settings )

        ##  Exit
        exitAction = QAction( QIcon( get_icon( "application-exit")),
                "&Exit", self )
        exitAction.setShortcut( "Ctrl+Q" )
        exitAction.setStatusTip( "Exit the application" )
        exitAction.triggered.connect( qApp.quit )

        ##  Go
        goAction = QAction( QIcon( get_icon( "go-next")), "Download URLs", self)
        goAction.setShortcut( "Return" )
        goAction.setStatusTip( "Download current URL list" )
        goAction.triggered.connect( self.mainWidget.start_download )

        ##  Paste
        pasteAction = QAction( QIcon( get_icon( "edit-paste")), "&Paste", self)
        pasteAction.setShortcut( "Ctrl+V" )
        pasteAction.setStatusTip( "Add URL from clipboard" )
        pasteAction.triggered.connect( self.mainWidget.quick_add_item )

        ##  Set destination
        setDestAction = QAction( QIcon( get_icon( "folder-open")),
                "Set &Download directory", self )
        setDestAction.setShortcut( "Ctrl+D" )
        setDestAction.setStatusTip( "Choose your download directory" )
        setDestAction.triggered.connect( self.mainWidget.set_destination )

        ##  Allow duplicates
        self.dupeAction = QAction( "Allow duplicates", self )
        self.dupeAction.setStatusTip( "Allow duplicate URLs in queue" )
        self.dupeAction.setCheckable( True )
        self.dupeAction.triggered.connect( self.check_dupe_box )


        ##  About action
        aboutAction = QAction( QIcon( get_icon( "help-about" )), "&About", self)
        aboutAction.setStatusTip( "Information about the program" )
        aboutAction.triggered.connect( self.about )


        ##  Create the menubar
        menuBar = self.menuBar()

        ##  Create file menu
        fileMenu = menuBar.addMenu( "&File" )
        fileMenu.addAction( saveAction )
        fileMenu.addAction( goAction )
        fileMenu.addSeparator()
        fileMenu.addAction( exitAction )

        editMenu = menuBar.addMenu( "&Edit" )
        editMenu.addAction( pasteAction )
        editMenu.addAction( setDestAction )
        editMenu.addAction( self.dupeAction )

        helpMenu = menuBar.addMenu( "&Help" )
        helpMenu.addAction( aboutAction )


    def load_urls( self, urls ):
        self.mainWidget.load_urls( urls )


    def write_config( self ):

        self.opts[ "downloadDir" ] = self.mainWidget.destEdit.text()
        self.opts[ "duplicates" ] = self.dupeAction.isChecked()

        write_config( self.opts )


    def save_settings( self ):

        self.write_config()
        self.statusBar().showMessage( "Settings saved", 2000 )


    def check_dupe_box( self ):
        self.opts[ "duplicates" ] = self.dupeAction.isChecked()
        self.save_settings()


    def about( self ):
        aboutStr = """
        qYoutube-DL is a basic PyQt5 frontend to Youtube-DL.

        Version:    0.92
        License:    GPLv3 - https://www.gnu.org/licenses/gpl-3.0.txt
        Author:     James Hendrie - hendrie.james@gmail.com
        Git:        https://github.com/jahendrie/qytdl
        """
        msg = QMessageBox.about( self, "About qYoutube-DL", aboutStr )
