#implementation of fordward chaining algorithm with linear complexity

# entry :
#  - facts_base : a list of True variables (fact base)
#  - rules: a system of rules
#  - Q : a variable of which we must determine the value

# exit :
#     - A : a boolean which value is True if the algorith succeded to determine the value of Q 
#                                 and Fake otherwise
#           that's to says, return true if Q is a LOGICAL CONSEQUENCE of the fact base

from memory_profiler import profile

'''
Note Brice : Algorithm is correct except for the question returned
at the end of for loop

Need to ensure that variable.rules and rule.count are well initialized

'''

def forward_algorithm_steps (facts_base, question) :
    print()
    print("Execution ...")
    print()
    for variable in facts_base :
        print ("fact " + variable.name + " is being processed ")
        #We ensure that all facts are True
        variable.assign()
        if not variable.isUsed() :
            for rule in variable.rules :
                print ("rule " + str(rule) + " is being processed")
                rule.counter -= 1
                if rule.counter == 0 :
                    consequent = rule.consequent
                    print(str(consequent) + " deduced with rule : " + str(rule))
                    consequent.assign()
                    if consequent.__eq__(question) :
                        print ("Question find brice")
                        return question.evaluate
                    facts_base.append(consequent)
            variable.use()

    print("No more variable found")
    print()

    #Should not be here
    return question.evaluate()



'''
Note Brice: Forward algorithm is correct with the condition that
all facts in BF reference the same object as Brulesantecedents.

If not, it means that the facts do not know the rules they are in
(fact.rules is empty) because the preTreatment only add rules to
antecedents and not the facts (antecedent.addRule(rule))

'''



def pre_processing (facts_base,rules) :
    for rule in rules :
        for antecedent in rule.antecedents :
            rule.counter += 1
            antecedent.addRule(rule)
    for variable in facts_base :
        variable.assign()
    return facts_base    

def forward_algorithm (facts_base, question) :
    for variable in facts_base :
        if variable.used == False :
            for rule in variable.rules :
                rule.counter -= 1
                if rule.counter == 0 :
                    if rule.consequent.name == question.name :
                        return True
                    facts_base.append(rule.consequent)
            variable.used = True

    return False




def pre_processing3 (rules) :
    for rule in rules:
        for antecedent in rule.antecedents :
            rule.counter += 1
            antecedent.addRule(rule)



    
def pre_processing_steps3 (rules) :
    for rule in rules:
        for antecedent in rule.antecedents :
            print (" rule "+ str(rule) + " added to " + str(antecedent))
            rule.counter += 1
            antecedent.addRule(rule)

def forward_algorithm3 (facts_base, question) :
    for variable in facts_base :
        variable.assign()
        if not variable.isUsed() :
            for rule in variable.rules :
                rule.counter -= 1
                if rule.counter == 0 :
                    consequent = rule.consequent
                    consequent.assign()
                    if consequent.__eq__(question) :
                        #print ("Question find brice")
                        return question.evaluate
                    facts_base.append(consequent)
            variable.use()

    return question.evaluate()



