import random
import numpy as np
import copy

crossoverProbability = 0.5
carryPercentage = 0.1
populationSize = 100
mutationProbability = 0.5


class EquationBuilder:

    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber
        self.population = self.makeFirstPopulation()
        self.maxgenerations = 1000

    def makeFirstPopulation(self):
        population = []
        for _ in range(populationSize):
            chromosome = []
            for j in range(self.equationLength):
                if j % 2 == 0:
                    chromosome.append(random.choice(self.operands))
                else:
                    chromosome.append(random.choice(self.operators))
            population.append(chromosome)
        return population

    def findEquation(self):
        while (True):
            if self.maxgenerations == 0:
                return "There is no solution"
            random.shuffle(self.population)
            # Calculate fitness
            fitnesses = []
            total_fitness = 0
            for i in range(populationSize):
                fitnesses.append(self.calcFitness(self.population[i]))
                if fitnesses[i] == 1:
                    return self.population[i]
                total_fitness = total_fitness + fitnesses[i]

            # Calculate probability
            prob_fitness = []
            for i in range(len(fitnesses)):
                prob_fitness.append(fitnesses[i] / total_fitness)

            # Carry over the best chromosomes
            fit = [(fitnesses[i], chromo) for i, chromo in enumerate(self.population)]
            sorted_fitness = sorted(fit, reverse=True)
            carriedChromosomes = []
            carry = int(carryPercentage * populationSize)
            for i in range(carry):
                carriedChromosomes.append(sorted_fitness[i][1])

            matingPool = self.createMatingPool(prob_fitness)
            crossoverPool = self.createCrossoverPool(matingPool)

            self.population.clear()
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))

            self.population.extend(carriedChromosomes)
            self.maxgenerations -= 1

    def calcFitness(self, chromosome):
        fitness = 0
        strr = ' '.join(chromosome)
        difference = abs(eval(strr) - goalNumber)
        fitness = 1/(1 + difference)
        return fitness

    def createMatingPool(self, prob_fitness):
        matingPool = []
        cum_sum = np.cumsum(prob_fitness)
        for _ in range(populationSize):
            r = random.random()
            for j in range(len(cum_sum)):
                if r < cum_sum[j]:
                    matingPool.append(self.population[j])
                    break
        return matingPool

    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        crossoverPool = copy.deepcopy(matingPool)
        for i in range(0, populationSize, 2):
            if i != populationSize - 1:
                r = random.random()
                if r < crossoverProbability:
                    crossoverPoint = random.randint(1, self.equationLength - 1)
                    crossoverPool[i][crossoverPoint:] = matingPool[i +1][crossoverPoint:]
                    crossoverPool[i +1][crossoverPoint:] = matingPool[i][crossoverPoint:]
        return crossoverPool

    def mutate(self, chromosome):
        r = random.random()
        if r < mutationProbability:
            mutationPoint = random.randint(0, self.equationLength - 1)
            if mutationPoint % 2 == 0:
                chromosome[mutationPoint] = random.choice(self.operands)
            else:
                chromosome[mutationPoint] = random.choice(self.operators)
        return chromosome


# get input from user
equationLength = int(input())
operands = input().split()
operators = input().split()
goalNumber = int(input())

equationBuilder = EquationBuilder(
    operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
result = ''.join(map(str, equation))
print(result)
