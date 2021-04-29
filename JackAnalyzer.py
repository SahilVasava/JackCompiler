#!/usr/bin/env python3

import sys
import os

from JackTokenizer import JackTokenizer

def main():
    path = os.path.abspath(sys.argv[1])
    if os.path.isdir(path):
        pass
        #dirName = os.path.basename(os.path.normpath(path))
        #path = os.path.join(path, dirName+'.asm')
    else:
        jFile = open(path, 'r')
        tokenizer = JackTokenizer(jFile)       
        tokenizer.advance()
        #path, _ = os.path.splitext(path) 
        #path = path + '.asm'

if __name__ == "__main__":
    main()
