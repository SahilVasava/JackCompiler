#!/usr/bin/env python3

class SymbolTable:

    def __init__(self):
        self.classST = {}
        self.subST = {}
        self.cInd = 0
        self.sInd = 0

    def startSubroutine(self):
        self.subST.clear()
        self.sInd = 0

    def define(self, name, tType, kind):
        print(f'KIND {kind}')
        if kind in ['STATIC', 'FIELD']:
            self.classST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.cInd
                    }
            self.cInd += 1
        else:
            self.subST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.sInd
                    }
            self.sInd += 1

    def varCount(self, kind):
        count = 0
        if kind in ['STATIC', 'FIELD']:
            for value in self.classST.values():
                if value['type'] == kind:
                    count += 1
        else:
            for value in self.subST.values():
                if value['type'] == kind:
                    count += 1
        return count

    def kindOf(self, name):
        kind = None
        if self.classST.get(name):
            kind = self.classST.get(name).get('kind')
        elif self.subST.get(name):
            kind = self.subST.get(name).get('kind')
        return kind

    def typeOf(self, name):
        tType = None
        if self.classST.get(name):
            tType = self.classST.get(name).get('type')
        elif self.subST.get(name):
            tType = self.subST.get(name).get('type')
        return tType

    def indexOf(self, name):
        index = None
        print(f'NAME: {name} {self.subST.get(name)}')
        if self.classST.get(name):
            index = self.classST.get(name).get('index')
        elif self.subST.get(name):
            index = self.subST.get(name).get('index')
        return str(index)


























        
