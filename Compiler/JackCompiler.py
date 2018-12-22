import sys
import os
from CompilationEngine import *
from JackTokenizer import *
#from SymbolTable import *
from SymbolTable import SymbolTable

# this class is the main class which handles files and directory input
class JackAnalyzer:
    Xml_code = ""

    def Main(self):
        file_name = sys.argv[1]
        if os.path.isdir(file_name):
            files = os.listdir(file_name)
            for file in files:
                if ".jack" in file:
                    abspath = os.path.join(file_name,file)
                    with open(abspath, 'r') as current_file:
                        tokenizer = JackTokenizer(current_file)

                        with open(abspath.replace(".jack", ".vm"),'a') as vmFile:
                            engine = CompilationEngine(tokenizer,vmFile)
                            engine.compileClass() # at this moment only vmWriter deal with output file
                            #XMLfile.write("\n".join(Xml_code))

        # if the file name is rather a normal file
        else:
            with open(file_name, 'r') as current_file:
                tokenizer = JackTokenizer(current_file)
                symbolTable = SymbolTable()
                with open(file_name.replace(".jack", ".vm"), 'a') as vmFile:
                    engine = CompilationEngine(tokenizer, vmFile)
                    engine.compileClass()
                    #XMLfile.write("\n".join(Xml_code))


# starter
if __name__ == '__main__':
    starter = JackAnalyzer()
    starter.Main()