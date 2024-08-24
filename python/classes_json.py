
ou = "∨"
et = "∧"
implique = "=>"
sVar = "single variable"
expr = "expression"

class Question : 

   def __init__ (self, expressions=[], connector = None):
      self.expressions = expressions
      self.connector = connector

   def __str__ (self) :
      string = ""
      for expression in self.expressions :
         string += str(expression) + " | "
      return (",,, exprs : " + string + " ,,, connector : " + self.connector)
   
   def evaluate(self) :
      value = None
      if self.connector == et :
         value = True
         for expr in self.expressions :
            value = value and expr.evaluate()
      elif self.connector == ou :
         for expr  in self.expressions :
            value = value or expr.evaluate()
      return value

class Expression :
   "an expression is made of variable(s) and connectors"
   "expr : var = [a,b,c], connector = '∧'"

   def __init__ (self, variables, connector=None):
      self.vars = variables
      self.connector = connector
      

   def isSingle(self) :
      return isinstance(self.vars, Variable)
   
   def evaluate(self) :
      value = None
      if self.connector == et :
         value = True
         for var in self.vars :
            value = value and var.value
      elif self.connector == ou :
         for var in self.vars :
            value = value or var.value
      return value
   
   def __str__ (self) :
      string = ""
      for var in self.vars :
         string += str(var) +" "
      return ("vars : " + string + ", connector : " + self.connector)



class Rule :
    "a Rule, in our case, is made of antecedent(s), connectors, and a consequent"

#utiliser une surcharge de fonction pour le constructeur ?
    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents
        self.connector = implique
        self.consequent = consequent
        self.used = False
        self.name = str(self)

    def __str__(self):
     toPrint = ""
     for i in range (len(self.antecedents)) :
        toPrint += str(self.antecedents[i])
        if i+1<(len(self.antecedents)) :
           toPrint += " ∧ "
        else :
           toPrint += " "
     toPrint += self.connector + " "
     toPrint += str(self.consequent)
     return toPrint
    
    #for step by step algorithm --------

    def use(self) :
     self.used = True
     return self.used

    def is_used(self) :
     return self.used
    
     # ----------------------------------
     
class Variable :
   
   def __init__ (self, name, value=False) :
      self.name = name
      self.value = value

   def __eq__(self, other):
      return self.name == other.name


   def assign(self, bool=True) :
      self.value = bool

   def isAssigned (self) :
      return (self.value != None)
   
   def is_true (self) :
      return self.value
   
   def evaluate (self) :
      return self.value
   
   def __str__(self) :
      description = self.name
      # if self.isAssigned() :
      #    description += " (" + str(self.value) +")"
      return description



# parsing the dictionnary from the JSON to an adapted format
# JSON dictionnary : 
# {'rules': [['Var1 ∧ ... ∧ VarN ', 'Consequence'], ... ], 
# 'question': 'Question', 
# 'facts base': ['Var31', ... 'Var40']}

# then will become :
# {'rules': [ Rule1, Rule2, ... ], 
# 'question': Variable 
# 'facts base': [Variable1, ..., VariableN]}

#     example :
# {'rules': [['A2 ∧ P2 ∧ Z3 ∧ A5', 'P4'], ['A2 ∧ Z5 ∧ P4', 'Z2'], ['P2 ∧ A2 ∧ Z1 ∧ A2', 'P3'], ['A2 ∧ Z4', 'Z5'], ['Z2 ∧ Z4 ∧ P2 ∧ P1 ∧ P1', 'P2'], ['P2', 'Z2']], 
# 'question': 'Z1', 
# 'facts base': ['P5', 'Z5', 'A4', 'A1', 'A2', 'A3', 'P1', 'A5', 'Z4', 'P2']}



def createSet (JSONobject) :
   variables = {}
   dictionnaire = {}          # FB, R, Q
   rules = JSONobject['rules']
   fb = JSONobject['facts base']
   question = parseQuestion(JSONobject['question'])
   rulesParsed = []
   for rule in rules :
      rulesParsed.append(listToRule(rule, variables))
   dictionnaire['rules'] = rulesParsed
   dictionnaire['facts base'] = create_fb(fb, variables)
   dictionnaire['question'] = create_question(question, variables)
   return dictionnaire



def create_ant (list, variables) :
   "takes a list of antecedents in the format ['Var1', ..., 'VarN']"
   "and returns a list of Variable objects [Variable1, ..., VariableN]"
   antList = []
   for antStr in list :
      if antStr not in variables :
         ant = Variable(antStr)
         variables[antStr] = ant
      else :
         ant = variables[antStr]
      antList.append(ant)
   return antList

def createCsqObj (var, variables) :
   "takes a string in the format 'Var'"
   "and return a Variable object Variable"

   if var not in variables :
      csq = Variable(var)
      variables[var] = csq
   else :
      csq = variables[var]
   return csq

# def create_question (var) :
#    "takes a string in the format 'Var'"
#    "and return a Variable object Variable"
#    return Variable(var)

