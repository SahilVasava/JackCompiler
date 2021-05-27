from VMWriter import VMWriter
import os

class CompilationEngine:
    def __init__(self, tokenizer, path, symTab, vmw):
        self.fileName = os.path.basename(path)
        self.ifInd = 1
        self.whileInd = 1
        self.nFieldVar = 0
        self.nLocalVars = 0
        self.subName = ''
        self.outF = open(path+'Out_ExtraTags.xml','w')
        self.vmw = vmw
        self.st = symTab
        self.tkz = tokenizer
        self.ops = ['+','-','*','/','|','=','<','>','&']+['&lt;', '&gt;', '&amp;']
        self.charSet = {}
        self.initCharSet()
        self.compileClass()


    def initCharSet(self):
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        sym1 = ['sp','!','"','#','$','%','&','\'','(',')','*','+',',','-','.','/'] 
        sym2 = [':',';','<','=','>','?','@']
        sym3 = ['[','gb',']','^','_','`'] 
        sym4 = ['{','|','}','~']
        smL = 97
        lL = 65
        numC = 48
        sym1C = 32
        sym2C = 58
        sym3C = 91
        sym4C = 123
        for i,l in enumerate(letters):
            self.charSet[l] = str(smL+i)
            self.charSet[l.upper()] = str(lL+i)
        for i,l in enumerate(sym1):
            self.charSet[l] = str(sym1C+i)
        for i,l in enumerate(sym2):
            self.charSet[l] = str(sym2C+i)
        for i,l in enumerate(sym3):
            self.charSet[l] = str(sym3C+i)
        for i,l in enumerate(sym4):
            self.charSet[l] = str(sym4C+i)
        for i in range(10):
            self.charSet[str(i)] = str(numC+i)


        for k,v in self.charSet.items():
            print(f'{k} : {v}')
        

    def compileClass(self):
        token = self.tkz.advance()
        print('<class>\n\t')
        self.outF.write('<class>\n\t')
        #print(f'Token: {token}')

        # class
        self.printTag(token)

        # className
        token = self.tkz.advance()
        self.printTag(token)

        self.printTag('class', 'identifierCat')
        self.printTag('defined', 'identifierDef')

        # {
        token = self.tkz.advance()
        self.printTag(token)

        token = self.tkz.advance()
        while token == 'static' or token == 'field':
            self.compileClassVarDec(token)
            token = self.tkz.advance()
        while token == 'constructor' or token == 'function' or token == 'method':
            self.compileSubroutineDec(token)
            token = self.tkz.advance()
        self.printTag(token)
        print('</class>\n\t')
        self.outF.write('</class>\n\t')
        self.outF.close()


    def compileClassVarDec(self,token):
        print('<classVarDec>\n\t')
        self.outF.write('<classVarDec>\n\t')


        # static | field
        self.printTag(token)
        kindToken = token.upper()

        token = self.tkz.advance()
        # type
        self.printTag(token)
        typeToken = token 

        if typeToken not in ['int', 'char', 'boolean']:
            self.printTag('class', 'identifierCat')
            self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        # varName
        self.printTag(token)
        if kindToken.lower() == 'field':
            self.nFieldVar += 1
            print(f'nfieldvar {self.nFieldVar}')
        nameToken = token
        self.printTag(kindToken, 'identifierCat')
        self.st.define(nameToken, typeToken, kindToken)
        indexToken = self.st.indexOf(nameToken)
        self.printTag(indexToken, 'identifierInd')
        self.printTag('defined', 'identifierDef')
        

        token = self.tkz.advance()
        # check if it is ,
        while token == ',':
            # ,
            self.printTag(token)
            # varName
            token = self.tkz.advance()
            self.printTag(token)
            if kindToken.lower() == 'field':
                self.nFieldVar += 1
            nameToken = token

            self.printTag(typeToken, 'identifierCat')
            self.st.define(nameToken, typeToken, kindToken)
            indexToken = self.st.indexOf(nameToken)
            self.printTag(indexToken, 'identifierInd')
            self.printTag('defined', 'identifierDef')
            token = self.tkz.advance()

        self.printTag(token)
        print('</classVarDec>')
        self.outF.write('</classVarDec>\n\t')
        
    def compileSubroutineDec(self,token):
        print('<subroutineDec>\n\t')
        self.outF.write('<subroutineDec>\n\t')


        # constructor | function | method
        self.printTag(token)
        subRType = token

        token = self.tkz.advance()
        # void | type
        self.printTag(token)
        typeToken = token

        # start subroutine symbol table
        self.st.startSubroutine(subRType, typeToken)

        # append this in the symbol table if subR is a constructor
        #if subRType == 'constructor':
        #    self.st.define('this', typeToken, 'ARG')
        #    self.vmw.writePush('constant', self.nFieldVar)
        #    self.vmw.writeCall('Memory.alloc', '1')
        #    self.vmw.writePop('pointer', '0')
        #elif subRType == 'method':
        #    self.vmw.writePush('argument', '0')
        #    self.vmw.writePop('pointer', '0')

        if typeToken not in ['int', 'char', 'boolean', 'void']:
            self.printTag('class', 'identifierCat')
            self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        # subroutineName
        self.printTag(token)
        self.subName = token
        self.printTag('subroutine', 'identifierCat')
        self.printTag('defined', 'identifierDef')


        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        #while token != ')':
            # parameterList

        self.compileParameterList(token)
        token = self.tkz.advance()

        # )
        self.printTag(token)

        token = self.tkz.advance()
        # subroutineBody
        self.compileSubroutineBody(token)

        print('</subroutineDec>\n\t')
        self.outF.write('</subroutineDec>\n\t')
            
    def compileParameterList(self,token):
        print('<parameterList>\n\t')
        self.outF.write('<parameterList>\n\t')

        if self.st.getSubRType() == 'method':
            self.st.define('this', self.fileName, 'ARG')

        if token != ')':

            kindToken = 'ARG'
            # type
            self.printTag(token) 
            typeToken = token

            if typeToken not in ['int', 'char', 'boolean']:
                self.printTag('class', 'identifierCat')
                self.printTag('used', 'identifierDef')

            token = self.tkz.advance()
            # varName
            self.printTag(token)
            nameToken = token
            self.printTag(kindToken, 'identifierCat')
            self.st.define(nameToken, typeToken, kindToken)
            indexToken = self.st.indexOf(nameToken)
            self.printTag(indexToken, 'identifierInd')
            self.printTag('defined', 'identifierDef')

            token = self.tkz.advance()
            # , type varName
            while token != ')':
                # ,
                self.printTag(token)

                token = self.tkz.advance()
                # type
                self.printTag(token)
                typeToken = token

                if typeToken not in ['int', 'char', 'boolean']:
                    self.printTag('class', 'identifierCat')
                    self.printTag('used', 'identifierDef')

                token = self.tkz.advance()
                # varName
                self.printTag(token)
                nameToken = token
                self.printTag(kindToken, 'identifierCat')
                self.st.define(nameToken, typeToken, kindToken)
                indexToken = self.st.indexOf(nameToken)
                self.printTag(indexToken, 'identifierInd')
                self.printTag('defined', 'identifierDef')

                token = self.tkz.advance()
        self.tkz.backward()    
        print('</parameterList>\n\t')
        self.outF.write('</parameterList>\n\t')
        

    def compileSubroutineBody(self,token):
        print('<subroutineBody>\n\t')
        self.outF.write('<subroutineBody>\n\t')
        # {
        self.printTag(token) 

        token = self.tkz.advance()
        # check if it a variable declaration
        while token == 'var':
            self.compileVarDec(token)
            token = self.tkz.advance()

        # write the vm code 'function filename.subName nLocalVars'
        self.vmw.writeFunction(self.fileName+'.'+self.subName, self.nLocalVars)
        self.nLocalVars = 0

        # append this in the symbol table if subR is a constructor
        if self.st.getSubRType() == 'constructor':
            #self.st.define('this', self.st.getClassType(), 'ARG')
            self.vmw.writePush('constant', self.nFieldVar)
            self.vmw.writeCall('Memory.alloc', '1')
            self.vmw.writePop('pointer', '0')
        elif self.st.getSubRType() == 'method':
            self.vmw.writePush('argument', '0')
            self.vmw.writePop('pointer', '0')

        if token != '}':
            self.compileStatements(token)

        #while token != '}':
        #    if token == 'let':
        #        self.compileLetStatement(token)
        #    elif token == 'if':
        #        self.compileIfStatement(token)
        #    elif token == 'while':
        #        self.compileWhileStatement(token)
        #    elif token == 'do':
        #        self.compileDoStatement(token)
        #    elif token == 'return':
        #        self.compileReturnStatement(token)
        #    token = self.tkz.advance()
        
        token = self.tkz.advance()
        # }
        self.printTag(token)

        print('</subroutineBody>\n\t')
        self.outF.write('</subroutineBody>\n\t')

    def compileStatements(self,token):
        print('<statements>\n\t')
        self.outF.write('<statements>\n\t')
        
        while token != '}':
            if token == 'let':
                self.compileLetStatement(token)
            elif token == 'if':
                self.compileIfStatement(token)
            elif token == 'while':
                self.compileWhileStatement(token)
            elif token == 'do':
                self.compileDoStatement(token)
            elif token == 'return':
                self.compileReturnStatement(token)
            token = self.tkz.advance()
        
        self.tkz.backward()
        print('</statements>\n\t')
        self.outF.write('</statements>\n\t')
        
    def compileVarDec(self,token):
        print('<varDec>\n\t')
        self.outF.write('<varDec>\n\t')

        # var
        self.printTag(token) 
        kindToken = 'LOCAL'

        token = self.tkz.advance()
        # type
        self.printTag(token)
        typeToken = token

        if typeToken not in ['int', 'char', 'boolean']:
            self.printTag('class', 'identifierCat')
            self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        # varName
        self.printTag(token)
        self.nLocalVars += 1
        nameToken = token
        self.printTag(kindToken, 'identifierCat')
        self.st.define(nameToken, typeToken, kindToken)
        indexToken = self.st.indexOf(nameToken)
        print(f'INDEX TOKEN: {indexToken}')
        self.printTag(indexToken, 'identifierInd')
        self.printTag('defined', 'identifierDef')

        token = self.tkz.advance()
        # , varName
        while token != ';':
            # ,
            self.printTag(token)

            token = self.tkz.advance()
            # varName
            self.printTag(token)
            self.nLocalVars += 1
            nameToken = token
            self.printTag(kindToken, 'identifierCat')
            self.st.define(nameToken, typeToken, kindToken)
            indexToken = self.st.indexOf(nameToken)
            self.printTag(indexToken, 'identifierInd')
            self.printTag('defined', 'identifierDef')

            token = self.tkz.advance()

        # }
        self.printTag(token)
        
        print('</varDec>\n\t')
        self.outF.write('</varDec>\n\t')

    def compileLetStatement(self,token):
        print('<letStatement>\n\t')
        self.outF.write('<letStatement>\n\t')

        # let
        self.printTag(token)

        token = self.tkz.advance()
        # varName
        self.printTag(token)
        nameToken = token
        segment = self.st.kindOf(nameToken)
        index = self.st.indexOf(nameToken)

        kindToken = self.st.kindOf(nameToken)
        #print(f'KIND {kindToken} name {nameToken}')
        self.printTag(kindToken, 'identifierCat')

        #self.st.define(nameToken, typeToken, kindToken)
        indexToken = self.st.indexOf(nameToken)
        self.printTag(indexToken, 'identifierInd')
        self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        arr = False
        # [
        if token == '[':
            self.printTag(token)
            if segment == 'STATIC':
                self.vmw.writePush('static', index)
            elif segment == 'FIELD':
                self.vmw.writePush('this', index)
            elif segment == 'ARG':
                self.vmw.writePush('argument', index)
            elif segment == 'LOCAL':
                self.vmw.writePush('local', index)

            token = self.tkz.advance()
            # expression
            self.compileExpression(token)

            # write vm code for adding a and index i where let a[i] = b[j]
            self.vmw.writeArithmetic('add')
            
            token = self.tkz.advance()
            # ]
            self.printTag(token)
            token = self.tkz.advance()
            arr = True

        # =
        self.printTag(token)

        token = self.tkz.advance()
        # expression
        self.compileExpression(token)
        
        if arr:
            self.vmw.writePop('temp', '0')
            self.vmw.writePop('pointer', '1')
            self.vmw.writePush('temp', '0')
            self.vmw.writePop('that', '0')
        else:
            if segment == 'STATIC':
                self.vmw.writePop('static', index)
            elif segment == 'FIELD':
                self.vmw.writePop('this', index)
            elif segment == 'ARG':
                self.vmw.writePop('argument', index)
            elif segment == 'LOCAL':
                self.vmw.writePop('local', index)


        token = self.tkz.advance()
        # ;
        self.printTag(token)
            
        print('</letStatement>\n\t')
        self.outF.write('</letStatement>\n\t')
        
    def compileIfStatement(self,token):
        print('<ifStatement>\n\t')
        self.outF.write('<ifStatement>\n\t')
        
        # if
        self.printTag(token)

        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        # expression
        self.compileExpression(token)

        # write the not of exp
        self.vmw.writeArithmetic('not')

        # write if-goto label(else case label)
        l1 = f'{self.fileName}_if_{self.ifInd}'
        self.ifInd += 1
        self.vmw.writeIf(l1)

        token = self.tkz.advance()
        # )
        self.printTag(token)

        token = self.tkz.advance()
        # {
        self.printTag(token)

        token = self.tkz.advance()

        if token != '}':
            self.compileStatements(token)

        #while token != '}':
        #    if token == 'let':
        #        self.compileLetStatement(token)
        #    elif token == 'if':
        #        self.compileIfStatement(token)
        #    elif token == 'while':
        #        self.compileWhileStatement(token)
        #    elif token == 'do':
        #        self.compileDoStatement(token)
        #    elif token == 'return':
        #        self.compileReturnStatement(token)
        #    token = self.tkz.advance()
        
        token = self.tkz.advance()
        # }
        self.printTag(token)
        
        # write goto l2
        l2 = f'{self.fileName}_if_{self.ifInd}'
        self.ifInd += 1 
        self.vmw.writeGoto(l2)
        
        # write label l1(else case label)
        self.vmw.writeLabel(l1)

        token = self.tkz.advance()
        # else
        if token == 'else':
            self.printTag(token)
            
            token = self.tkz.advance()
            # {
            self.printTag(token)

            token = self.tkz.advance()
    
            #if token != '}':
            self.compileStatements(token)

            #while token != '}':
            #    if token == 'let':
            #        self.compileLetStatement(token)
            #    elif token == 'if':
            #        self.compileIfStatement(token)
            #    elif token == 'while':
            #        self.compileWhileStatement(token)
            #    elif token == 'do':
            #        self.compileDoStatement(token)
            #    elif token == 'return':
            #        self.compileReturnStatement(token)
            #    token = self.tkz.advance()
            
            token = self.tkz.advance()
            # }
            self.printTag(token)
        else:
            self.tkz.backward()

        # write label l2(else case label)
        self.vmw.writeLabel(l2)
 
        print('</ifStatement>\n\t')
        self.outF.write('</ifStatement>\n\t')

    def compileWhileStatement(self,token):
        print('<whileStatement>\n\t')
        self.outF.write('<whileStatement>\n\t')

        # while
        self.printTag(token)

        # write label l1
        l1 = f'{self.fileName}_while_{self.whileInd}'
        self.whileInd += 1 
        self.vmw.writeLabel(l1)

        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        # expression
        self.compileExpression(token)

        # write the not of exp
        self.vmw.writeArithmetic('not')

        # write if-goto label(else case label)
        l2 = f'{self.fileName}_while_{self.whileInd}'
        self.whileInd += 1 
        self.vmw.writeIf(l2)

        token = self.tkz.advance()
        # )
        self.printTag(token)

        token = self.tkz.advance()
        # {
        self.printTag(token)

        token = self.tkz.advance()
        if token != '}':
            self.compileStatements(token)

        #while token != '}':
        #    if token == 'let':
        #        self.compileLetStatement(token)
        #    elif token == 'if':
        #        self.compileIfStatement(token)
        #    elif token == 'while':
        #        self.compileWhileStatement(token)
        #    elif token == 'do':
        #        self.compileDoStatement(token)
        #    elif token == 'return':
        #        self.compileReturnStatement(token)
        #    token = self.tkz.advance()
        
        token = self.tkz.advance()
        # }
        self.printTag(token)

        # write goto l1
        self.vmw.writeGoto(l1)

        # write label l2
        self.vmw.writeLabel(l2)
        
        print('</whileStatement>\n\t')
        self.outF.write('</whileStatement>\n\t')

    def compileDoStatement(self,token):
        print('<doStatement>\n\t')
        self.outF.write('<doStatement>\n\t')
        subName = ''
        nArgs = 0
        
        # do
        self.printTag(token)

        token = self.tkz.advance()

        # subroutine call
        #self.compileSubroutineCall(token)

        # subroutineName | className | varName
        self.printTag(token)
        nameToken = token
        kindToken = self.st.kindOf(nameToken)

        # check if the subCall is of type varName.subR
        tok = self.tkz.advance()
        self.tkz.backward()
        if kindToken and tok == '.':
            nArgs += 1
            #print(f'varNammmmm {kindToken} {nArgs}')

        # cat of token is class or subroutine
        if not kindToken:
            if tok == '.':
                self.printTag('class', 'identifierCat')
                subName = nameToken+'.'
            else:
                self.printTag('subroutine', 'identifierCat')
                subName = self.fileName+'.'+nameToken
                self.vmw.writePush('pointer','0')
                nArgs += 1
        # cat of token is var, arg, static or field
        else:
            self.printTag(kindToken, 'identifierCat')
            indexToken = self.st.indexOf(nameToken)
            self.printTag(indexToken, 'identifierInd')
            typeToken = self.st.typeOf(nameToken)

            print(f'typetoken {typeToken}')
            subName = typeToken+'.' 

            # vm code writer
            if kindToken == 'STATIC':
                self.vmw.writePush(kindToken.lower(), indexToken) 
            elif kindToken == 'FIELD':
                self.vmw.writePush('this', indexToken) 
            elif kindToken == 'ARG':
                self.vmw.writePush('argument', indexToken) 
            elif kindToken == 'LOCAL':
                self.vmw.writePush('local', indexToken) 

        self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        if token == '.':
            # .
            self.printTag(token)

            token = self.tkz.advance()
            # subroutineName
            self.printTag(token)
            subName += token

            self.printTag('subroutine', 'identifierCat')
            self.printTag('used', 'identifierDef')

            token = self.tkz.advance()

        # (
        self.printTag(token)
        
        token = self.tkz.advance()
        #if token != ')':
        nArgs += self.compileExpressionList(token)
            
        token = self.tkz.advance()
        # )
        self.printTag(token)

        # write vm code for 'call subR|className.subR|varName.subR
        print(f'varNammmmm2 {kindToken} {nArgs}')
        self.vmw.writeCall(subName, nArgs)
        self.vmw.writePop('temp', '0')

        token = self.tkz.advance()
        # ;
        self.printTag(token)
        
        print('</doStatement>\n\t')
        self.outF.write('</doStatement>\n\t')

    def compileReturnStatement(self,token):
        print('<returnStatement>\n\t')
        self.outF.write('<returnStatement>\n\t')
        
        voidType = True
        # return
        self.printTag(token)

        token = self.tkz.advance()
        if token != ';':
            # expression
            self.compileExpression(token)
            token = self.tkz.advance()
            voidType = False

        # ;
        self.printTag(token)

        #print('thissssss '+self.st.kindOf('this'))
        if self.st.getSubRType() == 'constructor':
            #self.vmw.writePush('pointer', '0')
            pass
        elif voidType:
            self.vmw.writePush('constant', '0')
        
        # write vm code 'return'
        self.vmw.writeReturn()

        print('</returnStatement>\n\t')
        self.outF.write('</returnStatement>\n\t')

    #def compileSubroutineCall(self,token):
    #    print('<subroutineCall>\n\t')
    #    self.outF.write('<subroutineCall>\n\t')
    #    
    #    # subroutineName | className | varName
    #    self.printTag(token)

    #    token = self.tkz.advance()
    #    if token == '.':
    #        # .
    #        self.printTag(token)

    #        token = self.tkz.advance()
    #        # subroutineName
    #        self.printTag(token)
    #        token = self.tkz.advance()

    #    # (
    #    self.printTag(token)
    #    
    #    token = self.tkz.advance()
    #    if token != ')':
    #        self.compileExpressionList(token)
    #        
    #    # )
    #    self.printTag(token)
    #    
    #    print('</subroutineCall>\n\t')
    #    self.outF.write('</subroutineCall>\n\t')

    def compileExpressionList(self,token):
        print('<expressionList>\n\t')
        self.outF.write('<expressionList>\n\t')
        nArgs = 0
    
        if token != ')':
            # 1st expression
            self.compileExpression(token)
            nArgs += 1

            token = self.tkz.advance()

            while token != ')':
                # ,
                self.printTag(token)

                token = self.tkz.advance()
                # expression
                self.compileExpression(token)
                nArgs += 1

                token = self.tkz.advance()

        self.tkz.backward()
        
        print('</expressionList>\n\t')
        self.outF.write('</expressionList>\n\t')
        return nArgs

    #def compileExpression(self,token):
    #    print('<expression>\n\t')
    #    self.outF.write('<expression>\n\t')

    #    self.compileTerm(token)

    #    token = self.tkz.advance()
    #    while (token in self.ops):
    #        # op
    #        self.printTag(token)
    #        
    #        token = self.tkz.advance()
    #        # term
    #        self.compileTerm(token)

    #        token = self.tkz.advance()
    #
    #    self.tkz.backward()
    #    
    #    print('</expression>\n\t')
    #    self.outF.write('</expression>\n\t')

    def compileExpression(self,token):
        print('<expression>\n\t')
        self.outF.write('<expression>\n\t')

        self.compileTerm(token)

        token = self.tkz.advance()
        while (token in self.ops):
            # op
            opToken = token
            #print(f'optokennnn {opToken}')
            self.printTag(token)
            
            token = self.tkz.advance()
            # term
            self.compileTerm(token)

            # write op vm code
            if opToken == '+':
                self.vmw.writeArithmetic('add')
            elif opToken == '-':
                self.vmw.writeArithmetic('sub')
            elif opToken == '&':
                self.vmw.writeArithmetic('and')
            elif opToken == '|':
                self.vmw.writeArithmetic('or')
            elif opToken == '<':
                self.vmw.writeArithmetic('lt')
            elif opToken == '>':
                self.vmw.writeArithmetic('gt')
            elif opToken == '=':
                self.vmw.writeArithmetic('eq')
            elif opToken == '*':
                self.vmw.writeCall('Math.multiply', '2')
            elif opToken == '/':
                self.vmw.writeCall('Math.divide', '2')


            token = self.tkz.advance()
    
        self.tkz.backward()
        
        print('</expression>\n\t')
        self.outF.write('</expression>\n\t')

    def compileTerm(self,token):
        print('<term>\n\t')
        self.outF.write('<term>\n\t')
        subName = ''
        nArgs = 0

        if token == '(':
            # (
            self.printTag(token)

            token = self.tkz.advance()
            # expression
            self.compileExpression(token)

            token = self.tkz.advance()
            # )
            self.printTag(token)
        elif token in ['-','~']:
            # ['-','~']
            self.printTag(token)
            uopToken = token

            token = self.tkz.advance()
            # term
            self.compileTerm(token)
            if uopToken == '-':
                self.vmw.writeArithmetic('neg')
            elif uopToken == '~':
                self.vmw.writeArithmetic('not')
        else:
            # terms
            self.printTag(token)
            term = token
            if self.tkz.tokenType() == 'identifier':
                nameToken = token
                kindToken = self.st.kindOf(nameToken)
                
                # check if the subCall is of type varName.subR
                tok = self.tkz.advance()
                self.tkz.backward()
                if kindToken and tok == '.':
                    nArgs += 1

                # cat of token is class or subroutine
                if not kindToken:
                    if tok == '.':
                        self.printTag('class', 'identifierCat')
                        subName = nameToken+'.'
                    else:
                        self.printTag('subroutine', 'identifierCat')
                        subName = nameToken
                # cat of token is var, arg, static or field
                else:
                    self.printTag(kindToken, 'identifierCat')
                    indexToken = self.st.indexOf(nameToken)
                    self.printTag(indexToken, 'identifierInd')
                    typeToken = self.st.typeOf(nameToken)

                    print(f'typetoken {typeToken}')
                    subName = typeToken+'.' 

                    # vm code writer
                    if kindToken == 'STATIC':
                        self.vmw.writePush(kindToken.lower(), indexToken) 
                    elif kindToken == 'FIELD':
                        self.vmw.writePush('this', indexToken) 
                    elif kindToken == 'ARG':
                        self.vmw.writePush('argument', indexToken) 
                    elif kindToken == 'LOCAL':
                        self.vmw.writePush('local', indexToken) 

                self.printTag('used', 'identifierDef')
            # token is integerConstant
            elif self.tkz.tokenType() == 'integerConstant':
                self.vmw.writePush('constant', token) 

            # token is keywordConstant
            elif self.tkz.tokenType() == 'keyword':
                if token == 'true':
                    self.vmw.writePush('constant','0')
                    self.vmw.writeArithmetic('not')
                elif token in ['false','null']:
                    self.vmw.writePush('constant','0')
                else:
                    self.vmw.writePush('pointer','0')

            # token is stringConstant
            elif self.tkz.tokenType() == 'stringConstant':
                strLen = len(term) - 2
                self.vmw.writePush('constant', strLen)
                self.vmw.writeCall('String.new','1')
                for ch in term[1:-1]:
                    if ch.isspace():
                        self.vmw.writePush('constant', self.charSet['sp']) 
                    else:
                        self.vmw.writePush('constant', self.charSet[ch]) 
                    self.vmw.writeCall('String.appendChar','2')



            token = self.tkz.advance()
            if token == '[':
                # [
                self.printTag(token)
                #segment = self.st.kindOf(term)
                #index = self.st.indexOf(term)
                #if segment == 'STATIC':
                #    self.vmw.writePush('static', index)
                #elif segment == 'FIELD':
                #    self.vmw.writePush('this', index)
                #elif segment == 'ARG':
                #    self.vmw.writePush('argument', index)
                #elif segment == 'LOCAL':
                #    self.vmw.writePush('local', index)

                token = self.tkz.advance()
                # expression
                self.compileExpression(token)

                # write vm code to add b and j where b and j as in b[j]
                self.vmw.writeArithmetic('add')

                # write vm code to set 'that' pointer to b[j]
                self.vmw.writePop('pointer', '1')

                # write vm code to push b[j] value on the stack
                self.vmw.writePush('that', '0')

                token = self.tkz.advance()
                # ]
                self.printTag(token)
            elif token == '(' or token == '.':
                # subroutineName | className | varName
                #self.printTag(token)

                #token = self.tkz.advance()
                if token == '.':
                    # .
                    self.printTag(token)

                    token = self.tkz.advance()
                    # subroutineName
                    self.printTag(token)
                    subName += token
                    self.printTag('subroutine', 'identifierCat')
                    self.printTag('used', 'identifierDef')
                    token = self.tkz.advance()

                # (
                self.printTag(token)
                
                token = self.tkz.advance()
                #if token != ')':
                nArgs += self.compileExpressionList(token)
                    
                token = self.tkz.advance()
                # )
                self.printTag(token)

                # write vm code for 'call subR|className.subR|varName.subR
                self.vmw.writeCall(subName, nArgs)
            else:
                self.tkz.backward()
        
        print('</term>\n\t')
        self.outF.write('</term>\n\t')

    def printTag(self,token,tType=None):
        if tType == None:
            tType = self.tkz.tokenType()
        if token.startswith('"'):
            token = token[1:-1]
        print('<'+tType+'>')
        self.outF.write('<'+tType+'>')
        print(' ' + token + ' ')
        self.outF.write(' ' + token + ' ')
        print('</'+tType+'>\n')
        self.outF.write('</'+tType+'>\n')
         
