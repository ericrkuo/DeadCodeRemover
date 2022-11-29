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

Effective variables are variables that influence the program functionality. By merging the slices for all effective variables, we essentially exclude statements that do not affect the core logic of the code, in other words, we exclude the dead code. 

Our project either allows the user to specify a set of effective variables themselves through the CLI, or we scan the input code and approximate what the effective variables are.

Currently, our implementation treats all **return variables** from each function as effective variables. This is mainly for the reason that return variables from most functions are what's primarily computed in the function, thus the statements that the return variable depends on is not dead code.

However, this means that functions that do not have any return values will not have any effective variables, and thus, our analysis will be unable to detect dead code. Therefore, in the future, our project could have more advanced methods of finding effective variables, either by looking at the core variables mentioned in the function documentation, or by using the frequency of variables referenced in a function.

## Program slicing & design tradeoffs

We built on top of the program slicing algorithm learned in class and implemented more complex scenarios/behaviors.

### Assignments

In Python, it's possible to perform multiple assignments in one line. Here are just a few examples

```
a = b = 1
(a,b,c) = (d,e,f) = (x+y, z, w)
arr = [x,y,z]
a,b,c = arr
```

To handle these complex cases, we implemented two functions [analyzeAssign](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L193) and [analyzeAugAssign](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L251).

We also made sure to thoroughly test our code by testing different ways of assignments in Python.

Please see [Assignment Tests](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/test/test_ProgramSlicerService.py#L23-L25) for all the cases we covered.

### Conditionals

Building on top of what we learned in lecture for slicing conditionals, our group made a couple of optimizations.

1. In Python, it's not possible to have empty conditional blocks. Thus, if an `if` block or `elif` block has no statements kept after removing dead code, we replace the entire block with a `pass` statement
2. If the `else` block has no statements kept after removing dead code, we remove it entirely.
3. Lastly, if all blocks of the conditional are empty, we remove the conditional in its entirety.

Here's our function [programSlicerService::analyzeIf](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L119) and our function [programSliceTransformer::visit_If](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/visitor/programSliceTransformer.py#L89) that performs the optimizations mentioned above.

### Loops

In addition to for loops, our team also implemented support for while loops in Python. We did a similar optimization where if the body of the loop is empty after removing dead code, we remove the loop in its entirety.

Here's our function [analyzeWhile](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L50), [analyzeFor](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L75), and our function [programSliceTransformer loops](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/visitor/programSliceTransformer.py#L105-L121) that performs the optimization mentioned above.

### Slicing across functions

TODO talk about assumptions we had to make

TODO The design of your program analysis; to what extent does this seem a good fit for the use-case (task and users)?  (LO IIX). If applicable (usually for a static analysis), a sensible choice of trade-offs w.r.t. approximating information about possible executions (LO IX)

## Impossible 4 Properties

Similarly to what we learned about program slicing in lecture, our static analysis does not always say "no" when the answer should be "no" upon termination. Our project prefers false positives over false negatives because we don't want to mistakenly remove live code. Thus, our project over-approximates and is pessimistic, similar to the program slicing algorithm we learned in class.

## UI

Our UI is built using [Jinja](https://jinja.palletsprojects.com/en/3.1.x/), a templating engine. 

### Statistics

Our UI also displays some key statistics such as 

1. The amount of code removed and which lines were removed
2. The variables that depend on each line.
   1. This statistic is useful for our target users in the sense that they can identify any variables that mistakenly should not depend on the current line. Furthermore, they can also use this to identify lines that have *too* many implicit and explicit dependencies, which may motivate them to further simplify their code.

# User Studies

# Future Work
TODO talk about what we don't support & limitations in our project

# References
1. https://www.cs.wm.edu/~denys/pubs/TSE'18-DeadCode.pdf?fbclid=IwAR38JynyhFk7aWL51v6mqAlH8E-pHnHIgFSOQxpHMRuUkzOXTsBSdbq1uX4
2. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8486334 

