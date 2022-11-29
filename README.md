# Project 2 Group12

# Disclaimer

Our group changed our idea midway during Milestone 4. We sent an email to Alex and received approval to change our project idea. We redid Milestones 2 and 3 in [MILESTONES.md](./MILESTONES.md), but kept an archive at the very bottom to show that we put significant effort in our previous ideas and that we submitted previous milestones on time. Please contact our group if there's any questions!

# Introduction, Use Case & Motivation

TODO define dead code, target users, motivation, problem

TODO why we chose Python

## Static vs Dynamic Analysis

TODO why we chose static analysis

# Getting Started

## Running our project
1. First install all dependencies
   - Run the command `pip install -r requirements.txt` from the project directory

TODO talk about example inputs directory

TODO add more details
- command line usage
  - e.g. -d is debug mode and will print to terminal
- how to interpret the HTML report

## Disclaimer about what we don't support

Please see the section [Future Work](#future-work)

## Running tests

The tests can either be ran by executing the command `python -m pytest`, or alternatively by using the `Testing` tab in VSCode which should discover the tests in our repo.

![image](https://media.github.students.cs.ubc.ca/user/1272/files/ccca1d73-31e4-49ef-8ff0-f8098aac8062)


# Relevant documents

Please see our [Google Doc](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit?usp=sharing) for all the documentation and planning we did for our project.

Here are our [Presentation Slides](https://docs.google.com/presentation/d/19lBsd1kV9K8-WTmjm7iKl9PKMK03tVnVeWeO9uBxy9o/edit?usp=sharing) as well

# Design
Our project targets the 3 criteria required for the project. Namely,
1. A static analysis component
2. Targets the Python language and its AST
3. Has a substantial visualization component.

## Architecture

Here's a high-level overview of our project.

![image](https://media.github.students.cs.ubc.ca/user/1272/files/23852ef8-6c16-41bf-b820-6d0c65795dd4)

1. The user uses our program analysis through the CLI by specifying an input file with potential dead code, and an output directory to generate the HTML report
2. In parallel, two things happen:
   1. First, we run program slicing on the input code. This generates the final abstract state `(M,L)` pair.
   2. Second, if the user did not specify a set of effective variables, our program scans the code and approximates the effective variables.
      1. Please see the section [Effective variables](#effective-variables) for more details
3. Afterwards, for each effective variable, we get it's program slice and then merge the resulting slices together by taking the union of the line numbers they depend on. 
4. We then pass this information to our UI which formats our findings into a report.

## Code structure

- [ProgramSlicerService](./service/programSlicerService.py) is our main algorithm that performs program slicing
- [visitor](./visitor/) contains multiple visitors that traverse the Python AST. For example, we use visitors to:
  - Find all function declarations
  - Get the code segment corresponding to a line number
  - Get all referenced variables in a node or a function call
- [ProgramSliceTransformer](./visitor/programSliceTransformer.py) gets the resulting slicing program given a sequence of line numbers to keep
- [ui](./ui) contains the files to generate our HTML report

## Effective variables

## Program slicing & design tradeoffs

TODO talk about enhancements

TODO The design of your program analysis; to what extent does this seem a good fit for the use-case (task and users)?  (LO IIX). If applicable (usually for a static analysis), a sensible choice of trade-offs w.r.t. approximating information about possible executions (LO IX)

## Impossible 4 Properties

Similarly to what we learned about program slicing in lecture, our static analysis does not always say "no" when the answer should be "no" upon termination. Our project prefers false positives over false negatives because we don't want to mistakenly remove live code. Thus, our project over-approximates and is pessimistic, similar to the program slicing algorithm we learned in class.

## UI

# User Studies

# Future Work
TODO talk about what we don't support & limitations in our project

# References
1. https://www.cs.wm.edu/~denys/pubs/TSE'18-DeadCode.pdf?fbclid=IwAR38JynyhFk7aWL51v6mqAlH8E-pHnHIgFSOQxpHMRuUkzOXTsBSdbq1uX4
2. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8486334 

