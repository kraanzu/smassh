#   Gary Davenport preferredsoundplayer functions 7/9/2021
#
#   This module has no dependencies, other than what comes with Windows 10,
#       the standard Linux kernel, MacOS 10.5 or later, and the
#       Python Standard Library.
#
#   Looping:
#   If sound files are .wav files they will loop in a thread loop duration is equal to length of .wav file
#   Mp3s will be looped by checking 5 times a second to see if sound has finished, and if so relaunch
#   (this is because it is harder to figure out time length of mp3 due to different styles encoding)
#
#   ----------------Windows----------------
#   Windows 10 uses the Windows winmm.dll Multimedia API to play sounds.
#   Windows 10 uses a single instance of a player, allowing for garbage collection tracking
#       See references:
#       “Programming Windows: the Definitive Guide to the WIN32 API,
#           Chapter 22 Sound and Music Section III Advanced Topics
#           ‘The MCI Command String Approach.’”
#           Programming Windows: the Definitive Guide to the WIN32 API,
#           by Charles Petzold, Microsoft Press, 1999.
#       https://stackoverflow.com/questions/22253074/how-to-play-or-open-mp3-or-wav-sound-file-in-c-program
#       https://github.com/michaelgundlach/mp3play
#       & https://github.com/TaylorSMarks/playsound/blob/master/playsound.py
#
#
#   ----------------Linux------------------
#   Linux uses ALSA and gstreamer, part of Linux kernel, also may use ffmpg if available

#   -Linux will always play .wavs with ALSA
#   Otherwise:
#   -Linux will use the first available player in this order: gst-1.0-play, ffmpeg, gst playbin(built on the fly) or ALSA
#   -Linux will try to use gst-1.0-play first (usually present), if not present then
#   -Linux will try to use ffmpeg as its player (usually present), if not present then
#   -Linux will initialize a gstreamer playbin player (is supposed to always be present), if not present then
#   -Linux will play the sound with ALSA, and if not a .wav file will sound like white noise.
#
#   If the playbin player must be used, each sound gets its own instance of a player, to avoid internal conflicts
#       with gstreamers internal looping
#
#   ----------------MacOS-------------------
#   -MacOS uses the afplay module which is present OS X 10.5 and later
#

from random import random
from platform import system
import subprocess
from subprocess import Popen, PIPE
import os
from threading import Thread
from time import sleep
import sndhdr

if system() == "Linux":
    import shutil

    try:
        import gi

        gi.require_version("Gst", "1.0")
        from gi.repository import Gst
    except:
        pass
    import os

if system() == "Windows":
    from ctypes import c_buffer, windll
    from sys import getfilesystemencoding
    from threading import Thread
    from time import sleep

# This module creates a single sound with winmm.dll API and returns the alias to the sound


