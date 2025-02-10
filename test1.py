class Board:
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

    def flip(self, bitboard):
        bitboardBinary = '{:064b}'.format(bitboard)
        bitboardBinary = bitboardBinary.replace('1','2')
        bitboardBinary = bitboardBinary.replace('0','1')
        bitboardBinary = bitboardBinary.replace('2','0')
        return int(bitboardBinary, 2)
    
    def empty(self):
        return self.flip(self.occupied())

    def occupiedByColour(self,colour):
        occupiedBoard = 0
        if colour == "w":
            for x in range(0,6):
                occupiedBoard = occupiedBoard|self.pieceBoards[x]
        else:
            for x in range(6,12):
                occupiedBoard = occupiedBoard|self.pieceBoards[x]
        return occupiedBoard

    def north(self,bitboard):
        return bitboard<<8
    
    def south(self,bitboard):
        return bitboard>>8

    def east(self,bitboard):
        return bitboard<<1

    def west(self,bitboard):
        return bitboard>>1

    def northEast(self,bitboard):
        return bitboard<<9

    def northWest(self,bitboard):
        return bitboard<<7

    def southEast(self,bitboard):
        return bitboard>>7

    def southWest(self,bitboard):
        return bitboard>>9

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
        print(file + str(rank))

    def notationToInt(self, notation):
        index = self.notationToIndex(notation)
        binRep = "0"*64
        binRep = binRep[0:index] + "1" + binRep[index+1:64]
                
        return int(binRep,2)

    def executeMove(self,piece,startSquare,endSquare):
        oldBoard = self.pieceBoards[self.pieceNotation.index(piece)]
        newBoard = (oldBoard|self.notationToInt(endSquare))&~self.notationToInt(startSquare)
        self.pieceBoards[self.pieceNotation.index(piece)] = newBoard

    def generateMoves(self, colour):
        if colour == "w":
            singlePawnMoves = self.north(self.pieceBoards[0])&self.empty()
            #4278190080 = rank 4
            doublePawnMoves = self.north(singlePawnMoves)&self.empty()&4278190080
            attackPawnMoves = (self.northEast(self.pieceBoards[0])|self.northWest(self.pieceBoards[0]))&self.occupiedByColour("b")
        return singlePawnMoves|doublePawnMoves|attackPawnMoves

def visBitboard(intBoard):
    bitboard = '{:064b}'.format(intBoard)
    for x in range(0, 8):
        print(bitboard[8*x:8*x+8])

board = Board()
board.loadBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
board.printBoard()

while True:
    print(" ")
    move = input("Move: ")
    board.executeMove("P",move.split(" ")[0], move.split(" ")[1])
    board.printBoard()

#visualizeBitboard(board.generateMoves("w"))

#visualizeBitboard('{:064b}'.format(board.pieceBoards[0]))
#board.printBoard()
