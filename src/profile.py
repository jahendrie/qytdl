import sys, os
import xml.etree.ElementTree as ET


def boolify( B ):
    b = B.lower()
    if b == "true" or b == "yes" or b == "1":
        return( True )
    elif b == "false" or b == "no" or b == "0":
        return( False )
    else:
        return( B )


class Profile():
    def __init__( self, pro = None ):

        ##  Default profile settings
        self.mode = None
        self.params = None
        self.fullParams = None
        self.videoFormat = None
        self.audioFormat = None
        self.mergeOutputFormat = None
        self.example = False
        self.comment = None
        self.postprocessors = None
        self.writeThumbnail = False

        if pro != None:
            self.parse( pro )

    def parse( self, pro ):
        ##  The ostensibly unique ID of this profile
        self.id = pro.find( "id" ).text

        ##  The user-friendly name of this profile
        self.name = pro.find( "name" ).text

        ##  Profile's mode
        mode = pro.find( "mode" )
        if mode != None:
            modeText = mode.text.lower()
            if modeText == "external" or modeText == "internal":
                self.mode = modeText
            else:
                self.mode = "system"

        ##  Extra params used by this profile if using external ydl
        params = pro.find( "params" )
        if params != None:
            self.params = params.text

        ##  Full, no-bullshit 'only use these' params
        fullParams = pro.find( "full_params" )
        if fullParams != None:
            self.fullParams = fullParams.text

        ##  Get the formats and stuff
        videoFormat = pro.find( "video_format" )
        audioFormat = pro.find( "audio_format" )
        mergeOutputFormat = pro.find( "merge_output_format" )

        #self.videoFormat = pro.find(
        if videoFormat != None:
            self.videoFormat = videoFormat.text

        #self.audioFormat = None
        if audioFormat != None:
            self.audioFormat = audioFormat.text

        #self.mergeOutputFormat = None
        if mergeOutputFormat != None:
            self.mergeOutputFormat = mergeOutputFormat.text


        ##  See if we're explicitly writing the thumbnail
        writeThumbnail = pro.find( "write_thumbnail" )
        if writeThumbnail != None:
            self.writeThumbnail = boolify( writeThumbnail.text )

        ##  Post-processors, used for some formats
        postProcessors = pro.find( "postprocessors" )
        if postProcessors != None:
            self.postprocessors = self.parse_post_processors( postProcessors )


    def parse_post_processors( self, postProcessors ):
        ppList = []
        for pp in postProcessors.iter( "pp" ):
            d = {}
            for pt in pp.text.split():
                keyVal = pt.replace( ',', '', -1 )
                keyValParts = keyVal.partition( ':' )
                if keyVal != None and keyVal != '' and keyVal != '\n':
                    d[ keyValParts[0] ] = boolify( keyValParts[2] )

                ppList.append( d )

        return( ppList if len( ppList ) > 0 else None )


    def write_post_processors( self, fp ):

        if self.postprocessors != None:
            fp.write( "\t\t<postprocessors>\n" )

            for pp in self.postprocessors:
                fp.write( "\t\t\t<pp>\n" )
                for key in pp:
                    fp.write( "\t\t\t\t%s:%s,\n" % (key, pp[ key ]))

                fp.write( "\t\t\t</pp>\n" )

            fp.write( "\t\t</postprocessors>\n" )


    def write_header( self,  fp ):
        ##  If it's an example, start the comment block
        if self.example:
            if self.comment != None and self.comment != "":
                fp.write( "\n\t<!-- %s -->\n\n" % self.comment )

        ##  Profile section
        fp.write( "\t<profile>\n" )

        ##  Its mandatory stats
        fp.write( "\t\t<id>%s</id>\n" % self.id )
        fp.write( "\t\t<name>%s</name>\n" % self.name )

    def write_footer( self, fp ):
        ##  Finish off
        fp.write( "\t</profile>\n" )


    def write( self, fp ):

        ##  Write the beginning part
        self.write_header( fp )

        ##  Mode
        if self.mode != None:
            fp.write( "\t\t<mode>%s</mode>\n" % self.mode )

        ##  Write the parameters baby
        if self.fullParams != None:
            fp.write( "\t\t<full_params>%s</full_params>\n" % self.fullParams )
        elif self.params != None:
            fp.write( "\t\t<params>%s</params>\n" % self.params )

        if self.videoFormat != None:
            fp.write( "\t\t<video_format>%s</video_format>\n" % self.videoFormat )

        if self.audioFormat != None:
            fp.write( "\t\t<audio_format>%s</audio_format>\n" % self.audioFormat)

        if self.mergeOutputFormat != None:
            fp.write( "\t\t<merge_output_format>%s</merge_output_format>\n" %
                    self.mergeOutputFormat )

        if self.writeThumbnail != None and self.writeThumbnail == True:
            fp.write( "\t\t<write_thumbnail>true</write_thumbnail>\n" )

        ##  Handle the pp
        self.write_post_processors( fp )

        ##  Finish it off
        self.write_footer( fp )


