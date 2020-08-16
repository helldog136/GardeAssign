# GardeAssign
Python helper to choose nicely the guards for students in medicine at ULB (Affectation problem solved using SCIP)

You need to have obtained a licence for SCIP (https://www.scipopt.org/index.php#download) and installed it. 
You also need to have "scip" command added to your PATH.

This script has been tested with SCIP 7.0.1 on a Windows10 machine and seems to be working.

To run it simply launch:

`python3 main.py input.csv`

input csv file must have the following structure:

First line: "Places,[number of students to assign per day]"

Second line: "Dates,[List of dates where you want to assign students]"

Third line: "Day,[S/W S=weekday, W=weekend]"

All next lines: "Student Name, [empty if the student doesn't want to go at this date, any text otherwise]"

For an example of input file see provided input.csv

## How it works:
This program creates a function to minimize by SCIP. 
Each variable X_i_j represents the potential affectation of the student i to the guard j. Each variable is binary.

The variables are subject to constraints (each day has X students (from config),...)

The function tries to balance the number of guards per student and between weekday and weekend day.
The rest is magic from SCIP. 

SCIP will find the optimal value for each X_i_j (1 or 0). 
This result is then interpreted to give the final affectation.

## Future improvements?
Migrate from SCIP (needing external installs) to https://pypi.org/project/lpsolvers/

Add neat graphical interface (Angular?)