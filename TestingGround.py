from BitboardUtilities import BitboardUtilities
from Board import Board

board = Board()
bitUtil = BitboardUtilities()

board.loadBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
board.printBoard()
moveList = board.generateMoves("w")
board.executeMove("P", moveList[0][0], moveList[0][1])
board.printBoard()
