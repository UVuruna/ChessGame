from tkinter import *
import copy
from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from pawn import Pawn
from rook import Rook


class AI():
       
    def attackedPieces(Turn,team=None,clas=None,defenders=None):
        if team is None:
            turnI = 'b'
            turnII = 'w'
        else:
            turnI = 'w'
            turnII = 'b'

        def noKing(clas):
            if clas:
                return not isinstance(piece,King)
            else:
                return True     
        def noDefenders(defenders):
            if defenders:
                return piece not in defenders
            else:
                return True

        PossibleTakes = []
        PossibleMoves = []

        for piece in Chess.pieces:
            if noKing(clas) and noDefenders(defenders):
                if Turn == 1 and piece.side == turnI:
                    PossibleTakes += piece.possibleMoves()[1]
                    PossibleTakes += piece.possibleMoves()[3]
                    PossibleMoves +=piece.possibleMoves()[0]
                elif Turn == -1 and piece.side == turnII:
                    PossibleTakes += piece.possibleMoves()[1]
                    PossibleTakes += piece.possibleMoves()[3]
                    PossibleMoves +=piece.possibleMoves()[0]

        return set(PossibleTakes), set(PossibleMoves)
        
    def dangerZone(turn):
        Turn = turn
        CurrentTableDict = Chess.currentTableDict()

        # Ovaj Method daje:
            # selfKing =CLASS.KING
            # selfKingActions =LISTA [xy,xy,xy]
        def selfKingActionsCalc():
            selfKingActions = []
            for piece in Chess.pieces:
                if Turn == 1 and isinstance(piece,King) and piece.side == 'w':
                    selfKingActions += piece.possibleMoves()[0]
                    selfKingActions += piece.possibleMoves()[1]
                    selfKing = copy.deepcopy(piece)
                elif Turn == -1 and isinstance(piece,King) and piece.side == 'b':
                    selfKingActions += piece.possibleMoves()[0]
                    selfKingActions += piece.possibleMoves()[1]
                    selfKing = copy.deepcopy(piece)
            return selfKing, set(selfKingActions)
        
        # Ovaj Method moze da se koristi na dva nacina:
            # 1. Da daje ko sve napada tu poziciju
                    # Figure koje DIREKTNO napadaju Kralja == LIST [Class.CHESS]
            # 2. Da daje koje pozicije su napadnuta ili branjene
                    # Pozicije oko Kralja na koje ne sme da stane dobijaju se uz sledeci Method
        def enemyAttDefCalc(position,noKing):
            king = copy.deepcopy(selfKing)
            TableDict = CurrentTableDict.copy()
            if noKing == 'noKing':
                TableDict[king.position()] = ''

            enemyAttack = []
            positionsAttacked = []
            for piece in Chess.pieces:
                T,D,A = piece.possibleMoves(TableDict)[1:]
                if Turn == 1 and  piece.side == 'b':
                    if any(position in lists for lists in [T,D,A]):
                        enemyAttack.append(piece.position())
                        positionsAttacked.append(position)
                elif Turn == -1 and  piece.side == 'w':
                    if any(position in lists for lists in [T,D,A]):
                        enemyAttack.append(piece.position())
                        positionsAttacked.append(position)
            return enemyAttack,positionsAttacked
        
        # Ovaj Method daje:
            # Ubacuje LISTE za prethodni METOD
        def enemyAttDefListCalc(positionList,noKing):
            enemyAttack = []
            for pos in positionList:
                a = enemyAttDefCalc(pos,noKing)[1]
                if a:
                    enemyAttack +=a
            return set(enemyAttack)
 
        # Ovaj metod analizira dobijenu liniju i skracuje je do neophodnog dela (2 Defender ili blokiran Attacker)
        # daje 3 podatka:
                # IndirectAttackers  == Gde se nalaze napadaci koji INDIREKTNO napadaju
                # Defender           == Ko su nase figure koje ne smemo pomeriti
                # Blockable Lines    == Koje pravce napada mozemo izblokirati. Ovo cemo morati staviti u uslov samo ako napada jedna linija inace mora pomeranje kralja       
        
        def enemyRangersAttackCalc():
            Defenders = {}
            BlockableLine = []
            for i in range(8):
                possMove = copy.deepcopy(selfKing)
                try:
                    d,bl = iteratingLine(possMove,i)
                    Defenders.update(d)
                    BlockableLine.extend(bl)
                except TypeError: # za None situacije, koje su ceste.
                    continue
            return Defenders,BlockableLine
        
        # Ovaj Method analizira jednu liniju, sta se desava na njoj, i potom ga sledeci metod provlaci kroz sve DIRECTIONS
        def iteratingLine(possMove,dirIndex):
            Line = []
            BlockableLine = []
            Defenders = {}
            defenderCount = 0
            while possMove.granica():
                possMove.incrementation(possMove.direction[dirIndex])
                if possMove.granica() and defenderCount <2:
                    Line.append(possMove.position())
                    if CurrentTableDict[possMove.position()] != '' and CurrentTableDict[possMove.position()].side != possMove.side:
                        if isinstance(CurrentTableDict[possMove.position()],Queen):
                            if defenderCount ==0:
                                BlockableLine += Line
                            else:
                                Defenders[defender] = Line
                            return Defenders,BlockableLine
                        elif isinstance(CurrentTableDict[possMove.position()],Rook) and dirIndex < 4:
                            if defenderCount ==0:
                                BlockableLine += Line
                            else:
                                Defenders[defender] = Line
                            return Defenders,BlockableLine
                        elif isinstance(CurrentTableDict[possMove.position()],Bishop) and dirIndex > 3:
                            if defenderCount ==0:
                                BlockableLine += Line
                            else:
                                Defenders[defender] = Line
                            return Defenders,BlockableLine
                        else:
                            return
                    elif CurrentTableDict[possMove.position()] !='' and CurrentTableDict[possMove.position()].side == possMove.side:
                        defenderCount +=1
                        defender = CurrentTableDict[possMove.position()]
                else:
                    return


        
        selfKing,selfKingActions = selfKingActionsCalc()
        Defenders,BlockableLine = enemyRangersAttackCalc()
        

        directAttackers: set = set(enemyAttDefCalc(selfKing.position(),None)[0]) 
        defendedEnemies: set = enemyAttDefListCalc(selfKingActions,'noKing') # srediti ovo i prethodne, ne treba sve
 

        # Da li kralj moze da se izvuce, na koja polja moze da pobegne ili koga moze da pojede
        DangerKingSolve: set = selfKingActions - defendedEnemies

        # Da li tim moze da spasi kralja 
        teamPossTake,teamPossMove = AI.attackedPieces(turn,'ourTeam','noKing',None)
        BlockingLineSolu = set(BlockableLine)&teamPossMove
        RemovingDirAttackSolu = directAttackers&AI.attackedPieces(turn,'ourTeam','noKing',list(Defenders.keys()))[0]
        DangerTeamSolve: set = BlockingLineSolu|RemovingDirAttackSolu if len(directAttackers)==1 else None

        teamPossMove: set = teamPossMove if teamPossMove is not None else set()
        teamPossTake: set = teamPossTake if teamPossTake is not None else set()
        DangerKingSolve: set = DangerKingSolve if DangerKingSolve is not None else set()
        DangerTeamSolve: set = DangerTeamSolve if DangerTeamSolve is not None else set()
        TeamOptions: set = teamPossMove|teamPossTake

        # Napraviti sa Rekurzijom da vrti dok ne napravi mat
            # Pa onda neka rekurzija da pokaze na koje nacine moze da odradi mat sa datim figurama
                # Na kraju da resava Mat zagonetke
        
        return selfKing,directAttackers,TeamOptions,Defenders,DangerKingSolve,DangerTeamSolve,CurrentTableDict



    def GameOverCheck(turn):
        selfKing,directAttackers,TeamOptions,Defenders,DangerKingSolve,DangerTeamSolve,CurrentTableDict = AI.dangerZone(turn)
        king = None
        Solution: set =  DangerKingSolve|DangerTeamSolve
        StaleMate: set = Solution|directAttackers|TeamOptions

        GameOver = None
        selfTeam = []
        enemyTeam = []
        for piece in Chess.pieces:
            if piece.side == selfKing.side:
                if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                    selfTeam.clear()
                    break
                selfTeam.append(piece)
            else:
                if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                    enemyTeam.clear()
                    break
                enemyTeam.append(piece)

        if 3>len(selfTeam)>=1 and 3>len(enemyTeam)>=1:
            GameOver = 'StaleMate'
        if not StaleMate:
            GameOver = 'StaleMate'
        if directAttackers and not Solution:
            GameOver = 'CheckMate'
        if directAttackers:
            king = selfKing.position()

        return king,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,GameOver,CurrentTableDict
    

    def CastlingCheck(turn,king):
        castling = [{(0,4),(0,5),(0,6),(0,7)},{(0,4),(0,3),(0,2),(0,1),(0,0)},
                    {(7,4),(7,5),(7,6),(7,7)},{(7,4),(7,3),(7,2),(7,1),(7,0)}]
        CastlingList = [[(0,7),(0,4)],[(0,0),(0,4)],[(7,7),(7,4)],[(7,0),(7,4)]]
        attackPos,attackPie = AI.attackedPieces(turn,None,None,None)
        attack = attackPos | attackPie
        kW,qW,kB,qB = 0,0,0,0 ; castlingOptions = [kW,qW,kB,qB]
        castlingOptions[0],castlingOptions[1],castlingOptions[2],castlingOptions[3] = king.castlingCheck()

        if castling[0] & attack:
            castlingOptions[0] *=0
        if castling[1] & attack:
            castlingOptions[1] *=0
        if castling[2] & attack:
            castlingOptions[2] *=0
        if castling[3] & attack:
            castlingOptions[3] *=0

        squares = []
        for i in range(4):
            if castlingOptions[i] !=0:
                squares += CastlingList[i]

        return squares,castlingOptions[0],castlingOptions[1],castlingOptions[2],castlingOptions[3]