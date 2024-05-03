# CAP6635: Advanced Artificial Intelligence Assignment 1 <br> A* shortest path graph search

## About
Assignment 1 is a graph created from two text files, `graph.txt` and `coords.txt`.
Once a graph is created, vertex/nodes can be optionally blocked, and the graph
can be searched using A* or Dijkstra algorithms.

<p align="center">
  <img alt="Screenshot of GUI" src="https://github.com/wltjr/cap6635/assets/12835340/f783c99a-2563-40e5-8112-3fdc348aed39" width=45% />
  <img alt="Screenshot of GUI" src="https://github.com/wltjr/cap6635/assets/12835340/2072e8ac-48ab-427b-a8ad-04ff3738410c" width=45% /> 
</p>

## System Requirements
The following software is required for proper operation

  [Pillow >= 10.2.0](https://pillow.readthedocs.io/en/stable/installation.html)  
  [Python >= 3.9](https://www.python.org/downloads/)  
  [Tkinter >= 8.6](https://docs.python.org/3/library/tkinter.html)  
  [Tcl/Tk >= 8.6](https://www.tcl.tk/software/tcltk/)  

## Installation
Installation is not required for usage and operation of the program,
simply download and unpack an archive of the project.

## Building
Building is not required for usage and operation of the program,
simply run `python main.py` as instructed in the following section.

## Running
In order to run the program navigate to `assignment1/`
(or the directory the project was unpacked into) in a terminal and run

```sh
python main.py
```
When that command is run the GUI should initialize and start the program.

## Test/Sample files
Test/sample files containing coordinates and adjacency information is provided
in the `graph.txt` and `coords.txt` files.

## Operation and Usage
Proper operation and usage requires properly formatted `graph.txt` and
`coords.txt` files, space separated values in each.

1. Enter the name of the coordinates file, or select the file using the button
   and file selection dialog.

2. Enter the name of the adjacency file, or select the file using the button
   and file selection dialog.

3. Press the Create Graph button

4. Select a Start Vertex/Node from the list

5. Select a Goal Vertex/Node from the list

6. Optionally enter one or more Vertices/Nodes to the block field

7. Press A* or Djikstra button

Each button can be pressed one or more times. A reset button is provided to
reset all fields and tables for multiple runs using different files/input.
A quit button is provided for convenience as an alternative to normal window
closure.

A copy of the graph image will be generated and saved to `graph.jpg` within the
same folder the program is running within. This file is overwritten each time,
so, it will only display the last graph generated or searched.

