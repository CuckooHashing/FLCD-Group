from LL1 import LL1
from grammar import Grammar

class Parser:
    def __init__(self, filename: str):
        self.ll1 = LL1(filename)
        self.rows = self.ll1.grammar.nonterminals + self.ll1.grammar.terminals 
        self.columns = self.ll1.grammar.terminals 
        # self.table = [[None]*len(self.columns)]*len(self.rows)
        self.table = [] 
        for i in range(len(self.rows)):
            new_lst = []
            for j in range(len(self.columns)):
                new_lst.append(None)
            self.table.append(new_lst)

        self.ll1.follow = self.ll1.follow_iterative()     
        self.productions = {}
    


    def apply_rules_to_obtain_position(self, key, value):
        # we apply the rules from course 7
        # it returns the position in the matrix
        
        row = key 
        result = []
        first = self.ll1.real_first[value[0]]
        if "eps" not in value:
            for terminal in first:
                result.append((row, terminal))
        else:
            follow = self.ll1.follow[key] 
            # print(key)
            # print(follow)
            for ceva in follow:
                result.append((row, ceva))
        return result


    def create_the_nightmare_table(self):
        # As per our discussion, we take each production, and we see 
        # where its rhs belongs, aka we compute the position in the table
        prods = self.ll1.grammar.productions
        i=1
        for key in prods.keys():
            # print("ACI II KEY: ", key)
            num_row =  self.rows.index(key)

            for rhs in prods[key]:
                indices = self.apply_rules_to_obtain_position(key,rhs.split(" "))
                # print("KEY II {0} RHS II {1} ".format(key, rhs))
                # print(indices)
                # print(i)
                for  column in indices:
                    num_col = self.columns.index(column[1])

                    if self.table[num_row][num_col] != None and self.table[num_row][num_col] != i:
                        print ("CONFLICT AT CELL (" + key + ", " + column[1] + ")" )
                    else:
                        self.table[num_row][num_col] = i
                self.productions[i] = (key, rhs)
                i+=1
        
        for terminal in self.ll1.grammar.terminals:
            num_row = self.rows.index(terminal)
            num_col = self.columns.index(terminal) 
            self.table[num_row][num_col] = "pop"
        
        num_row = self.rows.index("eps")
        num_col = self.columns.index("eps") 
        self.table[num_row][num_col] = "acc"  

        

    def parse(self, alpha: list, beta: list):
        # When we get our table done, we start parsing 
        # we get as parameter our stack (which is a list, but it does the trick)
        # we go with the algo from the seminar
        pi = []
        while True:

            top_alpha = alpha[-1] 
            top_beta = beta[-1] 

            if top_alpha == 'eps' and top_beta == 'eps': 
                return pi 
            
            if self.table[self.rows.index(top_beta)][self.columns.index(top_alpha)] == None:
                return alpha 

            prod_number = self.table[self.rows.index(top_beta)][self.columns.index(top_alpha)]

            if prod_number == "pop":
                alpha.pop() 
                beta.pop() 
            else:
                rhs = self.productions[prod_number][1] 
                toks = rhs.split(" ") 
                toks.reverse() 
                if toks[-1] == 'eps':
                    toks.pop()
                beta.pop()
                beta+=toks 
                pi.append(prod_number)


            
if __name__ == "__main__":
    pareser = Parser("grammar-ioana.txt")
    # pareser.table[0][0] = 7
    # print(pareser.rows)
    # print(pareser.columns)
    pareser.create_the_nightmare_table()
    # for line in pareser.table:
    #     print(line)
    print(pareser.parse(['eps','}' ,';' ,'intConst', '<-' ,'id','{','main_body'], ['eps', 'START']))
    # print(pareser.parse(['eps','}',';', ')','stringConst','(','read_integer','<-','id','{','main_body'], ['eps', 'START']))
