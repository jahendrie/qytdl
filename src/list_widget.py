import sys

from PyQt5.QtWidgets import QListWidget, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QAction

from icons import *

class ListWidget( QListWidget ):

    def __init__( self, parent = None ):
        super().__init__()
        self.parent = parent
        self.debug = self.parent.debug

    def open_context_menu( self, event ):
        ##  Make life easier
        get_icon = Icons().get_icon

        ##  Is this a system install?
        sysInstall = ( os.path.expanduser( '~' ) in sys.argv[0] )

        menu = QMenu( self )

        ##  Edit item
        editAction = QAction( QIcon( get_icon( "edit-entry", sysInstall)),
                "Edit entry", self )
        editAction.setStatusTip( "Edit entry" )
        editAction.triggered.connect( self.parent.edit_item )

        ##  The remove item
        removeAction = QAction( QIcon( get_icon( "list-remove", sysInstall )),
                "Remove item", self )
        removeAction.setStatusTip( "Remove item" )
        removeAction.triggered.connect( self.parent.remove_item )

        ##  Add the actions to the menu
        menu.addAction( editAction )
        menu.addAction( removeAction )

        ##  Execute the menu
        menu.exec( event.globalPos() )


    def contextMenuEvent( self, event ):
        ##  Only open the menu if the download ain't happening
        if self.isEnabled() and self.currentItem() != None:
            self.open_context_menu( event )
