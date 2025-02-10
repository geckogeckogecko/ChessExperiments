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
        file = self.files.index(notation[1])        
        rank = abs(8 - int(notation[2]))

        return 8*rank + file

    def notationToInt(self, notation):
        index = self.notationToIndex(notation)
        binRep = "0"*64
        binRep = binRep[0:index] + "1" + binRep[index+1:64]
                
        return int(binRep,2)

def visualizeBitboard(intBoard):
    bitboard = '{:064b}'.format(intBoard)
    for x in range(0, 8):
        print(bitboard[8*x:8*x+8])

board = Board()
board.loadBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

visualizeBitboard(board.empty())

#visualizeBitboard('{:064b}'.format(board.pieceBoards[0]))
#board.printBoard()
