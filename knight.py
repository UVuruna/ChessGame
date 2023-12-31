from chess import Chess
import copy

class Knight(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = (1 if self.name == 'L' else 6)  if name else 0
    def __str__(self) -> str:
        white_knight = '♘'
        black_knight = '♞'
        return f"{white_knight if self.side == 'w' else black_knight}Knight"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    direction = ['U+R','UR+','U+L','UL+','D+R','DR+','D+L','DL+']  
    def incrementation(self, path):
        if path == self.direction[0]:
            self.x +=2 ; self.y +=1
            return self.x,self.y
        elif path == self.direction[1]:
            self.x +=1 ; self.y +=2
            return self.x,self.y
        elif path == self.direction[2]:
            self.x +=2 ; self.y -=1
            return self.x,self.y
        elif path == self.direction[3]:
            self.x +=1 ; self.y -=2
            return self.x,self.y
        elif path == self.direction[4]:
            self.x -=2 ; self.y +=1
            return self.x,self.y
        elif path == self.direction[5]:
            self.x -=1 ; self.y +=2
            return self.x,self.y
        elif path == self.direction[6]:
            self.x -=2 ; self.y -=1
            return self.x,self.y
        elif path == self.direction[7]:
            self.x -=1 ; self.y -=2
            return self.x,self.y
        
    def possibleMoves(self,TableDict=None):
        if TableDict is None:
            CurrentTableDict = Chess.currentTableDict()
        else:
            CurrentTableDict = TableDict

        def polje(content):
            return CurrentTableDict[content.x,content.y]
        
        possibleMoveAttack_List = []
        possibleTake_List = []
        possibleDefend_List = []
        
        for dir in self.direction:
            possMove = copy.deepcopy(self)
            while possMove.granica(): 
                possMove.incrementation(dir)
                if possMove.granica() and polje(possMove) == '':
                    possibleMoveAttack_List.append(possMove.position())
                    break
                elif possMove.granica() and possMove.side !=polje(possMove).side:
                    possibleTake_List.append(possMove.position())
                    break
                elif possMove.granica() and possMove.side ==polje(possMove).side:
                    possibleDefend_List.append(possMove.position())
                    break
                else:
                    break
                         
        return possibleMoveAttack_List, possibleTake_List, possibleDefend_List, possibleMoveAttack_List