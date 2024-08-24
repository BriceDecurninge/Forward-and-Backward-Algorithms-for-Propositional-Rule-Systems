import math

on = "ON"

def preTreatment (R, FB) :
    for rule in R :
        rule.consequent.addRule(rule)
    for var in FB :
        var.assign()

def OR(P) :

    P.assign(on)
    flag = None
    for R in P.rules :
        output = AND(R)

        if output == True :
            P.assign()
            INVERSE(P)
            return()
        
        if output != False :
            for p in output :
                p.addSuccessor(R)
                # add R to p.successors
            flag = True

    if not flag :
        P.assign(False)
    
    return


def INVERSE(P) :
    for R in P.successors :
        allTrue = True
        for antecedent in R.antecedents :
            if not antecedent.isTrue() :
                allTrue = False
                break
        if allTrue :
            R.consequent.assign()
            if R.consequent.successors :
                INVERSE(R.consequent)
        


def AND(R) :
    for p in R.antecedents :
        if p.isTrue3() :
            continue
        if p.evaluate() == None :
            OR(p)
        if p.evaluate() == False :
            return (False)
        if p.evaluate() == on :
            R.addSuccessor(p)
            # add p to R.successors
            

    if not R.successors :
        return (True)
    
    return R.successors

