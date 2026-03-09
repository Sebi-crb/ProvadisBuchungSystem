import BckE.Modelle.Gruppe as Gruppe
import BckE.Modelle.Raum as Raum
import BckE.Modelle.Trainer as Trainer
import BckE.Modelle.Modul as Modul


import datetime
from dataclasses import dataclass, field, fields
import inspect

@dataclass
class Kurs:
    _name: str = field(default="")
    _gruppe: str = field(default="")
    _trainer: str = field(default="")
    _raum: str = field(default="")
    _modul: str = field(default="")
    _start: int = field(default=0)
    _end: int = field(default=0)



    def __str__(self):
        return self.name


    def strip(self, string):
        return string.replace(' ', '').replace('\n', '')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name.strip(' ')

    @property
    def gruppe(self):
        return self._gruppe
    @gruppe.setter
    def gruppe(self, gruppe):
        self._gruppe = gruppe#.strip(' ')



    @property
    def trainer(self):
        return self._trainer
    @trainer.setter
    def trainer(self, trainer):
        self._trainer = trainer#.strip(' ')

    @property
    def raum(self):
        return self._raum
    @raum.setter
    def raum(self, raum):
        self._raum = raum#.strip(' ')

    @property
    def modul(self):
        return self._modul
    @modul.setter
    def modul(self, modul):
        self._modul = modul#.strip(' ')

    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, start):
        self._start = start#.strip(' ')

    @property
    def end(self):
        return self._end
    @end.setter
    def end(self, end):
        self._end = end#.strip(' ')




if __name__ == "__main__":

    trainer1 = Trainer('Jan', 'Christoph', ['Datanbanken', 'Engineering'], ['ef', 'efef'] ,'2')
    print(trainer1)



