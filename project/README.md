# CAP6635: Advanced Artificial Intelligence Course Project

## About
This project is using [IRRT* from AtsushiSakai/PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/InformedRRTStar/informed_rrt_star.py) 
along with a custom Bug 2/Tangent Bug implementation to simulate going around
unknown obstacles on a predetermined path in online and offline modes.

In online mode, IRRT* determines the initial path, and unknown obstacles
are placed along this path, either circular or rectangular and
Bug 2/Tangent Bug goes around those obstacles. Bug algorithm will stop
if a Euclidean point is encountered, otherwise it will return to the
previously determined path. Then IRRT* is run again, and this process
is repeated for each unknown obstacle between the start and goal. This
process is considered online mode.

After the run in online mode with unknown obstacles being placed on the
path, IRRT* is run again from the start to the goal with all the
unknown obstacles being known and added to the previous obstacle map.

<p align="center">
  <img alt="Animated Screenshot" src="https://github.com/wltjr/cap6635/assets/12835340/2569c722-2527-489e-bc50-a044555abf48" width=60% />
  <img alt="Screenshot of Stats" src="https://github.com/wltjr/cap6635/blob/master/project/screenshots/stats.jpg" width=35% /> 
</p>

## System Requirements
The following software is required for proper operation

  [Matplotlib >= 3.8.4](https://pypi.org/project/matplotlib/)  
  [Numpy >= 1.26.4](https://pypi.org/project/numpy/)  
  [Python >= 3.9](https://www.python.org/downloads/)  

## Installation
Installation is not required for usage and operation of the program,
simply download and unpack an archive of the project.

## Building
Building is not required for usage and operation of the program,
simply run `python main.py` as instructed in the following section.

## Running
In order to run the program navigate to `project/`
(or the directory the project was unpacked into) in a terminal and run

```sh
python main.py
```
When that command is run the GUI should initialize and start the program.

### Running Stats
There is an additional program for statistics, minimum, maximum,
and average node counts and path lengths, based on some theoretical
unit, meters or feet.
```sh
python stats.py
```
This program is depend on `data.csv` in the same directory
