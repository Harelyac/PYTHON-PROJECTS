from JackTokenizer import *
from SymbolTable import SymbolTable
from VMWriter import *

op = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]
unaryOp = ["-", "~"]
term = ["int_constant", "string_constant", "true", "false", "null", "this", "identifier"]

segment_dict = {"field": "this",
                "static": "static",
                "var": "local",
                "arg": "argument"}


class CompilationEngine:
    def __init__(self, tokenizer,outputFile):
        self.XMLCode = []
        self.CodeIndent = 0
        self.tokenizer = tokenizer
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(outputFile)
        self.class_name = None
        self.segment_local_dict = segment_dict
        self.while_count = 0
        self.if_count = 0
    def nextToken(self):
        "advancing and retreiving the next token by Tokenizer"
        self.tokenizer.advance()
        current_token = self.tokenizer.getCurrentToken()
        token_type = self.tokenizer.typeOfToken()
        return current_token, token_type

    def compileToken(self, token):
        current_token, token_type = self.nextToken()
        self.compileLine(current_token,token_type)
        return current_token

    def compileTitle(self, title_name, isEntered):
        self.XMLCode.append(self.writeXMLCodeTitle(title_name, isEntered))

    def compileLine(self,current_token, token_type):
        self.XMLCode.append(self.writeXMLCodeLine(current_token, token_type))

    def writeXMLCodeLine(self, token_to_write, type_of_token):
        """writes into XML line all sorts of tokens which are not title
        @:param token_to_write: the current token to write
        @:param type_of_token: the current's token's type
        @:return: the XML code line"""

        return " "*self.CodeIndent + "<" + str(type_of_token) + ">" + " " + token_to_write.lstrip() + " " + "</" + str(type_of_token) + ">"

    def writeXMLCodeTitle(self,type_of_token, isEntered):
        """writes into XML line all sorts of tokens which are  titles
                @:param isEntered: a boolean parameter implies if the current token is already opened
                 if it is the token's first occurance isEntered== True, and False otherwise
                @:param type_of_token: the current's token's type
                @:return: the XML code line"""

        if isEntered == True:#if the title is opening
            myLine = " "*self.CodeIndent + "<" + str(type_of_token) + ">"
            self.CodeIndent += 2 #indent the lines of all other tokens within the current_token's scope
            return myLine
        else:
            #if isEntered == False we have to close the title token
            self.CodeIndent -= 2
            myLine = " " * self.CodeIndent + "</" + str(type_of_token) + ">"
            return myLine


    def compileIdentifier(self,isClass = False):
        current_token, token_type = self.nextToken()
        if isClass:
            self.class_name = current_token # i've changed it because it was swapped

        self.XMLCode.append(self.writeXMLCodeLine(current_token, token_type))
        return current_token


    def compileClass(self):
        self.compileTitle("class", True)
        self.compileToken("class") # increnmenting the tokenizer and checking if the current token is indeed a class declaration
        self.compileIdentifier(True)
        self.compileToken("{")
        current_token, token_type = self.nextToken()
        while current_token in ["field", "static"]:
            self.compileClassVarDeclaration(current_token, token_type)
            current_token, token_type = self.nextToken()

        while current_token in ["constructor","function","method"]:
            self.compilesubRoutineDec(current_token, token_type)
            current_token, token_type = self.nextToken()

        self.compileToken("}")
        self.compileTitle("class", False)
        return self.XMLCode

    def compileClassVarDeclaration(self,current_token, token_type):
        #self.compileTitle("classVarDec",True)  # first opening a new class title in XML
        #self.compileLine(current_token,token_type)
        VarKind = self.tokenizer.getCurrentToken()
        current_token, token_type = self.nextToken()
        VarType = current_token
        #self.compileType(current_token, token_type)
        VarName = self.compileIdentifier()
        self.symbolTable.define(VarName,VarType,VarKind)
        current_token, token_type = self.nextToken()
        while current_token == ",": # also the validation itself so no need of compile token
            self.compileLine(current_token, token_type)
            VarName = self.compileIdentifier()
            self.symbolTable.define(VarName, VarType, VarKind)
            current_token, token_type = self.nextToken()
        self.compileLine(current_token, token_type)
        self.compileTitle("classVarDec", False)

    def compileType(self,current_token,token_type):
        if current_token in ["int","char", "boolean", self.class_name]:
            self.compileLine(current_token,token_type)
        else:
            self.compileLine(current_token, token_type)
        return current_token



    def compilesubRoutineDec(self,current_token, token_type):
        self.symbolTable.startSubroutine()
        self.if_count = 0
        self.while_count = 0
        #self.compileTitle("subroutineDec", True)
        #self.compileLine(current_token, token_type)
        func_type = self.tokenizer.getCurrentToken()

        current_token, token_type = self.nextToken()
        return_type = current_token
        if current_token in ["int","char", "boolean", self.class_name] or current_token == "void":
            self.compileLine(current_token, token_type)
        func_name = self.compileIdentifier()
        self.symbolTable.set_functionName(func_name, self.class_name)
        self.symbolTable.setFuncType(func_type)
        self.symbolTable.setReturnType(return_type)
        if func_type == "method":
            self.symbolTable.define("this",return_type,"arg")
        self.compileToken("(")
        self.compileParameterList()
        self.compileLine(")","symbol")
        self.compileSubroutineBody()
        self.compileTitle("subroutineDec", False)

    def compileParameterList(self):
        self.compileTitle("parameterList", True)
        current_token, token_type = self.nextToken()
        while current_token != ")":
            VarType = self.compileType(current_token, token_type)
            VarName = self.compileIdentifier()
            self.symbolTable.define(VarName,VarType,"arg")
            current_token, token_type = self.nextToken()
            if current_token == ",":
                self.compileLine(current_token,token_type)
                current_token, token_type = self.nextToken()
        self.compileTitle("parameterList", False)


    def compileSubroutineBody(self):
        #self.compileTitle("subroutineBody", True)# first opening a new subroutineBody title in XML
        self.compileToken("{")

        current_token = self.tokenizer.showNextToken()
        while current_token == "var" :
            self.compilevarDec()
            current_token = self.tokenizer.showNextToken()
        self.vmWriter.writeFunction(self.symbolTable.function_name, str(self.symbolTable.VarCount("var")))
        # check wether the function type is method or constructor /*todo*/
        if self.symbolTable.function_type == "method":

            self.vmWriter.writePush("argument", "0")
            self.vmWriter.writePop("pointer", "0")

        if self.symbolTable.function_type == "constructor":
            #slide 6 (7:00) about constructors
            field_num = self.symbolTable.VarCount("field")
            self.vmWriter.writePush("constant" , str(field_num))
            self.vmWriter.writeCall("Memory.alloc", "1")
            self.vmWriter.writePop("pointer", "0")
        current_token, token_type = self.nextToken()
        self.compileStatements(current_token, token_type)
        #self.compileLine("}","symbol")
        #self.compileTitle("subroutineBody", False)

    def compilevarDec(self):
        #self.compileTitle("varDec", True)
        current_token, token_type = self.nextToken()
        VarKind = "var"
        current_token, token_type = self.nextToken()
        VarType = current_token
        current_token, token_type = self.nextToken()
        VarName = current_token
        self.symbolTable.define(VarName,VarType,VarKind)
        #self.compileLine(current_token, token_type)
        current_token, token_type = self.nextToken()
        while current_token == ",":
            #self.compileLine(current_token, token_type)
            VarName = self.compileIdentifier()
            self.symbolTable.define(VarName, VarType, VarKind)
            current_token, token_type = self.nextToken()
        #self.compileLine(";", "symbol")
        #self.compileTitle("varDec", False)

    def compileStatements(self,current_token, token_type):
        self.compileTitle("statements", True)
        while current_token != "}":
            if current_token == "let":
                self.compileLet()
            elif current_token == "if":
                self.compileIf()
            elif current_token == "while":
                self.compileWhile()
            elif current_token == "do":
                self.compileDo()
            elif current_token == "return":
                self.compileReturn()
            current_token, token_type = self.nextToken()
        self.compileTitle("statements", False)

    def compileLet(self):
        self.compileTitle("letStatement", True)
        self.compileLine("let","keyword")
        current_token, token_type= self.nextToken()
        temp = current_token # saves the new local variable
        current_token, token_type = self.nextToken()
        if current_token == "[": # if the left side is array
            self.compileLine("[", "symbol")
            self.compileExpression()
            self.compileLine("]", "symbol")
            var_memory_segment = self.segment_local_dict[self.symbolTable.KindOf(temp)]#the kind of current var
            var_index = self.symbolTable.IndexOf(temp)
            self.vmWriter.writePush(var_memory_segment,str(var_index))
            self.vmWriter.WriteArithmetic("add")#if the left side is  an array - add the index to get the value
            self.nextToken()

        #self.compileLine("=","symbol")
        self.compileExpression()
        #self.compileLine(";", "symbol")
        #self.compileTitle("letStatement", False)
        var_kind = self.symbolTable.KindOf(temp)
        var_type = self.symbolTable.TypeOf(temp)
        index_segment = self.symbolTable.IndexOf(temp)
        kind_seg = self.segment_local_dict[var_kind]
        if current_token == "[" and kind_seg in ["local","argument"]:
            #slide 8 (20:00) !!!
            self.vmWriter.writePop("temp", "0")
            self.vmWriter.writePop("pointer", "1")
            self.vmWriter.writePush("temp", "0")
            self.vmWriter.writePop("that","0")
        else:
            #if the first var was not an Arrayso just pop the value from the expression to it
            self.vmWriter.writePop(kind_seg,str(index_segment))

    def compileIf(self):
        #self.compileTitle("ifStatement", True)
        #self.compileLine("if", "keyword")
        self.compileToken("(")
        self.compileExpression()
        self.compileLine(")", "symbol")

        if_true_label = "TRUE" + str(self.if_count)#define true and false labels!!
        if_false_label = "FALSE" + str(self.if_count)
        end_if_label = "END" + str(self.if_count)
        self.if_count += 1
        self.vmWriter.WriteIf(if_true_label)# after pushing to stack the expression write labels
        self.vmWriter.WriteGoto(if_false_label)

        self.compileToken("{")
        self.vmWriter.WriteLabel(if_true_label) # put the TRUE_LABEL at the begining of the if clause
        current_token, token_type = self.nextToken()
        self.compileStatements(current_token, token_type)
        #self.compileLine("}","symbol")

        #check if there is "else" statement
        temp = self.tokenizer.showNextToken()
        if temp == "else":
            #put the END_LABEL and put the False_label If the condionn not true
            self.vmWriter.WriteGoto(end_if_label)
            self.vmWriter.WriteLabel(if_false_label)
            current_token, token_type = self.nextToken()
            #self.compileLine("else","keyword")
            self.compileToken("{")
            current_token, token_type = self.nextToken()
            self.compileStatements(current_token, token_type)
            self.vmWriter.WriteLabel(end_if_label)
            #self.compileLine("}","symbol")
        else:
            self.vmWriter.WriteLabel(if_false_label)
        #self.compileTitle("ifStatement", False)

    def compileWhile(self):
        #self.compileTitle("whileStatement", True)
        #self.compileLine("while", "keyword")
        while_start_label = "STRAT" + str(self.while_count)# defining astart and stop labels!!
        while_end_label = "END" + str(self.while_count)
        self.while_count += 1

        self.vmWriter.WriteLabel(while_start_label)
        self.compileToken("(")
        self.compileExpression()
        #self.compileLine(")","symbol")
        #negating the boolean expression and check whether to enter or not
        self.vmWriter.WriteArithmetic("not")
        self.vmWriter.WriteIf(while_end_label)
        self.compileToken("{")
        current_token, token_type = self.nextToken()
        self.compileStatements(current_token, token_type)
        self.vmWriter.WriteGoto(while_start_label)
        self.vmWriter.WriteLabel(while_end_label)
        #self.compileLine("}", "symbol")
        #self.compileTitle("whileStatement", False)

    def compileDo(self):
        #self.compileTitle("doStatement", True)
        #self.compileLine("do", "keyword")
        self.compileSubroutineCall()
        self.vmWriter.writePop("temp", "0")
        self.nextToken()
        #self.nextToken()
        #self.compileLine(";","symbol")
        #self.compileTitle("doStatement", False)

    def compileReturn(self):
        #self.compileTitle("returnStatement", True)
        #self.compileLine("return", "keyword")
        if self.symbolTable.return_type == "void":
            self.vmWriter.writePush("constant", "0") # always push 0 to the stack!!
            temp = self.tokenizer.showNextToken()
            while not temp == ";":
                self.nextToken()
                temp = self.tokenizer.showNextToken()
        else:
            temp = self.tokenizer.showNextToken()
            if temp != ";":
                self.compileExpression()
            else:
                self.vmWriter.writePush("constant", "0")
        self.vmWriter.writeReturn()

        #self.compileLine(";","symbol")
        #self.compileTitle("returnStatement", False)

    def compileExpression(self):
        #self.compileTitle("expression", True)
        self.compileTerm()
        current_token, token_type = self.nextToken()
        while current_token  in op:
            self.compileLine(current_token, token_type)
            self.compileTerm()
            self.vmWriter.WriteArithmetic(current_token) # after two expression/terms we will write arithmetic
            current_token, token_type = self.nextToken()
        self.compileTitle("expression", False)

    def compileExpressionList(self):
        num_of_args = 0
        self.compileTitle("expressionList", True)
        current_token = self.tokenizer.showNextToken()
        if current_token != ")":
            self.compileExpression()
            num_of_args +=1 # add the first parameter found inside paranthesis( )
            while (self.tokenizer.getCurrentToken() == ","):
                num_of_args += 1
                self.compileLine(",", "symbol")
                self.compileExpression()
        if current_token == ")":
            self.nextToken()
        self.compileTitle("expressionList", False)
        return num_of_args

    def compileTerm(self):
        #self.compileTitle("term", True)
        current_token, token_type  = self.nextToken()
        kind = self.symbolTable.KindOf(current_token)
        temp = self.tokenizer.showNextToken()
        if token_type == "int_constant":
            # self.compileLine(current_token,"integerConstant")
            self.vmWriter.writePush("constant",str(current_token))

        elif kind == "var" and temp != "[" and temp != ".":
            self.vmWriter.writePush("local", str(self.symbolTable.IndexOf(current_token)))

        elif kind == "arg" and current_token != "this":
            self.vmWriter.writePush("argument",str(self.symbolTable.IndexOf(current_token)))

        elif token_type == "string_constant":
            #self.compileLine(current_token.strip("\""),"stringConstant")
            string_constant = current_token.strip("\"")
            string_lenth = len(string_constant)
            self.vmWriter.writePush("constant", str(string_lenth))
            self.vmWriter.writeCall("String.new", 1)
            #now getting the numerical value of each char in the string and append them
            for char in string_constant:
                self.vmWriter.writePush("constant", str(ord(char)))
                self.vmWriter.writeCall("String.appendChar", "2")

        elif kind == "static" and temp != "." and temp != "[":
            self.vmWriter.writePush("static", str(self.symbolTable.IndexOf(current_token)))

        elif kind == "field" and temp != "." and temp != "]":
            self.vmWriter.writePush("this", str(self.symbolTable.IndexOf(current_token)))

        elif current_token in ["true", "false", "null", "this"]: # not the kind it only means that the tokens itself is one of them
            #self.compileLine(current_token,token_type) #its a keyword!
            if current_token == "true":
                self.vmWriter.writePush("constant", "0")
                self.vmWriter.WriteArithmetic("not")
            elif current_token == "this":
                self.vmWriter.writePush("pointer", "0")
            else: # its false or null
                self.vmWriter.writePush("constant", "0")
        # if its ( expression )
        elif current_token == "(":
            self.compileLine(current_token, token_type)
            self.compileExpression()
            self.compileLine(")", "symbol")
        #if its Unary Op
        elif current_token in ["~", "-"]:
            self.compileLine(current_token,token_type)
            self.compileTerm()
            if current_token == "~":
                self.vmWriter.WriteArithmetic("not")
            else:
                self.vmWriter.WriteArithmetic("neg")
        #if its varName [ expression ]
        elif token_type == "identifier" and temp != ".":# maybe add and temp != ";"  ????????
            self.compileLine(current_token, token_type)
            if temp == "[":
                self.compileLine(temp,"symbol")
                var_name = current_token
                current_token, token_type = self.nextToken()
                self.compileExpression()
                self.compileLine("]", "symbol")
                var_memory_segment = self.segment_local_dict[self.symbolTable.KindOf(var_name)]  # the kind of current var
                var_index = self.symbolTable.IndexOf(var_name)
                self.vmWriter.writePush(var_memory_segment, str(var_index))
                self.vmWriter.WriteArithmetic("add")  # if the left side is  an array
                self.vmWriter.writePop("pointer", "1")
                self.vmWriter.writePush("that", "0")


        # subroutine
        elif token_type == "identifier" and temp in ["(" , "."]:
            self.tokenizer.previousToken()
            self.compileSubroutineCall()
        # if its a var_name
        elif token_type == "identifier" and not temp in ["[", "(", "."]:
            var_name = current_token
            var_memory_segment = self.segment_local_dict[self.symbolTable.KindOf(var_name)]  # the kind of current var
            var_index = self.symbolTable.IndexOf(var_name)
            self.vmWriter.writePush(var_memory_segment, str(var_index))
        self.compileTitle("term", False)

    def compileSubroutineCall(self):
        num_of_args = 0
        func_name = self.compileIdentifier() # func_name first contain the class name
        current_token, token_type = self.nextToken()
        if current_token == ".":
            var_kind = self.symbolTable.KindOf(func_name)
            var_index = self.symbolTable.IndexOf(func_name)
            var_type = self.symbolTable.TypeOf(func_name)
            if var_type != False: # enter only if it is a method called by an object
                num_of_args += 1 # num of arguments of a method starts from 1 because of the "self" argument
                func_name = var_type
                mem_segment = self.segment_local_dict[var_kind]
                self.vmWriter.writePush(mem_segment,str(var_index)) # push memory segment to stack be calling function
            func_name += "."
            func_name += self.compileIdentifier()
            #self.compileLine(".", "symbol")
            self.compileToken("(")
            num_of_args += self.compileExpressionList()
            self.compileLine(")","symbol")
            self.vmWriter.writeCall(func_name, str(num_of_args))

        else:
            self.vmWriter.writePush("pointer", "0")
            num_of_args +=1
            func_name = self.class_name + "." + func_name
            self.compileLine("(","symbol")
            num_of_args += self.compileExpressionList()
            self.compileLine(")", "symbol")
            self.vmWriter.writeCall(func_name, str(num_of_args))


        




