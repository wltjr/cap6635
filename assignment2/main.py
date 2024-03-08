#!/usr/bin/python

import math
import random
import timeit

class SimulatedAnnealing:
    """
    Simulated Annealing algorithm to find goal state
    """

    def __init__(self, dim, problem):
        """
        Simulated Annealing constructor to create new instances of class/object

        :param dim          integer dimension of the 2D grid
        :param problem      2D list containing the problem start state
        """
        self.dim = dim
        self.N = dim ** 2 - 1
        T = 1000000000000000000   # temperature
        alpha = 0.999999          # cooling
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
        dim = self.dim
        # find the zero/empty space
        for r in range(dim):
            for c in range(dim):
                if solution[r][c] == 0:
                    x = c
                    y = r
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
        dim = self.dim
        for y in range(dim):
            for x in range(dim):
                x2, y2 = self.valueToCoords(solution[y][x], dim)
                # manhattan distance
                _score += abs(x - x2) + abs(y - y2)
                # euclidean distance
                _score += math.sqrt(abs(x - x2)**2 + abs(y - y2)**2)
                # incorrect/misplaced
                if (solution[y][x] == 0 and correct != self.N) and \
                   (solution[y][x] - 1) != correct:
                    _score += 1
                correct += 1

        # count vertical inversions
        array = sum(solution, [])
        inv_count = 0
        n = self.N - 1
        for i in range(n):
            for j in range(i + 1, n):
                if array[i] > array[j]:
                    inv_count += 1

        # inverted distance, vertical inversions
        _score += inv_count / 3 + inv_count % 3

        return _score


def runSA(dim, grid):
    """
    Run Simulated Annealing on the grid

    :param dim          dimensions/size of the grid
    :param grid         2D list containing the problem start state
    """
    # wrap algorithm in timer for runtime
    start = timeit.default_timer()
    sa = SimulatedAnnealing(dim, grid)
    stop = timeit.default_timer()

    # display results
    print("Time: %0.4fms" % ((stop - start) * 1000))
    print("Steps:", sa.steps)
    print("Goal State: ")
    for i in range(dim):
        print(sa.solution[i])

def runTests():
    """
    Run Simulated Annealing on the grid
    """
    grids = [
        [[7, 2, 4], [5, 0, 6], [8, 3, 1]],
        [[8, 6, 7], [2, 5, 4], [3, 0, 1]],
        [[6, 4, 7], [8, 5, 0], [3, 2, 1]],
        [[1, 2, 3], [4, 5, 6], [8, 7, 0]],
        [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 14, 0]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 15, 14, 12]],
        [[12, 1, 2, 15], [11, 6, 5, 8], [7, 10, 9, 4], [0, 13, 14, 3]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 14, 10, 15], [13, 0, 12, 11]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]],
        [[15, 14, 8, 12], [10, 11, 9, 13], [2, 6, 5, 1], [3, 7, 4, 0]]
    ]
    for grid in grids:
        dim = len(grid)
        print("\nTesting grid:")
        for i in range(dim):
            print(grid[i])
        print()
        runSA(dim, grid)

def main():

    grid = []
    dim = 0
    n = 0

    # prompt for N-puzzle size
    while n < 8 or n > 99:
        print("Please enter a value for N (8 <= N < 100): ")
        n = input()
        if n.lower() == 't':
            runTests()
            return
        n = int(n)

    # get square root for grid dimensions/size
    dim = math.ceil(math.sqrt(n + 1))

    # starting N-puzzle state
    print("\nPlease enter the start case state: ")
    for i in range(dim):
        grid.append([int(x) for x in input().split()])

    # empty line
    print()
    # run the algorithm timer wrapped with output
    runSA(dim, grid)


if __name__ == '__main__':
    main()

