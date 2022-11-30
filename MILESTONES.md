# Milestone 5
Full details can be found at [Milestone 5](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.4a7y505n126z)

## High Level Progress

1. We've redone our first user study and retyped Milestones 2 and 3
   1. Please see the Milestone 3 section for our first user study results
2. We've made significant progress implementing our project
   1. We finished most of the implementation work for our project. This includes things like program slicing (for loops, conditionals, while loops, assignments), creating a UI, adding a significant amount of test, etc.
   2. We've also had several discussions on the architecture/design decisions of our project such as what the UI should look like, the algorithms for finding effective variables, how we'll handle slicing across functions, etc.
   3. For more details, please see our pull requests, completed issues, and our progress against our planned timeline
   

## Plans for final video

We've started creating a rough [outline](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.nus8hfx32qoo) of what components our presentation entails. We'll be aiming to finish the slides and scripts before Sunday night, and start filming Sunday night.

## Status of final user study

We'll be completing our final user study this weekend. We're almost done preparing the examples we'll be showing our users, and will report our progress here shortly.

Edit 11/29/22: Our final user study results can be found in our README [here](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12#user-studies) 

## Planned timeline for the remaining days and progress against timeline

Please see [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.1vzl6m8472li) for our remaining work items.

In summary, what we have left to do is
- Polish up UI and integration with our program analysis
- Conduct final user study
- Prepare slides + scripts
- Film video
- Continue documenting our project in our README

## Feedback from TA
We showed Jifeng a demo of what we have so far, namely the genereated HTML report. His main feedback to us was to focus on selling project idea in our presentation. This could include talking about convincing use cases, the usefulness for programmers in the real world, any convincing statements, and to talk about design choices such as how it's control sensisitve.

# Milestone 4
Full details can be found at [Milestone 4](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.baebxgea595b)

## Meeeting Feedback from Jifeng
We showed Jifeng our prototype for program slicing and he seemed happy with it. Jifeng suggested we keep an old copy of our `MILESTONES.md` since we changed our project idea, that way the other TAs will not be confused why our M1, M2, and M3 were all updated at the same time. He also gave us an idea of some visualizations we could do such as what lines a variable depends on and where they're modified.

## Plans for the Final User Study
We’ll be redoing our first user study on Saturday, and will aim to finish development by next Saturday. After that, we’ll reserve the following weekend (26th and 27th) for our final user study.

## Status of Implementation So Far
- We researched heavily into program slicing and dead code optimization
- We’ve made a PR for basic program slicing 
    - https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/9 
    - No control flow, but covers complex variable assignment scenarios in Python such as
        - a = b = c = 1
        - (a,b) = (x+y, z)
        - (a,b) = (c,d) = (x,y+z)
- Created a practical example illustrating our use case - [DeadCodeExamples.md](DeadCodeExamples.md)
- Got approval of idea from Jifeng and Alex
- Identified use case, and target audience
- Plans for the Final User Study

## Next Steps
- We’ve got to redo Milestone 2 and 3
    - For M2 this includes
    - 3 guidelines we’re targeting
    - How this compares to other tools
    - Sketch of output visualization
- For M3 this includes
    - First user study
    - Mockup of how our project is supposed to operate (visualization/design)
- We’ll also need to document our design choices
    - Alex’s email pointed out some good things like what separates our project from what we learned in class vs the paper

## Progress against planned timeline
So far we're on progress according to our **new** planned timeline. We've split up tasks amongst ourselves, set the respective owners and the deadlines we'll finish them by.


# Milestone 3 REDO
Full details can be found at [Milestone 3](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.3stvz762s38c)

## Note
Since we changed our project idea, we'll be redoing our first user study for Milestone 3. Please see the archive below and our google doc for all the work we did in our previous Milestone 3

## First User Study Results
Note: full results can be found [here](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12#user-studies)

We created a series of example inputs and outputs to show to our users. It can be found at [FirstUserStudyRedo.md](FirstUserStudyRedo.md)

Some of the main feedback we received were:

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

# Milestone 2 REDO
Full details can be found at [Milestone 2](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.w0n4yolpgndx)

## Note
Since we changed our project idea, we'll be redoing Milestone 2. Please see the archive below and our google doc for all the work we did in our previous Milestone 2

## Description of Planned Program Analysis

### Overview
Our idea for our project would be a static program analysis to remove dead code. The definition of dead code for the scope of our project is code that is part of the source code of a program and is executed but is not used. This can include code that does not yield any results to the core logic of the program, or code that is not used in any other computation. Please see our practical example for further clarification.

### Motivation
From [this paper](https://www.cs.wm.edu/~denys/pubs/TSE'18-DeadCode.pdf?fbclid=IwAR38JynyhFk7aWL51v6mqAlH8E-pHnHIgFSOQxpHMRuUkzOXTsBSdbq1uX4), we found that dead code was quite common in the industry. Here are some examples they gave:

- Brown et al. [6] reported that, during the code examination of an industrial software system, they found a large amount of source code (between 30 and 50 percent of the total) that was not understood or documented by any developer currently working on it. Later, they learned that this was dead code. 
- Boomsma et al. [7] reported that on a subsystem of an industrial web system written in PHP, the developers removed 2,740 dead files, namely about 30% of the subsystem’s files. 
- Eder et al. [5] studied an industrial software system written in .NET in order to investigate how much maintenance involved dead code. They found that 25% of all method genealogies1 were dead.

Removing dead code helps developers better comprehend the source code and its structure, and allows the code to be more maintainable in the future. Small chunks of dead code could be negligible, but as applications grow in scale, this could be a bottleneck for performance due to increased time and memory consumption. 
 
Furthermore, oftentimes companies can accumulate a lot of tech debt when shipping out features and iterating fast. Because dev teams have to deal with lots of other problems related to functioning and execution, they may not pay attention to how much dead code is appearing. This could potentially be harmful as developers would have a hard time modifying the code in the future, which decreases the overall progress of the team.


### Target users
1. Programmers who are tasked with modifying a complex code base, but are having trouble understanding the core logic of the code due to surrounding code that’s dead - it doesn’t affect the output of the code. Please see our practical example for more details
2. Programmers who are tasked with cleaning up accumulated tech debt, but are unsure what the core functionality of the code is. Thus, by removing dead code, they can focus solely on the core logic of the program and clean up the code efficiently.
3. New Python programmers who have trouble writing maintainable and easy-to-read code can use our tool to help identify dead code

### Which of the 3 guidelines we’re targeting
Criteria 1: Includes a static analysis component

Criteria 2: Targets Python and its AST 

Criteria 3: We’ll also have a substantial visualization component

### How this compares with other tools
Current tools can suggest code that’s unreachable. However, dead code isn’t limited to code that’s unreachable, it includes code that can be executed, but is not used. It’s often harder to find.

### Design choices (Impossible 4 Properties)
1. Fully automatic
   = Yes
2. Always terminate
   - Yes, our analysis will always terminate. As we learned in lecture, program slicing will always terminate.
3. On termination: always says “yes” when the answer should be “yes”
   - Yes, we can think of the question as whether the variable depends on some other variable on a particular line. Since the program slicing over-approximates, it always says yes.
4. On termination: always says “no” when the answer should be “no”
   - No, our analysis will not always satisfy this property since we over-approximate.

### Rough implementation details
Regarding the implementation, we came across [this paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8486334) that described a really interesting approach to tackle this problem.

Here’s the high-level idea: as input, we receive from the user a program with dead code, and a set of effective variables. Effective variables are variables that influence the program's functionality. For prototype purposes, we’ll let the user specify the effective variables. However, if we have time, or for future work, we can implement a heuristic approach to approximate what the effective variables are.

Connecting this to an example use case, if I was a programmer tasked with modifying a function like the BFS example, I know that the effective variables are my queue and the nodes I’ve visited. Apart from that, I don’t want to spend time trying to understand the code instrumentation (tracing, logs, metrics) that other developers added. Instead, I’d like to focus on the core logic by removing the dead code.

Given these inputs, we would generate a program slice for each effective variable and then merge the resulting program slices together.

## Practical Example

See [DeadCodeExample.md](./DeadCodeExamples.md)

## Main Responsibilities & Deadlines
Please see our schedule [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.1vzl6m8472li) for our planned division of main responsibilities between team members and roadmap for what should be done when including specific goals for completion by future Milestones.

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

# Archive of Milestone 2 and Milestone 3

**Note**: Our group changed our idea midway during Milestone 4. We sent an email to Alex and received approval to change our project idea. We redid Milestones 2 and 3 above and are keeping an archive below of our previous milestones to preserve the timestamps to show that we submitted them on time. Please contact our group if there's any questions!

Here's Alex's response to our email:

> _Wow- thanks for the extremely detailed description! This is very helpful._
> _Overall I like the idea - it's also cool that you looked into a paper. I think this will work. In terms of the design of the analysis, are you considering doing something different from (a) what we cover in class, and (b) what they do in the paper? Do you see any questions for the design of your analysis?_
> _Which programming language do you plan to target? Have you thought about what features you will/won't support?_
> _I'm sure this can work as an idea for the project, so do go ahead with this - we can discuss more details along the way as useful._

> # Milestone 3
> Full details can be found at [Milestone 3](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.3stvz762s38c)
> 
> ## Progress against Planned Timeline & Changes to Original Design
> - We changed our idea from a dynamic program analysis dealing with traces to a static program analysis dealing with quirks of a programming language
> - We’ve made substantial progress in researching more about CFGs and data-flow analysis and have experimented with several CFG libraries
> - Updated our Main Responsibilities & Deadlines to adjust to the new project
>     - See [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=kix.lind24l64u5p)
> - We decided to use Python rather than JavaScript
>     - We tried two JS CFG static analysis libraries in the below PR, but both of them were not well maintained and documented, nor did they provide features we wanted (such as CFG for function calls, line numbers, and access to > original AST)
>     - PR: https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/3 
> - We discussed several checks we could do in Python - some of the main checks can be found [here](FirstUserStudyExamples.md)
> - Bootstrapped our repository with the Scalpel library used to generate CFGs for Python
>     - Experimented with their CFG and read their documentation/source code
>     - We believe the library provides us with all the information we need
>     - PR: https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/4 
> - Prepared and conducted first user study - results shown below
> - Began discussing possible visualization ideas
> - In terms of next steps
>     - Yu & Kai are currently working on a prototype that statically analyzes one of the checks our project will make. Once he creates the MVP and lays out the basic groundwork, we’ll be implementing the remaining checks
>     - Jin & Eric will be starting our visualization prototype
>
>## First User Study Results
>Note: full results can be found [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.9vxmjono8y9o)
>
>We created a series of example inputs and outputs to show to our users. It can be found at [FirstUserStudyExamples.md](FirstUserStudyExamples.md)
>
>Some of the main feedback we received were:
>
>- Users suggested standardizing the format of the line numbers
>    - E.g. mixing line numbers in the error messages hard to read
>- Users wanted to see a preview of the relevant lines of code so that they don’t have to read line numbers first to navigate to the code
>- Users also suggested considering integrating our program analysis in VSCode so that it could highlight relevant portions of code, rather than a command line tool
>    - Or a way to generate links to navigate to the respective block of code
>    - Another pro is that we could run our program analysis linter AS the user types their code
>- Users found the word “Error:” at the beginning of the output messages a bit redundant.
>    - Suggestion was to either remove or to have different classes such as Error, Warning, etc.
>    - This was because some of our examples weren’t 100% errors, just unintended side effects, so a simple warning could suffice
>- Users were a bit confused whether our linter analyzes across functions/files or whether it only looks at a single function. We’ll need to clarify this as a group
>
>## Notes of any important changes/feedback from TA discussion
>- Jifeng said our progress looks very good.
>- He gave one suggestion which is for us to consider more complicated examples with more sophisticated control flow, generate their Control Flow Graphs, and consider how your analysis will tackle these situations (especially by looking >at the Control Flow Graphs).
>    - Our group fully agrees since some of our current examples that utilize the full capabilities of the generated CFGs. We'll be iterating on this feedback, and will try to come up with more complex/sophisticated examples by >Milestone 4.
>
># Milestone 2
>Full details can be found at [Milestone 2](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.w0n4yolpgndx)
>
>## NOTE
>Jifeng gave us feedback and said our idea doesn't fulfill the requirements for Project 2 since we're not modelling or inferring anything from a single trace of the control flow of the program. He suggseted we can collect a bunch of >traces for varing inputs, and then model something based on that. Our group will spend the next one to two days discussing amongst ourselves how we can improve our idea, or we may change our idea.
>
>The remaining portion of this markdown is the details we had for our original project. We will update this once we decide on a new idea and confirm with Jifeng!
>
>## Description of Planned Program Analysis
>
>### Overview
>Our project will be a dynamic program analysis to visualize the control flow of a program. We would take in the user's code, run the program, and generate a trace showing things like: which methods were called, which branches were >taken in control flow, a way to visualize loops and recursion, and more.
>
>### Target users
>For new hires, or software engineers tasked to learn a new code base in large-scale projects, it can be quite daunting seeing so much code at once. If you’re learning a method, which calls several other methods, and those methods call >other methods, this can quickly go out of hand with the number of files and methods you need to look at. This is especially true when the execution of the program depends on control flow such as if statements, recursion, loops, etc.
>
>It’s also a very time-consuming process since software engineers would need to either manually draw call graphs or trace through a debugger, but easily get lost in a deep stack trace
>
>### Which of the 3 guidelines we’re targeting
>Criteria 1: Targets Javascript and its AST
>
>Criteria 2: A substantial visualization component
>
>### How this compares with other tools
>- Call stacks when debugging is hard to follow, visualize, and don’t necessarily show why a path was taken if there were multiple control flow paths
>- Drawing call graphs by hand is tedious and error-prone
>- Modern tracing tools exist, but this would require users to heavily instrument their code to emit traces.
>
>### Informal Sketch of Planned Analysis
>Please see our google doc for more details
>![image](https://media.github.students.cs.ubc.ca/user/1272/files/5db83cf5-6463-48a4-ae5c-cb518dffcb10)
>![image](https://media.github.students.cs.ubc.ca/user/1272/files/c66cb0fd-da0e-404c-bb02-66cc6bccb8e8)
>
>## Summary of Progress So Far
>- We spent a significant amount of time researching past solutions and debating pros/cons of the different projects we wanted to do.
>- Made a draft schedule of responsibilities and deadlines
>- Created a prototype playing with dynamic analysis
>  - Modify AST and execute the program with modified AST
>  - https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group12/pull/1/ 
>
>## Planned Follow-up Tasks or Features Still to Design
>- We still need to hash out how we want to visualize if-else conditionals, loops, and recursion.
>- We also need to do more research on what libraries we can use to visualize this.
>
>## Main Responsibilities & Deadlines
>Please see our schedule [here](https://docs.google.com/document/d/1rTH12Da8VUmN5pwcnyu2vJ35sXW-D8ipX03xwb-4nak/edit#bookmark=id.loop0xb0lgqh) for our planned division of main responsibilities between team members and roadmap for what >should be done when including specific goals for completion by future Milestones.
>
>## Notes of any important changes/feedback from TA discussion
>- Please see the beginning paragraph for Milestone 2
