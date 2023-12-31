from abc import ABC, abstractmethod
# Otvaranje Aplikacije = 1,014 Radnji
# New Game

class Chess(ABC):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Shared Initialization <<<
    pieces = [] 
    def __init__(self,side) -> None:
        super().__init__()
        self.side = side
        Chess.pieces.append(self)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Hash TABLES  --  CORE MECHANIC <<< 
    MovesSet = set()
    TakenDict = {} 

    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    # >>> STATIC Dictionaries <<<

    def emptyTableDict():
        emptyTableDict = {}
        for x in range(8):
            for y in range(8):
                emptyTableDict[x,y] = ''
        return emptyTableDict
    
    EmptyTableDict = emptyTableDict()   
    def notationTableDict():
        def notationTable():
            rowX = [chr(i) for i in range(ord('A'),ord('I'))]
            colY = [str(i) for i in range(1,9)]
            return [[(rowX[y]+colY[x]) for y in range(8)] for x in range(8)]
        
        NotationTable = notationTable()
        notationTableDict = {}
        for x in range(8):
            for y in range(8):
                notationTableDict[x,y] = NotationTable[x][y]
        return notationTableDict
    NotationTableDict = notationTableDict()
    
    # >>> DYNAMIC Dictionaries <<<

    #@countExecutionMethod
    def piecesDict():
        piecesDict = {}
        for i in Chess.pieces:
            piecesDict[i.position()] = i
        return piecesDict
    
    #@countExecutionMethod
    def currentTableDict():
        currentTableDict = Chess.EmptyTableDict.copy()
        piecesDict = Chess.piecesDict()

        for k in piecesDict.keys():
            currentTableDict[k] = piecesDict[k]
        return currentTableDict

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    direction = ['U','D','L','R','UL','UR','DL','DR']  
    def incrementation(self,path):
        if path == Chess.direction[0]:
            self.x +=1
            return self.x,self.y
        elif path == Chess.direction[1]:
            self.x -=1
            return self.x,self.y
        elif path == Chess.direction[2]:
            self.y -=1
            return self.x,self.y
        elif path == Chess.direction[3]:
            self.y +=1
            return self.x,self.y
        elif path == Chess.direction[4]:
            self.x +=1 ; self.y -=1
            return self.x,self.y
        elif path == Chess.direction[5]:
            self.x +=1 ; self.y +=1
            return self.x,self.y
        elif path == Chess.direction[6]:
            self.x -=1 ; self.y -=1
            return self.x,self.y
        elif path == Chess.direction[7]:
            self.x -=1 ; self.y +=1
            return self.x,self.y
    
    # Getter
    def position(self): 
        return self.x,self.y
    
    #symbols = '☀☘☛☥☦☯♋♻♺⚔🗡️🠊🢂⚜⛌🢣⚔⛦⛥⛤⛧⛨✚✟✡✰❌❎❭❯❱➔➩➵➸➼⭕⭐🕊🗙'
    #arrow = '➔'
    #sword = '🗙'
    # Setter #1
    def move(self,square):
        PossibleLines = self.possibleMoves()[0]
        if square in PossibleLines:
            position = Chess.NotationTableDict[self.position()]
            self.x,self.y = square
            Chess.MovesSet.add(self)
            transcript = f"{str(self)[1:]} {position} move {Chess.NotationTableDict[square]}\n"   
            moveOutput = f"{str(self).ljust(8)}{(position.ljust(5)+'➔').ljust(8)}{Chess.NotationTableDict[square]}"
            return moveOutput,transcript
    # Setter #2 
    def take(self,obj,enPassant=None):
        PossibleTake = self.possibleMoves()[1]
        if obj.position() in PossibleTake:
            position = Chess.NotationTableDict[self.position()]
            self.x,self.y = obj.position()
            Chess.TakenDict[obj] = self
            Chess.MovesSet.add(self)
            transcript = f"{str(self)[1:]} {position} took {Chess.NotationTableDict[obj.position()]} {str(obj)[1:]}\n"  
            moveOutput = f"{str(self).ljust(8)}{(position.ljust(4)+'❌').ljust(7)}{Chess.NotationTableDict[obj.position()]} {obj}"
            Chess.pieces.remove(obj)
            return moveOutput,transcript 
    
    @abstractmethod
    def possibleMoves():
        pass
    # Parameters For Possible Moves
    def granica(self):
        return (self.x <= 7 and self.x >= 0) and (self.y <= 7 and self.y >= 0)

