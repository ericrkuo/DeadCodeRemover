# Milestone 4
Full details can be found at [Milestone 4](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.baebxgea595b)

- Status of implementation so far.
- Plans for the final user study.
- Planned timeline for the remaining days.
- Progress against the timeline planned for your team, including the specific goals you defined (originally as part of Milestone 2) for Milestone 4; any revisions to Milestone 5 goals.

## Meeeting Feedback from Jifeng
- Updating MILESTONES.md
    - Keep a record of our OLD stuff
- Visualization ideas
    - What lines a variable depends on and where they’re modified

## Status of Implementation So Far
- We researched heavily into program slicing and dead code optimization
- We’ve made a PR for basic program slicing 
    - https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/9 
    - No control flow, but covers complex variable assignment scenarios in Python such as
        - a = b = c = 1
        - (a,b) = (x+y, z)
        - (a,b) = (c,d) = (x,y+z)
- Created a practical example illustrating our use case - DeadCodeExamples.md 
- Got approval of idea from Jifeng and Alex
- Identified use case, and target audience
- Plans for the Final User Study
- We’ll be redoing our first user study on Saturday, and will aim to finish development by next Saturday. After that, we’ll reserve the following weekend (26th and 27th) for our final user study.

## Next Steps
- We’ve got to redo Milestone 2 and 3
    - For M2 this includes
    - 3 guidelines we’re targeting
    - How this compares to other tools
    - Sketch of output visualization
    - TODO check if others
- For M3 this includes
    - First user study
    - Mockup of how our project is supposed to operate (visualization/design)
- We’ll also need to document our design choices
    - Alex’s email pointed out some good things like what separates our project from what we learned in class vs the paper


# Milestone 3
Full details can be found at [Milestone 3](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.3stvz762s38c)

## Progress against Planned Timeline & Changes to Original Design
- We changed our idea from a dynamic program analysis dealing with traces to a static program analysis dealing with quirks of a programming language
- We’ve made substantial progress in researching more about CFGs and data-flow analysis and have experimented with several CFG libraries
- Updated our Main Responsibilities & Deadlines to adjust to the new project
    - See [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.lind24l64u5p)
- We decided to use Python rather than JavaScript
    - We tried two JS CFG static analysis libraries in the below PR, but both of them were not well maintained and documented, nor did they provide features we wanted (such as CFG for function calls, line numbers, and access to original AST)
    - PR: https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/3 
- We discussed several checks we could do in Python - some of the main checks can be found [here](FirstUserStudyExamples.md)
- Bootstrapped our repository with the Scalpel library used to generate CFGs for Python
    - Experimented with their CFG and read their documentation/source code
    - We believe the library provides us with all the information we need
    - PR: https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/4 
- Prepared and conducted first user study - results shown below
- Began discussing possible visualization ideas
- In terms of next steps
    - Yu & Kai are currently working on a prototype that statically analyzes one of the checks our project will make. Once he creates the MVP and lays out the basic groundwork, we’ll be implementing the remaining checks
    - Jin & Eric will be starting our visualization prototype

## First User Study Results
Note: full results can be found [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.9vxmjono8y9o)

We created a series of example inputs and outputs to show to our users. It can be found at [FirstUserStudyExamples.md](FirstUserStudyExamples.md)

Some of the main feedback we received were:

- Users suggested standardizing the format of the line numbers
    - E.g. mixing line numbers in the error messages hard to read
- Users wanted to see a preview of the relevant lines of code so that they don’t have to read line numbers first to navigate to the code
- Users also suggested considering integrating our program analysis in VSCode so that it could highlight relevant portions of code, rather than a command line tool
    - Or a way to generate links to navigate to the respective block of code
    - Another pro is that we could run our program analysis linter AS the user types their code
- Users found the word “Error:” at the beginning of the output messages a bit redundant.
    - Suggestion was to either remove or to have different classes such as Error, Warning, etc.
    - This was because some of our examples weren’t 100% errors, just unintended side effects, so a simple warning could suffice
- Users were a bit confused whether our linter analyzes across functions/files or whether it only looks at a single function. We’ll need to clarify this as a group

## Notes of any important changes/feedback from TA discussion
- Jifeng said our progress looks very good.
- He gave one suggestion which is for us to consider more complicated examples with more sophisticated control flow, generate their Control Flow Graphs, and consider how your analysis will tackle these situations (especially by looking at the Control Flow Graphs).
    - Our group fully agrees since some of our current examples that utilize the full capabilities of the generated CFGs. We'll be iterating on this feedback, and will try to come up with more complex/sophisticated examples by Milestone 4.

# Milestone 2
Full details can be found at [Milestone 2](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.w0n4yolpgndx)

## NOTE
Jifeng gave us feedback and said our idea doesn't fulfill the requirements for Project 2 since we're not modelling or inferring anything from a single trace of the control flow of the program. He suggseted we can collect a bunch of traces for varing inputs, and then model something based on that. Our group will spend the next one to two days discussing amongst ourselves how we can improve our idea, or we may change our idea.

