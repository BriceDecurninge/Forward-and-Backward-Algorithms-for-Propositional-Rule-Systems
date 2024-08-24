from classes import *

# implementation of fordward chaining algorithm with squared complexity

# entry :
#  - FB : a list of True variables (fact base)
#  - R : a system of rules
#  - Q : a variable of which we must determine the value

# exit :
#     - A : a boolean which value is True if the algorith succeded to determine the value of Q 
#                                 and Fake otherwise
#           that's to says, return true if Q is a LOGICAL CONSEQUENCE of the fact base


def FordwardAlgorithmSteps2 (FB, R, Q) :
    print()
    print("Execution ...")
    print()

    for variable in FB :
        variable.assign()    

    newFB = FB.copy()
    while (True) :
        for rule in R :
            if not rule.consequent.isTrue() : 
                allTrue = True  
                for ant in rule.antecedents :
                    if not ant.isTrue() : 
                        allTrue = False
                if allTrue : 
                    csq = rule.consequent
                    csq.assign()  
                    print(str(csq) + " deduced with rule : " + str(rule))

            
        if (areTheSame(FB,newFB)) :
            print("No more variable found")
            print()
            break
        else : 
            FB = newFB.copy()
            

    return Q.evaluate()

def FordwardAlgorithm2 (FB, R, Q) :

    for variable in FB :
        variable.assign()    

    newFB = FB.copy()
    while (True) :
        for rule in R :
            if not rule.consequent.isTrue() : 
                allTrue = True  
                for ant in rule.antecedents :
                    if not ant.isTrue() : 
                        allTrue = False
                if allTrue : 
                    csq = rule.consequent
                    csq.assign()  

            
        if (areTheSame(FB,newFB)) :
            break
        else : 
            FB = newFB.copy()
            

    return Q.evaluate()



def areTheSame (l1, l2) :
    for e1 in l1 :
        if e1 not in l2 :
            return False
    for e2 in l2 :
        if e2 not in l1 :
            return False
    return True


