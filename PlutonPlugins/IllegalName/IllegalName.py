# coding=utf-8
__author__ = 'DreTaX'
__version__ = '1.3'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import re
import sys
path = Util.GetPublicFolder()
Lib = True
try:
    sys.path.append(path + "\\Python\\Lib\\")
    import random
except ImportError:
    Lib = False
"""
    Class
"""


class IllegalName:

    RandNames = []
    Words = {}

    def On_PluginInit(self):
        ini = self.IllegalNameConfig()
        replace = ini.EnumSection("ReplaceCharactersTo")
        for wr in replace:
            s = str(ini.GetSetting("ReplaceCharactersTo", wr))
            self.Words.update({wr:s})

    def GetRand(self):
        d = random.randrange(0, 550)
        while d in self.RandNames:
            d = random.randrange(0, 550)
        return d

    def getIllegal(self):
        if not Plugin.IniExists("IllegalNames"):
            IllegalNames = Plugin.CreateIni("IllegalNames")
            IllegalNames.AddSetting("IllegalNames", "Name1", "Suck")
            IllegalNames.AddSetting("IllegalNames", "Name2", "Fuck")
            IllegalNames.AddSetting("IllegalNames", "Name3", "SHITSERVER")
            IllegalNames.Save()
        return Plugin.GetIni("IllegalNames")

    def IllegalNameConfig(self):
        if not Plugin.IniExists("IllegalNameConfig"):
            loc = Plugin.CreateIni("IllegalNameConfig")
            loc.Save()
        return Plugin.GetIni("IllegalNameConfig")

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+','', string)
        return name

    def Replace(self, Old, To, Text):
        return re.sub('(?i)'+re.escape(Old), lambda m: To, Text)

    def On_ClientAuth(self, AuthEvent):
        name = AuthEvent.Connection.username
        ini = self.IllegalNameConfig()
        asciie = int(ini.GetSetting("options", "CheckForNonAscii"))
        regex = int(ini.GetSetting("options", "CheckWithRegEx"))
        illini = self.getIllegal()
        listnames = illini.EnumSection("IllegalNames")
        compile = re.compile(r'\b(' + '|'.join(self.Words.keys()) + r')\b')
        name = compile.sub(lambda x: self.Words[x.group()], name)
        for checkn in listnames:
            get = illini.GetSetting("IllegalNames", checkn)
            name = self.Replace(get, '', name)
        if asciie == 1:
            newname = self.CutName(name)
            name = newname
        if regex == 1:
            name = re.sub(' +',' ', name)
            name = re.sub('[\t]+','', name)
            starts = name.startswith(' ')
            ends = name.endswith(' ')
            if starts is True:
                name.replace(name[0], '')
            if ends is True:
                n = len(name)
                name.replace(name[n-1], '')
            a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
            if not a:
                name = re.sub('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', "", name)
            n = len(name)
            if n <= 1:
                name = name + "Stranger"
                if Lib:
                    rand = self.GetRand()
                    name = name + str(rand)
        AuthEvent.con.username = str(name)