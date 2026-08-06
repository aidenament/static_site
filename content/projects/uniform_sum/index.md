# Sum of Uniform Random Variables

[< Back to Projects](/projects)

## The Expected Number of Uniform Variables Required to Exceed 1

Pick numbers uniformly at random from $[0, 1]$ and add them up one at a time. How many do you need, on average, before the total passes 1? The answer is $e$.

Formally, let $X_1, X_2, X_3, \ldots$ be independent and uniform on $[0, 1]$, and write $Y_n = X_1 + \cdots + X_n$ for the running total. The probability that exactly $n$ terms are needed is

$$
\mathbb{P}(Y_{n-1} < 1 \text{ and } Y_n > 1) = \frac{n-1}{n!}
$$

Establishing this reduces to an iterated integral over the part of the unit $n$-cube where the first $n-1$ coordinates sum to less than 1 and all $n$ sum to more than 1. Linearity splits that integral into $n-1$ pieces, one for each coordinate that could be the last to push the total over. A repeated substitution collapses each piece to $1/n!$, and none of them depend on which coordinate you picked.

Weighting each $n$ by its probability and shifting the index by two leaves the Taylor series for $e$:

$$
\mathbb{E} = \sum_{n=2}^{\infty} n \cdot \frac{n-1}{n!} = \sum_{n=2}^{\infty} \frac{1}{(n-2)!} = \sum_{n=0}^{\infty} \frac{1}{n!} = e
$$

There's no exponential anywhere in the setup, and $e$ turns up anyway.

An interviewer asked me this and I didn't get it. I wrote it up afterward, in August 2024.

### The Full Paper

Read it below, or [download it directly](/projects/uniform_sum/Sum_of_Uniform_Random_Variables.pdf).

```pdf
/projects/uniform_sum/Sum_of_Uniform_Random_Variables.pdf
```