The remaining portion of this markdown is the details we had for our original project. We will update this once we decide on a new idea and confirm with Jifeng!

## Description of Planned Program Analysis

### Overview
Our project will be a dynamic program analysis to visualize the control flow of a program. We would take in the user's code, run the program, and generate a trace showing things like: which methods were called, which branches were taken in control flow, a way to visualize loops and recursion, and more.

### Target users
For new hires, or software engineers tasked to learn a new code base in large-scale projects, it can be quite daunting seeing so much code at once. If you’re learning a method, which calls several other methods, and those methods call other methods, this can quickly go out of hand with the number of files and methods you need to look at. This is especially true when the execution of the program depends on control flow such as if statements, recursion, loops, etc.

It’s also a very time-consuming process since software engineers would need to either manually draw call graphs or trace through a debugger, but easily get lost in a deep stack trace

### Which of the 3 guidelines we’re targeting
Criteria 1: Targets Javascript and its AST

Criteria 2: A substantial visualization component

### How this compares with other tools
- Call stacks when debugging is hard to follow, visualize, and don’t necessarily show why a path was taken if there were multiple control flow paths
- Drawing call graphs by hand is tedious and error-prone
- Modern tracing tools exist, but this would require users to heavily instrument their code to emit traces.

### Informal Sketch of Planned Analysis
Please see our google doc for more details
![image](https://media.github.students.cs.ubc.ca/user/1272/files/5db83cf5-6463-48a4-ae5c-cb518dffcb10)
![image](https://media.github.students.cs.ubc.ca/user/1272/files/c66cb0fd-da0e-404c-bb02-66cc6bccb8e8)

## Summary of Progress So Far
- We spent a significant amount of time researching past solutions and debating pros/cons of the different projects we wanted to do.
- Made a draft schedule of responsibilities and deadlines
- Created a prototype playing with dynamic analysis
  - Modify AST and execute the program with modified AST
  - https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/1/ 

## Planned Follow-up Tasks or Features Still to Design
- We still need to hash out how we want to visualize if-else conditionals, loops, and recursion.
- We also need to do more research on what libraries we can use to visualize this.

## Main Responsibilities & Deadlines
Please see our schedule [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.loop0xb0lgqh) for our planned division of main responsibilities between team members and roadmap for what should be done when including specific goals for completion by future Milestones.

## Notes of any important changes/feedback from TA discussion
- Please see the beginning paragraph for Milestone 2

# Milestone 1

## Discussion of Ideas So Far
Full details can be found [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.p37clgyszzlv)

Our group came up with 3-4 ideas this week. The two main ideas we are leaning towards are:

### 1. Big-O Calculator

Our program analysis tool would calculate the time complexity (best case and worst case) given a block of code. The code can be complex with recursion, conditionals that affect the time complexity, loops, etc.

For example, if the condition is always satisfied, time complexity would be `O(N)`, otherwise, it would be `O(logN)`

``` java
i = N; // some input N
while (i!=0) {
  if (<some condition>) {
    i--;
  } else {
    i/=2;
  }
}
```

- Target user: leetcode programmers, or general computer science students wanting to learn more about time complexity.

### 2. Control-Flow Visualizer
Our tool would produce a graph/sequence diagram of how a function is executed. The motivation behind this is that it's difficult to know where code flows during run time. Statically, we'd have to go through lots of files for large-scale projects, but this is time-consuming since have to start drawing call diagrams and multiple control flow paths can go to different areas.

For example, in the function below, our tool could produce a visualization that shows `foo` calls `A`.

```
function foo(int x) {
  if (x) {
    return A();
  } else {
    return B();
  }
}
```

- Target user: new hires onboarding to companies, tasked with changing the code base, but unsure how 100+ methods interact with each other

## Follow-up Tasks
We plan on hashing out our ideas further by seeing how feasible they are. Once we've decided on one idea, we'll start working on the requirements for M2 such as planned responsibilities & deadlines, as well as a formal proposal of our idea.

## Notes of any important changes/feedback from TA discussion
Jifeng provided us with great feedback. Here are the main points he provided

- Jifeng recommends we research existing work to understand the feasibility, and to start thinking about which parts would be statically or dynamically analyzed.
- We should make sure we satisfy at least 2 of the 3 guidelines
- Our target user case needs to be important, it should not only differentiate us from other groups, but other existing solutions as well. For example, explain what current tools lack
- The tool should not reason about the code’s architecture - that’s meta-analysis, things we get when scanning the code and visualizing
  - Instead, reason about the behaviour of code when executing - control flow
- The analysis tool should have some design choices
  - Not obvious which approach to take, several approaches (2-3) are possible
  - We should discuss pros and cons, and which we choose
