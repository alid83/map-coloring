# Advanced Map Coloring with Neighbourhood Awareness
This file contains a template for solving the map coloring problem. You have to complete the code to implement the solution.  
The goal is to color the map of continents such that no two adjacent countries have the same color.There is another option, You can define the Neighbourhood-distance parameter to specify the threshold for neighboring elements. For instance, setting the Neighbourhood-distance to 2 will include the neighbors of neighbors within the defined neighborhood. For instance, Pakistan is a neighbor of Iran, and China is a neighbor of Pakistan,  setting the Neighborhood-distance to 2 would mean that China is also considered a neighbor of Iran.


## Installation

**Recommended Python version: Python 3.10.9**

```python
pip install -r requirements.txt
```
## Contents
Below is a brief overview of the contents: 

- CSP.py: Contains the CSP class representing a Constraint Satisfaction Problem and provides functions to define CSP problems.

- graphics.py: Functions for visualizing the colored map for continents based on the solution found.

- map_generator.py: Function to generate a dictionary from a CSV file, essential for defining CSP constraints.

- Solver.py: Contains a class with functions to implement algorithms for finding the CSP solution.

- main.py: Main file to execute the code with specified parameters.

## Parameters
* -m, --map: Specifies the continent(s) to color. Choose from: Asia, Africa, America, and Europe.

* -lcv, --lcv: Enables the Least Constraint Value (LCV) heuristic as an order-type optimizer.

* -mrv, --mrv: Enables the Minimum Remaining Values (MRV) heuristic as an order-type optimizer.

* -ac3, --arc-consistency: Enables arc consistency as a mechanism to eliminate the domain of variables for an optimized solution.

* -ND, --Neighbourhood-distance: Specifies the threshold for neighboring regions' similarity in color, default is 1.

## Running the Code
To run the code, you have to execute main.py with the following command format: 

* If you want to color Asia with lcv and mrv heuristics: 

python3 main.py -m Asia -lcv -mrv 
(If python 3 is the default version on your system, you can simply use python instead of python3: 
python main.py -m Asia -lcv -mrv)
 
* If you want to also enable arc consistency: 

python3 main.py -m Europe -lcv -mrv -ac3

* to also add Neighbourhood-distance parameter:

python main.py -m Europe -lcv -mrv -ac3 -ND 2

you can observe the number of assignments for each run, which is displayed alongside the map, enabling you to compare algorithms

