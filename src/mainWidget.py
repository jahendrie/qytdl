import os

from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
        QPushButton, QListWidget, QLineEdit, QLabel, QInputDialog,
        QProgressBar, QComboBox )

from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.Qt import QApplication
from PyQt5.QtCore import Qt

from icons import Icons
from util import *

import sip

import subprocess
#from PyQt5.QtCore import Qt


class MainWidget( QWidget ):

    def __init__( self, parent = None ):

        super().__init__()
        self.parent = parent
        self.init_UI()



    def connect_all( self ):

        self.destButton.clicked.connect( self.set_destination )
        self.formatBox.currentIndexChanged.connect( self.set_format )
        self.addButton.clicked.connect( self.add_item )
        self.quickAddButton.clicked.connect( self.quick_add_item )
        self.removeButton.clicked.connect( self.remove_item )
        self.goButton.clicked.connect( self.start_download )

    
    def disconnect_all( self ):

        self.destButton.clicked.disconnect()
        self.formatBox.currentIndexChanged.disconnect()
        self.addButton.clicked.disconnect()
        self.quickAddButton.clicked.disconnect()
        self.removeButton.clicked.disconnect()
        self.goButton.clicked.disconnect()


    def disable_stuff( self, disabled ):

        self.destButton.setDisabled( disabled )
        self.addButton.setDisabled( disabled )
        self.quickAddButton.setDisabled( disabled )
        self.removeButton.setDisabled( disabled )
        self.goButton.setDisabled( disabled )

        self.destEdit.setDisabled( disabled )
        self.listWidget.setDisabled( disabled )
        self.formatBox.setDisabled( disabled )




    def init_UI( self ):

        ##  Just to make life easier
        get_icon = Icons().get_icon

        ##  Start all of the widgets
        self.listWidget = QListWidget( self )

        ##  The Destination button
        self.destButton = QPushButton( QIcon( get_icon( "folder-open" )), "" )
        self.destButton.setToolTip( "Choose download directory" )

        ##  Destination path edit
        self.destEdit = QLineEdit( self.parent.opts[ "downloadDir" ] )
        self.destEdit.setToolTip( "Path to destination directory" )

        ##  The formats
        self.formatBox = QComboBox( self )
        self.init_format_box()


        ##  The other buttons
        self.addButton = QPushButton( QIcon( get_icon( "list-add" )), "" )
        self.addButton.setToolTip( "Add a URL manually" )

        self.removeButton = QPushButton( QIcon( get_icon( "list-remove" )),"" )
        self.removeButton.setToolTip( "Remove selected URL" )

        self.quickAddButton = QPushButton(QIcon( get_icon( "edit-paste" )), "")
        self.quickAddButton.setToolTip("Add a URL directly from the clipboard" )

        self.goButton = QPushButton( QIcon( get_icon( "go-next" )), "" )
        self.goButton.setToolTip( "Download the list of URLs" )

        ##  The progress bar
        self.progressBar = QProgressBar( self )
        self.progressBar.setTextVisible( False )

        ##  The free space label
        self.freeLabel = QLabel( self )
        self.update_free_label()


        ##  Connect it up
        self.connect_all()

        ##  The destination layout
        dest = QHBoxLayout()
        dest.addWidget( self.destButton )
        dest.addWidget( self.destEdit, 1 )

        ##  Dest + formats
        dBox = QVBoxLayout()
        dBox.addLayout( dest, 1 )
        dBox.addWidget( self.formatBox )

        ##  Free space
        fBox = QHBoxLayout()
        fBox.addWidget( QWidget(), 1 )
        fBox.addWidget( self.freeLabel )


        ##  Buttons layout
        hbox = QHBoxLayout()
        hbox.addWidget( QWidget(), 1 )
        hbox.addWidget( self.addButton )
        hbox.addWidget( self.quickAddButton )
        hbox.addWidget( self.removeButton )
        hbox.addWidget( self.goButton )

        ##  List label
        listLabel = QHBoxLayout()
        listLabel.addWidget( QLabel( "URLs:" ))

        ##  List
        lBox = QVBoxLayout()
        lBox.addLayout( listLabel )
        lBox.addWidget( self.listWidget, 1 )


        ##  Lay 'em down by the fi-yah
        vbox = QVBoxLayout()
        vbox.addLayout( dBox )
        vbox.addLayout( lBox )
        vbox.addLayout( hbox )
        vbox.addWidget( self.progressBar )
        vbox.addLayout( fBox )

        ##  Set the layout
        self.setLayout( vbox )



    def init_format_box( self ):

        ##  Add the items
        self.formatBox.addItem( "Best (Auto)", "0" )
        self.formatBox.addItem( "720p MP4", "22" )

        ##  Set the initial value
        idx = self.formatBox.findData( self.parent.opts[ "format" ] )
        self.formatBox.setCurrentIndex( idx )

        ##  Misc
        self.formatBox.setToolTip( "Desired format for video downloads" )


    def set_format( self ):

        fmt = self.formatBox.currentData()
        self.parent.opts[ "format" ] = fmt


    def load_urls( self, urls ):
        for url in urls:
            self.listWidget.addItem( url )


    def add_item( self ):
        url, ok = QInputDialog.getText( self, "URL:", "URL:",
                QLineEdit.Normal, "" )

        if ok and url != "":
            self.add_url_to_list( url )


    def quick_add_item( self ):
        url = QApplication.clipboard().text()
        if url != "":
            self.add_url_to_list( url )



    def add_url_to_list( self, url ):

        if self.parent.opts[ "duplicates" ] == True:
            self.listWidget.addItem( url )

        else:
            inList = False
            for i in range( self.listWidget.count() ):
                li = self.listWidget.item( i )
                if li != None and li.text() == url:
                    inList = True
                    break

            if not inList:
                self.listWidget.addItem( url )


    def remove_item( self ):
        li = self.listWidget.currentItem()
        if li != None:
            sip.delete( li )


    def write_config( self ):

        self.parent.write_config()



    def start_download( self ):

        opts = self.parent.opts

        self.write_config()

        #self.setDisabled( True )
        self.disable_stuff( True )

        status = self.parent.statusBar()

        urls = []
        for i in range( self.listWidget.count() ):
            li = self.listWidget.item( i )
            urls.append( li.text() )




        totalUrls = len( urls )
        self.progressBar.setMaximum( totalUrls )

        currentUrl = 0
        if totalUrls > 0:


            ###  Formats
            ###
            ###  22  720p mp4 (I guess?)
            ###  136 720p mp4
            ###  137 1080p mp4

            cmdDefault = [ "youtube-dl",
                    "--no-mtime",
                    "-o%s/%%(title)s.%%(ext)s" % opts[ "downloadDir" ] ]

            cmdBase = []

            if opts[ "format" ] == "0":
                cmdBase = cmdDefault
            else:
                cmdBase = [ "youtube-dl",
                        "--no-mtime",
                        "-f", "%s" % opts[ "format" ],
                        "-o%s/%%(title)s.%%(ext)s" % opts[ "downloadDir" ]]
            
            ##  Change the cursor
            QApplication.setOverrideCursor( Qt.WaitCursor )

            for url in urls:

                status.showMessage(
                        "Downloading %d/%d, please wait..." %
                        ( currentUrl + 1, totalUrls ))

                self.progressBar.setValue( currentUrl + 1 )

                cmd = cmdBase
                cmd.append( url )

                ret = subprocess.call( cmd )
                if( ret == 1 ):
                    cmd = cmdDefault
                    cmd.append( url )

                    subprocess.call( cmd )

                currentUrl += 1

                ##  Update the free label
                self.update_free_label()

            ##  Restore old cursor
            QApplication.restoreOverrideCursor()




        self.listWidget.clear()

        self.disable_stuff( False )
        #self.setDisabled( False )

        self.progressBar.setValue( 0 )
        status.showMessage( "All done!", 2000 )


    def set_destination( self ):

        downloadsDir = QFileDialog.getExistingDirectory( self,
                "Choose download directory...", "%s" % self.destEdit.text() )

        if downloadsDir != "":
            self.destEdit.setText( downloadsDir )
            self.parent.opts[ "downloadDir" ] = downloadsDir
            self.update_free_label()



    def update_free_label( self ):
        freeSpace = get_free_space( self.parent.opts[ "downloadDir" ] )
        self.freeLabel.setText( "%s free" % freeSpace )
