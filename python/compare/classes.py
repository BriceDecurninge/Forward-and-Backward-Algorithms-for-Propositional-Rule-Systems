

ou = "∨"
et = "∧"
implique = "=>"
expr = "expression"

class Question :
   """a question is made of one or several expressions, and connectors (if there are several expressions)
    (a1∧a2)∨(b1∧b2) -> quest : expr = [a1∧a2,b1∧b2], connector = '∨'"""

   def __init__ (self, expressions=[], connector = None):
      self.expressions = expressions
      self.connector = connector

   def __str__ (self) :
      string = ""
      for i in range (len(self.expressions)) :
         string += "(" + str(self.expressions[i]) + ") "
         if i + 1 < len(self.expressions) :
            string += self.connector + " "
      return string
   
   def evaluate(self) :
      value = None
      if self.connector == et :
         value = True
         for expr in self.expressions :
            value = value and expr.evaluate()
      elif self.connector == ou :
         for expr  in self.expressions :
            value = value or expr.evaluate()
      elif self.connector == None :
         value = (self.expressions[0]).evaluate()
      return value

class Expression :
   """an expression is made of variable(s) and connectors
   a∧b∧c -> expr : var = [a,b,c], connector = '∧'"""

   def __init__ (self, variables, connector=None):
      self.vars = variables
      self.connector = connector
   
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
      for i in range (len(self.vars)) :
         string += str(self.vars[i]) + " "
         if i + 1 < len(self.vars) :
            string += self.connector + " "
      return string

class Rule :
    """a Rule, in our case, is made of antecedent(s), connectors, and a single consequent
    a∧b=>c -> rule : antecedents = [a,b], connector = '=>', consequent = c"""

    def __init__(self, antecedents, consequent, counter = 0):
        self.antecedents = antecedents
        self.connector = implique
        self.consequent = consequent
        self.counter = counter
        self.successors = []
    
    def reset (self):
       self.counter = 0
       self.successors.clear()


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
    
    def addSuccessor(self, successor) :
       self.successors.append(successor)
     
class Variable :
    """a variable is a string linked to a boolean value : True or False
    A -> variable : name = 'A', value = False (default)"""
   
    def __init__ (self, name, value=None) :
      self.name = name
      self.value = value
      self.rules = []
      self.used = False
      self.known = False
      self.successors = []
      self.order = None


    def reset(self) :
        self.value = None
        self.rules.clear()
        self.used = False
        self.known = False
        self.successors.clear()
        self.order = None
   
    def reset_ant(self) :
        self.value = None
        self.used = False
        self.known = False
        self.successors.clear()
        self.order = None
    
    
  
    def __eq__(self, other):
      return self.name == other.name
    
    def __str__(self) :
      description = self.name
      
      description += " (" + str(self.value) +")"
      return description

    def assign(self, bool=True) :
      self.value = bool
   
    def isTrue (self) :
      return self.value
    
    def isTrue3 (self) :
       return self.value is True
   
    def evaluate (self) :
      return self.value
    
    def use(self) :
       self.used = True

    def isUsed(self) :
       return self.used
    
    def addRule(self, rule) :
       (self.rules).append(rule)
       
    
    def know(self, value=True) :
       self.known = True
       self.value = value
   
    def isKnown(self) :
       return self.known
   
    def addSuccessor(self, successor) :
       self.successors.append(successor)
    



# parsing the dictionnary from the JSON to an adapted format
# JSON dictionnary : 
# {'rules': [['Var1 ∧ ... ∧ VarN ', 'Consequence'], ... ], 
# 'question': 'Question', 
# 'facts base': ['Var31', ... 'Var40']}

# then will become :
# {'rules': [ Rule1, Rule2, ... ], 
# 'question': Question
# 'facts base': [Variable1, ..., VariableN]}

#     example :
# {'rules': [['A2 ∧ P2 ∧ Z3 ∧ A5', 'P4'], ['A2 ∧ Z5 ∧ P4', 'Z2'], ['P2 ∧ A2 ∧ Z1 ∧ A2', 'P3'], ['A2 ∧ Z4', 'Z5'], ['Z2 ∧ Z4 ∧ P2 ∧ P1 ∧ P1', 'P2'], ['P2', 'Z2']], 
# 'question': 'Z1', 
# 'facts base': ['P5', 'Z5', 'A4', 'A1', 'A2', 'A3', 'P1', 'A5', 'Z4', 'P2']}



def createSet (JSONobject) :
   """create an entire set based on json data"""
   variables = {}
   dictionnaire = {}          # FB, R, Q
   rules = JSONobject['rules']
   fb = JSONobject['facts base']
   question = JSONobject['question']
   
   rulesParsed = []
   for rule in rules :
      rulesParsed.append(listToRule(rule, variables))
   dictionnaire['rules'] = rulesParsed
   dictionnaire['facts base'] = createFBObj(fb, variables)
   dictionnaire['question'] = createQObj(parseQuestion(question), variables)
   return dictionnaire

