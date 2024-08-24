import generateData
import toPrint
import toJSON
import string
from memory_profiler import profile
#number of sets that will be created, each one is stored in a different file
numberOfSets = 1

#number of elements in a single set
numberOfElements = 10

#the maximum number of rules an element could contain
maxNumberOfRules = 7

#the maximum number of antecedents a rule could contain
maxNumberOfAntecedents = 5

#the maximum number of variable a facts base could contain
#   if the number is greater than the length of the variable base, then it is set to its length
FactsBaseMaxLength = 25

#the maximum number of variables the database used to create rules could contain
DataBaseMaxLength = 30



#the letters that will be used to create the variables within the rules
strings = string.ascii_uppercase[13:] #from M to Z
#str = string.ascii_uppercase #from A to Z

#the numbers that will be used to create the variables within the rules
integ = string.digits #from 0 to 9
variableBase = generateData.generateListOfVariables(strings,integ, length=10)

#the directory where the files will be stored
dirName = "data/benchmark1/"


# k :
# number of rows of the benchmark

# n :
# number of columuns of the benchmark

def create_benchmark( k, n, stored=dirName, show=False) :

    for i in range (numberOfSets) :
        set = generateData.generateBenchmark(k, n, 1, variableBase=[])
        name = dirName +"bench" + str(i)
        toJSON.store(set,name)
        del set
        gc.collect()
        if show :
            print()
            print()
            print ("----------------------- " + name + " -----------------------" )
            print()
            toPrint.generationToPrint(set, benchmark = 1,k=k, n=n)

#@profile
def create_benchmark2( k, n,show) :

    set = generateData.generateBenchmark(k, n, 1, variableBase=[])
    if show :
            toPrint.generationToPrint(set, benchmark = 1,k=k, n=n)
    return set


def test_benchmark( k, n, show=False) :

    for i in range (numberOfSets) :
        set = generateData.generateBenchmark(k, n, 1, variableBase=[])
    return set
