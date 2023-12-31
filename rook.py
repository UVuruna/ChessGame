from chess import Chess
import copy

class Rook(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = (0 if self.name == 'L' else 7) if name else 0
    def __str__(self) -> str:
        white_rook = '♖'
        black_rook = '♜'
        return f"{white_rook if self.side == 'w' else black_rook}Rook"
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    direction = Chess.direction[:4]        
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