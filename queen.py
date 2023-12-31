from chess import Chess
import copy

class Queen(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = 3
    def __str__(self) -> str:
            black_queen = '♛'
            white_queen = '♕'
            return f"{white_queen if self.side == 'w' else black_queen}Queen"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
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
                elif possMove.granica() and possMove.side !=polje(possMove).side:
                    possibleTake_List.append(possMove.position())
                    break
                elif possMove.granica() and possMove.side ==polje(possMove).side:
                    possibleDefend_List.append(possMove.position())
                    break
                else:
                    break
                         
        return possibleMoveAttack_List, possibleTake_List, possibleDefend_List, possibleMoveAttack_List