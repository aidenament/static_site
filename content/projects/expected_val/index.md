# Expected Distance to the Nearest Face of an n-Cube

[< Back to Projects](/projects)

## One Closed Form for Every Dimension

Drop a point at random inside a unit square. How far is it from the nearest edge? The answer is $1/6$, the same argument gives $1/8$ for the cube, and it generalizes to a single closed form in every dimension:

$$
\mathbb{E}[X] = \frac{1}{2(n+1)}
$$

The paper does the square and the cube by hand, then the general case. The proof partitions the cube by which face is nearest, then subdivides each region so that symmetry makes every piece integrate to the same value. An $n$-cube has $2n$ faces of dimension $n-1$, and the region belonging to each face splits into $2^{n-1}(n-1)!$ congruent pieces. Evaluate one piece and multiply through.

The formula also says something about where volume sits in high dimensions. $\mathbb{E}[X]$ shrinks as $n$ grows, so more and more of the cube lies near its boundary. That part isn't new, and it follows more directly from $(1-\epsilon)^n \to 0$ for any fixed $\epsilon > 0$. What the expectation gives you is the rate. It goes like $1/n$, so halving the expected distance to the boundary costs you roughly a doubling of the dimension.

The problem came from my Math 170A final. I worked out the general case afterward, in July 2023.

### The Full Paper

Read it below, or [download it directly](/projects/expected_val/Expected_Distance_of_a_Random_Interior_Point_of_an_n_cube_to_its_nearest_face.pdf).

```pdf
/projects/expected_val/Expected_Distance_of_a_Random_Interior_Point_of_an_n_cube_to_its_nearest_face.pdf
```
