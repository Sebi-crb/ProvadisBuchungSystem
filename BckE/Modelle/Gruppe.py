import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Gruppe:
    _name: str = field(default="")
    _azubiList: list = field(default="")
    _block: str = field(default="")
    _attendedModules: str = field(default="")



    countAzubis: int = 0

    def __init__(self, name: str, azubiList: list):
        self._name = name
        self._azubiList = azubiList
        self.setCount(len(self._azubiList))

    def __str__(self):
        azubiListb = ', '.join(map(str, self.azubiList)) if self.azubiList else ''
        return self.name + ' ' + str(self.countAzubis) + ' '  + azubiListb

    def strip(self, string):
        return string.replace(' ', '').replace('\n', '')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, titel):
        self._titel = titel

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block):
        self._block = block

    @property
    def attendedModules(self):
        return self._attendedModules
    @attendedModules.setter
    def attendedModules(self, attendedModules):
        self._attendedModules = attendedModules#.strip(' ')

    #@property
    #def countAzubis(self):
        #return self._countAzubis
    #@countAzubis.setter
    #def countAzubis(self, countAzubis):
        #self._countAzubis = countAzubis.strip(' ')




    @property
    def azubiList(self):
        return self._azubiList

    @azubiList.setter
    def azubiList(self, azubiList):
        #print("ef")
        # accept either a list or a comma-separated string; keep minimal changes
        if isinstance(azubiList, list):
            self._azubiList = azubiList
        else:
            # treat as string: split on commas and strip whitespace/newlines
            if azubiList:
                self._azubiList = [item.strip() for item in str(azubiList).split(',') if item.strip()]
            else:
                self._azubiList = []
        self.setCount()

    def setCount(self, listlength):
        #print("ef")
        self.countAzubis = listlength

    def getAzubiCount(self):
        return self.countAzubis




if __name__ == "__main__":

    Gruppe1 = Gruppe('24FA03', ["Eren", "Ali", "Sebastian", "Farzad"])
    print(Gruppe1)

