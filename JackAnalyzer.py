#!/usr/bin/env python3

import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine as Parser

def parseFile(path):
    jFile = open(path, 'r')
    path, _ = os.path.splitext(jFile) 
    tokenizer = JackTokenizer(jFile)       
    parser = Parser(tokenizer, path)

def main():
    path = os.path.abspath(sys.argv[1])
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.jack'):
                    fPath = os.path.join(root,file)
                    parseFile(fPath) 
        #dirName = os.path.basename(os.path.normpath(path))
        #path = os.path.join(path, dirName+'.asm')
    else:
        parseFile(path)
        #path = path + '.asm'

if __name__ == "__main__":
    main()
