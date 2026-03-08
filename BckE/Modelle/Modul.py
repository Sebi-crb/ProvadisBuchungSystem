import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Modul:
    _name: str = field(default="")
    _beschreibung: str = field(default="")
    _dauer: float = field(default="")
    _zuordnungLernjahr: int = field(default="")
    _optionaleVorgängermodule: list = field(default="")
    _verpflichtendeVorgängermodule: list = field(default="")
    _pcKennzeichnung: bool = field(default="")



    def __str__(self):
        optionale = ', '.join(map(str, self.optionaleVorgängermodule)) if self.optionaleVorgängermodule else ''
        verpflichtende = ', '.join(map(str, self.verpflichtendeVorgängermodule)) if self.verpflichtendeVorgängermodule else ''
        return self.name + ' ' + self.beschreibung+ ' '  + self.dauer + ' ' + self.zuordnungLernjahr + ' ' + optionale + '' + verpflichtende + '' + self.pcKennzeichnung + '' + self.anzahlTrainer


    def strip(self, string):
        return string.replace(' ', '').replace('\n', '')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def beschreibung(self):
        return self._beschreibung
    @beschreibung.setter
    def beschreibung(self, beschreibung):
        self._beschreibung = beschreibung.strip(' ')



    @property
    def dauer(self):
        return self._dauer
    @dauer.setter
    def dauer(self, dauer):
        self._dauer = dauer.strip(' ')

    @property
    def zuordnungLernjahr(self):
        return self._zuordnungLernjahr
    @zuordnungLernjahr.setter
    def zuordnungLernjahr(self, zuordnungLernjahr):
        self._zuordnungLernjahr = zuordnungLernjahr.strip(' ')

    @property
    def optionaleVorgängermodule(self):
        return self._optionaleVorgängermodule
    @optionaleVorgängermodule.setter
    def optionaleVorgängermodule(self, optionaleVorgängermodule):
        self._optionaleVorgängermodule = optionaleVorgängermodule.strip(' ')

    @property
    def verpflichtendeVorgängermodule(self):
        return self._verpflichtendeVorgängermodule
    @verpflichtendeVorgängermodule.setter
    def verpflichtendeVorgängermodule(self, verpflichtendeVorgängermodule):
        self._verpflichtendeVorgängermodule = verpflichtendeVorgängermodule.strip(' ')

    @property
    def pcKennzeichnung(self):
        return self._pcKennzeichnung
    @pcKennzeichnung.setter
    def pcKennzeichnung(self, pcKennzeichnung):
        self._gender = pcKennzeichnung.strip(' ')




if __name__ == "__main__":

    Modul1 = Modul('Softwareentwicklung', 'Entwicklung von Software', '2.5', '2', ["ef", "efef"])
    print(Modul1)
