import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Trainer:
    _name: str = field(default="")
    _vorname: str = field(default="")
    _modulTeacher: list = field(default="")
    _urlaub: list = field(default="")
    _blockedModul: list = field(default="")



    def __str__(self):
        lehervon = ', '.join(map(str, self.modulTeacher)) if self.modulTeacher else ''
        urlaub = ', '.join(map(str, self.urlaub)) if self.urlaub else ''
        is_avail = str(self.isAvailable) if getattr(self, 'isAvailable', None) is not None else 'unbekannt'
        return self.name + ' ' + self.vorname +  ' ' +   lehervon + ' ' + urlaub + ' ' + is_avail + ''


    def strip(self, string):
        return string.replace(' ', '').replace('\n', '')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def vorname(self):
        return self._vorname
    @vorname.setter
    def vorname(self, vorname):
        self._vorname = vorname.strip(' ')



    @property
    def modulTeacher(self):
        return self._modulTeacher
    @modulTeacher.setter
    def modulTeacher(self, modulTeacher):
        self._modulTeacher = modulTeacher.strip(' ')

    @property
    def urlaub(self):
        return self._urlaub
    @urlaub.setter
    def urlaub(self, urlaub):
        self._urlaub = urlaub.strip(' ')

    @property
    def blockedModul(self):
        return self._blockedModul
    @blockedModul.setter
    def blockedModul(self, blockedModul):
        self._blockedModul = blockedModul.strip(' ')




if __name__ == "__main__":

    trainer1 = Trainer('Jan', 'Christoph', ['Datanbanken', 'Engineering'], ['ef', 'efef'] ,'2')
    print(trainer1)
