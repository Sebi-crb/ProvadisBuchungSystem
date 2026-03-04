import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Raum:
    _name: str = field(default="")
    _isPC: bool = field(default="")
    _isBlocked: list = field(default="")



    def __str__(self):
        is_avail = str(self.isAvailable) if getattr(self, 'isAvailable', None) is not None else 'unbekannt'
        return self.name + ' ' + self.isPC +  ' ' +   self.isFree


    def strip(self, string):
        return string.replace(' ', '').replace('\n', '')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def isPC(self):
        return self._isPC
    @isPC.setter
    def isPC(self, isPC):
        self._isPC = isPC.strip(' ')



    @property
    def isBlocked(self):
        return self._isBlocked
    @isBlocked.setter
    def isBlocked(self, isBlocked):
        self._isBlocked = isBlocked.strip(' ')





#if __name__ == "__main__":

 #   Raum1 = Raum('E102', 'True', 'True')
  #  print(Raum1)
