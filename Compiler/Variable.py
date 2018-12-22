import SymbolTable
class Variable:
    """Variable properties"""
    def __init__(self,name,type,kind):
        self.__name = name
        self.__type = type
        self.__kind = kind
        self.__index = None

    def getName(self):
        return self.__name

    def getType(self):
        return self.__type

    def getKind(self):
        return self.__kind

    def getIndex(self):
        return self.__index

    def setName(self,new_name):
        self.__name = new_name

    def setType(self,new_type):
        self.__type = new_type

    def setKind(self,new_kind):
        self.__kind = new_kind

    def setIndex(self,new_index):
        self.__index = new_index