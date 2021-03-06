# starter code for solving knapsack problem using genetic algorithm
import random,sys


fc = open('./c.txt', 'r')
fw = open('./w.txt', 'r')
fv = open('./v.txt', 'r')
fout = open('./out.txt', 'w')


c = int(fc.readline())
w = []
v = []
for line in fw:
    w.append(int(line))
for line in fv:
    v.append(int(line))

print('Capacity :', c)
print('Weight :', w)
print('Value : ', v)

popSize = int(input('Size of population : '))
genNumber = int(input('Max number of generation : '))

print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')
parentSelection = int(input('Which one? '))
if parentSelection == 2:
    k = int(input('k=? (between 1 and ' + str(popSize) + ') '))

print('\nN-point Crossover\n---------------------------')
n = int(input('n=? (between 1 and ' + str(popSize - 1) + ') '))

print('\nMutation Probability\n---------------------------')
mutProb = float(input('prob=? (between 0 and 1) '))

print('\Survival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
survivalSelection = int(input('Which one? '))
elitism = bool(input('Elitism? (Y or N) ' ))


print('\n----------------------------------------------------------')
print('initalizing population')
population = []
popAndFitness={}
popAndWeight={}
for i in range(popSize):
    temp = []
    for j in range(len(w)):
        temp.append(random.randint(0,1))
    population.append(temp)


def fitnessEvaluate(population):
    global popAndFitness
    print('evaluating fitnesses')
    popAndFitness={}
    for i, chrom in enumerate(population):
        ft = 0
        wt = 0
        for j, gene in enumerate(chrom):
            ft += gene * v[j]
            wt += gene * w[j]
        if wt>c:
            ft=0
        print(i + 1, chrom, ft, wt)
        popAndFitness[i]=ft
        popAndWeight[i]=wt


##################################################################   

def evolve_population(pop):
    global population
    forElitism=sorted(popAndFitness.items(), key=lambda kv: kv[1])[-1][0]
    forElitism=population[forElitism]
    #parent selection
    female=[]
    male=[]
    parents=[]
    if parentSelection == 1: #roulette whelle
        max=sum(item for item in popAndFitness.values())
        count=0
        while count<popSize:
            indicies=[]
            i=0
            while i<2:
                pick = random.randint(0, max)
                current = 0
                for key,value in popAndFitness.items():
                    current=current+value
                    if current>pick and key not in indicies:
                        indicies.append(key)
                        i=i+1
                        break
            if [indicies[0],indicies[1]] not in parents:
                male.append(population[indicies[0]])
                female.append(population[indicies[1]])
                parents.append([indicies[0],indicies[1]])
                count+=1

    elif parentSelection == 2: #tournament
        count=0
        while count<popSize:
            indicies=[]
            j=0
            while j<2:
                c=0
                tournamentDict={}
                while c < k:
                    index=random.randint(0,len(pop)-1)
                    if index in tournamentDict.keys():
                        pass
                    else:
                        tournamentDict[index]=popAndFitness[index]
                        c=c+1
                winner = sorted(tournamentDict.items(), key=lambda kv: kv[1])[-1]
                if winner[0] not in indicies:
                    indicies.append(winner[0])
                    j=j+1
            if [indicies[0],indicies[1]] not in parents:
                male.append(population[indicies[0]])
                female.append(population[indicies[1]])
                parents.append([indicies[0],indicies[1]])
                count+=1

    else:
        print("Error: Parent Selection Type")
        sys.exit()

    #Crossover
    childs=[]
    reverse=False
    mod=(len(w)//(n+1))+1
    for j in range(0,len(population)):
        child=[]
        for i in range(0,len(male[j])):
            if (i+1)%mod==0:
                if reverse==True:
                    reverse=False
                else:
                    reverse=True
            if reverse:
                child.append(male[j][i])
            else:
                child.append(female[j][i])
        childs.append(child)
    
    
    #Mutation
    for child in childs:
        for i in range(2):
            if mutProb>random.random():
                index=random.randint(0,len(child)-1)
                if i==0:
                    child[index]= 0 if child[index]==1 else 1

    #Survivor Selection
    if survivalSelection == 1: #Age-based
        population=childs[:]
    
    elif survivalSelection == 2:  #Fitness-based
        population=population+childs
        fitnessEvaluate(population)
        sortedByFitness=sorted(popAndFitness.items(), key=lambda kv: kv[1] ,reverse=True)
        newPopulation=[]
        for item in sortedByFitness[:popSize]:
            newPopulation.append(population[item[0]])
        population=newPopulation[:]
    
    else:
        print("Error: Survival Selection Type")

    #Elitism
    fitnessEvaluate(population)
    if (elitism and (forElitism not in population)):
        minFitnessIndex=sorted(popAndFitness.items(), key=lambda kv: kv[1])[0][0]
        population[minFitnessIndex]=forElitism

        
for i in range(genNumber):
    fitnessEvaluate(population)
    evolve_population(population)

fitnessEvaluate(population)
index=sorted(popAndFitness.items(), key=lambda kv: kv[1] ,reverse=True)[0][0]
elit=population[index]
elit="".join(str(x) for x in elit)
weight=popAndWeight[index]
fitness=popAndFitness[index]
fout.write('chromosome: {}\n'.format(elit))
fout.write('weight: {}\n'.format(str(weight)))
fout.write('value: {}'.format(str(fitness)))
fout.close() 
