from chess import Chess

class Bishop(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.type = 'Archer'
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = (2 if self.name == 'L' else 5)  if name else 0
    def __str__(self) -> str:
        black_bishop = '♝'
        white_bishop = '♗'
        return f"{white_bishop if self.side == 'w' else black_bishop}Bishop"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    direction = Chess.direction[4:]  
    def possibleMoves(self, tableDict):
         return super().possibleMoves(tableDict)