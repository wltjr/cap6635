# CAP6635: Advanced Artificial Intelligence Assignment 2 <br> Solving an N-puzzle problem using Simulated Annealing

## About
Assignment 2 is a command line N-puzzle problem solved using the Simulated
Annealing algorithm. The program prompts the user for the size of the N-puzzle
and then the initial start state, after which, results are displayed.

## System Requirements
The following software is required for proper operation

  [Pillow >= 10.2.0](https://pillow.readthedocs.io/en/stable/installation.html)  
  [Python >= 3.11](https://www.python.org/downloads/)  
  [Tkinter >= 8.6](https://docs.python.org/3/library/tkinter.html)  
  [Tcl/Tk >= 8.6](https://www.tcl.tk/software/tcltk/)  

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
Proper operation and usage requires properly formatted N-puzzle start state
e.g. For a 8-puzzle starting state
```text
7 2 4
5 0 6
8 3 1
```

1. Enter the desired N value for the N-puzzle, 8 <= N <= 100

2. Enter the N-puzzle start state with space separated columns, per the example.

3. Press enter/return after the last value  
   Note: this will happen automatically with copying & pasting start state

The results will be display after, the runtime, action steps, and goal state.
