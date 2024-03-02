#!/usr/bin/python

import math
import random
import timeit

class SimulatedAnnealing:
    """
    Simulated Annealing algorithm to find goal state
    """

    def __init__(self, problem):
        """
        Simulated Annealing constructor to create new instances of class/object

        :param problem      2D list containing the problem start state
        """
        T = 100000000000     # temperature
        alpha = 0.999        # cooling
        steps = 1
        solution = self.generate(problem)
        E = self.score(solution)
        while T > 0.0001 and E > 0:
            newSolution = self.generate(solution)
            newE = self.score(newSolution)
            deltaE = newE - E
            if self.accept(T, deltaE):
                solution = newSolution
                E = newE
            T *= alpha # cool the temp
            steps += 1
        self.steps = steps
        self.solution = solution

    def accept(self, T, deltaE):
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


    def generate(self, solution):
        """
        Generate a new solution from the current

        :param solution     2D list containing the current solution

        :return list        2D list containing a new random solution from current
        """
        dim = len(solution)
        dim_1 = dim - 1
        while True:
            x = random.randrange(0, dim)
            y = random.randrange(0, dim)

            if (y == dim_1 and x == dim_1 and solution[dim_1][dim_1] != 0) or \
            (solution[y][x] - 1) != (y * dim + x):
                break

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


    def valueToCoords(self, value, dim):
        """
        Get the 2D coords, column/y and row/y of a value

        :param value        integer value to determine coords in a 2D grid
        :param dim          integer dimension of the 2D grid

        :return int         column the value belongs to
        """
        if value == 0:
            return (dim - 1, dim - 1)

        x = -1
        for i in range(value):
            x += 1
            if x == dim:
                x = 0

        y = math.floor((value - 1) / dim)

        return (x, y)

    def score(self, solution):
        """
        Score the current solution using Manhattan distance

        :param solution     2D list containing the current solution

        :return int         integer score value of the solution
        """
        _score = 0
        correct = 0
        dim = len(solution)
        n = dim ** 2 - 1
        for y in range(dim):
            for x in range(dim):
                x2, y2 = self.valueToCoords(solution[y][x], dim)
                _score += abs(x - x2) + abs(y - y2)
                if (solution[y][x] == 0 and correct != n) and \
                (solution[y][x] - 1) != correct:
                    _score += 1
                correct += 1

        return _score


def main():

    grid = []
    dim = 0
    n = 0

    # prompt for N-puzzle size
    while n < 8 or n > 100:
        print("Please enter a value for N (8 <= N <= 100): ")
        n = int(input())

    # get square root for grid dimensions/size
    dim = math.ceil(math.sqrt(n + 1))

    # starting N-puzzle state
    print("Please enter the start case state: ")
    for i in range(dim):
        grid.append([int(x) for x in input().split()])

    # wrap algorithm in timer for runtime
    start = timeit.default_timer()
    sa = SimulatedAnnealing(grid)
    stop = timeit.default_timer()

    # display results
    print('Time: ', stop - start)
    print(sa.steps)
    print(sa.solution)



if __name__ == '__main__':
    main()

