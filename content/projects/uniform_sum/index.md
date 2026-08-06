# Sum of Uniform Random Variables

[< Back to Projects](/projects)

## The Expected Number of Uniform Variables Required to Exceed 1

Let $X_1, X_2, X_3, \ldots$ be independent random variables drawn uniformly from $[0, 1]$, and write $Y_n = X_1 + \cdots + X_n$ for the running total. Adding terms one at a time, how many are required on average before that total first exceeds 1?

This paper derives the exact distribution and the expectation that follows from it. The probability that exactly $n$ terms are needed is

$$
\mathbb{P}(Y_{n-1} < 1 \text{ and } Y_n > 1) = \frac{n-1}{n!}
$$

Establishing this reduces to an iterated integral over the region of the unit $n$-cube where the first $n-1$ coordinates sum to less than 1 while all $n$ sum to more than 1. Linearity splits that integral into $n-1$ pieces indexed by $k$, and a repeated substitution collapses each piece to $1/n!$. The value turns out not to depend on $k$, so the $n-1$ identical pieces give the result above.

Weighting each $n$ by its probability and shifting the index by two leaves the Taylor series for $e$:

$$
\mathbb{E} = \sum_{n=2}^{\infty} n \cdot \frac{n-1}{n!} = \sum_{n=2}^{\infty} \frac{1}{(n-2)!} = \sum_{n=0}^{\infty} \frac{1}{n!} = e
$$

The expected number of uniform variables required to exceed a total of 1 is therefore exactly $e$.

The problem was posed to me in a job interview. Written in August 2024.

### View the Full Paper

You can view the full paper below or [download it directly](/projects/uniform_sum/Sum_of_Uniform_Random_Variables.pdf).

```pdf
/projects/uniform_sum/Sum_of_Uniform_Random_Variables.pdf
```
