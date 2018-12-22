from Variable import *


class SymbolTable:
    def __init__(self):
        self.function_name = ""
        self.function_type = ""
        self.return_type = ""
        self.function_name = ""
        self.function_type = ""
        self.return_type = ""
        self.__ClassST = {}
        self.__MethodST = {}
        self.__Fieldcnt = 0
        self.__Staticcnt = 0
        self.__Argcnt = 0
        self.__Localcnt = 0


    """this method creates new subroutine scope and
    actually reset the subroutine's symbol table"""

    def startSubroutine(self):
        #self.__ClassST.clear()
        self.__MethodST.clear()
        self.__Argcnt = 0
        self.__Localcnt = 0

    """this method adds a new symbol(identifier) to the symbol table,
    accordingly to the class or subroutine symbols tables."""

    def define(self, Name, Type, Kind):
        var = Variable(Name, Type, Kind)
        if Kind == "field":
            self.__ClassST[Name] = var
            var.setIndex(self.__Fieldcnt)  # update the var index by its type
            self.__Fieldcnt += 1
        elif Kind == "static":
            self.__ClassST[Name] = var
            var.setIndex(self.__Staticcnt)  # update the var index by its type
            self.__Staticcnt += 1
        elif Kind == "arg":
             self.__MethodST[Name] = var
             var.setIndex(self.__Argcnt)  # update the var index by its type
             self.__Argcnt += 1
        elif Kind == "var":
            self.__MethodST[Name] = var
            var.setIndex(self.__Localcnt)  # update the var index by its type
            self.__Localcnt += 1


    """this method returns the number of variables of the given kind"""

    def VarCount(self, Kind):
        if Kind == "field":
            return self.__Fieldcnt
        elif Kind == "static":
            return self.__Staticcnt
        elif Kind == "arg":
            return self.__Argcnt
        elif Kind == "var":
            return self.__Localcnt

    """this method returns the kind of the given symbol(identifier) name"""

    def KindOf(self, Name):
        if Name in self.__MethodST.keys():
            return self.__MethodST[Name].getKind()
        elif Name in self.__ClassST.keys():
            return self.__ClassST[Name].getKind()
        else:
            return False

    """this method returns the type of the given symbol(identifier) name"""

    def TypeOf(self, Name):
        if Name in self.__MethodST.keys():
            return self.__MethodST[Name].getType()
        elif Name in self.__ClassST.keys():
            return self.__ClassST[Name].getType()
        else:
            return False

    """this method returns the index of the given symbol(identifier) name"""

    def IndexOf(self, Name):
        if Name in self.__MethodST.keys():
            return self.__MethodST[Name].getIndex()
        elif Name in self.__ClassST.keys():
            return self.__ClassST[Name].getIndex()
        else:
            return False


    def set_functionName(self,funcname, class_name):
        self.function_name = class_name + "." + funcname

    def setFuncType(self, func_Type):
        self.function_type=  func_Type

    def setReturnType(self,return_type):
        self.return_type = return_type