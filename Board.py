from BitboardUtilities import BitboardUtilities

class Board:

    bitUtil = BitboardUtilities()
    
    whiteSquares = 12273903644374837844
    blackSquares = 6172840429334713770

    pieceBoards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pieceNotation = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']

    files = ['a','b','c','d','e','f','g','h']

    sideToMove = ""
    castlingAbility = ""
    enPassantTarget = ""
    enPassantBitboard = 0
    halfMoveClock = 0
    fullMove = 0

    def occupied(self):
        occupiedBoard = 0
        for x in range(0,12):
            occupiedBoard = occupiedBoard|self.pieceBoards[x]
        return occupiedBoard

    def empty(self):
        return self.bitUtil.flip(self.occupied())

    def occupiedByColour(self,colour):
        occupiedBoard = 0
        if colour == "w":
            for x in range(0,6):
                occupiedBoard = occupiedBoard|self.pieceBoards[x]
        else:
            for x in range(6,12):
                occupiedBoard = occupiedBoard|self.pieceBoards[x]
        return occupiedBoard

    def clear(self):
        for x in range(0,12):
            self.pieceBoards[x] = 0

    def printBoard(self):
        print(self.castlingAbility + " " + self.enPassantTarget)

        if self.sideToMove == "b":
            print("=>+------------------------+")
        else:
            print("  +------------------------+")

        for x in range(0,8):
            rank = str(8-x) + " |"
            for x in range(8*x, 8*x + 8):
                if ('{:064b}'.format(self.blackSquares))[x] == "1":
                    rank += ":" + self.pieceFromIndex(x) + ":"
                else:
                    rank += " " + self.pieceFromIndex(x) + " "
            print(rank + "|")

        if self.sideToMove == "w":
            print("=>+------------------------+")
        else:
            print("  +------------------------+")

        print("    a  b  c  d  e  f  g  h")
            
    def pieceFromIndex(self, index):
        for x in range(0, 12):
            if ('{:064b}'.format(self.pieceBoards[x]))[index] == "1":
                return self.pieceNotation[x]
    
        if ('{:064b}'.format(self.blackSquares))[index] == "1":
            return ":"
        return " "

    def loadBoard(self, startingPosFEN):
        self.clear()
        
        startingPosFENArray = startingPosFEN.split(" ")

        startingPosBase = startingPosFENArray[0]
        self.sideToMove = startingPosFENArray[1]
        self.castlingAbility = startingPosFENArray[2]
        self.enPassantTarget = startingPosFENArray[3]
        if startingPosFENArray[3] != '-':
            self.enPassantBitboard = self.notationToInt(startingPosFENArray[3])
        self.halfMoveClock = startingPosFENArray[4]
        self.fullMove = startingPosFENArray[5]
        
        startingPos = ""
        for x in range(0, len(startingPosBase)):
            if startingPosBase[x].isdigit():
                startingPos += "0"*int(startingPosBase[x])
            elif startingPosBase[x] != '/':
                startingPos += startingPosBase[x]
        
        x = 0
        while x < len(startingPos):
            for y in range(0,12):
                if startingPos[x] == self.pieceNotation[y]:
                    binRep = '{:064b}'.format(self.pieceBoards[y])
                    binRep = binRep[0:x] + "1" + binRep[x+1:64]
                    self.pieceBoards[y] = int(binRep,2)
            x += 1
            
    def notationToIndex(self, notation):
        file = self.files.index(notation[0])        
        rank = abs(8 - int(notation[1]))
        return 8*rank + file

    def indexToNotation(self, index):
        rank = abs(8-(index>>3))
        file = self.files[index&7]
        return file + str(rank)

    def notationToInt(self, notation):
        index = self.notationToIndex(notation)
        binRep = "0"*64
        binRep = binRep[0:index] + "1" + binRep[index+1:64]
        return int(binRep,2)

    def executeMove(self,piece,startSquare,endSquare):
        oldBoard = self.pieceBoards[self.pieceNotation.index(piece)]
        newBoard = (oldBoard|self.notationToInt(endSquare))&~self.notationToInt(startSquare)
        self.pieceBoards[self.pieceNotation.index(piece)] = newBoard

    def getStartSquare(self,notation):
        match len(notation):
            case 2:
                endIndex = self.notationToIndex(notation)
                if format(self.pieceBoards[0],'064b')[endIndex+8] == "1":
                    return self.indexToNotation(endIndex+8)
                elif format(self.pieceBoards[0],'064b')[endIndex+16] == "1":
                    return self.indexToNotation(endIndex+16)
            case 3:
                if notation[0] == "x":
                    endIndex = self.notationToIndex(notation[1:3])
                    if format(self.pieceBoards[0],'064b')[endIndex+7] and notation[1] != "a":
                        return self.indexToNotation(endIndex+7)
                    elif format(self.pieceBoards[0],'064b')[endIndex+9] and notation[1] != "h":
                        return self.indexToNotation(endIndex+9)
            

    def generateWhitePawnMoves(self):
        pushMoves = []
        attackMoves = []
        singlePawnMoves = self.bitUtil.north(self.pieceBoards[0])&self.empty()
        #4278190080 = rank 4
        doublePawnMoves = self.bitUtil.north(singlePawnMoves)&self.empty()&4278190080
        pushMoveIndexes = self.bitUtil.findIndexes(singlePawnMoves|doublePawnMoves)
        for x in pushMoveIndexes:
            pushMoves.append([self.getStartSquare(self.indexToNotation(x)), self.indexToNotation(x)])

        attackPawnMovesEast = self.bitUtil.northEast(self.pieceBoards[0])&self.occupiedByColour("b")
        attackPawnMovesWest = self.bitUtil.northWest(self.pieceBoards[0])&self.occupiedByColour("b")
        attackMoveIndexes = self.bitUtil.findIndexes(attackPawnMovesEast) + self.bitUtil.findIndexes(attackPawnMovesWest)
        for x in attackMoveIndexes:
            attackMoves.append("x" + self.indexToNotation(x))
        return attackMoves + pushMoves
        


    def generateMoves(self, colour):
        moveList = []
        moveList += self.generateWhitePawnMoves()
        
        return moveList
