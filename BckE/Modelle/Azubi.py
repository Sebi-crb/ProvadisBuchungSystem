import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Azubi:
    _name: str = field(default="")
    _vorname: str = field(default="")
    _ausbildungsunternehmen: str = field(default="")
    _ausbildungsStart: int = field(default="")
    _attendedModules: list = field(default="")
    _abwesenheiten: list = field(default="")
    _block: str = field(default="")
    _id: str = field(default="")




    def __str__(self):
        _attendedModules = ', '.join(map(str, self.attendedModules)) if self.attendedModules else ''
        _abwesenheiten = ', '.join(map(str, self.abwesenheiten)) if self.abwesenheiten else ''
        is_avail = str(self.isAvailable) if getattr(self, 'isAvailable', None) is not None else 'unbekannt'
        return self.name + ' ' + self.vorname +  ' ' + self.ausbildungsStart +' ' + self.ausbildungsunternehmen +' '+  _attendedModules + ' ' + _abwesenheiten + ' ' + is_avail + ''


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
    def ausbildungsunternehmen(self):
        return self._ausbildungsunternehmen
    @ausbildungsunternehmen.setter
    def ausbildungsunternehmen(self, ausbildungsunternehmen):
        self._ausbildungsunternehmen = ausbildungsunternehmen.strip(' ')

    @property
    def ausbildungsStart(self):
        return self._ausbildungsStart
    @ausbildungsStart.setter
    def ausbildungsStart(self, ausbildungsStart):
        self._ausbildungsStart = ausbildungsStart


    @property
    def attendedModules(self):
        return self._attendedModules
    @attendedModules.setter
    def attendedModules(self, attendedModules):
        self._attendedModules = attendedModules#.strip(' ')

    @property
    def abwesenheiten(self):
        return self._abwesenheiten
    @abwesenheiten.setter
    def abwesenheiten(self, abwesenheiten):
        self._abwesenheiten = abwesenheiten.strip(' ')

    @property
    def block(self):
        return self._block
    @block.setter
    def block(self, block):
        self._block = block.strip(' ')

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id#.strip(' ')




if __name__ == "__main__":
    Azubi1 = Azubi('Eren', 'Senkaya', ['Datanbanken', 'Engineering'], ['ef', 'efef'] ,'2')
    print(Azubi1)
