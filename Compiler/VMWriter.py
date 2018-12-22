class VMWriter:
    """The constructor"""
    def __init__(self,outputFile):
        self.vmFile = outputFile

    """This method responsible for generating push commands"""
    def writePush(self,Segment,Index):
        self.vmFile.write("push " + Segment + " "+ Index  + "\n")

    """This method responsible for generating pop commands"""
    def writePop(self, Segment, Index):
        self.vmFile.write("pop " + Segment +" "+ Index + "\n")

    def WriteArithmetic(self,Command):
        if Command == "+":
            self.vmFile.write("add\n")
        elif Command == "-":
            self.vmFile.write("sub\n")
        elif Command == "neg":
            self.vmFile.write("neg\n")
        elif Command == "not":
            self.vmFile.write("not\n")
        elif Command == "add":
            self.vmFile.write("add\n")
        elif Command == "*":
            self.vmFile.write("call Math.multiply 2\n")
        elif Command == "/":
            self.vmFile.write("call Math.divide 2\n")
        elif Command == "=":
            self.vmFile.write("eq" + "\n")
        elif Command == "&gt;":
            self.vmFile.write("gt" + "\n")
        elif Command == "&lt;":
            self.vmFile.write("lt"+ "\n")
        elif Command == "&amp;":
            self.vmFile.write("and" + "\n")
        elif Command == "|":
            self.vmFile.write("or" + "\n")

    def WriteLabel(self,label):
        self.vmFile.write("label " + label + "\n")
    def WriteGoto(self,label):
        self.vmFile.write("goto " + label +"\n")

    def WriteIf(self,label):
        self.vmFile.write("if-goto " + label+"\n")

    def writeCall(self,Name,nArgs):
        self.vmFile.write("call " + Name +" "+ str(nArgs) +"\n")

    def writeFunction(self,Name,nLocals):
        self.vmFile.write("function " + Name +" "+ str(nLocals) +"\n")

    def writeReturn(self):
        self.vmFile.write("return\n")

    def close(self):
        self.vmFile.close()

