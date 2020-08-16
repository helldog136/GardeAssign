# ULBStageMedServicePicker
Python helper to choose nicely the service for students in medicine at ULB (Affectation problem solved using SCIP)

You need to have obtained a licence for SCIP (https://www.scipopt.org/index.php#download) and installed it. 
You also need to have "scip" command added to your PATH.

This script has been tested with SCIP 7.0.1 on a Windows10 machine and seems to be working.

To run it simply launch:

`python3 main.py input.csv`

input csv file must have the following structure:

First line: List of all Possible services (first column skipped)

Second line: Maximum number of students per service (first column skipped)

All next lines: Student Name, preferences being in a range of 1-n 1 being the most preferred service. 

Empty values are considered as "least preferred"

preferences can be unique (e.g. only one of each number) or multiple (e.g. same preference level for two services)

For an example of input file see provided input.csv

## How it works:
This program creates a function to minimize by SCIP. 
Each variable X_i_j represents the potential affectation of the student i to the service j. Each variable is binary.

The variables are subject to constraints (student only affected once and no more student per service than available places in the service)

The function accounts the preferences of the students by affecting a "weight" to each variable. 
The more the student wants the service, the more the affectation will minimize the value of the function. 
The rest is magic from SCIP. 

SCIP will find the optimal value for each X_i_j (1 or 0). 
This result is then interpreted to give the final affectation.

## Future improvements?
Migrate from SCIP (needing external installs) to https://pypi.org/project/lpsolvers/

Add neat graphical interface (Angular?)