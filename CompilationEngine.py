from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer, path, symTab):
        self.outF = open(path+'Out_ExtraTags.xml','w')
        self.vmw = VMWriter(path)
        self.st = symTab
        self.tkz = tokenizer
        self.ops = ['+','-','*','/','|','=']+['&lt;', '&gt;', '&amp;']
        self.compileClass()

    def compileClass(self):
        token = self.tkz.advance()
        print('<class>\n\t')
        self.outF.write('<class>\n\t')
        print(f'Token: {token}')

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

        # (TODO) Create a tag for index 

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

        # constuctor | function | method
        self.printTag(token)

        token = self.tkz.advance()
        # void | type
        self.printTag(token)
        typeToken = token

        if typeToken not in ['int', 'char', 'boolean', 'void']:
            self.printTag('class', 'identifierCat')
            self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        # subroutineName
        self.printTag(token)
        self.printTag('subroutine', 'identifierCat')
        self.printTag('defined', 'identifierDef')

        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        #while token != ')':
            # parameterList

        # (TODO) if we have args then create the corr tags inc index
        self.compileParamterList(token)
        token = self.tkz.advance()

        # )
        self.printTag(token)

        token = self.tkz.advance()
        # subroutineBody
        self.compileSubroutineBody(token)

        print('</subroutineDec>\n\t')
        self.outF.write('</subroutineDec>\n\t')
            
    def compileParamterList(self,token):
        print('<parameterList>\n\t')
        self.outF.write('<parameterList>\n\t')
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

        kindToken = self.st.kindOf(nameToken)
        print(f'KIND {kindToken} name {nameToken}')
        self.printTag(kindToken, 'identifierCat')

        #self.st.define(nameToken, typeToken, kindToken)
        indexToken = self.st.indexOf(nameToken)
        self.printTag(indexToken, 'identifierInd')
        self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        # [
        if token == '[':
            self.printTag(token)

            token = self.tkz.advance()
            # expression
            self.compileExpression(token)
            
            token = self.tkz.advance()
            # ]
            self.printTag(token)
            token = self.tkz.advance()

        # =
        self.printTag(token)

        token = self.tkz.advance()
        # expression
        self.compileExpression(token)

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

        token = self.tkz.advance()
        # )
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
 
        print('</ifStatement>\n\t')
        self.outF.write('</ifStatement>\n\t')

    def compileWhileStatement(self,token):
        print('<whileStatement>\n\t')
        self.outF.write('<whileStatement>\n\t')

        # while
        self.printTag(token)

        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        # expression
        self.compileExpression(token)

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
        
        print('</whileStatement>\n\t')
        self.outF.write('</whileStatement>\n\t')

    def compileDoStatement(self,token):
        print('<doStatement>\n\t')
        self.outF.write('<doStatement>\n\t')
        
        # do
        self.printTag(token)

        token = self.tkz.advance()

        # subroutine call
        #self.compileSubroutineCall(token)

        # subroutineName | className | varName
        self.printTag(token)
        nameToken = token
        kindToken = self.st.kindOf(nameToken)
        if not kindToken:
            tok = self.tkz.advance()
            self.tkz.backward()
            if tok == '.':
                self.printTag('class', 'identifierCat')
            else:
                self.printTag('subroutine', 'identifierCat')
        else:
            self.printTag(kindToken, 'identifierCat')
            indexToken = self.st.indexOf(nameToken)
            self.printTag(indexToken, 'identifierInd')

        self.printTag('used', 'identifierDef')

        token = self.tkz.advance()
        if token == '.':
            # .
            self.printTag(token)

            token = self.tkz.advance()
            # subroutineName
            self.printTag(token)

            self.printTag('subroutine', 'identifierCat')
            self.printTag('used', 'identifierDef')

            token = self.tkz.advance()

        # (
        self.printTag(token)
        
        token = self.tkz.advance()
        #if token != ')':
        self.compileExpressionList(token)
            
        token = self.tkz.advance()
        # )
        self.printTag(token)

        token = self.tkz.advance()
        # ;
        self.printTag(token)
        
        print('</doStatement>\n\t')
        self.outF.write('</doStatement>\n\t')

    def compileReturnStatement(self,token):
        print('<returnStatement>\n\t')
        self.outF.write('<returnStatement>\n\t')
        
        # return
        self.printTag(token)

        token = self.tkz.advance()
        if token != ';':
            # expression
            self.compileExpression(token)
            token = self.tkz.advance()

        # ;
        self.printTag(token)

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
    
        if token != ')':
            # 1st expression
            self.compileExpression(token)

            token = self.tkz.advance()

            while token != ')':
                # ,
                self.printTag(token)

                token = self.tkz.advance()
                # expression
                self.compileExpression(token)

                token = self.tkz.advance()

        self.tkz.backward()
        
        print('</expressionList>\n\t')
        self.outF.write('</expressionList>\n\t')

    def compileExpression(self,token):
        print('<expression>\n\t')
        self.outF.write('<expression>\n\t')

        self.compileTerm(token)

        token = self.tkz.advance()
        while (token in self.ops):
            # op
            self.printTag(token)
            
            token = self.tkz.advance()
            # term
            self.compileTerm(token)

            token = self.tkz.advance()
    
        self.tkz.backward()
        
        print('</expression>\n\t')
        self.outF.write('</expression>\n\t')

    def compileTerm(self,token):
        print('<term>\n\t')
        self.outF.write('<term>\n\t')

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

            token = self.tkz.advance()
            # term
            self.compileTerm(token)
        else:
            # terms
            self.printTag(token)
            if self.tkz.tokenType() == 'identifier':
                nameToken = token
                kindToken = self.st.kindOf(nameToken)
                # cat of token is class or subroutine
                if not kindToken:
                    tok = self.tkz.advance()
                    self.tkz.backward()
                    if tok == '.':
                        self.printTag('class', 'identifierCat')
                    else:
                        self.printTag('subroutine', 'identifierCat')
                # cat of token is var, arg, static or field
                else:
                    self.printTag(kindToken, 'identifierCat')
                    indexToken = self.st.indexOf(nameToken)
                    self.printTag(indexToken, 'identifierInd')

                    # vm code writer
                    if kindToken == 'STATIC':
                        self.vmw.writePush(kindToken.lower(), indexToken) 
                    elif kindToken == 'FIELD':
                        self.vmw.writePush('this', indexToken) 
                    elif kindToken == 'ARG':
                        self.vmw.writePush('argument', indexToken) 
                    elif kindToken == 'VAR':
                        self.vmw.writePush('local', indexToken) 


                self.printTag('used', 'identifierDef')

            token = self.tkz.advance()
            if token == '[':
                # [
                self.printTag(token)

                token = self.tkz.advance()
                # expression
                self.compileExpression(token)

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
                    self.printTag('subroutine', 'identifierCat')
                    self.printTag('used', 'identifierDef')
                    token = self.tkz.advance()

                # (
                self.printTag(token)
                
                token = self.tkz.advance()
                #if token != ')':
                self.compileExpressionList(token)
                    
                token = self.tkz.advance()
                # )
                self.printTag(token)
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
         
