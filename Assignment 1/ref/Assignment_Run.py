import sys

# no programming codes outside, they should be within functions!

def BC(pattern):
    return []
def GS(pattern):
    return []
def read_file(filename):
    return ""

def BM(text, pattern):
    print("hello")

if __name__ == "__main__":
    # the filename for the python run
    argument_00 = sys.argv[0]   # Assignment_Run.py
    # the actual argument
    argument_01 = sys.argv[1]   # argument_01 = "text.txt"    
    argument_02 = sys.argv[2]   # argument_02 = "pattern.lol"

    # call your functions using the arguments from argument_01 to argument_03
    BM(read_file(argument_01), read_file(argument_02))

'''
How is this ran from the command line, is as per the line below
python Assignment_Run.py text.txt pattern.lol
'''
