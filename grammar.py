
class Grammar:
    def __init__(self, nonterminals, terminals, productions, starting_symbol):
        self.nonterminals = nonterminals 
        self.terminals = terminals
        self.productions = productions
        # STARTING SYMBOL
        self.starting_symbol  = starting_symbol


    @staticmethod
    def parse_production(line):

        l1 = line.split("->")
        lhs = l1[0].strip()
        rhs = l1[1].split("|")
        for i in range(len(rhs)):
            rhs[i] = rhs[i].strip()
        
        return lhs, rhs

    @staticmethod
    def read_from_file(file_name):
        
        f = open(file_name)

        line = f.readline().strip()
        non_term = line.split(" ")
        line = f.readline().strip()
        terminals = line.split(" ")

        prods = {}
        while True:
            line = f.readline()
            if not line:
                break
            lhs, rhs_final = Grammar.parse_production(line)
            # TODO: insert this into the prods dict
            prods[lhs] = rhs_final
        
        return Grammar(non_term, terminals, prods, non_term[0])



    def print_set_of_nonterminals(self):
        print(self.nonterminals)
        print(self.starting_symbol) 

    def print_set_of_terminals(self):
        print(self.terminals) 

    def productions_for_nonterminal(self):
        
        print(self.productions) 


gram = Grammar.read_from_file("gr1.txt")
gram.print_set_of_nonterminals()
gram.print_set_of_terminals()
gram.productions_for_nonterminal()
