#!/usr/bin/env python3

from Deadline.Plugins import *
from Deadline.Scripting import *

def GetDeadlinePlugin():
    return HuskPlugin()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

class HuskPlugin( DeadlinePlugin ):

    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument

    def Cleanup( self ):
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback

         # Remove the stdout handlers
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

    def InitializeProcess( self ):
        self.PluginType = PluginType.Simple

         # Enable stdout handling
        self.StdoutHandling = True
        
        # Define a handler
        self.AddStdoutHandlerCallback( r"(?<=ALF_PROGRESS )[0-9]+(?=%)" ).HandleCallback += self.HandleStdoutProgress
    
    def HandleStdoutProgress( self ):
        print('regex matched: ' + str(self.GetRegexMatch( 0 )))
        # Set the progress to be the value of just the number
        self.SetProgress( float( self.GetRegexMatch( 0 ) ) )
        
        # Set the status message to be the full line of output.
        self.SetStatusMessage( self.GetRegexMatch( 0 ) )

    def RenderExecutable( self ):
        ##version = int( self.GetPluginInfoEntry( "Version" ) )
        exe = ""
        exeList = self.GetConfigEntry( "Husk_Executable" )
        exe = FileUtils.SearchFileList( exeList )
        if( exe == "" ):
            self.FailRender( "Husk render executable was not found in the configured separated list \"" + exeList + "\"" )
        return exe

    def RenderArgument( self ):
        sceneFile = self.GetPluginInfoEntryWithDefault( "SceneFile", self.GetDataFilename() )
        renderArguments = sceneFile 

        startFrame = str( self.GetStartFrame() )
        endFrame = str( self.GetEndFrame() )

        numFrames = str((int(endFrame) + 1) - int(startFrame))

        renderArguments = "-f %s -n %s -i 1 -Va2" % ( startFrame,numFrames ) + " " + renderArguments

        ##outputFilename = self.GetPluginInfoEntryWithDefault( "OutputFilename", "" )
        ##if outputFilename != "":
        ##    renderArguments += "-file \"%s\"" % outputFilename

        return renderArguments
        
        ##sceneFile = self.GetPluginInfoEntryWithDefault( "SceneFile", self.GetDataFilename() )
        ##return "-Va2 " + sceneFile
        
        ##return "-Va2 E:\\Projects\\0008_usd_testing\\geo\\test_render.usd"