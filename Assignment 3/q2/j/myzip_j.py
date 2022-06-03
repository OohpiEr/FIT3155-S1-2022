from heapq import heapify, heappop, heappush
import sys

def encodeElias(binaryStream, num):
    num += 1    # Non-zero range
    totalNumBits = num.bit_length()
    bits = num
    padNumBits = totalNumBits   # Num bits of the number itself
    while padNumBits > 1:
        pad = padNumBits - 1
        padNumBits = pad.bit_length()
        pad = pad ^ (1 << (padNumBits - 1))     # Flipping the first bit
        pad = pad << totalNumBits
        bits += pad
        totalNumBits += padNumBits
    
    binaryStream = binaryStream << totalNumBits
    binaryStream += bits
    
    return binaryStream

def encodeFileName(binaryStream, fileName):
    for char in fileName:
        binaryStream = binaryStream << 8
        binaryStream += ord(char)
    
    return binaryStream

def encodeHuffmanHeader(binaryStream, text, huffmanCharArray):
    charArray = [None] * 255
    distinctChars = 0
    for char in text:
        if charArray[ord(char)]:
            charArray[ord(char)] = charArray[ord(char)] + 1
        else:
            distinctChars += 1
            charArray[ord(char)] = 1
            
    charHeap = [(charArray[i], chr(i)) for i in range(len(charArray)) if charArray[i]]    # Filter out the characters that don't appear
    charArray = huffmanCharArray
    
    heapify(charHeap)
    
    while len(charHeap) > 1:
        firstChars = heappop(charHeap)
        secondChars = heappop(charHeap)
        
        for char in firstChars[1]:
            charArray[ord(char)].append(0)
        for char in secondChars[1]:
            charArray[ord(char)].append(1)
        
        combinedChars = (firstChars[0] + secondChars[0] + ( (len(firstChars[1]) + len(secondChars[1])) * 1 / 256 ), "".join((firstChars[1], secondChars[1])))   #! Increase 256 if bugs exist
        
        heappush(charHeap, combinedChars)
        
    for i in range(len(charArray)):
        if len(charArray[i]) > 0:
            charArray[i].reverse()
            
    binaryStream = encodeElias(binaryStream, distinctChars)
    for i in range(len(charArray)):
        if len(charArray[i]) > 0:
            binaryStream = binaryStream << 8
            binaryStream += i   # Encode ascii
            binaryStream = encodeElias(binaryStream, len(charArray[i]))
            for bit in charArray[i]:
                binaryStream = binaryStream << 1
                binaryStream += bit
                
    return binaryStream

def encodeHuffman(binaryStream, huffmanCharArray, char):
    bits = huffmanCharArray[ord(char)]
    for bit in bits:
        binaryStream = (binaryStream << 1) + bit
        
    return binaryStream


def getPrefixZArray(text, index, windowSize, lookaheadSize):
    prefixZArray = [0] * (lookaheadSize + windowSize)

    r = 0
    l = 0
    if len(text) > 0:
        prefixZArray[0] = lookaheadSize + windowSize

    for i in range(1, lookaheadSize + windowSize):
        zBoxSize = 0
        if r < i:   # Not in existing Z-box
            # Maximum match will be up to length of lookahead
            for j in range(windowSize + (lookaheadSize*2) - i):
                patternChar = ""
                textChar = ""
                if j < lookaheadSize:
                    patternChar = text[index+j]
                else:
                    patternChar = text[index-windowSize+j-lookaheadSize]
                if i + j < lookaheadSize:
                    textChar = text[index+j+i]
                else:
                    textChar = text[index-windowSize+j+i-lookaheadSize]

                if textChar == patternChar:
                    zBoxSize += 1
                else:
                    break

            prefixZArray[i] = zBoxSize
            r = i+zBoxSize
            l = i
        else:       # In existing Z-box
            k = i - l
            if prefixZArray[k] < r-i:       # Case 2a (z[k] < remaining)
                prefixZArray[i] = prefixZArray[k]
            elif prefixZArray[k] > r-i:     # Case 2b (z[k] > remaming)
                prefixZArray[i] = r-i
            else:                           # Case 2c (z[k] = remaining)
                zBoxSize = prefixZArray[k]
                step = zBoxSize
                for j in range(windowSize + (lookaheadSize*2) - i - step):
                    patternChar = ""
                    textChar = ""
                    if j + step < lookaheadSize:
                        patternChar = text[index+j+step]
                    else:
                        patternChar = text[index -
                                           windowSize+j+step-lookaheadSize]
                    if i + j + step < lookaheadSize:
                        textChar = text[index+j+i+step]
                    else:
                        textChar = text[index-windowSize +
                                        j+i-lookaheadSize+step]

                    if textChar == patternChar:
                        zBoxSize += 1
                    else:
                        break

                prefixZArray[i] = zBoxSize
                r = i+zBoxSize
                l = i

    return prefixZArray[lookaheadSize:]

