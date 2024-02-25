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


def generate(solution):
    """
    Generate a new solution from the current

    :param solution     2D list containing the current solution

    :return list        2D list containing a new random solution from current
    """
    dim = len(solution)
    x = random.randrange(0, dim)
    y = random.randrange(0, dim)

    # reduce for zero index
    dim -= 1

    # random action: up 0, down 1, left 2, right 3
    action = random.randrange(0, 4)

    # move up, if action up and y > 0, or if action down and y == dim
    if (action == 0 and y > 0) or \
       (action == 1 and y == dim):
        solution[y][x], solution[y - 1][x] = solution[y - 1][x], solution[y][x]

    # move down, if action down and y < dim, or if action up and y == 0
    elif (action == 1 and y < dim) or \
         (action == 0 and y == 0):
        solution[y][x], solution[y + 1][x] = solution[y + 1][x], solution[y][x]

    # move left, if action left and x > 0, or if action right and x == dim
    elif (action == 2 and x > 0) or \
         (action == 3 and x == dim):
        solution[y][x], solution[y][x - 1] = solution[y][x - 1], solution[y][x]

    # move right, if action right and x < dim, or if action left and x == 0
    elif (action == 3 and x < dim) or \
         (action == 2 and x == 0):
        solution[y][x], solution[y][x + 1] = solution[y][x + 1], solution[y][x]

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
            _score += abs(x - x2) + abs(y - y2)

    return _score


def simulated_annealing(problem):

    T = 10              # temperature
    alpha = 0.84        # cooling
    solution = generate(problem)
    E = score(solution)
    while T > 0 and E > 0:
        newSolution = generate(solution)
        newE = score(newSolution)
        deltaE = newE - E
        if accept(T, deltaE):
            solution = newSolution
            E = newE
        T *= alpha # cool the temp

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

    grid = generate(grid)

    print(grid)

    print(score(grid))


if __name__ == '__main__':
    main()

