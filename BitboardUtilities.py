class BitboardUtilities:
    
    def flip(self, bitboard):
        bitboardBinary = '{:064b}'.format(bitboard)
        bitboardBinary = bitboardBinary.replace('1','2')
        bitboardBinary = bitboardBinary.replace('0','1')
        bitboardBinary = bitboardBinary.replace('2','0')
        return int(bitboardBinary, 2)

    def north(self, bitboard):
        return bitboard<<8
    
    def south(self, bitboard):
        return bitboard>>8

    def east(self, bitboard):
        return bitboard<<1

    def west(self, bitboard):
        return bitboard>>1

    def northEast(self, bitboard):
        return bitboard<<9

    def northWest(self, bitboard):
        return bitboard<<7

    def southEast(self, bitboard):
        return bitboard>>7

    def southWest(self, bitboard):
        return bitboard>>9

    def findIndexes(self, bitboard):
        return [pos for pos, char in enumerate(format(bitboard, '064b')) if char == "1"]

    def visBitboard(self, intBoard):
        bitboard = '{:064b}'.format(intBoard)
        for x in range(0, 8):
            print(bitboard[8*x:8*x+8])