class WinMMSoundPlayer:
    def __init__(self):
        self.isSongPlaying = False
        self.sync = False
        self.P = None
        self.fileName = ""
        self.alias = ""
        self.loopAlias = ""
        self.aliasList = []

    # typical process for using winmm.dll
    def _processWindowsCommand(self, commmandString):
        buf = c_buffer(255)
        command = commmandString.encode(getfilesystemencoding())
        # print(command)
        windll.winmm.mciSendStringA(command, buf, 254, 0)
        return buf.value

    def _collectGarbarge(self):
        #
        #   Garbage Collection
        #
        #   go through alias list
        #       if song not playing
        #           close it
        #           remove it from list
        #
        # aliasListLength=len(self.aliasList)
        # for i in range(aliasListLength):
        #    if self.getIsPlaying(self.aliasList[i])==False:

        # make a list of sounds that are no longer playing
        removalList = []
        for i in range(len(self.aliasList)):
            if self.getIsPlaying(self.aliasList[i]) == False:
                # print("adding",self.aliasList[i],"to garbage collector removal list.")
                removalList.append(i)

        # issues stop(not necessary) and close commands to that list
        for i in range(len(removalList) - 1, -1, -1):
            # print("closing",self.aliasList[removalList[i]],"at index",removalList[i])#<-----unprint
            self.stopsound(self.aliasList[removalList[i]])
            del self.aliasList[removalList[i]]

    # make an alias, play the song.
    # For Sync play - use the wait flag, then stop and close alias.
    # For Async - unable to close.

    def soundplay(self, fileName, block=False):

        self._collectGarbarge()

        self.fileName = fileName
        # make an alias
        self.alias = "soundplay_" + str(random())
        # print("adding ", self.alias)# <------- unprint
        self.aliasList.append(self.alias)

        str1 = 'open "' + os.path.abspath(self.fileName) + '"' + " alias " + self.alias
        self._processWindowsCommand(str1)

        # use the wait feature to block or not block when constructing mciSendString command
        if block == False:
            str1 = "play " + self.alias
            # play the sound
            self._processWindowsCommand(str1)
        else:
            # construct mciSendString command to wait i.e. blocking
            str1 = "play " + self.alias + " wait"
            # play the sound (blocking)
            self._processWindowsCommand(str1)
            # stop and close the sound after done
            str1 = "stop " + self.alias
            self._processWindowsCommand(str1)
            str1 = "close " + self.alias
            self._processWindowsCommand(str1)

        # return the alias of the sound
        return self.alias

    # this function uses the mci/windows api with a repeat call to loop sound
    def loopsound(self, fileName):
        self._collectGarbarge()
        self.loopAlias = "loopalias_" + str(random())
        # print("adding looper alias",self.loopAlias) #<-------unprint
        self.aliasList.append(self.loopAlias)
        str1 = (
            'open "'
            + os.path.abspath(fileName)
            + '" type mpegvideo alias '
            + self.loopAlias
        )
        self._processWindowsCommand(str1)
        str1 = "play " + self.loopAlias + " repeat"
        self._processWindowsCommand(str1)
        return self.loopAlias

    # issue stop and close commands using the sound's alias
    def stopsound(self, sound):
        # print("------------------------")
        try:
            str1 = "stop " + sound
            self._processWindowsCommand(str1)
            str1 = "close " + sound
            self._processWindowsCommand(str1)
        except:
            pass

    # return True or False if song alias 'status' is 'playing'
    def getIsPlaying(self, song):
        try:
            str1 = "status " + song + " mode"
            myvalue = self._processWindowsCommand(str1)
            if myvalue == b"playing":
                self.isSongPlaying = True
            else:
                self.isSongPlaying = False
        except:
            self.isSongPlaying = False
        return self.isSongPlaying


def isFileAWav(fileName):
    try:
        if sndhdr.what(fileName)[0] == "wav":
            return True
    except:
        return False


class MusicLooper:
    def __init__(self, fileName):
        self.fileName = fileName
        self.playing = False
        self.songProcess = None
        # self.optionalForMp3s_CheckRestartHowOften = .2

    def _playwave(self):
        self.songProcess = playwave(self.fileName)

    def _playloop(self):
        while self.playing == True:
            # it is easy to get duration of wave file
            if isFileAWav(self.fileName) == True:
                self.songProcess = playwave(self.fileName)
                sleep(self._getWavDurationFromFile())
            else:
                # it is hard to get duration of non wave files so check 5 times a second and relaunch if ended
                if self.songProcess is not None:
                    if getIsPlaying(self.songProcess) == False:
                        self.songProcess = playwave(self.fileName)
                else:
                    self.songProcess = playwave(self.fileName)
                sleep(0.2)
                # sleep(self.optionalForMp3s_CheckRestartHowOften)

    # start looping a wave
    def startMusicLoopWave(self):
        # def startMusicLoopWave(self,optionalForMp3s_CheckRestartHowOften=.2):
        # self.optionalForMp3s_CheckRestartHowOften=optionalForMp3s_CheckRestartHowOften
        if (
            self.playing == True
        ):  # don't allow more than one background loop per instance of MusicLooper
            print("Already playing, stop before starting new.")
            return
        else:
            self.playing = True
            t = Thread(target=self._playloop)
            t.setDaemon(True)
            t.start()

    # stop looping a sound
    def stopMusicLoop(self):
        if self.playing == False:
            print(
                str(self.songProcess) + " already stopped, play before trying to stop."
            )
            return
        else:
            self.playing = False  # set playing to False, which stops loop
            # issue command to stop the current wave file playing also, so song does not finish out
            stopwave(self.songProcess)

    # get length of wave file in seconds
    def _getWavDurationFromFile(self):
        frames = sndhdr.what(self.fileName)[3]
        rate = sndhdr.what(self.fileName)[1]
        duration = float(frames) / rate
        return duration

    def getSongProcess(self):
        return self.songProcess

    def getPlaying(self):
        return self.playing


