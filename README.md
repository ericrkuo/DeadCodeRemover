# Project 2 Group12

The main components of this README include an overview of our project, how to run it, the architecture/design of our project, some tradeoffs of our static analysis, and much more!

# Disclaimer
Our group changed our idea midway during Milestone 4. We sent an email to Alex and received approval to change our project idea. We redid Milestones 2 and 3 in [MILESTONES.md](./MILESTONES.md), but kept an archive at the very bottom of the file to show that we put significant effort in our previous ideas and that we submitted previous milestones on time. Please contact our group if there's any questions!

# Introduction, Use Case & Motivation

## Definition of dead code

The definition of dead code for the scope of our project is code that is part of the source code of a program and is executed but is not used. This can include code that does not yield any results to the core logic of the program, or code that is not used in any other computation. Please see our [practical example](#practical-example) for further clarification.

## Motivation & Target users

From [this paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8486334&tag=1), we found that dead code was quite common in the industry. Here are some examples they gave:

- *Brown et al. [6] reported that, during the code examination of an industrial software system, they found a large amount of source code (between **30 and 50 percent** of the total) that was not understood or documented by any developer currently working on it. Later, they learned that this was **dead code**.*

- *Boomsma et al. [7] reported that on a subsystem of an industrial web system written in PHP, the developers removed **2,740 dead files**, namely about 30% of the subsystem’s files.* 

- *Eder et al. [5] studied an industrial software system written in .NET in order to investigate how much maintenance involved dead code. They found that **25% of all method genealogies1 were dead.***


Removing dead code helps developers better comprehend the source code and its structure, and allows the code to be more maintainable in the future. Small chunks of dead code could be negligible, but as applications grow in scale, this could be a bottleneck for performance due to increased time and memory consumption.

Furthermore, oftentimes companies can accumulate a lot of tech debt when shipping out features and iterating fast. Because dev teams have to deal with lots of other problems related to functioning and execution, they may not pay attention to how much dead code is appearing, and this could potentially be harmful as developers would have a hard time modifying the code in the future, which decreases the overall teams progress.

## Target Users
Our target uses are:
- Programmers who are tasked with modifying or learning a complex code base, but are having trouble understanding the core logic of the code due to surrounding code that’s dead - it doesn’t affect the output of the code. Please see our practical example for more details
- Programmers who are tasked with cleaning up accumulated tech debt, but are unsure what the core functionality of the code is. Removing dead code not only cleans up the tech debt as a first pass, but can afterwards also allow developers to focus solely on the core logic of the program and clean up the code even more.
- New Python programmers who have trouble writing maintainable and easy-to-read code can use our tool to help identify dead code.

## Why Python?

Since Python is a dynamically typed language, it's already difficult enough to infer what types certain variables are. Our group thought that by removing dead code, we can reduce the time spent by programmers understanding code that's not relevant to the output of the function, and instead, let them focus solely on the relevant parts.


## Static vs Dynamic Analysis

We did not choose a dynamic analysis because it would've kept code relevant for a single execution. However, our project needs to keep code relevant to all executions since removing dead code for one execution, may not be considered dead code for another execution path. Thus, our project is a static analysis.

## Practical Example

One of the use cases/target users of our project are software engineers who are having difficulty understanding the purpose of the codebase because of how much dead code there is.

For example, consider this code [example_image_uploader.py](./example_inputs/example_image_uploader.py). To the naked eye, it's difficult to understand what the code is doing. Upon looking closer, we can see that there's dead code such as logging, tracing, metrics, and DB IO. All these cloud what the purpose of the code is doing.

Running this example through our project, we can see that more than 50% of dead code is removed. Upon looking at the final resulting program, it's much easier for a developer to understand what the core logic of the code is.

![image](https://media.github.students.cs.ubc.ca/user/1272/files/2b6ce83b-a3aa-4f07-bdbe-490503eaf683)
[Source](https://docs.google.com/presentation/d/19lBsd1kV9K8-WTmjm7iKl9PKMK03tVnVeWeO9uBxy9o/edit#slide=id.g16a0b4bf3dd_0_4)

# Getting Started

## Running our project
1. First install all dependencies
   - Run the command `pip install -r requirements.txt` from the project directory

2. Run the program with example inputs
   - ```python main.py -i <filepath> -o <output dirpath>```
   - There is a directory of [example_inputs](./example_inputs/) that you can try out!

3. For full details of how to use our command line, run `python main.py -h`. This will output:

   - Please see the section [Effective Variables](#effective-variables) first to understand better what the option means
```
usage: main.py [-h] -i input -o output [-e [effective variables ...]] [-d]

CLI for dead code removal

optional arguments:
  -h, --help            show this help message and exit
  -i input, --input input
                        Path to input file
  -o output, --output output
                        Path to output directory
  -e [effective variables ...], --effective-vars [effective variables ...]
                        Space-separated list of effective variables to analyze in    
                        the form of <function name>:<variable name> or <variable     
                        name>; if omitted, target effective variables are found      
                        automatically.
  -d, --debug           Debug mode prints out logs
```

4. The command line will generate an HTML report in the specified output directory, which can then be opened in your local browser.

## Disclaimer about what we don't support

Please see the section [Future Work](#future-work) as well as our findings from our final user study in [User Study Results](#user-studies)

## Running our tests

The tests can either be ran by executing the command `python -m pytest`, or alternatively by using the `Testing` tab in VSCode which should discover the tests in our repo.

![image](https://media.github.students.cs.ubc.ca/user/1272/files/ccca1d73-31e4-49ef-8ff0-f8098aac8062)


# Relevant documents

Please see our [Google Doc](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit?usp=sharing) for all the documentation and planning we did for our project.

Here's a link to our [Schedule & Planning](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.1vzl6m8472li)

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
  - The motivation for this class is that the line numbers in map `M` of our abstract state do not tell us **all** the lines that need to be kept. For example, things like conditional declarations, loop declarations, function declarations, import statements, return statements, etc. all need to be kept.
- [ui](./ui) contains the files to generate our HTML report

## Effective variables

Effective variables are variables that influence the program functionality. By merging the slices for all effective variables, we essentially exclude statements that do not affect the core logic of the code, in other words, we exclude the dead code. 

Our project either allows the user to specify a set of effective variables themselves through the CLI, or we scan the input code and approximate what the effective variables are.

Currently, our implementation treats all **return variables** from each function as effective variables. This is mainly for the reason that return variables from most functions are what's primarily computed in the function, thus the statements that the return variable depends on is not dead code.

However, this means that functions that do not have any return values will not have any effective variables, and thus, our analysis will be unable to detect dead code. Therefore, in the future, our project could have more advanced methods of finding effective variables, either by looking at the core variables mentioned in the function documentation, or by using the frequency of variables referenced in a function. For the time being, the user can fix this by supplying their own list of effective variables through our CLI. Although this can be cumbersome for the user, we still think this is valuable since a programmer may know what the core variables of a function are, and just pass those to our analysis to remove the dead code.

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

### Slicing across functions - Tradeoffs w.r.t approximating information

Lastly, one of the main features of our project is the ability to perform program slicing across functions. Do note that there are key limitations mentioned here and in the [Future Work](#future-work) section.

### 1. Upgrading our abstract state to handle functions
To handle conflicting variable names across functions, we use the prefix of the function name in the abstract state map `M`. See the following example below:

```python
1. def foo():
2.   x = 1
3.
4. def moo():
5.   x = 1
6. 
7. x = 1

M = (foo:x→{2}, moo:x→{5}, x→{7})
```

Note that we do not handle aliasing yet or global variables. This is something we would be more than happy to take a stab at for our future work, and it also came up as feedback in our final user study.

### 2. Handling class methods

Our analysis pessimistically assumes calling methods on an object is an assignment that can modify the object.

- For example, if we have `arr.append(0)` or `arr.pop(0)`, then we can sort of think of it as an assignment `arr = arr + 0` or `arr = arr - <last element>` respectively, so we update `M[arr] <- M[arr] union {n} union S_l` (in addition to any other variables used in the assignment, e.g. `arr.append(x)`)

However, this does come with some drawbacks since we're over-approximating.

- Consider the case where we have `logger.log(...)`. Then we estimate that `logger` depends on the current line, even though it's not a statement that can modify the object.
- However, we would only keep the code with the logging statements IF our program finds that `logger` is an effective variable, or if any effective variable somehow depends on the `logger` variable. Because of these unlikely cases, we decided this would be okay for the time being, and through thorough testing, we saw that logging statements were being removed as dead code which is what's intended.

In the future, we can be smarter and potentially have a black list or white list of object methods that do modify or do not modify the object.

### 3. Parameters in function calls

Originally, we assumed that all parameters in function calls could be modified and depend on the current line. However, this was too pessimistic and so we could end up keeping statements like `print(x)` in our code, since we said `x` depends on this current line.

Our original intention was to handle cases where we have an object like `arr = [1,2]`, which gets passed to a method like `filterElements(arr)`, and since this function can modify `arr`, we should say `arr` depends on this line. 

To address these two issues, we decided that we should only consider parameters in function calls, for functions that are **defined** by the user. Thus, first we get all function declaration names, and once we approach an `ast.Call`, we only look at function calls defined by the user.

[analyzeCall](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/285b28d2c45206b893715318adbb80bf2c00b2fe/service/programSlicerService.py#L162) has our implementation details

### 4. Deciding which function calls to keep
Originally, we were keeping all function calls in our resulting slices. However, this ended up keeping irrelevant statements like

```python
print(...)
print(len(...))
# and a bunch more
```

To handle this, we decided to only keep function calls that are user-defined functions. This way, we could keep statements such as

```python
def foo(): return 1

# keep
foo()
len(foo())
print(foo())
```

Our reasoning was that since our analysis only works for single files at the moment, we wouldn't need to worry about accidentally removing function calls from other files. For function calls that are from external libraries, most likely those functions are class methods, in the form of `obj.method(...)`, so we handle that appropriately as mentioned earlier.

Thus, we end up keeping statements that are core to the program such as:

```python
if __name__ == 'main':
   functionOne()
   functionTwo()
   functionThree()
   ...
```

## Impossible 4 Properties

Similarly to what we learned about program slicing in lecture, our static analysis does not always say "no" when the answer should be "no" upon termination. Our project prefers false positives over false negatives because we don't want to mistakenly remove live code. Thus, our project over-approximates and is pessimistic, similar to the program slicing algorithm we learned in class.

## UI

Our UI is built using [Jinja](https://jinja.palletsprojects.com/en/3.1.x/), a templating engine.

Main code
- [template.html](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/main/ui/template.html) - the template of our HTML report
- [generateReport.py](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/blob/main/ui/generateReport.py) which takes the data from our program analysis, and feeds that to Jinja which renders the data in the template.

### Statistics

Our UI also displays some key statistics such as 

1. The amount of code removed and which lines were removed
2. The variables that depend on each line.
   1. This statistic is useful for our target users in the sense that they can identify any variables that mistakenly should not depend on the current line. Furthermore, they can also use this to identify lines that have *too* many implicit and explicit dependencies, which may motivate the user to simplify their code.

### Drill Down View

Our UI also displays the individual program slices for each effective variable. This is important to the programmer in case they want finer grained details on why some dependencies exist between variables.

# User Studies

For our final user study, we used several examples from our [example_inputs](./example_inputs/) directory, generated the HTML report, and got users to try out some example inputs themselves. We also showed them an output with no dead code, and tried asking them to generate some dead code as well.

For our first user study, we used this example [FirstUserStudy](./FirstUserStudyRedo.md)

## Notes from final user study

Overall, uses were quite happy with our program analysis, commenting about how they didn't know what dead code is, and how the CLI & UI were intuitive and easy to use. They enjoyed our practical example with tracing/logging/metrics, and wanted to experiment with more complex programs.

Some of the main feedback we got was:

- Users suggesting being able to do analysis across different files
  - Figure out the code that calls the function in different files. This makes the dependency complex.
- Some of our more experienced Python developers suggested more complex control flow mechanisms such as
   - Else statements in for loops and while loops
      ```
      for item in container:
         if search_something(item):
               # Found it!
               process(item)
               break
         else:
               # Didn't find anything..
               not_found_in_container()
      ```
  - Assignment expressions in while loops and if statements
    ```
    while line := data.readline(): 
        do_smthg(line)
    ```
  - Note: Python has plenty of special syntaxes that do not appear in other languages.

- Users suggested that it might be easier to use as a built-in editor extension instead of a command line. Running our analysis each time through a CLI for every file the user desires could be cumbersome for the user.
- Users suggested they want to see some dead code that is unreachable for any inputs.
  - Our thoughts: Yes, we agree. Right now our definition of dead code doesn't include unreachable code. Thus, we could extend this idea for the future.
- Users also wondered if it’s possible to differentiate parameters passed into function calls either by reference or by value.
  - Our current design chose to assume all arguments in function call depending on that line. But this was too pessimistic, so we acted on this feedback and only considered function calls for functions defined by the user.
  - We'd also have to think about aliasing and global variables.
- Users wondered if our project supports class definitions
  - Our thoughts: Class methods would include the code to modify the class variables but it does not return anything. In our current implementation, such code will be related to the effective variables so that it might be removed from our slicing algorithm.

Full details can be found [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.tzsjpiajuvw0)

## Notes from first user study

Some of the main feedback we got was:

- Users were a bit confused by what the definition of dead code was
  - We clarified afterwards that it’s not limited to unreachable code, but code that doesn’t affect the core logic of the program
- Outputting the number of lines removed was not that helpful. Users had some difficulty seeing which lines got removed. They suggested an inline or side-by-side diff view with highlighting, sort of like a git diff
- Users felt that specifying the effective variables was a little redundant, which meant that they had to understand the code to a certain extent to know which variables are important
  - Solution: we could find the effective variables by scanning across functions and finding their return statements. This could suggest to the user which variables are potentially more important and impactful
- Users felt a bit lost at times about why certain code was removed
  - They also said it might be because it was hard to see without some diff view as mentioned earlier
  - Our idea
    - We could show them the individual program slices for each effective variable
    - For each individual program slice, we can show which lines the variable depends on
- Users were wondering if we could support dead code removal across several functions at once
  - We’ll have to explore how to support program slicing across functions

Full details can be found [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.9vxmjono8y9o)

# Future Work

Based on our final user study results and our own analysis, our future work mainly includes:
- User Experience
  - On-the-fly analysis
  - VS Code built-in extension
- Support for more Python features
  - Support class definitions (e.g. self.foo(a))
  - Else statements in while loops and for loops
  - Assignments in while loops and if statements
  - Support aliasing, class definitions, global variables and more.
- Analysis Optimizations
  - More advanced algorithms for finding effective variables
  - Less pessimistic assumptions for variable dependencies

# References
1. https://www.cs.wm.edu/~denys/pubs/TSE'18-DeadCode.pdf?fbclid=IwAR38JynyhFk7aWL51v6mqAlH8E-pHnHIgFSOQxpHMRuUkzOXTsBSdbq1uX4
2. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8486334 

