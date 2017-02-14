#---VladVons@gmail.com
# 11.02.17
# micropython ESP8266
#---

import uos
import ujson
#
from common import TFile

class TConfig():
    def __init__(self):
        self.Data = {}

    def FindNode(self, aNode, aPath):
        for Item in aPath.strip('/').split('/'):
            if (Item != ''):
                Value = aNode.get(Item)
                if (Value == None):
                    return None
                else:
                    aNode = Value
        return aNode

    def LoadFile(self, aFile = 'config.json'):
        Result = TFile.Exists(aFile)
        if (Result):
            with open(aFile) as File:
                self.Data = ujson.load(File)

    def GetItem(self, aName, aDef = ''):
        Result = self.FindNode(self.Data, aName)
        if (Result == None):
            Result = aDef

        return Result

    def _GetItemsRecurs(self, aNode, aPath):
        Result = {}
        for Key in aNode.keys():
            Value = aNode[Key]
            Path  = aPath + '/' + Key
            if (type(Value) is dict):
                Items = self._GetItemsRecurs(Value, Path)
                # ??? slow method
                for Item in Items:
                    Result[Item] = Items[Item]
            else:
                Result[Path] = Value
        return Result

    def GetItems(self, aNode = None):
        if (aNode == None):
            aNode = self.Data
        return self._GetItemsRecurs(aNode, '')

    def Filter(self, aItems):
        Result = {}
        for Item in aItems:
            Result[Item] = self.GetItem(Item)
        return Result
