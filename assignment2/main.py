#!/usr/bin/python

import math
import random

def accept(T, deltaE):
    """
    Check equality of vertex based on coordinates, override default comparison

    :param T            Temperature
    :param deltaE       variation between new candidate solution and current

    :return boolean     value indicates if new solution is accepted or not
    """
    if deltaE < 0:
        return True
    else:
        r = random.randrange(0, 1)
        if r < math.exp(-deltaE / T ):
            return True
        else:
            return False


def generate(current):
    """
    Generate a new solution from the current

    :param current      2D list containing the current solution

    :return list        2D list containing a new random solution from current
    """
    solution = current

    return solution


def valueToCoords(value, dim):
    """
    Get the 2D coords, column/y and row/y of a value

    :param value        integer value to determine coords in a 2D grid
    :param dim          integer dimension of the 2D grid

    :return int         column the value belongs to
    """
    x = 0
    for i in range(value):
        x += 1
        if x == dim:
            x = 0

    y = math.floor(value / dim)

    return (x, y)

def score(solution):
    """
    Score the current solution using Manhattan distance

    :param solution     2D list containing the current solution

    :return int         integer score value of the solution
    """
    _score = 0
    dim = len(solution)
    for x in range(dim):
        for y in range(dim):
            x2, y2 = valueToCoords(solution[y][x], dim)
            print("value %d col/x = %d row/y = %d" % (solution[y][x], x2, y2))
            _score += abs(x - x2) + abs(y - y2)

    return _score


def simulated_annealing(problem):

    T = 10              # temperature
    alpha = 0.84        # cooling
    solution = generate(problem)
    E = score(solution)
    while T > 0:
        newSolution = generate(solution)
        newE = score()
        deltaE = newE - E
        if accept(T, deltaE):
            solution = newSolution
            E = newE
        T /= alpha # cool the temp

    return solution

def main():

    grid_size = 3
    grid = []
    n = 0

    while n < 8 or n > 100:
        print("Please enter a value for N (8 <= N <= 100): ")
        n = int(input())

    print("Please enter the start case state: ")
    for i in range(grid_size):
        grid.append([int(x) for x in input().split()])

    print(grid)

    print(score(grid))


if __name__ == '__main__':
    main()

