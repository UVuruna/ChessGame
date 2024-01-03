from tkinter import *
import copy
from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from pawn import Pawn
from rook import Rook


class AI():

    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    #@countExecutionMethod   
    def attackedPieces(Turn,tableDict,ourTeam,king,defenders,ActDict):
        def team(Turn,ourTeam):
            if ourTeam is False:
                if Turn==1:
                    return piece.side == 'b'
                else:
                    return piece.side == 'w'
            else:
                if Turn==1:
                    return piece.side == 'w'
                else:
                    return piece.side == 'b'
        def noKing(king):
            if king is False:
                return not isinstance(piece,King)
            else:
                return True     
        def noDefender(defenders):
            if defenders:
                return piece not in list(defenders.keys())
            else:
                return True

        PossibleTakes = set()
        PossibleMoves = set()
        possibleActionsDefenders = set()
        possibleActionsDict = {}
        for piece in Chess.pieces:
            take = set() ; move = set()
            if team(Turn,ourTeam) and noKing(king):
                if noDefender(defenders):
                    PossibleTakes.update(piece.possibleMoves(tableDict)[1])
                    PossibleMoves.update(piece.possibleMoves(tableDict)[0])
                    if ActDict:
                        possibleActionsDict[piece]=set(set(piece.possibleMoves(tableDict)[1])|set(piece.possibleMoves(tableDict)[0]))
                else:
                    take.update(piece.possibleMoves(tableDict)[1])
                    move.update(piece.possibleMoves(tableDict)[0])
                    actionsAll = take|move
                    possibleActionsDefenders.update(actionsAll&set(defenders[piece]))
                    if ActDict:
                        possibleActionsDict[piece]=set(actionsAll&set(defenders[piece]))
        return PossibleTakes, PossibleMoves, possibleActionsDefenders, possibleActionsDict
    
    #@countExecutionMethod    
    def dangerZone(turn):
        Turn = turn
        CurrentTableDict = Chess.currentTableDict()

        #@AI.countExecutionMethod
        def selfKingActionsCalc():
            global realKing
            selfKingActions = []
            for piece in Chess.pieces:
                if Turn == 1 and isinstance(piece,King) and piece.side == 'w':
                    selfKingActions += piece.possibleMoves(CurrentTableDict)[0]
                    selfKingActions += piece.possibleMoves(CurrentTableDict)[1]
                    selfKing = copy.deepcopy(piece)
                    realKing = piece
                elif Turn == -1 and isinstance(piece,King) and piece.side == 'b':
                    selfKingActions += piece.possibleMoves(CurrentTableDict)[0]
                    selfKingActions += piece.possibleMoves(CurrentTableDict)[1]
                    selfKing = copy.deepcopy(piece)
                    realKing = piece
            return selfKing, set(selfKingActions)

        #@AI.countExecutionMethod
        def enemyAttDefCalc(position,noKing):
            king = copy.deepcopy(selfKing)
            TableDict = CurrentTableDict.copy()
            if noKing == True:
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

        #@AI.countExecutionMethod
        def enemyAttDefListCalc(positionList,noKing):
            enemyAttack = []
            for pos in positionList:
                a = enemyAttDefCalc(pos,noKing)[1]
                if a:
                    enemyAttack +=a
            return set(enemyAttack)
     
        #@AI.countExecutionMethod
        def enemyArcherDanger():
            Defenders = {}
            BlockableLine = []
        #@AI.countExecutionMethod
            def iteratingLine(possMove,direction):
                Line = []
                BlockableLine = []
                Defenders = {}
                defenderCount = 0
                while possMove.insideBorder():
                    possMove.incrementation(direction)
                    if possMove.insideBorder() and defenderCount <2:
                        Line.append(possMove.position())
                        if CurrentTableDict[possMove.position()] != '' and CurrentTableDict[possMove.position()].side != possMove.side:
                            if CurrentTableDict[possMove.position()].type =="Archer" and direction in CurrentTableDict[possMove.position()].direction:
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

            for dir in Chess.direction:
                possMove = copy.deepcopy(selfKing)
                try:
                    d,bl = iteratingLine(possMove,dir)
                    Defenders.update(d)
                    BlockableLine.extend(bl)
                except TypeError: # za None situacije, koje su ceste.
                    continue
            return dict(Defenders),set(BlockableLine)
        
        selfKing,selfKingActions = selfKingActionsCalc()
        Defenders,BlockableLine = enemyArcherDanger()
        directAttacker: set = set(enemyAttDefCalc(selfKing.position(),noKing=False)[0]) 
        defendedEnemies: set = enemyAttDefListCalc(selfKingActions,noKing=True) 
        teamPossTake,teamPossMove,possibleActionsDefenders,possibleActionsDict  = AI.attackedPieces(turn,CurrentTableDict,ourTeam=True,king=False,defenders=Defenders,ActDict=True) 
        directAttackerSolution = directAttacker&teamPossTake
        blockableLineSolution = BlockableLine&teamPossMove

        DangerKingSolve: set = selfKingActions - defendedEnemies
        DangerTeamSolve: set = directAttackerSolution|blockableLineSolution if len(directAttacker)==1 else set()
        TeamOptions: set = teamPossMove|teamPossTake|possibleActionsDefenders
        possibleActionsDict[realKing]=DangerKingSolve

        return selfKing,directAttacker,TeamOptions,Defenders,DangerKingSolve,DangerTeamSolve,CurrentTableDict,possibleActionsDict


    #@countExecutionMethod
    def GameOverCheck(turn):
        selfKing,directAttacker,TeamOptions,Defenders,DangerKingSolve,DangerTeamSolve,CurrentTableDict,possibleActionsDict = AI.dangerZone(turn)
        king = None
        Solution: set =  DangerKingSolve|DangerTeamSolve
        StaleMate: set = Solution|directAttacker|TeamOptions

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
        if directAttacker and not Solution:
            GameOver = 'CheckMate'
        if directAttacker:
            king = selfKing.position()

        return king,DangerKingSolve,directAttacker,DangerTeamSolve,Defenders,GameOver,CurrentTableDict,possibleActionsDict
    
    #@countExecutionMethod
    def CastlingCheck(turn,tableDict,king):
        castling = [{(0,4),(0,5),(0,6),(0,7)},{(0,4),(0,3),(0,2),(0,1),(0,0)},
                    {(7,4),(7,5),(7,6),(7,7)},{(7,4),(7,3),(7,2),(7,1),(7,0)}]
        CastlingList = [[(0,7),(0,4)],[(0,0),(0,4)],[(7,7),(7,4)],[(7,0),(7,4)]]
        attackPos,attackPie = AI.attackedPieces(turn,tableDict,ourTeam=False,king=True,defenders=None,ActDict=False)[:2]
        attack = attackPos | attackPie
        kW,qW,kB,qB = 0,0,0,0 ; castlingOptions = [kW,qW,kB,qB]
        castlingOptions[0],castlingOptions[1],castlingOptions[2],castlingOptions[3] = king.castlingCheck(tableDict)

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