def createSet2 (set) :
   bench = set[0]

   """create an entire set based on json data"""
   variables = {}
   dictionnaire = {}          # FB, R, Q
   rules = bench['rules']
   fb = bench['facts base']
   question = bench['question']
   
   rulesParsed = []
   for rule in rules :
      rulesParsed.append(listToRule(rule, variables))
   dictionnaire['rules'] = rulesParsed
   dictionnaire['facts base'] = createFBObj(fb, variables)
   dictionnaire['question'] = createQObj(parseQuestion(question), variables)
   
   return dictionnaire


def createAntObj (list, variables) :
   """takes a list of antecedents in the format ['Var1', ..., 'VarN']
   and returns a list of Variable objects [Variable1, ..., VariableN]
   board effects : it stores these variables in the dictionary variables"""
   
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
   """takes a string in the format 'Var'
   and return a Variable object Variable"""

   if var not in variables :
      csq = Variable(var)
      variables[var] = csq
   else :
      csq = variables[var]
   return csq

def createQObj (question_dic, variables) :
   """takes a question in dictionnary format and return a question object """
  
   if ('connectors' not in question_dic) :
      # the question is just a variable
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
         # the question in a disjunction of conjunctions
         for expression in expressions :
            # expr.append(Expression(listToVars(parseAND(expression),variables),et))
            expr.append(Expression(listToVars(parseConnector(expression,et),variables),et))

      elif connector == et : 
         # the question is a conjunction of disjunctions
         for expression in expressions :
            expr.append(Expression(listToVars(parseConnector(expression,ou), variables),ou))

      elif connector == None :
         # the question is a disjunction or a conjunction of simple variables
         expression = expressions[0]
         if ou in expression :
            expr.append(Expression(listToVars(parseConnector(expression,ou), variables),ou))
         elif et in expression :
            expr.append(Expression(listToVars(parseConnector(expression,et), variables),et))

      question = Question(expr, connector)
      return question

def createFBObj (list, variables) :
   """takes a list of antecedents in the format ['Var1', ..., 'VarN']
   and returns a list of Variable objects [Variable1, ..., VariableN]"""
   
   fbList = []
   for varStr in list :
      if varStr not in variables :
         var = Variable(varStr)
         variables[varStr]=(var)
      else :
         var = variables[varStr]
      fbList.append(var)
   return fbList

def parseAND(string) :
   "takes a string of antecedents in the format 'Var1 ∧ ... ∧ VarN'"
   " and returns a list ['Var1', ..., 'VarN']"

   return string.replace(" ","").split(et)

def parseOR(string) :
   "takes a string of antecedents in the format 'Var1 ∧ ... ∧ VarN'"
   " and returns a list ['Var1', ..., 'VarN']"

   return string.replace(" ","").split(ou)

def parseConnector(string, connector) :
   """takes a string of antecedents in the format 'Var1 connector ... connector VarN'"
    and returns a list ['Var1', ..., 'VarN']"""
   
   return string.replace(" ","").split(connector)


def parseQuestion(string) :
   """takes a question in the format 'Var' : (case1), '(a1∨a2)∧(b1∨b2)' or '(a1∧a2)∨(b1∧b2)' : (case2), or '(a1∧a2)' : (case3)
      and returns a dictionnary {'expression':'Var'} :                                     case1
                                {'expression': ['(a1∨a2)','(b1∨b2)'], 'connector' : '∧'} : case2
                                {'expression': ['(a1∨a2)'], 'connector' : None}            case3   """

   insideParenthesis = []
   connectors = parseParenthesis(string, insideParenthesis)

   if not insideParenthesis :
      return {'expression':connectors}
   else :
      return {'expression':insideParenthesis, 'connectors':connectors}

def parseParenthesis(string, list) :
   """recursive function that get what is inside parenthesis whitin a string, put it in a list given in paramter,
     and return what is outside the parenthesis. 
      ex : parseParenthesis("(a1∨a2)∧(b1∨b2)", list=[]) returns ∧; list is now ['a1∨a2','b1∨b2']"""

   if string == "" or string == None:
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
   #in case there is a problem        
   return "failed"
   
def parseRule (rule, dict={}) :
   """takes a rule in the format [['Var1 ∧ ... ∧ VarN ', 'Consequence'], ... ]
   and returns a dictionnary {'antecedents':['Var1', ... , 'VarN'], 
                             'consequent' :  'Consequence' }"""

   antecedentsString = rule[0]
   consequent = rule[1]
   
   antecedent = parseConnector(antecedentsString, et)
   
   dict['antecedents'] = antecedent
   dict['consequent'] = consequent
   
   return dict

#Brice : verified
def listToRule(listRule, variables) :
   """takes a rule in the format ['Var1 ∧ ... ∧ VarN ', 'Consequence']
   and returns a Rule object"""

   parsedRule = parseRule(listRule) # dico
   ants = createAntObj(parsedRule['antecedents'], variables)
   csq = createCsqObj(parsedRule['consequent'], variables)

   return Rule(ants, csq)

def listToVars(list, variables) :
   """ convert a list of string into a list of variable objects"""
   
   vars = []
   for varStr in list :
      if varStr not in variables :
         var = Variable(varStr)
         variables[varStr] = var
      else : 
         var = variables[varStr]
      vars.append(var)
   return vars


