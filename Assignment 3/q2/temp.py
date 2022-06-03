import heapq

class HuffmanFreqTuple():
    def __init__(self, freq, chars):
        self.freq = freq
        self.chars = chars
    
    def __lt__(self, other):
        if self.freq == other.freq:
            return len(self.chars) < len(other.chars)
        else:
            return self.freq < other.freq
    
    def __gt__(self, other):
        if self.freq == other.freq:
            return len(self.chars) > len(other.chars)
        else:
            return self.freq > other.freq


def huffman(txt):
    unique_char_count = 0
    # initialize frequency/probability array
    encoding_arr = [0] * 256
    freq_arr = []  # contains list of (frequency, [ord(char)])
    for char in txt:
        encoding_arr[ord(char)] += 1
    for i in range(len(encoding_arr)):
        if encoding_arr[i] != 0:
            freq_arr.append(HuffmanFreqTuple(encoding_arr[i], [i]))
            unique_char_count += 1
        encoding_arr[i] = []

    # heapify freq_arr
    heapq.heapify(freq_arr)
    while freq_arr:
        serve1 = heapq.heappop(freq_arr)
        # print("serve1 {} {}".format(serve1.freq, [chr(c) for c in serve1.chars]))
        for i in serve1.chars:
            encoding_arr[i].append(0)

        if freq_arr:
            serve2 = heapq.heappop(freq_arr)
            # print("serve2 {} {}".format(serve2.freq, [chr(c) for c in serve2.chars]))
            for i in serve2.chars:
                encoding_arr[i].append(1)

            heapq.heappush(freq_arr, HuffmanFreqTuple(serve1.freq + serve2.freq, serve1.chars + serve2.chars))

    return encoding_arr, unique_char_count

if __name__ == "__main__":
    encoding_arr, unique_char_count = huffman("aaaabbccde")
