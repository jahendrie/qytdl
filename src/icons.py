"""
This module contains the Icons class, which is used as a relatively convenient
way of fetching the appropriate icons for a given action.  It first attempts
the built-in system defaults; if those are not found, fallbacks are provided.
"""

from PyQt5.QtGui import QIcon

from util import icon_path, system_install_path

class Icons():
    """
    Used to grab icons according to given strings.
    """
    
    def fallback_path( self, iconString, systemInstall = False ):
        """
        Icons.fallback_path( iconString ) -> str

        Returns the full path to the fallback icon graphic according to the
        original icon string provided.
        """

        if systemInstall:
            path = "%s/data/icons/%s.png" % ( system_install_path(), iconString)
            return( path )

        if iconString == "list-add":
            return( icon_path( "add.png" ) )

        elif iconString == "application-exit":
            return( icon_path( "exit.png" ) )

        elif iconString == "help-about":
            return( icon_path( "help.png" ) )

        elif iconString == "help-faq":
            return( icon_path( "helphint.png" ))

        elif iconString == "document-new":
            return( icon_path( "new.png" ) )

        elif iconString == "document-open":
            return( icon_path( "open.png" ) )

        elif iconString == "list-remove":
            return( icon_path( "remove.png" ) )

        elif iconString == "document-save-as":
            return( icon_path( "saveas.png" ) )

        elif iconString == "document-save":
            return( icon_path( "save.png" ) )

        elif iconString == "cTop" or iconString == "connected-top":
            return( icon_path( "connected-top.png" ))

        elif iconString == "cMiddle" or iconString == "connected-middle":
            return( icon_path( "connected-middle.png" ))

        elif iconString == "cBottom" or iconString == "connected-bottom":
            return( icon_path( "connected-bottom.png" ))

        elif iconString == "checkbox":
            return( icon_path( "checkbox.png" ))

        elif iconString == "help-contents":
            return( icon_path( "help-contents.png" ))

        elif iconString == "application-icon":
            return( icon_path( "application-icon.png" ))

        elif iconString == "go-next":
            return( icon_path( "go-next.png" ))

        elif iconString == "edit-paste":
            return( icon_path( "edit-paste.png" ))

        elif iconString == "folder-open":
            return( icon_path( "folder-open.png" ))

        elif iconString == "TEST":
            return( icon_path( "TEST.png" ) )

    

    def fallback_icon( self, iconString, systemInstall = False ):
        """
        Icons.fallback_icon( iconString ) -> QIcon

        Returns a QIcon object that corresponds (as best as possible) to the
        given icon string.
        """

        ##  The icon
        fbIcon = QIcon( self.fallback_path( iconString, systemInstall ))

        return( fbIcon )



    def get_icon( self, iconString, systemInstall = False ):
        """
        Icons.get_icon( iconString ) -> QIcon

        This method uses the built-in QIcon.fromTheme() method to send back
        either the system default for a given icon string or an appropriate
        fallback icon.
        """

        icon = QIcon().fromTheme(
                iconString, self.fallback_icon( iconString, systemInstall ))

        return( icon )
