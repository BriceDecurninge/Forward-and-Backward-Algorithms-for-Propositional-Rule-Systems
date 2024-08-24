import classes
from random import *
from memory_profiler import profile

# here is where the set of examples are created

# the data is stored as below :

#         the rules are in a list that itself contains a list for each rule :
#                                           the first element is a string of antecededents
#                                           the second element is a string of the consequent
#         the question is a string 
#         the facts base is a list of string 

#         example : 
#         rules = [['A4∧A3∧P3∧P5', 'Z2'], ['A4∧A1∧Z5∧P3', 'A1'], ['A5∧A2∧Z4∧Z3∧Z5', 'A4'], ['Z1∧A4∧Z4', 'P5'], ['P1∧Z3∧A3', 'A1'], ['A2∧Z2∧P3∧P4', 'P4'], ['A1∧Z3∧P3∧A4∧P2', 'P2'], ['A2', 'P3'], ['P1', 'A2'], ['A5∧A4∧A1∧Z5∧P3', 'Z5']]
#         question = Z2
#         facts base = ['A1', 'A3', 'P3', 'P2', 'Z4', 'P1', 'Z2', 'P4', 'Z1', 'A5']
    
# then several elements are created and stored in a set that is structured like this :

#         each element is a dictionary than contain many fileds :
#         "rules" : which coresponds to the rules above
#         "question" : which coresponds to the question above
#         "facts base" : which coresponds to the facts base above

#         example of a 3-elements set : 

#        [
#            {'rules': [['A1∧Z3∧Z2', 'A3']],
#              'question': 'Z5', 
#                 'facts base': ['A5', 'A4', 'P5', 'P2', 'Z1', 'A2', 'Z5']},
#            {'rules': [['A4∧Z5∧A2', 'P4'], ['Z1∧Z5∧Z2', 'Z4'], ['Z2∧P2∧A5', 'A1'], ['A3∧P5∧Z2∧Z5∧Z4', 'P2']],
#              'question': 'A5',
#                'facts base': ['A5', 'Z4', 'A2', 'A1', 'A4']},
#            {'rules': [['Z4∧A3', 'A4']],
#              'question': 'P2',
#                'facts base': ['A1', 'A2', 'P4', 'P1', 'Z5']}
#         ]



et = "∧"
implique = "=>"


