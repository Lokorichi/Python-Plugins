# coding=utf-8
__author__ = 'DreTaX'
__version__ = '1.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

RandNames = []

class ANA:

    def On_PluginInit(self):
        Util.ConsoleLog("Anti Non ASCII by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def GetNum(self):
        for x in xrange(0, 1000):
            if x in RandNames:
                continue
            RandNames.append(x)
            return x

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    def Replace(self, Old, To, Text):
        return re.sub('(?i)' + re.escape(Old), lambda m: To, Text)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        name = Player.Name
        name = self.CutName(name)
        name = re.sub(' +',' ', name)
        name = re.sub('[\t]+','', name)
        starts = name.startswith(' ')
        ends = name.endswith(' ')
        if starts is True:
            name = name.replace(name[0], '')
        if ends is True:
            n = len(name)
            if n > 1:
                name = name.replace(name[n-1], '')
        a = re.match('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', name)
        if not a:
            name = re.sub('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', "", name)
        n = len(name)
        if n <= 1:
            name = "Stranger"
            rand = self.GetNum()
            name = name + str(rand)
        Player.Name = name