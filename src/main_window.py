from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, qApp, QFileDialog,
        QMessageBox )
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QAction

from main_widget import MainWidget
#from aboutWidget import AboutWidget

import breeze_resources

from util import *
from icons import Icons
from config import *
from profile import *


class MainWindow( QMainWindow ):

    opts = read_config()
    profiles = read_profiles()
    urls = []

    def __init__( self ):
        super().__init__()

        self.icon_paths()

        self.init_UI()


    def icon_paths( self ):

        self.defaultIconTheme = QIcon.themeName()
        
        iconPaths = QIcon.themeSearchPaths()
        iconPaths.append( icon_path() )

        QIcon.setThemeSearchPaths( iconPaths )

        QIcon.setFallbackSearchPaths( [ icon_path( "default" ) ] )
        QIcon.setFallbackThemeName( "default" )

        #QIcon.setThemeName( "default" )


    def init_UI( self ):

        ##  Set the theme
        self.set_stylesheet( self.opts[ "theme" ] )

        self.profiles = read_profiles()
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

        ##  Is this a system install?
        sysInstall = ( os.path.expanduser( '~' ) in sys.argv[0] )

        ########  Actions

        ##  Save
        saveAction = QAction( QIcon( get_icon( "document-save-symbolic", sysInstall )),
                "&Save Settings",self)
        saveAction.setShortcut( "Ctrl+S" )
        saveAction.setStatusTip( "Save current settings" )
        saveAction.triggered.connect( self.save_settings )

        ##  Import playlist
        importAction = QAction( QIcon( get_icon( "document-open-symbolic", sysInstall )),
                "&Import URLs", self )
        importAction.setShortcut( "Ctrl+I" )
        importAction.setStatusTip( "Import a saved list of URLs" )
        importAction.triggered.connect( self.import_urls )

        ##  Export playlist
        exportAction = QAction( QIcon( get_icon( "document-save-symbolic", sysInstall )),
                "&Export URLs", self )
        exportAction.setShortcut( "Ctrl+E" )
        exportAction.setStatusTip( "Export URLs to a text file" )
        exportAction.triggered.connect( self.export_urls )

        ##  Exit
        exitAction = QAction( QIcon( get_icon( "application-exit-symbolic", sysInstall)),
                "&Exit", self )
        exitAction.setShortcut( "Ctrl+Q" )
        exitAction.setStatusTip( "Exit the application" )
        exitAction.triggered.connect( qApp.quit )

        ##  Go
        goAction = QAction( QIcon( get_icon( "go-next-symbolic", sysInstall )),
                "Download URLs", self)
        goAction.setShortcut( "Return" )
        goAction.setStatusTip( "Download current URL list" )
        goAction.triggered.connect( self.mainWidget.start_download )

        ##  Paste
        pasteAction = QAction( QIcon( get_icon( "edit-paste-symbolic", sysInstall )),
                "&Paste", self)
        pasteAction.setShortcut( "Ctrl+V" )
        pasteAction.setStatusTip( "Add URL from clipboard" )
        pasteAction.triggered.connect( self.mainWidget.quick_add_item )

        ##  Set destination
        setDestAction = QAction( QIcon( get_icon( "document-open-symbolic", sysInstall )),
                "Set &Download directory", self )
        setDestAction.setShortcut( "Ctrl+D" )
        setDestAction.setStatusTip( "Choose your download directory" )
        setDestAction.triggered.connect( self.mainWidget.set_destination )

        ##  Allow duplicates
        self.dupeAction = QAction( "Allow duplicates", self )
        self.dupeAction.setStatusTip( "Allow duplicate URLs in queue" )
        self.dupeAction.setCheckable( True )
        if self.opts[ "duplicates" ] == "true":
            self.dupeAction.setChecked( True )
        self.dupeAction.triggered.connect( self.check_dupe_box )

        ##  New folder for playlists
        self.playlistFolderAction = QAction( "New folder for playlists", self )
        self.playlistFolderAction.setStatusTip(
                "Create a new folder for every playlist downloaded" )
        self.playlistFolderAction.setCheckable( True )
        if self.opts[ "playlistFolder" ] == "true":
            self.playlistFolderAction.setChecked( True )
        self.playlistFolderAction.triggered.connect( self.check_playlist_dir_box )


        ##  About action
        aboutAction = QAction( QIcon( get_icon( "help-about-symbolic", sysInstall )),
                "&About", self)
        aboutAction.setStatusTip( "Information about the program" )
        aboutAction.triggered.connect( self.about )

        ##  ======  Theme actions
        ##  System default theme
        defaultThemeAction = QAction( "Default", self )
        defaultThemeAction.setStatusTip( "Set theme to system default" )
        defaultThemeAction.triggered.connect( self.toggle_theme_default )

        ##  Light theme
        lightThemeAction = QAction( "Light theme", self )
        lightThemeAction.setStatusTip( "Use a light theme" )
        lightThemeAction.triggered.connect( self.toggle_theme_light )

        ##  Dark theme
        darkThemeAction = QAction( "Dark theme", self )
        darkThemeAction.setStatusTip( "Use a dark theme" )
        darkThemeAction.triggered.connect( self.toggle_theme_dark )



        ##  Create the menubar
        menuBar = self.menuBar()

        ##  Create file menu
        fileMenu = menuBar.addMenu( "&File" )
        fileMenu.addAction( saveAction )
        fileMenu.addAction( exportAction )
        fileMenu.addSeparator()
        fileMenu.addAction( importAction )
        fileMenu.addSeparator()
        fileMenu.addAction( goAction )
        fileMenu.addSeparator()
        fileMenu.addAction( exitAction )

        ##  Edit Menu
        editMenu = menuBar.addMenu( "&Edit" )
        editMenu.addAction( pasteAction )

        ##  Settins Menu
        settingsMenu = menuBar.addMenu( "&Settings" )
        themesMenu = settingsMenu.addMenu( "Theme" )
        settingsMenu.addSeparator()
        settingsMenu.addAction( setDestAction )
        settingsMenu.addSeparator()
        settingsMenu.addAction( self.dupeAction )
        settingsMenu.addAction( self.playlistFolderAction )

        ##  Themes submenu
        themesMenu.addAction( defaultThemeAction )
        themesMenu.addAction( lightThemeAction )
        themesMenu.addAction( darkThemeAction )

        ##  Help menu
        helpMenu = menuBar.addMenu( "&Help" )
        helpMenu.addAction( aboutAction )


    def import_urls( self ):

        dDir = self.mainWidget.destEdit.text()

        filename, blank = QFileDialog.getOpenFileName( self, "Import URLs", dDir )
        if filename != "":
            try:

                fin = open( filename, "r" )
                rawUrls = fin.readlines()
                fin.close()

                urls = []
                for r in rawUrls:
                    urls.append( r.strip() )

                self.load_urls( urls )

                self.statusBar().showMessage( "URLs imported", 2000 )

            except ( OSError, PermissionError, FileNotFoundError ):
                print( "ERROR:  Cannot read from '%s'!  Unable to load URLs" %
                        filename )

    def export_urls( self ):

        dDir = self.mainWidget.destEdit.text()
        
        filename, blank = QFileDialog.getSaveFileName( self, "Export URLs", dDir)
        if filename != "":
            try:
                urls = self.mainWidget.get_urls()

                fout = open( filename, "w" )
                fout.writelines( urls )
                fout.close()

                self.statusBar().showMessage( "URLs exported", 2000 )

            except ( OSError, PermissionError, FileNotFoundError ):
                print( "ERROR:  Cannot write to '%s'!  Unable to export URLs" %
                        filename )

    def load_urls( self, urls ):
        self.mainWidget.load_urls( urls )


    def write_config( self ):

        self.opts[ "downloadPath" ] = self.mainWidget.destEdit.text()
        self.opts[ "duplicates" ] = str( self.dupeAction.isChecked() ).lower()

        boolStr = str( self.playlistFolderAction.isChecked() ).lower()
        self.opts[ "playlistFolder" ] = boolStr

        write_config( self.opts )


    def save_settings( self ):

        self.write_config()
        self.statusBar().showMessage( "Settings saved", 2000 )


    def check_dupe_box( self ):
        self.opts[ "duplicates" ] = str( self.dupeAction.isChecked() ).lower()
        self.save_settings()

    def check_playlist_dir_box( self ):
        boolStr = str( self.playlistFolderAction.isChecked() ).lower()
        self.opts[ "playlistFolder" ] = boolStr
        self.save_settings()


    def about( self ):
        aboutStr = """
        qYoutube-DL is a basic PyQt5 frontend to Youtube-DL.

        Version:    %s
        License:    GPLv3 - https://www.gnu.org/licenses/gpl-3.0.txt
        Author:     James Hendrie - hendrie.james@gmail.com
        Git:        https://github.com/jahendrie/qytdl
        """ % qytdl_version()
        msg = QMessageBox.about( self, "About qYoutube-DL", aboutStr )



    def toggle_theme_default( self ):
        self.set_stylesheet()
        self.opts[ "theme" ] = "default"
        self.write_config()

    def toggle_theme_light( self ):
        self.set_stylesheet( "light" )
        self.opts[ "theme" ] = "light"
        self.write_config()

    def toggle_theme_dark( self ):
        self.set_stylesheet( "dark" )
        self.opts[ "theme" ] = "dark"
        self.write_config()

    def set_stylesheet( self, ssStr="" ):
        if ssStr == "dark" or ssStr == "light":
            ssFile = open( stylesheets_path( "%s.qss" % ssStr ), "r" )
            self.setStyleSheet( ssFile.read() )
            ssFile.close()
            QIcon.setThemeName( ssStr )

        else:
            self.setStyleSheet( "" )
            QIcon.setThemeName( self.defaultIconTheme )