# Each sound gets its own Gst.init() and own sound player


class SingleSoundLinux:
    def __init__(self):
        import gi

        gi.require_version("Gst", "1.0")
        from gi.repository import Gst

        self.pl = None
        self.gst = Gst.init()
        self.playerType = ""

    def _gstPlayProcess(self):
        self.pl.set_state(Gst.State.PLAYING)
        bus = self.pl.get_bus()
        bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
        self.pl.set_state(Gst.State.NULL)

    def soundplay(self, fileName, block=False):
        if self.getIsPlaying(self.pl) == False:
            self.pl = Gst.ElementFactory.make("playbin", "player")
            self.pl.set_property("uri", "file://" + os.path.abspath(fileName))
            self.playerType = "gstreamer"
            self.T = Thread(target=self._gstPlayProcess, daemon=True)
            self.T.start()
            if block == True:
                self.T.join()
            return [self.pl, self.playerType]
        else:
            print(
                "already playing, open new SingleSound if you need to play simoultaneously"
            )

    def stopsound(self, sound):
        # print(sound[1])
        if sound[1] == "gstreamer":
            sound[0].set_state(Gst.State.NULL)

    def getIsPlaying(self, song):
        if song is None:
            return False
        # print(song[1])
        if song[1] == "gstreamer":
            state = str(song[0].get_state(Gst.State.PLAYING)[1]).split()[1]
            if state == "GST_STATE_READY" or state == "GST_STATE_PLAYING":
                return True
            else:
                return False


#########################################################################
# These function definitions are intended to be used by the end user,   #
# but an instance of the class players above can be used also.          #
#########################################################################

# plays a sounnd file and also returns the alias of the sound being played, async method is default
# 3 separate methods allows for the Windows module to initialize an instance of 'WinMMSoundPlayer' class
# this way only one windows type player allows to keep track of all aliases made and garbage can be collected
# when songs have finished playing


def _soundplayWindows(fileName, block=False):
    song = windowsPlayer.soundplay(fileName, block)  # change
    return song


def _soundplayLinux(fileName, block=False):
    if isFileAWav(fileName) == True:  # use alsa if .wav
        # print("using alsa because its a wav")
        command = "exec aplay --quiet " + os.path.abspath(fileName)
    elif (
        shutil.which("gst-play-1.0") is not None
    ) == True:  # use gst-play-1.0 if available
        # print("using gst-play-1.0 since available")
        command = "exec gst-play-1.0 " + os.path.abspath(fileName)
    elif (shutil.which("ffplay") is not None) == True:  # use ffplay if present
        # print("using ffplay since available")
        command = "exec ffplay -nodisp -autoexit -loglevel quiet " + os.path.abspath(
            fileName
        )
    else:
        try:
            import gi

            gi.require_version("Gst", "1.0")
            from gi.repository import Gst

            song = SingleSoundLinux().soundplay(fileName, block)
            # print("using gst playbin - successful try")
            return song
        except:
            print("must use ALSA, all else failed")
            command = "exec aplay --quiet " + os.path.abspath(fileName)
    if block == True:
        P = subprocess.Popen(
            command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE
        ).communicate()
    else:
        P = subprocess.Popen(
            command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE
        )
    return P