def create_question (question_dic, variables) :
   ""
   # try :
   #    question_dic['connectors']
   if ('connectors' not in question_dic) :
      if (question_dic['expression'] not in variables) :
         question = Variable(question_dic['expression'])
         variables[question_dic['expression']]=question
      else :
         question = variables[question_dic['expression']]
      return question
   else :
      expressions = question_dic['expression']
      expr = []
      connector = question_dic['connectors']
      if connector == ou :
         for expression in expressions :
            expr.append(Expression(listToVars(parseAND(expression),variables),et))
         question = Question(expr, ou)
      elif connector == et :
         for expression in expressions :
            expr.append(Expression(listToVars(parseOR(expression), variables),ou))
         question = Question(expr, et)
      return question









def create_fb (list, variables) :
   "takes a list of antecedents in the format ['Var1', ..., 'VarN']"
   "and returns a list of Variable objects [Variable1, ..., VariableN]"
   fbList = []
   for varStr in list :
      if varStr not in variables :
         var = Variable(varStr)
         variables[varStr]=(var)
      else :
         var = variables[varStr]
      fbList.append(var)
   return fbList

def parseAntecedent(string) :
   "takes a string of antecedents in the format 'Var1 ∧ ... ∧ VarN'"
   " and returns a list ['Var1', ..., 'VarN']"

   return string.replace(" ","").split(et)

def parseAND(string) :
   "takes a string of antecedents in the format 'Var1 ∧ ... ∧ VarN'"
   " and returns a list ['Var1', ..., 'VarN']"

   return string.replace(" ","").split(et)


def parseOR(string) :
   "takes a string of antecedents in the format 'Var1 ∧ ... ∧ VarN'"
   " and returns a list ['Var1', ..., 'VarN']"

   return string.replace(" ","").split(ou)

# def parseParenthesisBis(string) :
#    "takes a question in a string format '((Q1∧Q2)vQ3)'"
#    " and returns I DON'T KNOW WHAT "

#    if "(" not in string :
#       return string
#    newString = ""
#    for caracter1 in string :
#       if caracter1 == '(' :
#          index = string.index(caracter1)
#          newString = string[index+1:]
#          #getting the string after the first parenthesis
#          for caracter2 in newString :
#             if caracter2 == '(':
#                string = newString
#                break
#             elif caracter2 == ')' :
#                return newString[:newString.index(caracter2)]
            
#    return "failed"

def parseQuestion(string) :
   insideParenthesis = []
   connectors = parseParenthesis(string, insideParenthesis)

   if not insideParenthesis :
      return {'expression':connectors}
   else :
      return {'expression':insideParenthesis, 'connectors':connectors}



def parseParenthesis(string, list) :
   ""

   if string == "" :
      return
   if "(" not in string :
      return string
   newString = ""
   for caracter1 in string :
      if caracter1 == '(' :
         index1 = string.index(caracter1)
         newString = string[index1+1:]
         #getting the string after the first parenthesis
         for caracter2 in newString :
            if caracter2 == ')' :
               index2 = string.index(caracter2)
               list.append(newString[:newString.index(caracter2)])
               return parseParenthesis(string[:index1] + string[index2+1:], list)
            
   return "failed"
   



#    string.split('; |, |\*|\n',a)

def parse_rule (rule, dict) :
   "takes a rule in the format [['Var1 ∧ ... ∧ VarN ', 'Consequence'], ... ]"
   "and returns a dictionnary {'antecedents':['Var1', ... , 'VarN'], "
   "                          'consequent' :  'Consequence' }"

   antecedentsString = rule[0]
   consequent = rule[1]
   
   antecedent = parseAntecedent(antecedentsString)
   
   dict['antecedents'] = antecedent
   dict['consequent'] = consequent
   
   return dict


def listToRule(listRule, variables) :
   "takes a rule in the format [['Var1 ∧ ... ∧ VarN ', 'Consequence']"
   "and returns a Rule object"

   parsedRule = parse_rule(listRule, {})
   ants = create_ant(parsedRule['antecedents'], variables)
   csq = createCsqObj(parsedRule['consequent'], variables)

   return Rule(ants, csq)

def listToVars(list, variables) :
   vars = []
   for varStr in list :
      if varStr not in variables :
         var = Variable(varStr)
         variables[varStr] = var
      else : 
         var = variables[varStr]
      vars.append(var)
   return vars


#----------------------tests-----------------

# var = "q^b"
# exp = Expression(var)
# print(exp.isSingle())

# chain = "(a∧b∧c)v(d∧e)"
# chain1 = "a"
# liste = []
# print(parseParenthesis(chain, liste))
# print (liste)


# a = Variable('A', True)
# b = Variable('B', True)
# c = Variable('C')
# d = Variable('D')

# expr1 = Expression([a,b],ou)
# expr2 = Expression([c,d],ou)

# question = Question([expr1,expr2], et)

# print(question.evaluate())

# print(parseAND('Var1 ∧ ... ∧ VarN'))

# print (create_question(parseQuestion("(A∨B)∧(C∨D)")))
# a = Variable('A')
# a.assign()
