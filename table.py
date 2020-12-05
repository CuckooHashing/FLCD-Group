
from grammar import Grammar
from LL1 import LL1
from parsing import Parser

class Node:
    def __init__(self,val,parent, soeur, index):
        self.val = val 
        self.parent = parent 
        self.soeur = soeur
        self.index = index
    

class ParseTree:
    def __init__(self, ll1: LL1, production_string:[int], productions: dict):
        self.ll1 = ll1
        self.grammar = self.ll1.grammar 
        self.production_string = production_string
        self.productions =productions
        self.crt = 1
        self.nodes = []
        print(self.production_string)

        self.build_nightmare_tree()


    
    def build_nightmare_tree(self):

        #since it goes dfs ish, we need a stack 
        stack = []
        index = 0
        value = self.productions[self.production_string[0]][0]
        self.root = Node(value, None, None, self.crt)
        self.crt+=1
        self.nodes.append(self.root)
        stack.append(self.root)

        while index<len(self.production_string) and len(stack)>0:
            current = stack[-1]

            if current.val in self.grammar.terminals or current.val == "eps":
                while len(stack)>0 and stack[-1].soeur == None:
                    stack.pop() 
                if len(stack) > 0:
                    stack.pop() 
                if len(stack) == 0:
                    break  

            else:
                prod = self.productions[self.production_string[index]] 
                
                list_of_rhs = prod[1].split(" ")

                self.crt+=len(list_of_rhs) -1
                for i in range(len(list_of_rhs)-1, -1, -1):
                    prunc = Node(None, current.index, None, self.crt) 
                    self.crt-=1 
                    if i>0:
                        prunc.soeur = self.crt
                    else:
                        prunc.soeur = None
                    prunc.val = list_of_rhs[i]
                    stack.append(prunc)
                    self.nodes.append(prunc)
                self.crt += len(list_of_rhs) + 1
                index += 1
    
    def __str__(self):
        string = ""

        for node in self.nodes:
            substring = ""
            substring += str(node.index) + " " + str(node.val) + " " + str(node.parent) + " " + str(node.soeur) + "\n"
            string += substring
        return string

parser = Parser("gr1.txt")
parser.create_the_nightmare_table()
tree = ParseTree(parser.ll1, parser.parse(['eps', 'a', '+', 'a'], ['eps', 'S']), parser.productions)

print(str(tree))






            
            


    
        

