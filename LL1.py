from grammar import Grammar


class LL1:
    def __init__(self, grammar: str):
        self.grammar = Grammar.read_from_file(grammar)
        self.first = self.FIRST()#to avoid max recursion in follow
        # self.follow = self.FOLLOW()
        self.follow = {}
        self.real_first = self.FIRST()
        # self.first = {}



    def get_first_existing_terminals(self, non_term):

        l = []
        values = self.grammar.productions[non_term]
        for elem in values:
            toks = elem.split(" ")
            for tok in toks:
                if tok in self.grammar.terminals:
                    l.append(tok)
                    break
        return l


    def get_first_terminals(self, non_term:str):

        first_terminals_from_each_production_of_a_non_terminal = []
        values = self.grammar.productions[non_term]
        for elem in values:
            toks = elem.split(" ")
            if toks[0] in self.grammar.terminals:
                first_terminals_from_each_production_of_a_non_terminal.append(toks[0])

        
        return first_terminals_from_each_production_of_a_non_terminal

    

    def first_rec(self, non_term:str):
        '''
        generates the FIRST of a non-terminal -> result has to be setifyed
        '''
        
        if len(self.get_first_terminals(non_term)):
            return self.get_first_terminals(non_term)
        else:
            
            values = self.grammar.productions[non_term]
            toks = values[0].split(" ")
            final_list = []
            for elem in values:
                toks = elem.split(" ")
                final_list+= self.first_rec(toks[0])
                 
            return final_list + self.get_first_existing_terminals(non_term)


    def FIRST(self):
        '''
        wrapper for first_rec -> returns the first for all nonterminals
        '''
        first_map = {}
        for key in self.grammar.nonterminals:
            first_map[key] = set(self.first_rec(key))
        
        return first_map

    def FOLLOW(self):
        '''
        wrapper for follow_rec -> returns the follow for all nonterminals
        '''
        # follow_map = {}
        for key in self.grammar.nonterminals:
            self.follow[key] = set(self.follow_rec(key))

        # return self.follow

    def productions_with_nonterminal(self, non_term):
        '''
        get all productions that contain a specific non terminal in their lhs
        '''
        productions_that_contain_nonterminal = {}
        values = self.grammar.productions
        for elem in values.keys():
            for ceva in values[elem]:
                if non_term in ceva:
                    productions_that_contain_nonterminal[elem] = values[elem]
                    break
        return productions_that_contain_nonterminal


    def follow_rec(self, non_term):
        l = []
        if non_term == self.grammar.starting_symbol:
            l = ['eps']
            # return l
        productions = self.productions_with_nonterminal(non_term)
        for prod in productions.keys():
            for value in productions[prod]:
                ceva = value
                if ceva[-1].strip() == non_term:
                    #if our good non-terminal buddy is the last thing in the production, there is no y
                    # return l + self.follow_rec(prod)#max recusion without return here 
                    if prod in self.follow.keys():
                        l+=list(self.follow[prod])
                    else:
                        l += self.follow_rec(prod)
                    return l
                else:
                    actual_values = value.split(" ")
                    #find whomst is y in aBy thing
                    found = False
                    for i in range(len(actual_values)):
                        if actual_values[i] == non_term:
                            index =i+1
                            found = True #check if the nonterminal was found in the product
                            break 
                    if found:
                        #get what is basically FIRST(y)
                        if actual_values[index] in self.grammar.terminals:
                            first = [actual_values[index]]
                        else:
                            first = self.first[actual_values[index]]

                        if "eps" in first:
                            first.remove("eps")
                            l += first
                            if prod in self.follow.keys():
                                l+=self.follow[prod]
                            else:
                                l += self.follow_rec(prod)
                            # return l
                        else:
                            l += first
        return l


    def get_prods_with_nt_in_rhs(self, nonterminal):
        productions_that_contain_nonterminal = {}
        # values = self.grammar.productions
        for key in self.grammar.productions:
            values = self.grammar.productions[key]
            for value in values:
                if nonterminal in value:
                    if key in productions_that_contain_nonterminal.keys():
                        productions_that_contain_nonterminal[key].append(value)
                    else:
                        productions_that_contain_nonterminal[key] = [value]
        
        return productions_that_contain_nonterminal



    def initialize_for_follow(self):

        follow_map = {}
        for nt in self.grammar.nonterminals:
            follow_map[nt] = []        
        return follow_map


    def concatenate_for_follow(self, l1:list, l2: list):

        if "eps" in l1:
            l1.remove("eps") 
            l1+=l2 
            return l1 

        return l1


    def get_first_for_prod(self, prod):
        result = ["eps"]
        contains_terminal = False
        for s in prod:
            first = [] 
            if s in self.grammar.terminals:
                first.append(s)
                contains_terminal = True
            else:
                first = self.real_first[s]
            result = self.concatenate_for_follow(result, first)
            if contains_terminal or "eps" in first:
                return list(set(result))
        
        return list(set(result))

    def follow_iterative(self):

        follow_map = self.initialize_for_follow()
        follow_map[self.grammar.starting_symbol].append("eps")
        while True:
            current_follow_map = self.initialize_for_follow()
            current_follow_map[self.grammar.starting_symbol].append("eps")
            for nt in self.grammar.nonterminals:
                current_follow_map[nt]+= follow_map[nt]
                prods = self.get_prods_with_nt_in_rhs(nt)
                for key in prods.keys():
                    lhss = prods[key]
                    for lhs in lhss:
                        toks = lhs.split(" ")
                        index = toks.index(nt)
                        if index == len(toks) - 1:
                            if key!=nt:
                                current_follow_map[nt]+=follow_map[key]
                        else:
                            first = self.get_first_for_prod(toks[index+1:])
                            if "eps" in first:
                                first.remove("eps")
                                current_follow_map[nt] += follow_map[key] 

                            current_follow_map[nt] += first 
            
            for key in current_follow_map.keys():
                current_follow_map[key]  = set(current_follow_map[key])
            contin = False
            for key in follow_map.keys():

                if len(follow_map[key]) != len(current_follow_map[key]):
                    contin = True
                    break 
            
            if not contin:
                return current_follow_map
            follow_map = current_follow_map
           
                            


# ll1 = LL1("gr3.txt")
# print("--------------------------------")
# ll1.FIRST()
# # ll1.FOLLOW()
# print(ll1.real_first)
# print(ll1.follow_iterative())