def _soundplayMacOS(fileName, block=False):
    command = "exec afplay '" + os.path.abspath(fileName) + "'"
    if block == True:
        P = subprocess.Popen(
            command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE
        ).communicate()
    else:
        P = subprocess.Popen(
            command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE
        )
    return P


# stops the wave being played, 'process' in the case of windows is actually the alias to the song
# otherwise process is a process in other operating systems.


def stopsound(process):
    if process is not None:
        try:
            if process is not None:
                if system() == "Windows":
                    windowsPlayer.stopsound(process)
                elif system() == "Linux":
                    # see if process is GSTPlaybin
                    if str(process).find("gstreamer") != -1:
                        SingleSoundLinux().stopsound(process)
                    else:
                        process.terminate()  # Linux but not GSTPlaybin
                else:
                    process.terminate()  # MacOS
        except:
            pass
            # print("process is not playing")
    else:
        pass
        # print("process ", str(process), " not playing")


# pass the process or alias(windows) to the song and return True or False if it is playing


def getIsPlaying(process):
    if system() == "Windows":
        return windowsPlayer.getIsPlaying(process)
    else:
        isSongPlaying = False
        if process is not None:
            # see if process is GSTPlaybin
            if system() == "Linux":
                # see if process is GSTPlaybin
                if str(process).find("gstreamer") != -1:
                    return SingleSoundLinux().getIsPlaying(process)
                else:  # Linux but not GSTPlaybin
                    try:
                        return process.poll() is None
                    except:
                        pass
            else:
                try:
                    return process.poll() is None
                except:
                    pass

        return isSongPlaying


# this function will loop a wave file and return an instance of a MusicLooper object that loops music,
# or in the case of Windows it just calls the loop function in the Windows SingleSoundWindows class

"""
def loopsound(fileName,optionalForMp3s_CheckRestartHowOften=.2):
    if system() == "Windows":
        return(windowsPlayer.loopsound(fileName))
    else:
        looper=MusicLooper(fileName)
        looper.startMusicLoopWave(optionalForMp3s_CheckRestartHowOften)
        return(looper)
"""


def loopsound(fileName):
    if system() == "Windows":
        return windowsPlayer.loopsound(fileName)
    else:
        looper = MusicLooper(fileName)
        looper.startMusicLoopWave()
        return looper


# pass an instance of a MusicLooper object and stop the loop, in Windows, use the Windows SingleSoundWindows class method


def stoploop(looperObject):
    if looperObject is not None:
        if system() == "Windows":
            stopsound(looperObject)
        else:
            looperObject.stopMusicLoop()
    else:
        pass
        # print("looperObject ", str(looperObject), " not playing")


# checks to see if song process is playing, (or if song alias's status is 'playing' in the case of Windows), returns True or False


def getIsLoopPlaying(looperObject):
    if looperObject is not None:
        if system() == "Windows":
            return getIsPlaying(looperObject)
        else:
            return looperObject.getPlaying()
    else:
        return False


# This just references the command 'playsound' to 'soundplay' with default to block/sync behaviour in case you want to use this in place
# of the playsound module, which last I checked was not being maintained.


def playsound(fileName, block=True):
    return soundplay(fileName, block)


# --------------------------------------------------------------------------------------------
if system() == "Windows":
    windowsPlayer = (
        WinMMSoundPlayer()
    )  # uses a single instance of the WinMMSoundPlayer class
    soundplay = windowsPlayer.soundplay

elif system() == "Darwin":
    soundplay = _soundplayMacOS

else:
    soundplay = _soundplayLinux
# --------------------------------------------------------------------------------------------

# definitely these names used by MusicLooper, could also used by end user
playwave = soundplay
stopwave = stopsound
loopwave = loopsound
