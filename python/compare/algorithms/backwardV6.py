from collections import deque

import math
import pdb 

ON = "ON"
counter = 0
root = math.inf
on_list = []

def preTreatment (R, FB) :
    #print()
    #print("Execution ...")
    #print()
    for rule in R :
        rule.consequent.addRule(rule)
    for var in FB :
        var.assign()
        #print(str(var) + " TRUE ")

    # counter = 0
    # root = math.inf
    # on_list = []


    
def main(Q):
    stack = []
    
    if Q.evaluate() == None :
        OR(Q, stack)
        while stack:
            function, args = stack.pop()
            function(*args)

    if Q.isTrue() :
        return (True)
    else :
        return (False)
    



def OR(P, stack):
    global counter
    global root
    global on_list

    P.assign(ON)
    flag = None

    P.order = counter
    counter += 1

    for R in P.rules:
        output = AND(R, stack)

        if output == True:
            P.assign()

            INVERSE(P, stack)
            if P.order == root:
                assignFalse()
            return

        if output != False:
            for p in output:
                p.addSuccessor(R)
                if p.order < root:
                    root = p.order
            flag = True
            R.counter = len(output)
            on_list.append(P)

    if not flag:
        P.assign(False)
        if P.order == root:
            assignFalse()


def INVERSE(P, stack):
    for R in P.successors:
        R.counter -= 1
        if R.counter == 0:
            R.consequent.assign()
            if R.consequent.successors:
                INVERSE(R.consequent, stack)


def AND(R, stack):
    global on_list

    for p in R.antecedents:
        if p.isTrue3():
            continue
        if p.evaluate() == None:
            stack.append((OR, (p, stack)))
        if p.evaluate() == False:
            return False
        if p.evaluate() == ON:
            R.addSuccessor(p)

    if not R.successors:
        return True

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


