import json

#this program aim is to print the several datasets created in generate.py so a human can easily read it

implique = "=>"


def JsonToPrint(path_json, vb=None) :

    with open(path_json, "r") as file:
        jsonSet = json.load(file)
    file.close() 

    if vb :
        print("Variables Base : " + printDB(vb))
    length = len(jsonSet)
    for i in range (length) :
        printElement(jsonSet[i])
        print("")
    
    return

def generationToPrint(set,vb=False, benchmark=False, k=False, n=False, orientation=False) :
    if vb :
        print("Variables Base : " + printDB(vb))
    length = len(set)
    if not benchmark or benchmark == 4 :
        for i in range (length) :
            printElement(set[i])
            print("")

    elif benchmark == 1 :
        for i in range (length) :
            printElementBenchmark1(set[i],k, n)
            print("")

    elif benchmark == 2 :
        for i in range (length) :
            printElementBenchmark2(set[i],k, n)
            print("")

    elif benchmark == 3 :
        for i in range (length) :
            printElementBenchmark3(set[i],k, orientation)
            print("")

    elif benchmark == 5 :
        for i in range (length) :
            printElementBenchmark5(set[i],k,n)
            print("")

    return


def printElement(element) :
    rules = element["rules"]
    question = element["question"]
    fb = element["facts base"]

    print ("Rules : ")
    for rule in rules :
        print(printRule(rule))
    print ("Facts Base : " + printDB(fb))
    if question :
        print ("Question : " + question)

def printElementBenchmark1(element, k, n) :
    rules = element["rules"]
    question = element["question"]
    fb = element["facts base"]

    print ("Rules : ")
    lenRules = len(rules)
    shift = len(str(lenRules))
    string = ""
    for rule in range (0, len(rules), n ) :
        string = ""
        for i in range (n) :
            raw = rule//n
            length = len(str(raw))
            string += (printRule(rules[rule + i])) + "    "
            decalage = shift-length
            string += "  "*decalage
        print (string)
    print ("Facts Base : " + printDB(fb))
    print ("Question : " + question)


def printElementBenchmark2(element, k, n) :
    rules = element["rules"]
    question = element["question"]
    fb = element["facts base"]
    
    print ("Rules : ")  
    lenRules = len(rules)
    print("nb regles : " + str(lenRules))
    shift = len(str(k))
    string = ""
    for rule in range (k) :
        string = ""
        for i in range (2*n-2) :
            raw = rule
            length = len(str(raw))
            string += (printRule(rules[k*i + rule])) + "    "
            decalage = shift-length
            string += " "*decalage

        print (string)
    print ("Facts Base : " + printDB(fb))
    print ("Question : " + str(question))

def printElementBenchmark3(element, k, oriented = False) :
    rules = element["rules"]
    question = element["question"]
    fb = element["facts base"]
    
    print ("Rules : ")  
    lenRules = len(rules)
    
    if oriented :
        counter1 = k - 1
        counter2 = 0
        for i in range (k) :
            while counter1  :
                string = ""
                for i in range(counter1) : 
                    string += (printRule(rules[counter2])) + "   "
                    counter2 += 1
                counter1 -= 1
                print (string)     

    else :
        for i in range (0, lenRules, k) :
            string = ""
            for j in range (k) :
                string += (printRule(rules[i + j])) + "   "
            print (string) 

    print ("Facts Base : " + printDB(fb))
    print ("Question : " + str(question))

def printElementBenchmark5(element, k, n) :
    rules = element["rules"]
    question = element["question"]
    fb = element["facts base"]

    print ("Rules : ")  
    lenRules = len(rules)

    compteur = 0
    for i in range(1,n+1) :
        for j in range(k**i) :
            if compteur < len(rules):
                print(printRule(rules[compteur]))
                compteur += 1

        print()

    print ("Facts Base : " + printDB(fb))
    print ("Question : " + str(question))



def printDB(db) :
    factsBase =""
    length = len(db)
    for i in range (length) :
        factsBase += db[i]
        if i < length-1 :
            factsBase += ", "
    return factsBase

def printRule(rule) :
    antecedants = rule[0]
    consequent = rule[1]
    ruleString = antecedants + " " + implique + " " + consequent
    return ruleString

