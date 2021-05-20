class VMWriter:
    def __init__(self, path):
        self.outF = open(path+'Out.vm','w')

    def writePush(self, segment, index):
        
        self.outF.write(f'push {segment} {index}\n') 

    def writePop(self, segment, index):
        
        self.outF.write(f'pop {segment} {index}\n')

    def writeArithmetic(self, command):
        
        self.outF.write(command+'\n')

    def writeLabel(self, label):

        self.outF.write(f'label {label}\n')

    def writeGoto(self, label):

        self.outF.write(f'goto {label}\n')

    def writeIf(self, label):

        self.outF.write(f'if-goto {label}\n')

    def writeCall(self, name, nArgs):

        self.outF.write(f'call {name} {nArgs}\n')

    def writeFunction(self, name, nLocals):

        self.outF.write(f'call {name} {nLocals}\n')

    def writeReturn(self):

        self.outF.write(f'return')

    def close(self):

        self.outF.close()

