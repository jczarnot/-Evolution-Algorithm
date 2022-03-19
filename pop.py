from copy import deepcopy
import random
from functions import *
import statistics
import pandas as pd


def initialization(limitations_for_points, num_of_ind):
    population = []
    for i in range(num_of_ind):
        individual = []
        for limit in limitations_for_points:
            min_val, max_val = limit
            point = random.uniform(min_val, max_val)
            individual.append(point)
        population.append(individual)
    return population


def tournament_for_maximum(x1, x2, func, limitations):
    x1_in_limitation = check_if_in_limitations(x1, limitations)
    x2_in_limitation = check_if_in_limitations(x2, limitations)
    if x1_in_limitation and x2_in_limitation:
        if (func(x1) > func(x2)):
            return x1
        else:
            return x2
    if x1_in_limitation:
        return x1

    if x2_in_limitation:
        return x2

    else:
        return None


def mutation(x):
    for idx in range(len(x)):
        random_value = random.uniform(-1.0, 1.0)
        x[idx] = x[idx] + random_value
    return x


def select_for_mutation(s_population1, sigma):
    s_population = deepcopy(s_population1)
    m_population = []
    population_without_mutation = []
    for i in s_population:
        random_value = random.uniform(0, 1.0)
        if random_value < sigma:
            i1 = deepcopy(i)
            m_population.append(mutation(i1))
        else:
            population_without_mutation.append(i)
    return m_population, population_without_mutation


def selection(population1, func, limitations, num_of_iteration=None):
    population = deepcopy(population1)
    if num_of_iteration == None:
        num_of_iteration = len(population)
    s_population = []
    for i in range(num_of_iteration):
        result = tournament_for_maximum(
            random.choice(population), random.choice(population), func, limitations)
        if result == None:
            num_of_iteration += 1
        else:
            s_population.append(result)
    return s_population


def evolution_alg(limitations_for_points, func, fix_func, population=[], number_of_individuals=100, sigma=0.4):
    m_population = []
    population_without_mutation = []
    if population == []:
        population = initialization(
            limitations_for_points, number_of_individuals)
    else:
        population = population
    s_population = selection(population, func, limitations_for_points)
    m_population, population_without_mutation = select_for_mutation(
        s_population, sigma)
    if fix_func == 1:
        correct_population = resampling(
            m_population, population_without_mutation, limitations_for_points, sigma)
    elif fix_func == 2:
        correct_population = before_projection(
            m_population, limitations_for_points)
    elif fix_func == 3:
        correct_population = reflection(m_population, limitations_for_points)
    elif fix_func == 4:
        correct_population = wrapping(
            m_population, limitations_for_points, k=1)
    elif fix_func == 5:
        correct_population = our_method(m_population, limitations_for_points)
    elif fix_func == 6:
        correct_population = our_method_random_value(
            m_population, limitations_for_points)
    new_population = correct_population + population_without_mutation
    return new_population
###############################################################################
# FIX FUNCTION
###############################################################################


def resampling(m_population, correct, limitations, sigma):
    for i in range(len(m_population)):
        p = m_population[i]
        while not check_if_in_limitations(p, limitations):
            p = deepcopy(random.choice(m_population+correct))
            random_value = random.uniform(0, 1.0)
            if random_value < sigma:
                p = mutation(p)
        m_population[i] = p
    return m_population


def check_if_in_limitations(invidual, limitations):
    for i in range(len(limitations)):
        if not (limitations[i][0] < invidual[i] < limitations[i][1]):
            return False
    return True


def before_projection(population, limitations):
    after_projection = []
    for individuals in population:
        new_ind = projection(individuals, limitations)
        after_projection.append(new_ind)
    return after_projection


def projection(individuals, limitations):
    for i in range(len(individuals)):
        min_val, max_val = limitations[i]
        if individuals[i] > max_val:
            individuals[i] = max_val
        if individuals[i] < min_val:
            individuals[i] = min_val
    return individuals


def reflection(population, limitations):
    for p in population:
        for dimetion in range(len(limitations)):
            if p[dimetion] > limitations[dimetion][1]:
                p[dimetion] = 2*limitations[dimetion][1]-p[dimetion]
            elif p[dimetion] < limitations[dimetion][0]:
                p[dimetion] = 2*limitations[dimetion][0]-p[dimetion]
    return population


def wrapping(population, limitations, k=1):
    for p in population:
        for dimetion in range(len(limitations)):
            if p[dimetion] > limitations[dimetion][1]:
                d_size = limitations[dimetion][1]-limitations[dimetion][0]
                p[dimetion] = p[dimetion]-k*d_size
            elif p[dimetion] < limitations[dimetion][0]:
                d_size = limitations[dimetion][1]-limitations[dimetion][0]
                p[dimetion] = p[dimetion]+k*d_size
    return population


def our_method(population, limitations):
    for p in population:
        for dimetion in range(len(limitations)):
            half_length = (limitations[dimetion]
                           [1] - limitations[dimetion][0])*0.5
            middle = limitations[dimetion][0]+half_length
            if p[dimetion] > limitations[dimetion][1]:
                p[dimetion] = middle+half_length / \
                    (p[dimetion]+limitations[dimetion][1])
            elif p[dimetion] < limitations[dimetion][0]:
                p[dimetion] = middle+half_length / \
                    (p[dimetion]+limitations[dimetion][0])
    return population


