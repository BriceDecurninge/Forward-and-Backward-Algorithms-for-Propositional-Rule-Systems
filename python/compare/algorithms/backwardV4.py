import math
ON = "ON"
counter = 0
root = math.inf
on_list = []

def preTreatment (R, FB, Q) :
    for rule in R :
        rule.consequent.addRule(rule)
    for var in FB :
        var.assign()
        #print(str(var) + " TRUE ")


    if Q.evaluate() == None :
        OR(Q)

    if Q.isTrue() :
        return (True)
    else :
        return (False)
    


def OR(P) :
    global counter
    global root
    global on_list


    P.assign(ON)
    #print(str(P) + " ON ")
    flag = None

    P.order = counter #fonction ?
    counter += 1

    for R in P.rules :
        output = AND(R)

        if output == True :
            P.assign()
            #print(str(P) + " TRUE ")
            INVERSE(P)
            if P.order == root :
                assignFalse()
            return()
        
        if output != False :
            for p in output :
                p.addSuccessor(R)
                if p.order < root :
                    root = p.order
            flag = True
            R.counter = len(output)
            on_list.append(P)
            

    if not flag :
        P.assign(False)
        #print(str(P) + " FALSE ")

        if P.order == root :
            assignFalse()
    
    return


def INVERSE(P) :
    for R in P.successors :
        R.counter -= 1
        if R.counter == 0 :
            R.consequent.assign()
            if R.consequent.successors :
                INVERSE(R.consequent)
        


def AND(R) :
    global on_list

    for p in R.antecedents :
        if p.isTrue3() :
            continue
        if p.evaluate() == None :
            OR(p)
        if p.evaluate() == False :
            return (False)
        if p.evaluate() == ON :
            R.addSuccessor(p)
            # add p to R.successors
            

    if not R.successors :
        return (True)
    
    return R.successors

def assignFalse() :
    global counter
    global root
    global on_list

    for p in on_list :
        if p.value == ON :
            p.assign(False)
            #print(str(p) + " FALSE ")
    on_list = []
    counter = 0
    root = math.inf


