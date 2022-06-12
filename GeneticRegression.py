# Import relevant Python modules
import operator
import math
import random
import numpy  as np
from matplotlib import pyplot

# Import DEAP modules
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# ====================================================================
# PARAMETERS - change the parameters in this section
# Population size: 500 vs 2000
# Tournament Size: 2 vs 5
# repeat at least 10 times per setting

no_generations = 75   # number of generations
no_population = 1000   # population size
no_tournaments =  5   # tournament size

# other parameters that you can change and explore
p_xo = 0.7  # XO rate
p_m  = 0.3  # Mutation rate
UseSqError = True # use Least Squares approach 

# ====================================================================
# Define your Problems/Target Functions and create sample data
# Assume you make measurments at specific test points:

# test_points = np.linspace(-math.pi,math.pi, 65).tolist()
test_points = [2, 3, 4, 5, 6, 7]
## Defining the functions. ##
#measurement = lambda x: x**6-2*x**4-13*x**2 # Function 1
#measurement = lambda x: math.sin(math.pi/4 + 3*x) # Function 2

# ====================================================================

target = [1606, 2398, 3399, 4277, 4956, 5752]
measurement = lambda idx, x: target[idx] - x
#target = np.empty(len(test_points))
#for i in range(len(test_points)): target[i] = measurement(test_points[i])

fig, ax = pyplot.subplots(figsize=(15,4))
ax.scatter(test_points, target)
ax.set_xlabel('Test points')
ax.set_ylabel('Measurements')
ax.set_title('Data set')
pyplot.show()

# Define new functions
def protectedDiv(left, right):
    return left / right if right else 1    
    
# create Primitive set & classes 
if "pset" not in globals():
    pset = gp.PrimitiveSet("MAIN", 1)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(protectedDiv, 2)
    pset.addPrimitive(operator.neg, 1)
    pset.addPrimitive(math.cos, 1)
    pset.addPrimitive(math.sin, 1)
    pset.addTerminal(1)
    pset.addTerminal(-1)    
    pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
    pset.renameArguments(ARG0='x')

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)
    
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    if UseSqError:
      # squared error
      error = (abs(func(x) - measurement(idx, x))**2 for idx, x in enumerate(test_points))    
    else:
      # Absolute distance between target curve and solution
      error = (abs(func(x) - measurement(idx, x)) for idx, x in enumerate(test_points))    

    return math.fsum(error)/len(test_points),


toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=no_tournaments)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=64))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=64))

random.seed()

pop = toolbox.population(n=no_population)
hof = tools.HallOfFame(1)

stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("mdn", np.median)
mstats.register("avg", np.mean)
mstats.register("std", np.std)
mstats.register("min", np.min)
mstats.register("max", np.max)

pop, log = algorithms.eaSimple(pop, toolbox, p_xo, p_m, no_generations, stats=mstats, halloffame=hof, verbose=True)

# Plot Fitness and Size
x = np.arange(0, no_generations+1)
s = log.chapters['size'].select("mdn")
f = log.chapters['fitness'].select("mdn")

fig, ax = pyplot.subplots()
ax.plot(x, f/max(f), 'k--', label='Fitness')
ax.plot(x, s/max(s), 'k:', label='Size')
ax.set_xlabel('Generations')
ax.set_ylabel('Normalised Fitness/Size')
ax.set_title('Median')
legend = ax.legend(shadow=True, fontsize='x-large')
print('Fitnes: [' + str(min(f))+', '+str(max(f))+']')
print('Size: [' + str(min(s))+', '+str(max(s))+']')
print('Evaluations: ' +str(sum(log.select("nevals"))))

pyplot.show()

# Best individual 
print(hof[0])

# Plot comparison Tagret vs. evolved solution

x = test_points + [8]
f = toolbox.compile(expr=hof[0])

y = np.empty(len(x))
for i in range(len(x)): y[i] = f(x[i])

print(x)
print(y)

target2 = target + [0]

fig, ax = pyplot.subplots()
ax.plot(x, y, 'r-', label='Best Solution')
ax.plot(x, target2, 'k-', label='Target func')
#legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
legend = ax.legend(shadow=True, fontsize='x-large')

pyplot.show()

print("8 Users")
print(f(8))
print("200 Users")
print(f(200))
