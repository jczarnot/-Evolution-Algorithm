from optparse import Values
import matplotlib.pyplot as plt
from functions import equal_maxima, five_uneven_peak_trap, himmelblau, modified_rastrigin_all, six_hump_camel_back, uneven_decreasing_maxima
from pop import modified_rastrigin_all_set_up, projection, evolution_alg, initialization, our_method, our_method_random_value, resampling, reflection, return_the_best, wrapping, run_algorithm
import copy
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF


def population_plot(iterations, limitations, population, function):
    populations = []
    for i in range(iterations):
        population = evolution_alg(
            limitations, population=copy.deepcopy(population), func=simple_function_2D,  fix_func=function)
        populations.append(population)

    x = []
    y = []
    for p in populations:
        for i in p:
            x.append(i[0])
            y.append(i[1])

    plt.plot(x, y, "o")
    plt.show()


def simple_function_2D(x):
    return x[0]*x[0]+2*x[1]


def population_value_plot(iterations, limitations, size, bench_function):
    all_fix_fun = ['resampling', 'projection', 'reflection',
                   'wrapping', 'our method', 'our method random']
    values = [[] for _ in range(6)]
    s_population = initialization(limitations, size)
    for i in range(1, 7):
        population = copy.deepcopy(s_population)
        for j in range(iterations):
            population = evolution_alg(
                limitations, bench_function, i, copy.deepcopy(population))
            _, best_val = return_the_best(population, bench_function)
            values[i-1].append(best_val)

    plt.xlabel("Iterations")
    plt.ylabel("Values")
    for i in range(len(values)):
        plt.plot(values[i], label=all_fix_fun[i])
    plt.legend()
    plt.show()


def ecdf_plot(iterations, limitations, size, bench_function):
    all_fix_fun = ['resampling', 'projection', 'reflection',
                   'wrapping', 'our method', 'our method random']
    values = [[] for _ in range(6)]
    s_population = initialization(limitations, size)
    for i in range(1, 7):
        population = copy.deepcopy(s_population)
        for j in range(iterations):
            population = evolution_alg(
                limitations, bench_function, i, copy.deepcopy(population))
            _, best_val = return_the_best(population, bench_function)
            values[i-1].append(best_val)

    plt.xlabel("Iterations")
    plt.ylabel("ECDF")
    max_value = max(map(max, values))
    min_value = max(map(min, values))
    x = [j for j in range(round(min_value-2), round(max_value+2))]
    for i in range(len(values)):
        ecdf = ECDF(values[i])
        ecdf_values = ecdf(x)
        plt.plot(ecdf_values, label=all_fix_fun[i])
    plt.legend()
    plt.show()


limitations = [(-10, 20), (-5, 25)]
population = initialization(limitations, 100)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 1)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 2)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 3)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 4)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 5)

pop = copy.deepcopy(population)
population_plot(1000, limitations, pop, 6)

five_uneven_peak_trap_limitations = [(0, 30)]
population_value_plot(500, five_uneven_peak_trap_limitations,
                      100, five_uneven_peak_trap)
ecdf_plot(500, five_uneven_peak_trap_limitations,
          100, five_uneven_peak_trap)

himmelblau_limitations = [(-6, 6), (-6, 6)]
population_value_plot(500, himmelblau_limitations, 100, himmelblau)
ecdf_plot(500, himmelblau_limitations,
          100, himmelblau)

six_hump_camel_back_limitations = [(-1.9, 1.9), (-1.1, 1.1)]
population_value_plot(500, six_hump_camel_back_limitations,
                      100, six_hump_camel_back)
ecdf_plot(500, six_hump_camel_back_limitations,
          100, six_hump_camel_back)
