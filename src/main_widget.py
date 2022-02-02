import os, sys

from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
        QPushButton, QListWidget, QLineEdit, QLabel, QInputDialog,
        QProgressBar, QComboBox, QMenu )

from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.Qt import QApplication, QAction
from PyQt5.QtCore import Qt

from list_widget import ListWidget

from icons import Icons
from util import *
from classes import *

import sip

import subprocess
import importlib
#from PyQt5.QtCore import Qt



class MainWidget( QWidget ):

    def __init__( self, parent = None ):
        super().__init__()
        self.parent = parent
        self.debug = self.parent.debug
        self.profile = None
        self.init_UI()


    def connect_all( self ):

        self.destButton.clicked.connect( self.set_destination )
        self.profileBox.currentIndexChanged.connect( self.set_profile )
        self.addButton.clicked.connect( self.add_item )
        self.quickAddButton.clicked.connect( self.quick_add_item )
        self.removeButton.clicked.connect( self.remove_item )
        self.goButton.clicked.connect( self.start_download )

    
    def disconnect_all( self ):

        self.destButton.clicked.disconnect()
        self.profileBox.currentIndexChanged.disconnect()
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
        self.profileBox.setDisabled( disabled )


    def init_UI( self ):

        ##  Just to make life easier
        get_icon = Icons().get_icon

        ##  Start all of the widgets
        self.listWidget = ListWidget( self )

        ##  The Destination button
        self.destButton = QPushButton( QIcon( get_icon( "folder-open" )), "" )
        self.destButton.setToolTip( "Choose download directory" )

        ##  Destination path edit
        self.destEdit = QLineEdit( self.parent.opts[ "downloadPath" ] )
        self.destEdit.setToolTip( "Path to destination directory" )

        ##  The profiles
        self.profileBox = QComboBox( self )
        self.init_profile_box()


        ##  The other buttons
        self.addButton = QPushButton( QIcon( get_icon( "list-add" )), "" )
        self.addButton.setToolTip( "Add a URL manually" )

        self.removeButton = QPushButton( QIcon( get_icon( "list-remove" )),"" )
        self.removeButton.setToolTip( "Remove selected URL" )

        self.quickAddButton = QPushButton(QIcon( get_icon( "edit-paste" )), "")
        self.quickAddButton.setToolTip("Add a URL directly from the clipboard" )

        self.goButton = QPushButton( QIcon( get_icon( "go-next" )), "" )
        self.goButton.setToolTip( "Download the list of URLs" )

        ##  The current progress bar
        self.currentProgressBar = QProgressBar( self )
        self.currentProgressBar.setTextVisible( False )

        ##  The total progress bar
        self.totalProgressBar = QProgressBar( self )
        self.totalProgressBar.setTextVisible( False )

        ##  The free space label
        self.freeLabel = QLabel( self )
        self.update_free_label()


        ##  Connect it up
        self.connect_all()

        ##  The destination layout
        dest = QHBoxLayout()
        dest.addWidget( self.destButton )
        dest.addWidget( self.destEdit, 1 )

        ##  Dest + profiles
        dBox = QVBoxLayout()
        dBox.addLayout( dest, 1 )
        dBox.addWidget( self.profileBox )

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

        ##  Progress bars
        #currentProgress = QHBoxLayout()
        #currentProgress.addWidget( QLabel( "Current" ))
        #currentProgress.addWidget( self.currentProgressBar )
        #vbox.addLayout( currentProgress )

        #totalProgress = QHBoxLayout()
        #totalProgress.addWidget( QLabel( "Total" ))
        #totalProgress.addWidget( self.totalProgressBar )
        #vbox.addLayout( totalProgress )
        vbox.addWidget( QLabel( "Current" ))
        vbox.addWidget( self.currentProgressBar )
        vbox.addWidget( QLabel( "Total" ))
        vbox.addWidget( self.totalProgressBar )

        vbox.addLayout( fBox )

        ##  Set the layout
        self.setLayout( vbox )



    def init_profile_box( self ):

        ##  Add the items
        profiles = self.parent.profiles
        for key in profiles:
            self.profileBox.addItem( profiles[ key ].name, profiles[ key ].id )

        ##  Set the initial value
        idx = self.profileBox.findData( self.parent.opts[ "profile" ] )
        self.profileBox.setCurrentIndex( idx )

        ##  Set the current profile
        if self.parent.profiles != None and len( self.parent.profiles ) > 0:
            self.profile = self.parent.profiles[ self.parent.opts[ "profile" ] ]

        ##  Misc
        self.profileBox.setToolTip( "Desired profile for video downloads" )


    def set_profile( self ):

        pro = self.profileBox.currentData()
        self.parent.opts[ "profile" ] = pro
        self.profile = self.parent.profiles[ pro ]


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


    def is_duplicate( self, text ):
        inList = False
        for i in range( self.listWidget.count() ):
            li = self.listWidget.item( i )
            if li != None and li.text() == text:
                inList = True
                break

        return( inList )


    def add_url_to_list( self, url ):

        if self.parent.opts[ "duplicates" ] == "true":
            self.listWidget.addItem( url )

        elif not self.is_duplicate( url ):
            self.listWidget.addItem( url )


    def remove_item( self ):
        li = self.listWidget.currentItem()
        if li != None:
            sip.delete( li )


    def edit_item( self ):
        li = self.listWidget.currentItem()
        if li != None:
            url = li.text()
            url, ok = QInputDialog.getText( self, "URL:", "URL:",
                    QLineEdit.Normal, url )

            if ok:
                if self.parent.opts[ "duplicates" ] == "true":
                    li.setText( url )

                elif not self.is_duplicate( url ):
                        li.setText( url )



    def write_config( self ):

        self.parent.write_config()

    

    def qytdl_hook( self, d ):
        #if d[ "status" ] == "finished":
        #    print( "yay done" )

        try:
            if d[ "status" ] == "downloading":
                x = d[ "downloaded_bytes" ]
                y = d[ "total_bytes" ]

                #val = 100 * ((y/x) * ( totalUrls/(currentUrl+1)))
                val = 100.0 * ( x / y )
                self.currentProgressBar.setValue( int( val ) )
        except KeyError:
            self.currentProgressBar.setValue( 100 )


    def ydl_opts( self, profile ):
        ydl_opts = {
                "outtmpl" : "%(title)s.%(ext)s",
                "updatetime" : False,
                "logger" : QYTDLLogger(),
                "progress_hooks" : [ self.qytdl_hook ],
                }

        ##  Format stuff
        fmt = ""
        if profile.videoFormat != None and profile.audioFormat != None:
            fmt = "%s+%s" % ( profile.videoFormat, profile.audioFormat )
        elif profile.videoFormat != None:
            fmt = profile.videoFormat
        elif profile.audioFormat != None:
            fmt = profile.audioFormat

        ydl_opts[ "format" ] = fmt

        ##  Merge output, if applicable
        if profile.mergeOutputFormat != None:
            ydl_opts[ "merge_output_format" ] = profile.mergeOutputFormat

        if profile.postprocessors != None:
            ydl_opts[ "postprocessors" ] =  profile.postprocessors

            #for pp in profile.postprocessors:
            #    if "EmbedThumbnail" in pp.values():
            #        ydl_opts[ "writethumbnail" ] = True

        if profile.writeThumbnail != None and profile.writeThumbnail == True:
            ydl_opts[ "writethumbnail" ] = True

        return( ydl_opts )


    def standard_download( self, opts, profile, url ):

        try:
            ydl_module = importlib.import_module( opts[ "module" ] )
            if self.debug:
                print( "Module:\t%s" % opts[ "module" ] )

        except ImportError:
            ydl_module = youtube_dl
            if self.debug:
                print( "Module:\tyoutube_dl")

        ydl_opts = self.ydl_opts( profile )

        try:
            with ydl_module.YoutubeDL( ydl_opts ) as ydl:
                ydl.download( [url] )

            return True

        except ydl_module.utils.DownloadError:
            return False

        return False



    def external_download( self, opts, pro, url ):

        cmd = [ pro.externalBin ]

        ##  If the user wants FULL control over the params
        if( pro.fullParams != None and pro.fullParams != "none"
                and pro.fullParams != "" ):
            for param in pro.fullParams.split():
                if param != None and param.lower() != "none" and param != "":
                    cmd.append( param )

        ##  Otherwise, make some assumptions
        else:
            ##  Add 'smart' defaults to cmd
            cmd.append( "--no-mtime" )
            cmd.append( "-o%s/%%(title)s.%%(ext)s" % ( opts[ "downloadPath" ] ))

            ##  All of the custom stuff the user wants
            if pro.params != None:
                for param in pro.params.split():
                    if param != None and param.lower() != "none" and param != "":
                        cmd.append( param )

        ##  Append the URL
        cmd.append( url )


        ##  Call the command
        if self.debug:
            print( cmd )

        ret = subprocess.call( cmd )
        return( ret != 1 )


    def download_video( self, opts, url ):

        ##  Get all of the profiles we're gonna use
        profiles = [ self.parent.profiles[ opts[ "profile" ]] ]
        for pro in opts[ "fallback" ]:
            profiles.append( self.parent.profiles[ pro ] )

        ##  Add 'auto' if it ain't in there
        if "auto" not in opts[ "fallback" ]:
            profiles.append( self.parent.profiles[ "auto" ] )

        ##  Finally do it baby
        skipCount = 0
        for pro in profiles:
            if skipCount > 0:
                print( "Using fallback profile:\t'%s'" % pro.name )


            if pro.externalBin != None:
                if self.debug:
                    print( "(external download)" )

                if self.external_download( opts, pro, url ):
                    return True
                else:
                    skipCount += 1

            else:
                if self.debug:
                    print( "(standard download)" )

                if self.standard_download( opts, pro, url ):
                    return True
                else:
                    skipCount += 1


        return False


    def process_playlist( self, info, opts, url ):

        ###  Title of the playlist
        title = info[ "title" ]

        ##  If they want a new directory for the playlist, make it and move in
        currentDirectory = os.path.abspath( '.' )
        if opts[ "playlistFolder" ] == "true":
            dirName = generate_dirname( currentDirectory, title )
            os.mkdir( dirName )
            os.chdir( os.path.join( currentDirectory, dirName ))

        ##  Get the entries
        if "entries" in info:
            vids = list( info[ "entries" ] )
        else:
            vids = [ info ]

        ##  Number of videos
        numVids = len( vids )

        ##  Set 'current' maximum to whatever that number is
        self.currentProgressBar.setMaximum( numVids )

        ##  Start 'er up
        status = self.parent.statusBar()
        currentVid = 0
        for vid in vids:
            status.showMessage(
                    "Downloading playlist entry %d/%d, please wait..." %
                    ( currentVid+1, numVids ))
            self.currentProgressBar.setValue( int( currentVid ) )
            currentVid += 1

            #profile = self.parent.profiles[ opts[ "profile" ] ]
            if not self.download_video( opts, vid[ "url" ] ):
                print( "WARNING:  Unable to download URL '%s'" % vid[ "url" ] )
                continue


        ##  Reset the maximum for current bar
        self.currentProgressBar.setMaximum( 100 )

        ##  Change back out of the playlist directory
        os.chdir( currentDirectory )


    def confirm_dir( self, dDir ):
        if not os.path.exists( dDir ):
            try:
                print( "Creating directory '%s'" % dDir )
                os.mkdir( dDir )
            except (PermissionError, OSError):
                print( "ERROR:  Cannot create director '%s'.  Aborting." %
                        dDir )
                return( False )

        return( True )


    def start_download( self ):

        ##  Don't do anything if there ain't stuff in the list
        if self.listWidget.count() < 1:
            return False

        opts = self.parent.opts

        self.write_config()

        #self.setDisabled( True )
        self.disable_stuff( True )

        status = self.parent.statusBar()

        urls = []
        for i in range( self.listWidget.count() ):
            li = self.listWidget.item( i )
            urls.append( li.text() )
            if self.debug:
                print( "Adding '%s' to download queue" % li.text() )




        totalUrls = len( urls )
        self.currentProgressBar.setMaximum( 100 )
        self.totalProgressBar.setMaximum( totalUrls )

        currentUrl = 0
        if totalUrls > 0:

            ###  Formats
            ###
            ###  22  720p mp4 (I guess?)
            ###  136 720p mp4
            ###  137 1080p mp4

            ##  Get current directory then change to the download dir
            prevDir = os.path.abspath( '.' )

            ##  Make sure the download path exists and change to it
            dDir = opts[ "downloadPath" ]
            if not self.confirm_dir( dDir ):
                print( "ERROR:  Cannot write to directory '%s'.  Aborting." %
                        dDir )
                return( False )

            os.chdir( dDir )
            
            ##  Change the cursor
            QApplication.setOverrideCursor( Qt.WaitCursor )

            ##  Just grab this here for convenience's sake
            if not self.debug:
                ydl = youtube_dl.YoutubeDL( { "quiet" : True } )
            else:
                ydl = youtube_dl.YoutubeDL()

            for url in urls:

                ##  Current URL stuff
                #currentUrl += 1
                self.totalProgressBar.setValue( int( currentUrl ) )

                msg = ( "Downloading %d/%d, please wait..." %
                        ( currentUrl+1, totalUrls ) )
                status.showMessage( msg )
                if self.debug:
                    print( msg )

                ##  First off, see if it's a playlist
                info = ydl.extract_info( url, process = False )
                if info[ "extractor" ] == "youtube:playlist":


                    ##  Work the playlist, baby
                    self.process_playlist( info, opts, url )

                    ##  Update the free label thingy
                    self.update_free_label()

                    ##  Go back to top of loop
                    currentUrl += 1
                    continue

                ##  Reset the 'current' progress bar
                self.currentProgressBar.setValue( 0 )

                #profile = self.parent.profiles[ opts[ "profile" ] ]
                if not self.download_video( opts, url ):
                    print( "WARNING:  Unable to download URL '%s'" % url )
                    continue



                ##  Remove the top (processed) item
                li = self.listWidget.item( 0 )
                if li != None:
                    self.listWidget.setDisabled( False )
                    sip.delete( li )
                    self.listWidget.setDisabled( True )

                self.totalProgressBar.setValue( int( currentUrl + 1 ) )
                currentUrl += 1

                ##  Update the free label
                self.update_free_label()

            ##  Restore old cursor
            QApplication.restoreOverrideCursor()

            ##  Return to previous directory
            os.chdir( prevDir )




        self.listWidget.clear()

        self.disable_stuff( False )
        #self.setDisabled( False )

        self.currentProgressBar.setValue( 0 )
        self.totalProgressBar.setValue( 0 )
        status.showMessage( "All done!", 2000 )


    def set_destination( self ):

        downloadsDir = QFileDialog.getExistingDirectory( self,
                "Choose download directory...", "%s" % self.destEdit.text() )

        if downloadsDir != "":
            self.destEdit.setText( downloadsDir )
            self.parent.opts[ "downloadPath" ] = downloadsDir
            self.update_free_label()



    def update_free_label( self ):
        freeSpace = get_free_space( self.parent.opts[ "downloadPath" ] )
        self.freeLabel.setText( "%s free" % freeSpace )


    def get_urls( self ):

        urls = []

        for i in range( self.listWidget.count() ):
            urls.append( self.listWidget.item( i ).text() + '\n' )
        
        return( urls )
