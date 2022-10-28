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
