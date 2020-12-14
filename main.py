
from parsing import Parser 
from table import ParseTree


def read_pif(file_name):
    
    f = open(file_name) 
    result = []
    while True: 
        line = f.readline() 
        if not line:
            break 

        toks = line.split(" ")

        result.append(toks[0])

    result.reverse() 
    result = ['eps'] + result 
    return result

def read_seq(file_name):

    f = open(file_name)
    line = f.readline()
    toks = line.split(" ")
    toks = ['eps'] + toks

    return toks

def print_menu():
    print("1. run first grammar")
    print("2. run second grammar")


def main():

    print_menu()
    cmd = input(">")
    if cmd == "1":
        parser = Parser("gr1.txt")
        seq = read_seq("seq.txt")
        parser.create_the_nightmare_table()
        parsing = parser.parse(seq, ["eps", "S"])
        if len(parsing) == 0:
            print("amu ii bai")
        elif type(parsing[0]) == type("mno"):
            print("amu ii bai si incepe la tokenul:")
            print(parsing.reverse())
        else:
            tree = ParseTree(parser.ll1, parsing, parser.productions)
            print(str(tree))      
 
    if cmd == "2":
        parser = Parser("grammar-ioana.txt")
        out = read_pif("PIFU_BUN2.txt")
        # print(out)
        parser.create_the_nightmare_table()
        parsing = parser.parse(out, ["eps", "START"])
        print(parsing)
        out = read_pif("PIF.out")
        # print(out)
        parser.create_the_nightmare_table()
        parsing = parser.parse(out, ["eps", "START"])
        # print(parsing)
        if len(parsing) == 0:
            print("amu ii bai")
        elif type(parsing[0]) == type("mno"):
            print("amu ii bai si incepe la tokenul:")
            parsing.reverse()
            print(parsing)
            print(parsing.reverse())
        else:
            tree = ParseTree(parser.ll1, parsing, parser.productions)
            print(str(tree))        


if __name__ == "__main__":
    main()

