class CompilationEngine:
    def __init__(self, tokenizer, path):
        self.outF = open(path+'Out.xml','w')
        self.tkz = tokenizer
        self.compileClass()

    def compileClass(self):
        token = self.tkz.advance()
        print('<class>\n\t')
        self.outF.write('<class>\n\t')
        print(f'Token: {token}')
        self.printTag(token)
        token = self.tkz.advance()
        self.printTag(token)
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
        self.printTag(token)
        token = self.tkz.advance()
        self.printTag(token)
        token = self.tkz.advance()
        self.printTag(token)
        token = self.tkz.advance()
        while token == ',':
            self.printTag(token)
            token = self.tkz.advance()
            self.printTag(token)
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

        token = self.tkz.advance()
        # subroutineName
        self.printTag(token)

        token = self.tkz.advance()
        # (
        self.printTag(token)

        token = self.tkz.advance()
        #while token != ')':
            # parameterList
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
            # type
            self.printTag(token) 

            token = self.tkz.advance()
            # varName
            self.printTag(token)

            token = self.tkz.advance()
            # , type varName
            while token != ')':
                # ,
                self.printTag(token)

                token = self.tkz.advance()
                # type
                self.printTag(token)

                token = self.tkz.advance()
                # varName
                self.printTag(token)
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

        token = self.tkz.advance()
        # type
        self.printTag(token)

        token = self.tkz.advance()
        # varName
        self.printTag(token)

        token = self.tkz.advance()
        # , varName
        while token != ';':
            # ,
            self.printTag(token)

            token = self.tkz.advance()
            # varName
            self.printTag(token)
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

        #token = self.tkz.advance()
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

        token = self.tkz.advance()
        if token == '.':
            # .
            self.printTag(token)

            token = self.tkz.advance()
            # subroutineName
            self.printTag(token)
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
        
        print('</expression>\n\t')
        self.outF.write('</expression>\n\t')

    def compileTerm(self,token):
        print('<term>\n\t')
        self.outF.write('<term>\n\t')

        # terms
        self.printTag(token)
        
        print('</term>\n\t')
        self.outF.write('</term>\n\t')

    def printTag(self,token):
        tType = self.tkz.tokenType()
        print('<'+tType+'>')
        self.outF.write('<'+tType+'>')
        print(' ' + token + ' ')
        self.outF.write(' ' + token + ' ')
        print('</'+tType+'>\n')
        self.outF.write('</'+tType+'>\n')
         
