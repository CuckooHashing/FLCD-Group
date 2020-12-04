
# from grammar import Grammar

class Node:
    def __init__(self,line,column, val):
        self.val = val 
        self.left_child = None 
        self.right_sibiling = None
    
    def __str__(self):
        return self.val + ": left child: " + self.left_child.val + ": right sibiling: " + self.right_sibiling.val  



class ParseTree:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar 
        self.rows = self.grammar.nonterminals + self.grammar.terminals 
        self.columns = self.grammar.terminals 
        self.root = None 



#     def get_value_of_node(self, line, column):
        
#         if line == column:
#             return "pop"
#         else:
#             return "err"

#     def create_tree(self):
#         self.root = Node(self.rows[0], self.columns[0], "err")
#         current = self.root
#         descending = self.root
#         for j in range(1,len(self.columns)):
#             val = self.get_value_of_node(self.rows[0], self.columns)
#             current.right_sibiling = Node(self.rows[0], self.columns[j], "err")
#             current = current.right_sibiling
#         for i in range(1, len(self.rows)):
#             current = Node(self.rows[i], self.columns[j], "err")
#             descending.left_child = current
#             descending = descending.left_child
#             for j in range(1,len(self.columns)):
#                 current.right_sibiling = Node(self.rows[i], self.columns[j], "err")
#                 current = current.right_sibiling


#     def print_tree(self):

#         current = self.root 
#         descending = self.root
#         print(self.columns)
#         while descending!=None:
#             s = descending.line + " "
#             while current!=None:
#                 s+=current.val + " "
#                 current = current.right_sibiling 
#             print(s) 
#             descending = descending.left_child
#             current = descending


# pt = ParseTree(Grammar.read_from_file("gr1.txt"))
# pt.create_tree()
# # pt.print_tree()
# print("=========================================")
# # print(pt.rows)
# # print(pt.columns)
# pt.print_tree()








            
            


    
        

