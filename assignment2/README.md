# CAP6635: Advanced Artificial Intelligence Assignment 2 <br> Solving an N-puzzle problem using Simulated Annealing

## About
Assignment 2 is a command line N-puzzle problem solved using the Simulated
Annealing algorithm. The program prompts the user for the size of the N-puzzle
and then the initial start state, after which, results are displayed.

The heuristics in use are a combination of incorrect positions, manhattan distance,
euclidean distance, and a partial inversion distance using vertical inversions.
This combination seemed to produce the best results, though all runs are random,
so any trials varied considerable in runtime, making heuristic improvements hard
to determine if beneficial. It did seem that horizontal inversions did not improve
results, therefore, were omitted and just kept vertical inversions.

![Screenshot](https://github.com/wltjr/cap6635/assets/12835340/88903d91-c5af-45b6-b7c6-4c123e2ac24c)

## System Requirements
The following software is required for proper operation

  [Python >= 3.11](https://www.python.org/downloads/)  

## Installation
Installation is not required for usage and operation of the program,
simply download and unpack an archive of the project.

## Building
Building is not required for usage and operation of the program,
simply run `python main.py` as instructed in the following section.

## Running
In order to run the program navigate to `assignment2/`
(or the directory the project was unpacked into) in a terminal and run
```sh
python main.py
```
When that command is run the program will start with prompts in the same
terminal window.

## Operation and Usage
Proper operation and usage requires properly formatted space separated N-puzzle
start state.
e.g. For a 8-puzzle starting state
```text
7 2 4
5 0 6
8 3 1
```

1. Enter the desired N value for the N-puzzle, 8 <= N < 100
   Note: there are two valid hidden single character values
   - 'r' will run tests through a series of random puzzles 3 x 3 up to 10 x 10
   - 't' will run tests through a series of pre-determined 3 x 3 and 4 x 4 puzzles

2. Enter the N-puzzle start state with space separated columns, per the example.

3. Press enter/return after the last value  
   Note: this will happen automatically with copying & pasting start state

The results will be display after, the runtime, action steps, and final or goal
state. Some results can take upward of 10 minutes, this may increase as
temperature and cooling values change and/or other heuristics added.

## Heuristic References
The following sources were used for heuristics research
- [Michael Kim's Blog: Solving the 15 Puzzle](https://michael.kim/blog/puzzle)
- [An approach to heuristics: 35-Puzzle with simulated annealing](https://kcir.pwr.edu.pl/~witold/aiarr/2009_projekty/35Puzzle/)
