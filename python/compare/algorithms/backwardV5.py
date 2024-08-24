import math
import sys

ON = "ON"
counter = 0
root = math.inf
on_list = []

global size


class SizeTracker:
    def __init__(self):
        self.cumulative_size = 0

    def track_size(self, obj):
        self.cumulative_size += sys.getsizeof(obj)

    def get_cumulative_size(self):
        return self.cumulative_size




def pre_processing (rules, facts_base) :
    
    for rule in rules :
        rule.consequent.addRule(rule)
    for var in facts_base :
        var.assign()

    
def main(Q):

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
    flag = None

    P.order = counter #fonction ?
    counter += 1

    for R in P.rules :
        output = AND(R)

        if output == True :
            P.assign()
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

        if P.order == root :
            assignFalse()
    



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


### FUNCTIONS TO TEST MEMORY USAGE OF BACKWARD ALGORITHM ##""

def test_main(Q,size_tracker):

    if Q.evaluate() == None :
        test_OR(Q,size_tracker)

    if Q.isTrue() :
        return (True)
    else :
        return (False)

def test_OR(P,size_tracker):
    global counter, root, on_list


    P.assign(ON)
    flag = None

    P.order = counter
    counter += 1

    # Measure size of local variables
    size_counter = sys.getsizeof(counter)
    size_root = sys.getsizeof(root)
    size_on_list = sys.getsizeof(on_list)
    size_P = sys.getsizeof(P)
    size_f = sys.getsizeof(flag)
    size_tracker.track_size(size_f)

    # Print sizes or do further processing
    print(f"Size of counter: {size_counter} bytes")
    print(f"Size of root: {size_root} bytes")
    print(f"Size of on_list: {size_on_list} bytes")
    print(f"Size of P: {size_P} bytes")

    for R in P.rules:
        output = test_AND(R,size_tracker=size_tracker)
        size_o = sys.getsizeof(output)
        size_tracker.track_size(size_o)


        print(f"Size of flag: {size_f} bytes")
        print(f"Size of output: {size_o} bytes")



        if output == True:
            P.assign()
            INVERSE(P)
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

    return

def test_AND(R,size_tracker):
    global on_list

    # Measure size of local variables
    size_on_list = sys.getsizeof(on_list)
    size_R = sys.getsizeof(R)

    # Print sizes or do further processing
    print(f"Size of on_list: {size_on_list} bytes")
    print(f"Size of R: {size_R} bytes")

    for p in R.antecedents:
        if p.isTrue3():
            continue
        if p.evaluate() == None:
            test_OR(p,size_tracker=size_tracker)
        if p.evaluate() == False:
            return False
        if p.evaluate() == ON:
            R.addSuccessor(p)

    if not R.successors:
        return True

    return R.successors



   
def main_steps(Q):

    if Q.evaluate() == None :
        OR_steps(Q)

    if Q.isTrue() :
        return (True)
    else :
        return (False)
    


### FUNCTION TO PRINT ALGORITHM STEPS ###

def OR_steps(P) :
    global counter
    global root
    global on_list

    print ("OR " + str(P))
    P.assign(ON)
    #print(str(P) + " ON ")
    flag = None

    P.order = counter #fonction ?
    counter += 1

    if P.rules == [] :
        print("c'est vide batard")

    for R in P.rules :
        output = AND_steps(R)

        if output == True :
            P.assign()
            print(str(P) + " TRUE ")
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
        print(str(P) + " FALSE ")

        if P.order == root :
            assignFalse()
    
def AND_steps(R) :
    print("AND" + str(R))
    global on_list

    for p in R.antecedents :
        if p.isTrue3() :
            continue
        if p.evaluate() == None :
            OR_steps(p)
        if p.evaluate() == False :
            return (False)
        if p.evaluate() == ON :
            R.addSuccessor(p)
            # add p to R.successors
            

    if not R.successors :
        return (True)
    
    return R.successors
