#!/usr/bin/env python3

import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine as Parser
from SymbolTable import SymbolTable

def parseFile(path):
    jFile = open(path, 'r')
    path, _ = os.path.splitext(path) 
    tokenizer = JackTokenizer(jFile)       
    symTab = SymbolTable()
    parser = Parser(tokenizer, path, symTab)
    jFile.close()

def main():
    path = os.path.abspath(sys.argv[1])
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for filee in files:
                if filee.endswith('.jack'):
                    fPath = os.path.join(root,filee)
                    print(f'parsing file: {fPath}')
                    parseFile(fPath) 
        #dirName = os.path.basename(os.path.normpath(path))
        #path = os.path.join(path, dirName+'.asm')
    else:
        parseFile(path)
        #path = path + '.asm'

if __name__ == "__main__":
    main()