def config_path():
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


def profile_file():

    if sys.platform == "win32" or sys.platform == "win64":
        cfg = "%s\\profiles.xml" % config_path()
    else:
        cfg = "%s/profiles.xml" % config_path()

    return( cfg )


def default_profiles():
    profiles = []
    examples = []

    ##  Auto
    pro = Profile()
    pro.id = "auto"
    pro.name = "Auto"
    pro.videoFormat = "bestvideo"
    pro.audioFormat = "bestaudio"
    profiles.append( pro )

    ##  Auto (external) (example)
    pro = Profile()
    pro.id = "ext_auto"
    pro.name = "Auto (External) (Example)"
    pro.example = True
    pro.mode = "external"
    examples.append( pro )

    ##  1080p, 60fps (external) (example)
    pro = Profile()
    pro.id = "mp4_1080p_60"
    pro.name = "MP4 1080p 60fps (External) (Example)"
    pro.example = True
    pro.comment = "Program will make a few assumptions if using normal params"
    pro.params = "-f 299+140 --merge-output-format mkv"
    pro.mode = "external"
    examples.append( pro )

    ##  1080p 60fps ('strict' external) (example)
    pro = Profile()
    pro.id = "strict_ext_1080p_60"
    pro.name = "1080p, 60fps (Strict External) (Example)"
    pro.example = True
    pro.comment = "Program will not make any assumptions if using full params"
    pro.fullParams = "-f 299+140 -o%%(title)s.%%(ext)s --merge-output-format mp4"
    pro.mode = "external"
    examples.append( pro )

    ##  1080p, 60fps
    pro = Profile()
    pro.id = "mp4_1080p_60"
    pro.name = "MP4 1080p 60fps"
    pro.videoFormat = "299"
    pro.audioFormat = "140"
    pro.mergeOutputFormat = "mp4"
    profiles.append( pro )
    
    ##  1080p, 30fps
    pro = Profile()
    pro.id = "mp4_1080p_30"
    pro.name = "MP4 1080p 30fps"
    pro.videoFormat = "137"
    pro.audioFormat = "140"
    pro.mergeOutputFormat = "mp4"
    profiles.append( pro )
    
    ##  720p, 30fps
    pro = Profile()
    pro.id = "mp4_720p"
    pro.name = "MP4 720p"
    pro.videoFormat = "22"
    pro.audioFormat = None
    profiles.append( pro )

    ##  mp3, 192kbps
    pro = Profile()
    pro.id = "mp3_192"
    pro.name = "MP3 192kbps"
    pro.videoFormat = None
    pro.audioFormat = "bestaudio/best"
    pro.writeThumbnail = True
    pro.postprocessors = [
            {
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192",
            },
            { "key" : "FFmpegMetadata", },
            { "key" : "EmbedThumbnail", },
        ]

    profiles.append( pro )

    return( profiles, examples )

def create_profiles( path, profiles, examples = [] ):

    try:
        fp = open( path, "w" )

        ##  File header
        fp.write( "<qytdl>\n" )

        for pro in profiles:
            fp.write( "\n" )
            pro.write( fp )

        if len( examples ) > 0:

            fp.write( "\n\t<?Examples\n\n" )

            for example in examples:
                fp.write( "\n" )
                example.write( fp )

            fp.write( "\n\t?>\n" )


        ##  Finish it all off
        fp.write( "\n</qytdl>\n" )

        fp.close()

    except PermissionError:
        print( "ERROR:  Cannot write to '%s'." % path )
        print( "Unable to create settings file, cannot save preferences." )


def parse_profiles( fp ):

    et = ET.parse( fp )

    profiles = {}
    examples = {}
    for it in et.iter( "profile" ):
        profile = Profile( it )

        if profile.example:
            examples[ profile.id ] = profile
        else:
            profiles[ profile.id ] = profile

    return( profiles, examples )


def read_profiles():

    #opts = default_opts()
    #cfg = config_file()
    profilePath = profile_file()
    profiles = {}

    try:
        fp = open( profilePath, "r" )
        profiles, examples = parse_profiles( fp )
        fp.close()

    except FileNotFoundError:
        defaults, examples = default_profiles()
        create_profiles( profilePath, defaults, examples )
        profiles = read_profiles()

    except PermissionError:
        print( "ERROR:  Cannot read from '%s'." % profilePath )
        print( "Unable to read profiles" )


    return( profiles )



def write_profiles( profiles ):

    #cfg = config_file()
    #create_config( cfg, opts )

    profilePath = profile_file()
    create_profiles( profilePath, profiles )