maxRulesNumberDefault = 5
maxLengthAntecedentsDefault = 3
maxLengthFactsBaseDefault = 10
maxLengthDataBaseDefault = 30
symbolDefault = et
variableBaseDefault = ['P1', 'P2', 'P3', 'P4', 'P5', 'A1', 'A2', 'A3', 'A4', 'A5', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5']

def generateRules (listOfVariable, symbol, maxRulesNumber=maxRulesNumberDefault, maxLengthAntecedents=maxLengthAntecedentsDefault) :
    rules = []
    rulesNumber = randint(1,maxRulesNumber)
    for i in range (rulesNumber) :
        antecedents = generateAntecedents(listOfVariable, symbol, maxLengthAntecedents)
        consequent = generateConsequent(listOfVariable)
        rules.append([antecedents, consequent])
   
    return rules

def generateRulesBenchmark1(k, n=1, variableBase=[]) :
    rules = []
    for i in range (k) :
        for j in range (n) :
            antecedent = "P" + str(j) +"." + str(i)
            consequent = "P" + str(j+1) +"." + str(i)
            rules.append([antecedent, consequent])
            variableBase.append(antecedent)
            variableBase.append(consequent)
   
    return rules

def generateRulesBenchmark2(k, n=1, variableBase=[]) :
    rules = []
    for i in range (n-1) :
        liste1 = []
        liste2 = []
        for j in range (k) :
            antecedent = "P" + str(i)
            consequent = "P" + str(i) +"." + str(j)
            liste1.append([antecedent, consequent])
            antecedent_bis = consequent
            consequent_bis = "P" + str(i+1)
            liste2.append([antecedent_bis, consequent_bis])
            if antecedent not in variableBase :
                variableBase.append(antecedent)
            variableBase.append(consequent)
            variableBase.append(consequent_bis)
        liste = liste1 + liste2
        rules += liste
   
    return rules

def generateRulesBenchmark3(k, oriented) :
    rules = []
    for i in range (k) :
        antecedent = "P" + str(i)
        if oriented :
            for j in range (i+1,k) :
                consequent = "P" + str(j)
                rules.append([antecedent, consequent])
                
        else :
            for j in range (k) :
                if i != j :
                    consequent = "P" + str(j)
                    rules.append([antecedent, consequent])
                    

    return rules

def generateRulesBenchmark4(k,variableBase=[], symbol=symbolDefault) :
    rules = []
    for i in range (1,k) :
        antecedents = ""
        for j in range (i+1, k+1) :
            antecedent = "P" + str(j)
            antecedents += antecedent
            if j < k :
                antecedents += " " + symbol + " "
            if antecedent not in variableBase :
                        variableBase.append(antecedent)
        consequent = "P" + str(i)
        if consequent not in variableBase :
                        variableBase.append(consequent)
        rules.append([antecedents, consequent])

    return rules

def generateRulesBenchmark5(k, n, variableBase=[]) :
    rules = []
    for i in range(1,n+1) :
        index = 0
        for j in range(0, k**i, k) :
            antecedent = "P" + str(i) + "." + str(index)
            if antecedent not in variableBase :
                        variableBase.append(antecedent)
            for l in range(k) :
                consequent = "P" + str(i+1) + "." + str(j+l)
                if consequent not in variableBase :
                        variableBase.append(consequent)
                rules.append([antecedent, consequent])
            index += 1
    
    return rules


def generateConsequent(listOfConsequents) :
    consequent = choice(listOfConsequents)
    #print ("csq from generateConsequent() : " + consequent)
    return consequent

def generateAntecedents(listOfAntecedents, symbol, maxLength=maxLengthAntecedentsDefault) :
    antecedents = ""
    length = randint(1,maxLength)
    for i in range (length) :
        antecedents += str(choice(listOfAntecedents))
        if i < length-1 :
            antecedents += " " + symbol + " "
        #print ("ant from generateAntecedent() : " + antecedents)
    return antecedents
            
def generateFB(listOfVariable, maxLength=maxLengthFactsBaseDefault) :
    FactsBase = []
    listOfVariableBis = listOfVariable.copy()
    length = randint(1, min(len(listOfVariable),maxLength)) 
    for i in range (length) : 
        variable = choice(listOfVariableBis)
        FactsBase.append(variable)
        listOfVariableBis.remove(variable)
    return FactsBase

def generateFBBenchmark(rules, n, benchmark) :
    FactsBase = []
    if benchmark == 1 :
        for rule in range (0, len(rules), n ) :
            FactsBase.append(rules[rule][0])
    elif benchmark == 2:
        if len(rules) > 0 :
            FactsBase.append(rules[0][0])
    elif benchmark == 3 :
        if len(rules) > 0 :
            FactsBase.append(rules[0][0])
    elif benchmark == 4 :
         length = len(rules)
         if len(rules) > 0 :
            FactsBase.append(rules[length-1][0])
    elif benchmark == 5 :
          length = len(rules)
          if len(rules) > 0 :
               FactsBase.append(rules[0][0])
         
    
    return FactsBase

def generateQuestion(listOfQuestions,cheat=False) :
    if len(listOfQuestions) < 1 :
        return
    question = choice(listOfQuestions)
    if cheat :
        question=cheat[len(cheat)-1]
    return question

def generateListOfVariables(letters, integers, maxlength=maxLengthDataBaseDefault, length =None) :
    if length is None :
        length = randint(1,maxlength)
    variables = []
    
    for i in range (length) :
        variable = choice(letters) + choice(integers)
        while (variable in variables) :
            variable = choice(letters) + choice(integers)
        variables.append(variable)

    return variables


def generateSet(elementsNumber, variableBase=variableBaseDefault, maxRulesNumber=maxRulesNumberDefault, maxLengthAntecedents=maxLengthAntecedentsDefault, maxLengthFactsBase=maxLengthFactsBaseDefault, maxLengthDataBase=maxLengthDataBaseDefault,symbol=symbolDefault) :
    set = []

    for i in range (elementsNumber) :
        element = {}
        element["rules"]= generateRules(variableBase, symbol, maxRulesNumber, maxLengthAntecedents)
        element["question"]= generateQuestion(variableBase)
        element["facts base"]= generateFB(variableBase,maxLengthFactsBase)
        set.append(element)
    return set

#@profile
def generateBenchmark(k, n=1, benchmark=1, variableBase=[], oriented=False) :
    set = []
    element = {}
    if benchmark == 1 :
        element["rules"]= generateRulesBenchmark1(k, n, variableBase)
        element["facts base"]= generateFBBenchmark(element["rules"], n, 1)
    elif benchmark == 2 :
        element["rules"]= generateRulesBenchmark2(k, n, variableBase)
        element["facts base"]= generateFBBenchmark(element["rules"], n, 2)
        #element["facts base"]= []
    elif benchmark == 3 :
        element["rules"]= generateRulesBenchmark3(k, oriented, variableBase)
        element["facts base"]= generateFBBenchmark(element["rules"], n, 3)
    elif benchmark == 4 :
         element["rules"]= generateRulesBenchmark4(k, variableBase)
         element["facts base"]= generateFBBenchmark(element["rules"], n, 4)
    elif benchmark ==  5 :
         element["rules"]= generateRulesBenchmark5(k, n, variableBase)
         element["facts base"]= generateFBBenchmark(element["rules"], n, 5)
    element["question"]= generateQuestion(variableBase, cheat=variableBase)


    
    set.append(element)
    return set

'''
Le problème est que générate data génère les JSON plutot que
les benchmarks en eux même.
les fonctions generateRulesBenchmark et generateFBBenchmark
se basent sur des strings plutot que les objets en eux même
ce qui n'est pas correct.
En effet, pour que certains algorithmes fonctionnent nottament
le forward lineaire et backward, il faut que la BF possède
certains antécédents de rules. Il faut que les faits référencent
les antécédents de règles. Il ne faut pas uniquement que le fait
soit une meme string que l'antécédent.

'''
def generateFBBenchmark1(rules, n, benchmark) :
    FactsBase = []
    if benchmark == 1 :
        for rule in rules :
            FactsBase.append(rule.consequent)
    return FactsBase

def generateRulesBenchmark1B(k, n=1, variableBase=[]) :
    rules = []
    for i in range (k) :
        for j in range (n) :
            antecedent = classes.Variable("P" + str(j) +"." + str(i))
            consequent = classes.Variable("P" + str(j+1) +"." + str(i))
            rules.append(classes.Rule([antecedent], consequent))
            variableBase.append(antecedent)
            variableBase.append(consequent)
   
    return rules