def our_method_random_value(population, limitations):
    for p in population:
        for dimetion in range(len(limitations)):
            if p[dimetion] > limitations[dimetion][1]:
                p[dimetion] = random.uniform(
                    limitations[dimetion][0], limitations[dimetion][1])
            elif p[dimetion] < limitations[dimetion][0]:
                p[dimetion] = random.uniform(
                    limitations[dimetion][0], limitations[dimetion][1])
    return population

###############################################################################
# SET UP FUNCTION
###############################################################################


def five_uneven_peak_set_up(fix_func=1):
    five_uneven_peak_trap_limitations = [(0, 30)]
    population = run_algorithm(
        100, five_uneven_peak_trap_limitations, five_uneven_peak_trap, fix_func)
    best_ind, best_val = return_the_best(population, five_uneven_peak_trap)
    return best_ind, best_val


def equal_maxima_set_up(fix_func=1):
    equal_maxima_limitations = [(0, 1)]
    population = run_algorithm(
        100, equal_maxima_limitations, equal_maxima, fix_func)
    best_ind, best_val = return_the_best(population, equal_maxima)
    return best_ind, best_val


def uneven_decreasing_maxima_set_up(fix_func=1):
    uneven_decreasing_maxima_limitations = [(0, 1)]
    population = run_algorithm(
        100, uneven_decreasing_maxima_limitations, uneven_decreasing_maxima, fix_func)
    best_ind, best_val = return_the_best(population, uneven_decreasing_maxima)
    return best_ind, best_val


def himmelblau_set_up(fix_func=1):
    himmelblau_limitations = [(-6, 6), (-6, 6)]
    population = run_algorithm(
        100, himmelblau_limitations, himmelblau, fix_func)
    best_ind, best_val = return_the_best(population, himmelblau)
    return best_ind, best_val


def six_hump_camel_back_set_up(fix_func=1):
    six_hump_camel_back_limitations = [(-1.9, 1.9), (-1.1, 1.1)]
    population = run_algorithm(
        100, six_hump_camel_back_limitations, six_hump_camel_back, fix_func)
    best_ind, best_val = return_the_best(population, six_hump_camel_back)
    return best_ind, best_val


def shubert_set_up(fix_func=1, D=4):
    shubert_limitations = [(-10, 10)]*D
    population = run_algorithm(100, shubert_limitations, shubert, fix_func)
    best_ind, best_val = return_the_best(population, shubert)
    return best_ind, best_val


def vincent_set_up(fix_func=1, D=4):
    vincent_limitations = [(0.25, 10)]*D
    population = run_algorithm(100, vincent_limitations, vincent, fix_func)
    best_ind, best_val = return_the_best(population, vincent)
    return best_ind, best_val


def modified_rastrigin_all_set_up(fix_func=1):
    modified_rastrigin_all_limitations = [(0, 1)]*16
    population = run_algorithm(
        100, modified_rastrigin_all_limitations, vincent, fix_func)
    best_ind, best_val = return_the_best(population, modified_rastrigin_all)
    return best_ind, best_val

###############################################################################
# PRINT RESULTS
###############################################################################


def run_algorithm(num, limitations, func, fix_func):
    population = []
    for i in range(num):
        population = evolution_alg(
            limitations, func, fix_func, deepcopy(population))
    return population


def return_the_best(population, func):
    best_val = -math.inf
    best_ind = None
    for ind in population:
        if func(ind) > best_val:
            best_val = func(ind)
            best_ind = ind
    return best_ind, best_val


def statistic(b_fun, run=10):
    all_average = []
    all_standard_deviation = []
    for i in range(1, 7):
        average = 0
        sample = []
        sum = 0
        for j in range(run):
            best_ind, best_val = b_fun(i)
            if best_val != -math.inf:
                sample.append(best_val)
                average += best_val
                sum += 1
        if sum != 0:
            all_average.append(average/sum)
            all_standard_deviation.append(statistics.stdev(sample))
    return all_average, all_standard_deviation


def print_result(bench_func, names):
    result_avg = []
    result_std = []
    for functon in bench_func:
        avg, std = statistic(functon)
        result_avg += avg
        result_std += std
    all_name = []
    for name in names:
        all_name += [f'{name} resampling', f'{name} projection', f'{name} reflection',
                     f'{name} wrapping', f'{name} our method', f'{name} our method random']
    dict = {'name': all_name, 'average': result_avg, 'std': result_std}
    df = pd.DataFrame(dict, columns=['name', 'average', 'std'])
    df.to_csv("results.csv")
    print(df.head(len(all_name)))


if __name__ == "__main__":
    bench_func = [five_uneven_peak_set_up, equal_maxima_set_up, uneven_decreasing_maxima_set_up,
                  himmelblau_set_up, six_hump_camel_back_set_up, shubert_set_up, vincent_set_up, modified_rastrigin_all_set_up]
    names = ['five_uneven_peak_trap', 'equal_maxima', 'uneven_decreasing_maxima',
             'himmelblau', 'six_hump_camel_back', 'shubert', 'vincent', 'modified_rastrigin_all']
    print_result(bench_func, names)
