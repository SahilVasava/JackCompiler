import os

class JackTokenizer:
    def __init__(self, jFile):
        self.jFile = jFile
        filePath, _ = os.path.splitext(jFile.name)
        self.outFile = open(filePath + 'TOut.xml', 'w')
        self.outFile.write('<tokens>\n')
        self.keywords = ['class' , 'constructor' , 'function' , 'method' ,'field' , 'static' , 'var' , 'int' , 'char' , 'boolean' ,'void' , 'true' , 'false' , 'null' , 'this' , 'let' , 'do' ,'if' , 'else' , 'while' , 'return']
        self.symbols = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' , '*' ,'/' , '&' , '|' , '<' , '>' , '=' , '~']

    def advance(self):
        cmtLines = False
        for line in self.jFile:
            line = line.strip()
            token = ''
            tokens = []
            if line.startswith('/*') and line.endswith('*/'):
                pass
            elif line.startswith('/*'):
                cmtLines = True
            elif line.endswith('*/'):
                cmtLines = False
            elif not line.startswith('//') and not cmtLines and line:
                if (ind:=line.find('//')) != -1:
                    line = line[:ind] 
                stringC = False
                for ch in line:
                    # check if the char is a symbol
                    if ch in self.symbols and not stringC:
                        # if token is not empty
                        if token.strip():
                            self.outFile.write('<'+self.tokenType(token) +'>'+ token + '</' +self.tokenType(token) +'>\n')
                            print(self.tokenType(token))
                            print(token)
                        if ch == '<':
                           token = '&lt;' 
                        elif ch == '>':
                           token = '&gt;' 
                        elif ch == '"':
                           token = '&quot;' 
                        elif ch == '&':
                           token = '&amp;' 
                        else:
                            token = ch
                        self.outFile.write('<'+self.tokenType(token) +'>'+ token + '</' +self.tokenType(token) +'>\n')
                        print(self.tokenType(token))
                        print(token)
                        token = ''
                    # else if char is not a white space char
                    elif ch == '"':
                        stringC =  not stringC 
                        if token.strip() and stringC:
                            self.outFile.write('<'+self.tokenType(token) +'>'+ token + '</' +self.tokenType(token) +'>\n')
                            print(self.tokenType(token))
                            print(token)
                        if stringC:
                            token = ch
                        else:
                            token += ch
                            self.outFile.write('<'+self.tokenType(token) +'>'+ token[1:-1] + '</' +self.tokenType(token) +'>\n')
                            print(self.tokenType(token))
                            print(token)
                            token = ''
                    elif ch.strip():
                        token += ch
                    elif not stringC:
                        if token.strip():
                            self.outFile.write('<'+self.tokenType(token) +'>'+ token + '</' +self.tokenType(token) +'>\n')
                            print(self.tokenType(token))
                            print(token)
                        token = ''
        self.outFile.write('</tokens>')
        self.outFile.close()

    def tokenType(self,token):
        if token in self.symbols + ['&lt;', '&gt;', '&quot;', '&amp;']:
            return 'symbol'
        elif token in self.keywords:
            return 'keyword'
        elif token.startswith('"'):
            return 'stringConstant'
        else:
            try:
                int(token)
                return 'integerConstant'
            except:
                return 'identifier'
