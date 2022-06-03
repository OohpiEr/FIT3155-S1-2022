import sys

class BinaryStream:
    
    def __init__(self, binaryStream):
        self.binaryStream = binaryStream
        self.pointer = binaryStream.bit_length() - 1 + (8 - (binaryStream.bit_length() % 8))    # binaryStreamPointer denotes distance from LSB (Least Significant Bit)

    def nextBit(self, n=1):
        n -= 1
        filter = 1
        for i in range(n):
            filter = (filter << 1) + 1
        bits = (self.binaryStream >> (self.pointer - n)) & filter
        self.pointer -= (n + 1)
        return bits
    
class HuffmanBinaryTreeNode:
    
    def __init__(self, char=None):
        self.char = char
        self.left = None
        self.right = None
        self.isLeaf = True
        
    def insertLeft(self, node):
        self.char = None
        self.left = node
        self.isLeaf = False
        
    def insertRight(self, node):
        self.char = None
        self.right = node
        self.isLeaf = False

class HuffmanBinaryTree:
    
    def __init__(self):
        self.root = HuffmanBinaryTreeNode()
        
    def insertChar(self, char, encoding, encodingLength):
        current = self.root
        for i in range(encodingLength):
            newNode = HuffmanBinaryTreeNode(char)
            bit = encoding >> (encodingLength - i - 1) & 1
            if bit == 0:
                if not current.left:
                    current.insertLeft(newNode)
                current = current.left
            else:
                if not current.right:
                    current.insertRight(newNode)
                current = current.right
                
    def getChar(self, encoding, encodingLength):
        current = self.root
        for i in range(encodingLength):
            bit = encoding >> (encodingLength - i - 1) & 1
            if bit == 0:
                current = current.left
            else:
                current = current.right
        
        return current.char
    
def decodeElias(binaryStream):
    numBits = 1
    bits = binaryStream.nextBit(numBits)
    while (bits >> (numBits - 1)) & 1 == 0:     # Checking the first bit to see if bits represent a bit length or the final number
        bits = bits | (1 << (numBits - 1))      # Flip the first bit
        numBits = bits + 1
        bits = binaryStream.nextBit(numBits)
        
    # Found the number
    num = bits - 1  # Account for non-negative range encoding
    return num
    
def decodeOutputFileName(binaryStream):
    outputFileNameLength = decodeElias(binaryStream)
    outputFileNameChars = [None] * outputFileNameLength 
    for char in range(outputFileNameLength):
        ascii = binaryStream.nextBit(8)
        outputFileNameChars[char] = chr(ascii)
        
    outputFileName = "".join(outputFileNameChars)
    
    return outputFileName

def getHuffmanCharTree(binaryStream, numDistinctChars):
    huffmanCharTree = HuffmanBinaryTree()
    for i in range(numDistinctChars):
        ascii = binaryStream.nextBit(8)
        char = chr(ascii)
        encodingLength = decodeElias(binaryStream)
        encoding = binaryStream.nextBit(encodingLength)
        huffmanCharTree.insertChar(char, encoding, encodingLength)
    
    return huffmanCharTree

def decodeHuffman(binaryStream, huffmanCharTree):
    encodingLength = 1
    encoding = binaryStream.nextBit()
    char = huffmanCharTree.getChar(encoding, encodingLength)
    while not char:
        encodingLength += 1
        encoding = (encoding << 1) + binaryStream.nextBit()
        char = huffmanCharTree.getChar(encoding, encodingLength)
    
    return char

def decodeLZ77(binaryStream, huffmanCharTree, inputFileSize):
    text = [None] * inputFileSize
    charsDecoded = 0
    while charsDecoded < inputFileSize:
        position = decodeElias(binaryStream)
        length = decodeElias(binaryStream)
        if length > 0:
            for i in range(length):
                text[charsDecoded] = text[charsDecoded - position]
                charsDecoded += 1
        
        if charsDecoded < inputFileSize:
            text[charsDecoded] = decodeHuffman(binaryStream, huffmanCharTree)
            charsDecoded += 1
            
    text = "".join(text)
    return text

def decodeText(binaryStream, inputFileSize):
    numDistinctChars = decodeElias(binaryStream)
    huffmanCharTree = getHuffmanCharTree(binaryStream, numDistinctChars)
    text = decodeLZ77(binaryStream, huffmanCharTree, inputFileSize)
    
    return text

def writeToOutput(outputFileName, text):
    outputFile = open(outputFileName, 'w')
    outputFile.write(text)
    outputFile.close()

def decode(inputFileName):
    inputFile = open(inputFileName, 'rb')
    binaryStream = inputFile.read()
    byteArray = bytes(binaryStream)
    binaryStream = int.from_bytes(byteArray, 'big')
    binaryStream = BinaryStream(binaryStream)
    outputFileName = decodeOutputFileName(binaryStream)     # Decode the output file name
    inputFileSize = decodeElias(binaryStream)
    text = decodeText(binaryStream, inputFileSize)
    writeToOutput(outputFileName, text)
    
    
if __name__ == "__main__":
    inputFileName = sys.argv[1]
    decode(inputFileName)
