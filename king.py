from chess import Chess
from rook import Rook
import copy

class King(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<   
    def __init__(self, side) -> None:
        super().__init__(side)
        self.x = (0 if self.side == 'w' else 7)
        self.y = 4
    def __str__(self) -> str:
        white_king = '♔'
        black_king = '♚'
        return f"{white_king if self.side == 'w' else black_king}King"        

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
       
    def castlingCheck(self):
        CurrentTableDict = Chess.currentTableDict()
        kingsideWhite, queensideWhite, kingsideBlack, queensideBlack = 0,0,0,0

        if self not in Chess.MovesSet:
            for ownRook in Chess.pieces:
                if isinstance(ownRook,Rook) and (ownRook.side == self.side) and (ownRook not in Chess.MovesSet):
                    if ownRook.name == 'R' and self.side == 'w' and \
                        CurrentTableDict[(0,5)] == '' and CurrentTableDict[(0,6)] == '':
                        kingsideWhite = 1
                    elif ownRook.name == 'L' and self.side == 'w' and CurrentTableDict[(0,1)] == '' and \
                        CurrentTableDict[(0,2)] == '' and CurrentTableDict[(0,3)] == '':
                        queensideWhite = 1   
                    elif ownRook.name == 'R' and self.side == 'b' and \
                        CurrentTableDict[(7,5)] == '' and CurrentTableDict[(7,6)] == '':
                        kingsideBlack = 1
                    elif ownRook.name == 'L' and self.side == 'b' and CurrentTableDict[(7,1)] == '' and \
                        CurrentTableDict[(7,2)] == '' and CurrentTableDict[(7,3)] == '':
                        queensideBlack = 1
            return kingsideWhite, queensideWhite, kingsideBlack, queensideBlack
    
    #castle = '⚜'
    def castling(self,obj,kingWh,queenWh,kingBl,queenBl):
        k = 'Kingside:'
        q = 'Queenside:'
        if obj.name == 'L':
            if queenWh == 1: # Duga rokada - Queenside castling
                self.x = 0 ; self.y = 2
                obj.x = 0 ; obj.y = 3
                Chess.MovesSet.add(self) ; Chess.MovesSet.add(obj)
                transcript = f"{q} white\n"
                moveOutput = f"{q.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript
            elif queenBl == 1: # Duga rokada - Queenside castling
                self.x = 7 ; self.y = 2
                obj.x = 7 ; obj.y = 3
                Chess.MovesSet.add(self) ; Chess.MovesSet.add(obj)
                transcript = f"{q} black\n"
                moveOutput = f"{q.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript
        else:              
            if kingBl == 1: # Kratka rokada - Kingside castling
                self.x = 7 ; self.y = 6
                obj.x = 7 ; obj.y = 5
                Chess.MovesSet.add(self) ; Chess.MovesSet.add(obj)
                transcript = f"{k} black\n"
                moveOutput = f"{k.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript           
            elif kingWh == 1: # Kratka rokada - Kingside castling
                self.x = 0 ; self.y = 6
                obj.x = 0 ; obj.y = 5
                Chess.MovesSet.add(self) ; Chess.MovesSet.add(obj)
                transcript = f"{k} white\n"
                moveOutput = f"{k.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Test
if __name__ == '__main__':
    a1 = King('w')
    a2 = King('b')
    print(f'\ncurrentTableDict\n{Chess.currentTableDict()}')
    print(f'\nnotationTableDict\n{Chess.notationTableDict()}')
    print(f'\nemptyTableDict\n{Chess.emptyTableDict()}')
    print(f'\npiecesDict\n{Chess.piecesDict()}')
    print(f'\npieces\n{Chess.pieces}')  