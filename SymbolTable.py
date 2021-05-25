#!/usr/bin/env python3

class SymbolTable:

    def __init__(self):
        self.classST = {}
        self.subST = {}
        self.fInd = 0
        self.sInd = 0
        self.aInd = 0
        self.lInd = 0
        self.currentSubRType = ''
        self.currentClassType = ''

    def startSubroutine(self, subRType, classType):
        self.subST.clear()
        self.aInd = 0
        self.lInd = 0
        self.currentSubRType = subRType
        self.currentClassType = classType

    def getSubRType(self):
        return self.currentSubRType

    def getClassType(self):
        return self.currentClassType

    def define(self, name, tType, kind):
        print(f'KIND {kind}')
        if kind == 'STATIC':
            self.classST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.sInd
                    }
            self.sInd += 1
        elif kind == 'FIELD':
            self.classST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.fInd
                    }
            self.fInd += 1
        elif kind == 'ARG':
            self.subST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.aInd
                    }
            self.aInd += 1
        elif kind == 'LOCAL':
            self.subST[name] =  {
                        'type' : tType,
                        'kind' : kind,
                        'index' : self.lInd
                    }
            self.lInd += 1

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


























        
