"""
This module contains the Icons class, which is used as a relatively convenient
way of fetching the appropriate icons for a given action.  It first attempts
the built-in system defaults; if those are not found, fallbacks are provided.
"""

import os
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
            path = os.path.join( system_install_path(), "icons" )
        else:
            path = icon_path()

        fbPath = os.path.join( path, "fallback" )

        iSVG = os.path.join( fbPath, "svg/" ) + iconString + ".svg"
        iPNG = os.path.join( fbPath, "png/" ) + iconString + ".png"

        return( iSVG if os.path.exists( iSVG ) else iPNG )

    

    def fallback_icon( self, iconString, systemInstall = False ):
        """
        Icons.fallback_icon( iconString ) -> QIcon

        Returns a QIcon object that corresponds (as best as possible) to the
        given icon string.
        """

        ##  The icon
        iString = iconString.replace( "-symbloic", '', -1 )
        fbIcon = QIcon( self.fallback_path( iString, systemInstall ))

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