def modifiedZAlgorithm(text, index, windowSize, lookaheadSize):
    zArray = getPrefixZArray(text, index, windowSize, lookaheadSize)
    maxZBoxSize = 0
    distanceFromSeparator = 0
    for i in range(len(zArray)):
        if zArray[i] >= maxZBoxSize and zArray[i] <= lookaheadSize and zArray[i] != 0:
            maxZBoxSize = zArray[i]
            distanceFromSeparator = len(zArray) - i
    
    return distanceFromSeparator, maxZBoxSize

def encodeTextLZ77(binaryStream, text, windowSize, lookaheadSize, huffmanCharArray):
    i = 0
    while i < len(text):
        tempWindowSize = min(windowSize, i)
        tempLookaheadSize = min(lookaheadSize, len(text)-i)
        
        position, length = modifiedZAlgorithm(text, i, tempWindowSize, tempLookaheadSize)
        binaryStream = encodeElias(binaryStream, position)
        binaryStream = encodeElias(binaryStream, length)
        i += length + 1
        if i < len(text) + 1:
            binaryStream = encodeHuffman(binaryStream, huffmanCharArray, text[i-1])

    return binaryStream

def getBytes(binaryStream):
    while binaryStream.bit_length() % 8 != 1:
        binaryStream = binaryStream << 1
        
    binaryStream = binaryStream ^ (1 << (binaryStream.bit_length() - 1))
    bytes = binaryStream.to_bytes((binaryStream.bit_length() + 7) // 8, 'big')
    
    return bytes

def writeToOutput(inputFileName, bytes):
    outputFile = open(inputFileName + ".bin", 'wb')
    outputFile.write(bytes)
    outputFile.close()

def encode(inputFileName, windowSize, lookaheadSize):
    binaryStream = 1    # Pad with a 1
    huffmanCharArray = [[] for i in range(255)]
    binaryStream = encodeElias(binaryStream, len(inputFileName))    # Encode input file name size 
    binaryStream = encodeFileName(binaryStream, inputFileName)      # Encode input file name
    inputFile = open(inputFileName, 'r')
    text = inputFile.read()
    inputFile.close()
    binaryStream = encodeElias(binaryStream, len(text))             # Encode input file size
    binaryStream = encodeHuffmanHeader(binaryStream, text, huffmanCharArray)          # Encode the huffman codewords in header
    binaryStream = encodeTextLZ77(binaryStream, text, windowSize, lookaheadSize, huffmanCharArray)  # Encode data (text) using LZ77
    bytes = getBytes(binaryStream)  # Convert to a byte array to write to file
    writeToOutput(inputFileName, bytes)
    
    return bytes

# if __name__ == "__main__":
#     inputFileName = sys.argv[1]
#     windowSize = sys.argv[2]
#     lookaheadSize = sys.argv[3]
#     encode(inputFileName, windowSize, lookaheadSize)


# print("{0:b}".format(encode("x.asc", 15, 15)))
print("{0:b}".format(int.from_bytes(encode("x.asc", 15, 15), 'big')))
